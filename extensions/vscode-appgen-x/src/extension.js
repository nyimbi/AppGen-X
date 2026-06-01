"use strict";

const cp = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");
const vscode = require("vscode");

let client;
let diagnosticCollection;

function activate(context) {
  diagnosticCollection = vscode.languages.createDiagnosticCollection("appgen");
  context.subscriptions.push(diagnosticCollection);
  client = new AppGenLanguageClient(diagnosticCollection);
  context.subscriptions.push({ dispose: () => client.stop() });
  client.start();
  for (const document of vscode.workspace.textDocuments) {
    client.didOpen(document);
  }
  context.subscriptions.push(vscode.workspace.onDidOpenTextDocument((document) => client.didOpen(document)));
  context.subscriptions.push(vscode.workspace.onDidChangeTextDocument((event) => client.didChange(event.document)));
  context.subscriptions.push(vscode.workspace.onDidSaveTextDocument((document) => lintDocument(document)));
  context.subscriptions.push(vscode.workspace.onDidChangeConfiguration((event) => {
    if (event.affectsConfiguration("appgen.command")) {
      client.restart();
    }
  }));
  registerProviders(context);
  registerCommand(context, "appgen.lint", () => runForActiveFile(["lint", activeFile(), "--json"], "AppGen-X Lint"));
  registerCommand(context, "appgen.semantic", () => runForActiveFile(["semantic", activeFile(), "--json"], "AppGen-X Semantic Model"));
  registerCommand(context, "appgen.previewSemantic", previewSemanticModel);
  registerCommand(context, "appgen.validate", validateActiveFile);
  registerCommand(context, "appgen.format", () => runForActiveFile(["format", activeFile(), "--write", "--json"], "AppGen-X Format"));
  registerCommand(context, "appgen.graph", () => runForActiveFile(["graph-suite", activeFile(), "--json"], "AppGen-X Graphs"));
  registerCommand(context, "appgen.previewGraph", previewGraph);
  registerCommand(context, "appgen.previewDesigner", previewDesignerSync);
  registerCommand(context, "appgen.migrationPlan", migrationPlan);
  registerCommand(context, "appgen.nlPlan", naturalLanguagePlan);
  registerCommand(context, "appgen.agentHandoff", agentHandoff);
  registerCommand(context, "appgen.explain", explainActiveSymbol);
  registerCommand(context, "appgen.generate", generateActiveFile);
  registerCommand(context, "appgen.previewArtifacts", previewGeneratedArtifacts);
  registerCommand(context, "appgen.verifyRelease", verifyRelease);
  registerCommand(context, "appgen.package", packageActiveFile);
  registerCommand(context, "appgen.doctor", doctorReport);
  registerCommand(context, "appgen.toolingAudit", toolingAudit);
  registerCommand(context, "appgen.contractSchema", contractSchemaCatalog);
  registerCommand(context, "appgen.validateContract", validateSemanticContract);
  registerCommand(context, "appgen.pbcCatalog", browsePbcCatalog);
  registerCommand(context, "appgen.restartLanguageServer", () => client.restart());
  registerViews(context);
}

function deactivate() {
  if (client) {
    client.stop();
  }
}

class AppGenLanguageClient {
  constructor(diagnostics) {
    this.diagnostics = diagnostics;
    this.sequence = 1;
    this.pending = new Map();
    this.buffer = Buffer.alloc(0);
    this.process = undefined;
  }

  start() {
    if (this.process) {
      return;
    }
    this.process = cp.spawn(appgenCommand(), ["lsp", "--stdio"], {
      cwd: workspaceRoot(),
      stdio: ["pipe", "pipe", "pipe"]
    });
    this.process.stdout.on("data", (chunk) => this.receive(chunk));
    this.process.stderr.on("data", (chunk) => console.warn(`AppGen-X language server: ${chunk.toString()}`));
    this.process.on("exit", () => {
      this.process = undefined;
      for (const pending of this.pending.values()) {
        pending.reject(new Error("AppGen-X language server exited."));
      }
      this.pending.clear();
    });
    this.request("initialize", {
      processId: process.pid,
      rootUri: vscode.workspace.workspaceFolders?.[0]?.uri.toString(),
      capabilities: {}
    }).catch((error) => vscode.window.showWarningMessage(error.message));
  }

  restart() {
    this.stop();
    this.start();
    for (const document of vscode.workspace.textDocuments) {
      this.didOpen(document);
    }
    vscode.window.setStatusBarMessage("AppGen-X language server restarted", 3000);
  }

  stop() {
    if (!this.process) {
      return;
    }
    this.request("shutdown", {}).finally(() => {
      this.notify("exit", {});
      if (this.process) {
        this.process.kill();
        this.process = undefined;
      }
    });
  }

  didOpen(document) {
    if (!isAppGen(document)) {
      return;
    }
    this.notify("textDocument/didOpen", {
      textDocument: {
        uri: document.uri.toString(),
        languageId: "appgen",
        version: document.version,
        text: document.getText()
      }
    });
  }

  didChange(document) {
    if (!isAppGen(document)) {
      return;
    }
    this.notify("textDocument/didChange", {
      textDocument: { uri: document.uri.toString(), version: document.version },
      contentChanges: [{ text: document.getText() }]
    });
  }

  request(method, params) {
    this.start();
    const id = this.sequence++;
    this.send({ jsonrpc: "2.0", id, method, params });
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
    });
  }

  notify(method, params) {
    this.start();
    this.send({ jsonrpc: "2.0", method, params });
  }

  send(message) {
    if (!this.process || !this.process.stdin.writable) {
      return;
    }
    const body = Buffer.from(JSON.stringify(message), "utf8");
    this.process.stdin.write(`Content-Length: ${body.length}\r\n\r\n`);
    this.process.stdin.write(body);
  }

  receive(chunk) {
    this.buffer = Buffer.concat([this.buffer, chunk]);
    while (true) {
      const headerEnd = this.buffer.indexOf("\r\n\r\n");
      if (headerEnd < 0) {
        return;
      }
      const header = this.buffer.slice(0, headerEnd).toString("ascii");
      const match = /Content-Length:\s*(\d+)/i.exec(header);
      if (!match) {
        this.buffer = this.buffer.slice(headerEnd + 4);
        continue;
      }
      const length = Number(match[1]);
      const messageEnd = headerEnd + 4 + length;
      if (this.buffer.length < messageEnd) {
        return;
      }
      const message = JSON.parse(this.buffer.slice(headerEnd + 4, messageEnd).toString("utf8"));
      this.buffer = this.buffer.slice(messageEnd);
      this.handle(message);
    }
  }

  handle(message) {
    if (message.method === "textDocument/publishDiagnostics") {
      this.publishDiagnostics(message.params);
      return;
    }
    if (!this.pending.has(message.id)) {
      return;
    }
    const pending = this.pending.get(message.id);
    this.pending.delete(message.id);
    if (message.error) {
      pending.reject(new Error(message.error.message));
    } else {
      pending.resolve(message.result);
    }
  }

  publishDiagnostics(params) {
    const uri = vscode.Uri.parse(params.uri);
    const diagnostics = (params.diagnostics || []).map((diagnostic) => new vscode.Diagnostic(
      asRange(diagnostic.range),
      diagnostic.message,
      diagnostic.severity === 1 ? vscode.DiagnosticSeverity.Error : vscode.DiagnosticSeverity.Warning
    ));
    this.diagnostics.set(uri, diagnostics);
  }
}

function registerProviders(context) {
  const selector = { language: "appgen", scheme: "*" };
  context.subscriptions.push(vscode.languages.registerCompletionItemProvider(selector, {
    provideCompletionItems(document, position) {
      return client.request("textDocument/completion", textParams(document, position)).then((result) => {
        return (result.items || []).map((item) => {
          const completion = new vscode.CompletionItem(item.label, asCompletionKind(item.kind));
          completion.detail = item.detail;
          completion.insertText = item.insertText || item.label;
          return completion;
        });
      });
    }
  }, ".", " ", ":"));
  context.subscriptions.push(vscode.languages.registerHoverProvider(selector, {
    provideHover(document, position) {
      return client.request("textDocument/hover", textParams(document, position)).then((result) => {
        if (!result) {
          return undefined;
        }
        return new vscode.Hover(new vscode.MarkdownString(result.contents.value), asRange(result.range));
      });
    }
  }));
  context.subscriptions.push(vscode.languages.registerDefinitionProvider(selector, {
    provideDefinition(document, position) {
      return client.request("textDocument/definition", textParams(document, position)).then(asLocation);
    }
  }));
  context.subscriptions.push(vscode.languages.registerReferenceProvider(selector, {
    provideReferences(document, position) {
      return client.request("textDocument/references", textParams(document, position)).then((items) => (items || []).map(asLocation));
    }
  }));
  context.subscriptions.push(vscode.languages.registerDocumentSymbolProvider(selector, {
    provideDocumentSymbols(document) {
      return client.request("textDocument/documentSymbol", { textDocument: textDocument(document) }).then((symbols) => (symbols || []).map(asDocumentSymbol));
    }
  }));
  context.subscriptions.push(vscode.languages.registerCodeActionsProvider(selector, {
    provideCodeActions(document) {
      return client.request("textDocument/codeAction", { textDocument: textDocument(document) }).then((actions) => (actions || []).map(asCodeAction));
    }
  }));
  context.subscriptions.push(vscode.languages.registerDocumentFormattingEditProvider(selector, {
    provideDocumentFormattingEdits(document) {
      return client.request("textDocument/formatting", { textDocument: textDocument(document) }).then((edits) => (edits || []).map(asTextEdit));
    }
  }));
  context.subscriptions.push(vscode.languages.registerRenameProvider(selector, {
    provideRenameEdits(document, position, newName) {
      return client.request("textDocument/rename", { ...textParams(document, position), newName }).then(asRenameWorkspaceEdit);
    }
  }));
  context.subscriptions.push(vscode.languages.registerWorkspaceSymbolProvider({
    provideWorkspaceSymbols(query) {
      return client.request("workspace/symbol", { query }).then((symbols) => (symbols || []).map(asSymbolInformation));
    }
  }));
}

function registerViews(context) {
  const viewGroups = {
    "appgen.workspace": [
      { label: "Validate", command: "appgen.validate", icon: "checklist" },
      { label: "Designer Sync", command: "appgen.previewDesigner", icon: "layout" },
      { label: "Graph Preview", command: "appgen.previewGraph", icon: "type-hierarchy" },
      { label: "Generate", command: "appgen.generate", icon: "run" },
      { label: "Package", command: "appgen.package", icon: "package" }
    ],
    "appgen.reports": [
      { label: "Doctor", command: "appgen.doctor", icon: "tools" },
      { label: "Tooling Audit", command: "appgen.toolingAudit", icon: "verified" },
      { label: "Contract Schemas", command: "appgen.contractSchema", icon: "json" },
      { label: "Validate Contract", command: "appgen.validateContract", icon: "check-all" },
      { label: "Release Verification", command: "appgen.verifyRelease", icon: "shield" },
      { label: "Migration Plan", command: "appgen.migrationPlan", icon: "git-compare" }
    ],
    "appgen.agents": [
      { label: "Natural Language Plan", command: "appgen.nlPlan", icon: "sparkle" },
      { label: "Coding Agent Handoff", command: "appgen.agentHandoff", icon: "robot" },
      { label: "Semantic Preview", command: "appgen.previewSemantic", icon: "symbol-class" },
      { label: "PBC Catalog", command: "appgen.pbcCatalog", icon: "library" }
    ]
  };
  for (const [viewId, items] of Object.entries(viewGroups)) {
    context.subscriptions.push(vscode.window.registerTreeDataProvider(viewId, new AppGenCommandTreeProvider(items)));
  }
}

class AppGenCommandTreeProvider {
  constructor(items) {
    this.items = items;
    this.onDidChangeTreeData = new vscode.EventEmitter().event;
  }

  getTreeItem(item) {
    const treeItem = new vscode.TreeItem(item.label, vscode.TreeItemCollapsibleState.None);
    treeItem.command = { command: item.command, title: item.label };
    treeItem.iconPath = new vscode.ThemeIcon(item.icon);
    treeItem.contextValue = "appgenCommand";
    return treeItem;
  }

  getChildren() {
    return this.items;
  }
}

function asRange(range) {
  return new vscode.Range(
    range.start.line,
    range.start.character,
    range.end.line,
    range.end.character
  );
}

function asLocation(location) {
  if (!location) {
    return undefined;
  }
  return new vscode.Location(vscode.Uri.parse(location.uri), asRange(location.range));
}

function asTextEdit(edit) {
  return new vscode.TextEdit(asRange(edit.range), edit.newText);
}

function asWorkspaceEdit(edit) {
  const workspaceEdit = new vscode.WorkspaceEdit();
  for (const [uri, edits] of Object.entries(edit.changes || {})) {
    for (const textEdit of edits) {
      workspaceEdit.replace(vscode.Uri.parse(uri), asRange(textEdit.range), textEdit.newText);
    }
  }
  return workspaceEdit;
}

function asRenameWorkspaceEdit(result) {
  if (result && result.blocked) {
    const diagnostics = result.diagnostics || [];
    const message = diagnostics.map((diagnostic) => {
      return diagnostic.code ? `${diagnostic.code}: ${diagnostic.message}` : diagnostic.message;
    }).filter(Boolean).join("; ") || "Rename requires explicit migration approval.";
    vscode.window.showWarningMessage(`AppGen-X rename blocked: ${message}`);
    throw new Error(`AppGen-X rename blocked: ${message}`);
  }
  return asWorkspaceEdit(result || { changes: {} });
}

function asCodeAction(action) {
  const codeAction = new vscode.CodeAction(action.title, vscode.CodeActionKind.QuickFix);
  codeAction.edit = asWorkspaceEdit(action.edit || { changes: {} });
  return codeAction;
}

function asDocumentSymbol(symbol) {
  const documentSymbol = new vscode.DocumentSymbol(
    symbol.name,
    symbol.detail || "",
    asSymbolKind(symbol.kind),
    asRange(symbol.range),
    asRange(symbol.selectionRange || symbol.range)
  );
  documentSymbol.children = (symbol.children || []).map(asDocumentSymbol);
  return documentSymbol;
}

function asSymbolInformation(symbol) {
  return new vscode.SymbolInformation(
    symbol.name,
    asSymbolKind(symbol.kind),
    symbol.containerName || "",
    asLocation(symbol.location)
  );
}

function asCompletionKind(kind) {
  return vscode.CompletionItemKind.Text + Math.max(0, Math.min(Number(kind || 1), 25)) - 1;
}

function asSymbolKind(kind) {
  return Math.max(1, Math.min(Number(kind || 1), 26));
}

function textDocument(document) {
  return { uri: document.uri.toString() };
}

function textParams(document, position) {
  return {
    textDocument: textDocument(document),
    position: { line: position.line, character: position.character }
  };
}

function isAppGen(document) {
  return document.languageId === "appgen";
}

function registerCommand(context, command, handler) {
  context.subscriptions.push(vscode.commands.registerCommand(command, () => {
    Promise.resolve(handler()).catch((error) => vscode.window.showErrorMessage(error.message));
  }));
}

function appgenCommand() {
  return vscode.workspace.getConfiguration("appgen").get("command") || "appgen";
}

function activeFile() {
  const editor = vscode.window.activeTextEditor;
  if (!editor || editor.document.languageId !== "appgen") {
    throw new Error("Open an AppGen-X DSL file first.");
  }
  return editor.document.uri.fsPath;
}

function workspaceRoot() {
  const folders = vscode.workspace.workspaceFolders;
  return folders && folders.length ? folders[0].uri.fsPath : process.cwd();
}

function runForActiveFile(args, title) {
  return runAppGen(args, title).then((result) => {
    vscode.window.showInformationMessage(`${title} completed with exit ${result.code}`);
    return result;
  });
}

function runAppGen(args, title) {
  return new Promise((resolve) => {
    const output = vscode.window.createOutputChannel(title);
    output.show(true);
    output.appendLine(`$ ${appgenCommand()} ${args.join(" ")}`);
    const child = cp.spawn(appgenCommand(), args, { cwd: workspaceRoot() });
    child.stdout.on("data", (chunk) => output.append(chunk.toString()));
    child.stderr.on("data", (chunk) => output.append(chunk.toString()));
    child.on("close", (code) => resolve({ code, output }));
  });
}

function runAppGenJson(args, title) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    const errors = [];
    const child = cp.spawn(appgenCommand(), args, { cwd: workspaceRoot() });
    child.stdout.on("data", (chunk) => chunks.push(chunk));
    child.stderr.on("data", (chunk) => errors.push(chunk));
    child.on("error", reject);
    child.on("close", (code) => {
      const stdout = Buffer.concat(chunks).toString("utf8");
      const stderr = Buffer.concat(errors).toString("utf8");
      if (code !== 0 && !stdout.trim()) {
        reject(new Error(`${title} failed with exit ${code}: ${stderr}`));
        return;
      }
      try {
        resolve({ code, payload: JSON.parse(stdout), stderr });
      } catch (error) {
        reject(new Error(`${title} did not return JSON: ${error.message}`));
      }
    });
  });
}

function showJsonPreview(title, payload, renderer) {
  const panel = vscode.window.createWebviewPanel(
    "appgenPreview",
    title,
    vscode.ViewColumn.Beside,
    { enableScripts: false }
  );
  panel.webview.html = renderer ? renderer(payload) : renderJsonDocument(title, payload);
}

function renderJsonDocument(title, payload) {
  return `<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { font-family: var(--vscode-font-family); padding: 16px; }
    pre { white-space: pre-wrap; background: var(--vscode-textCodeBlock-background); padding: 12px; }
  </style>
</head>
<body>
  <h1>${escapeHtml(title)}</h1>
  <pre>${escapeHtml(JSON.stringify(payload, null, 2))}</pre>
</body>
</html>`;
}

function renderGraphPreview(payload) {
  const reports = payload.reports || {};
  const sections = Object.entries(reports).map(([kind, report]) => {
    const graph = report.graph || {};
    const nodes = graph.nodes || [];
    const edges = graph.edges || [];
    return `<section>
      <h2>${escapeHtml(kind)}</h2>
      <p>${nodes.length} nodes, ${edges.length} edges</p>
      <h3>Nodes</h3>
      <ul>${nodes.map((node) => `<li>${escapeHtml(node.id || node.name || JSON.stringify(node))}</li>`).join("")}</ul>
      <h3>Edges</h3>
      <ul>${edges.map((edge) => `<li>${escapeHtml(edge.from || "")} -> ${escapeHtml(edge.to || "")} ${escapeHtml(edge.label || "")}</li>`).join("")}</ul>
    </section>`;
  }).join("");
  return previewShell("AppGen-X Graph Preview", sections || `<pre>${escapeHtml(JSON.stringify(payload, null, 2))}</pre>`);
}

function renderSemanticModel(payload) {
  const sourceFiles = payload.source_files || [];
  const symbols = payload.symbols || {};
  const tables = payload.tables || {};
  const views = payload.views || {};
  const flows = payload.flows || {};
  const diagnostics = payload.diagnostics || [];
  const symbolCounts = payload.source_file_symbol_counts || {};
  const symbolRows = Object.entries(symbolCounts).map(([file, count]) => `<li>${escapeHtml(file)}: ${escapeHtml(count)} symbols</li>`).join("");
  const body = `<p>Status: ${escapeHtml(payload.ok ? "ok" : "failed")}</p>
    <p>Format: ${escapeHtml(payload.format || "")}</p>
    <p>Source mode: ${escapeHtml(payload.source_mode || "file")}; files: ${sourceFiles.length}; symbols: ${Object.keys(symbols).length}</p>
    <h2>Source Files</h2>
    <ul>${sourceFiles.map((file) => `<li>${escapeHtml(file)}</li>`).join("")}</ul>
    <h2>Symbols By File</h2>
    <ul>${symbolRows}</ul>
    <h2>Model Summary</h2>
    <ul>
      <li>Tables: ${Object.keys(tables).length}</li>
      <li>Views: ${Object.keys(views).length}</li>
      <li>Flows: ${Object.keys(flows).length}</li>
      <li>Diagnostics: ${diagnostics.length}</li>
    </ul>
    <details><summary>Raw semantic model</summary><pre>${escapeHtml(JSON.stringify(payload, null, 2))}</pre></details>`;
  return previewShell("AppGen-X Semantic Model", body);
}

function renderArtifactPreview(payload) {
  const artifacts = payload.artifacts || payload.written_artifacts || [];
  const gaps = payload.blocking_gaps || [];
  const body = `<p>Status: ${escapeHtml(payload.ok ? "ok" : "failed")}</p>
    <h2>Artifacts</h2>
    <ul>${artifacts.map((artifact) => `<li>${escapeHtml(artifact.path || artifact.name || JSON.stringify(artifact))}</li>`).join("")}</ul>
    <h2>Blocking Gaps</h2>
    <ul>${gaps.map((gap) => `<li>${escapeHtml(String(gap))}</li>`).join("")}</ul>
    <details><summary>Raw report</summary><pre>${escapeHtml(JSON.stringify(payload, null, 2))}</pre></details>`;
  return previewShell("AppGen-X Generated Artifact Preview", body);
}

function renderValidationReport(payload) {
  const diagnostics = payload.diagnostics || [];
  const gaps = payload.blocking_gaps || [];
  const targets = payload.targets || [];
  const body = `<p>Status: ${escapeHtml(payload.ok ? "ok" : "failed")}</p>
    <p>Targets: ${escapeHtml(targets.join(", ") || "default")}</p>
    <h2>Diagnostics</h2>
    <ul>${diagnostics.map((diagnostic) => `<li>${escapeHtml(diagnostic.code || "")} ${escapeHtml(diagnostic.message || JSON.stringify(diagnostic))}</li>`).join("")}</ul>
    <h2>Blocking Gaps</h2>
    <ul>${gaps.map((gap) => `<li>${escapeHtml(String(gap))}</li>`).join("")}</ul>
    <details><summary>Raw validation report</summary><pre>${escapeHtml(JSON.stringify(payload, null, 2))}</pre></details>`;
  return previewShell("AppGen-X Validation", body);
}

function renderDesignerSync(payload) {
  const surfaces = payload.surfaces || [];
  const checks = payload.checks || [];
  const projections = payload.projections || {};
  const body = `<p>Status: ${escapeHtml(payload.ok ? "ok" : "failed")}</p>
    <p>Semantic model: ${escapeHtml(payload.semantic_model_format || "")}</p>
    <h2>Surfaces</h2>
    <ul>${surfaces.map((surface) => `<li>${escapeHtml(surface)}</li>`).join("")}</ul>
    <h2>Projection Counts</h2>
    <ul>${Object.entries(projections).map(([key, value]) => `<li>${escapeHtml(key)}: ${escapeHtml(Array.isArray(value) ? value.length : Object.keys(value || {}).length)}</li>`).join("")}</ul>
    <h2>Checks</h2>
    <ul>${checks.map((check) => `<li>${escapeHtml(check.id || check.check || "check")}: ${escapeHtml(check.ok ? "ok" : "failed")}</li>`).join("")}</ul>
    <details><summary>Raw designer sync report</summary><pre>${escapeHtml(JSON.stringify(payload, null, 2))}</pre></details>`;
  return previewShell("AppGen-X Designer Sync", body);
}

function renderMigrationPlan(payload) {
  const steps = payload.steps || payload.plan || [];
  const diagnostics = payload.diagnostics || [];
  const body = `<p>Status: ${escapeHtml(payload.ok ? "ok" : "failed")}</p>
    <p>Backend: ${escapeHtml(payload.backend || "")}</p>
    <h2>Plan</h2>
    <ol>${steps.map((step) => `<li>${escapeHtml(step.description || step.sql || step.kind || JSON.stringify(step))}</li>`).join("")}</ol>
    <h2>Diagnostics</h2>
    <ul>${diagnostics.map((diagnostic) => `<li>${escapeHtml(diagnostic.code || "")} ${escapeHtml(diagnostic.message || JSON.stringify(diagnostic))}</li>`).join("")}</ul>
    <details><summary>Raw migration plan</summary><pre>${escapeHtml(JSON.stringify(payload, null, 2))}</pre></details>`;
  return previewShell("AppGen-X Migration Plan", body);
}

function renderNaturalLanguagePlan(payload) {
  const operations = payload.edit_operations || payload.operations || [];
  const handoffs = payload.agent_handoffs || [];
  const compactModels = payload.compact_model_briefs || payload.compact_models || [];
  const body = `<p>Status: ${escapeHtml(payload.ok ? "ok" : "failed")}</p>
    <h2>Operations</h2>
    <ul>${operations.map((operation) => `<li>${escapeHtml(operation.kind || operation.type || JSON.stringify(operation))}</li>`).join("")}</ul>
    <h2>Agent Handoffs</h2>
    <ul>${handoffs.map((handoff) => `<li>${escapeHtml(handoff.vector || handoff.agent || handoff.id || "agent")}: ${escapeHtml((handoff.backends || []).join(", "))}</li>`).join("")}</ul>
    <h2>Compact Model Briefs</h2>
    <ul>${compactModels.map((model) => `<li>${escapeHtml(model.model || model.id || "")}: prompt ${escapeHtml(model.prompt_tokens || "")}, patch ${escapeHtml(model.patch_tokens || "")}, ok ${escapeHtml(model.ok)}</li>`).join("")}</ul>
    <details><summary>DSL Patch</summary><pre>${escapeHtml(payload.dsl_patch || "")}</pre></details>
    <details><summary>Raw natural language plan</summary><pre>${escapeHtml(JSON.stringify(payload, null, 2))}</pre></details>`;
  return previewShell("AppGen-X Natural Language Plan", body);
}

function renderAgentHandoff(payload) {
  const handoffs = payload.agent_handoffs || [];
  const compactModels = payload.compact_model_briefs || [];
  const commands = payload.commands || [];
  const notes = payload.token_budget_notes || [];
  const digest = payload.prompt_digest || {};
  const body = `<p>Status: ${escapeHtml(payload.ok ? "ok" : "failed")}</p>
    <p>Operation: ${escapeHtml(payload.operation || "")}</p>
    <p>Backends: ${escapeHtml((payload.observed_backends || []).join(", ") || "none")}</p>
    <h2>Agent Vectors</h2>
    <ul>${handoffs.map((handoff) => `<li><strong>${escapeHtml(handoff.vector || "")}</strong> launcher=${escapeHtml(handoff.launcher || "")}; backends=${escapeHtml((handoff.backends || []).join(", "))}; outputs=${escapeHtml((handoff.required_outputs || []).join(", "))}</li>`).join("")}</ul>
    <h2>Compact Model Briefs</h2>
    <ul>${compactModels.map((model) => `<li>${escapeHtml(model.model || "")}: ${escapeHtml(model.backend || "")}; prompt ${escapeHtml(model.prompt_tokens || "")}; patch ${escapeHtml(model.patch_tokens || "")}; ok ${escapeHtml(model.ok)}</li>`).join("")}</ul>
    <h2>Commands</h2>
    <ol>${commands.map((command) => `<li><code>${escapeHtml(command)}</code></li>`).join("")}</ol>
    <h2>Token Budget Notes</h2>
    <ul>${notes.map((note) => `<li>${escapeHtml(note)}</li>`).join("")}</ul>
    <details><summary>Prompt digest</summary><pre>${escapeHtml(JSON.stringify(digest, null, 2))}</pre></details>
    <details><summary>Raw agent handoff</summary><pre>${escapeHtml(JSON.stringify(payload, null, 2))}</pre></details>`;
  return previewShell("AppGen-X Coding Agent Handoff", body);
}

function renderReleaseVerifier(payload) {
  const reports = payload.reports || {};
  const checks = payload.checks || [];
  const body = `<p>Status: ${escapeHtml(payload.ok ? "ok" : "failed")}</p>
    <h2>Targets</h2>
    <ul>${Object.keys(reports).map((target) => `<li>${escapeHtml(target)}: ${escapeHtml(reports[target].ok ? "ok" : "failed")}</li>`).join("")}</ul>
    <h2>Checks</h2>
    <ul>${checks.map((check) => `<li>${escapeHtml(check.id || check.check || "check")}: ${escapeHtml(check.ok ? "ok" : "failed")}</li>`).join("")}</ul>
    <details><summary>Raw release verification</summary><pre>${escapeHtml(JSON.stringify(payload, null, 2))}</pre></details>`;
  return previewShell("AppGen-X Release Verification", body);
}

function renderToolingAudit(payload) {
  const checks = payload.checks || [];
  const gaps = payload.blocking_gaps || [];
  const body = `<p>Status: ${escapeHtml(payload.ok ? "ok" : "failed")}</p>
    <p>Source: ${escapeHtml(payload.source_of_truth || "")}</p>
    <h2>Checks</h2>
    <ul>${checks.map((check) => `<li>${escapeHtml(check.id || check.check || "check")}: ${escapeHtml(check.ok ? "ok" : "failed")} ${escapeHtml(check.section || "")}</li>`).join("")}</ul>
    <h2>Blocking Gaps</h2>
    <ul>${gaps.map((gap) => `<li>${escapeHtml(gap.id || JSON.stringify(gap))}</li>`).join("")}</ul>
    <details><summary>Raw tooling audit</summary><pre>${escapeHtml(JSON.stringify(payload, null, 2))}</pre></details>`;
  return previewShell("AppGen-X Tooling Audit", body);
}

function renderContractSchema(payload) {
  const formats = payload.available_schema_formats || payload.schemas && Object.keys(payload.schemas) || [];
  const selected = payload.selected_format || payload.format_name || "";
  const body = `<p>Status: ${escapeHtml(payload.ok ? "ok" : "failed")}</p>
    <p>Schema count: ${escapeHtml(payload.available_schema_count || formats.length || 0)}</p>
    <p>Selected: ${escapeHtml(selected || "all")}</p>
    <h2>Contract Formats</h2>
    <ul>${formats.slice(0, 250).map((format) => `<li>${escapeHtml(format)}</li>`).join("")}</ul>
    <details><summary>Raw schema catalog</summary><pre>${escapeHtml(JSON.stringify(payload, null, 2))}</pre></details>`;
  return previewShell("AppGen-X Contract Schemas", body);
}

function renderContractValidation(payload) {
  const diagnostics = payload.diagnostics || [];
  const groups = payload.grouped_counts || payload.counts || {};
  const body = `<p>Status: ${escapeHtml(payload.ok ? "ok" : "failed")}</p>
    <p>Payload format: ${escapeHtml(payload.payload_format || payload.inferred_format || "")}</p>
    <p>Schema format: ${escapeHtml(payload.schema_format || "")}</p>
    <h2>Counts</h2>
    <ul>${Object.entries(groups).map(([key, value]) => `<li>${escapeHtml(key)}: ${escapeHtml(JSON.stringify(value))}</li>`).join("")}</ul>
    <h2>Diagnostics</h2>
    <ul>${diagnostics.map((diagnostic) => `<li>${escapeHtml(diagnostic.code || "")} ${escapeHtml(diagnostic.message || JSON.stringify(diagnostic))}</li>`).join("")}</ul>
    <details><summary>Raw validation report</summary><pre>${escapeHtml(JSON.stringify(payload, null, 2))}</pre></details>`;
  return previewShell("AppGen-X Contract Validation", body);
}

function renderPbcCatalog(payload) {
  const pbcs = payload.pbcs || payload.catalog || payload.items || [];
  const items = Array.isArray(pbcs) ? pbcs : Object.entries(pbcs).map(([key, value]) => ({ key, ...value }));
  const body = `<p>${items.length} catalog entries</p>
    <ul>${items.map((item) => `<li><strong>${escapeHtml(item.key || item.name || item.id || "pbc")}</strong> ${escapeHtml(item.title || item.description || "")}</li>`).join("")}</ul>
    <details><summary>Raw report</summary><pre>${escapeHtml(JSON.stringify(payload, null, 2))}</pre></details>`;
  return previewShell("AppGen-X PBC Catalog", body);
}

function previewShell(title, body) {
  return `<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { font-family: var(--vscode-font-family); padding: 16px; }
    section { border-bottom: 1px solid var(--vscode-panel-border); margin-bottom: 16px; padding-bottom: 16px; }
    pre { white-space: pre-wrap; background: var(--vscode-textCodeBlock-background); padding: 12px; }
  </style>
</head>
<body>
  <h1>${escapeHtml(title)}</h1>
  ${body}
</body>
</html>`;
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function lintDocument(document) {
  if (!isAppGen(document)) {
    return;
  }
  return runAppGen(["lint", document.uri.fsPath, "--json"], "AppGen-X Lint");
}

function explainActiveSymbol() {
  const editor = vscode.window.activeTextEditor;
  const file = activeFile();
  const selection = editor.document.getText(editor.selection) || editor.document.getText(editor.document.getWordRangeAtPosition(editor.selection.active));
  const symbol = selection && selection.trim() ? selection.trim() : path.basename(file);
  return runForActiveFile(["explain", file, "--symbol", symbol, "--json"], "AppGen-X Explain");
}

function generateActiveFile() {
  const file = activeFile();
  const out = path.join(path.dirname(file), "generated");
  return runForActiveFile(["generate", file, "--out", out, "--json"], "AppGen-X Generate");
}

function previewGraph() {
  const file = activeFile();
  return runAppGenJson(["graph-suite", file, "--json"], "AppGen-X Graph Preview").then((result) => {
    showJsonPreview("AppGen-X Graph Preview", result.payload, renderGraphPreview);
  });
}

function previewSemanticModel() {
  const file = activeFile();
  return runAppGenJson(["semantic", file, "--json"], "AppGen-X Semantic Model Preview").then((result) => {
    showJsonPreview("AppGen-X Semantic Model", result.payload, renderSemanticModel);
  });
}

function validateActiveFile() {
  const file = activeFile();
  return runAppGenJson(["validate", file, "--targets", "web,mobile,desktop", "--json"], "AppGen-X Validation").then((result) => {
    showJsonPreview("AppGen-X Validation", result.payload, renderValidationReport);
  });
}

function previewDesignerSync() {
  const file = activeFile();
  return runAppGenJson(["designer-sync", file, "--json"], "AppGen-X Designer Sync").then((result) => {
    showJsonPreview("AppGen-X Designer Sync", result.payload, renderDesignerSync);
  });
}

function previewGeneratedArtifacts() {
  const file = activeFile();
  const out = path.join(path.dirname(file), ".appgen-preview");
  return runAppGenJson(["generate", file, "--out", out, "--allow-warnings", "--json"], "AppGen-X Artifact Preview").then((result) => {
    showJsonPreview("AppGen-X Generated Artifacts", result.payload, renderArtifactPreview);
  });
}

async function migrationPlan() {
  const current = activeFile();
  const previous = await vscode.window.showOpenDialog({
    canSelectFiles: true,
    canSelectFolders: false,
    canSelectMany: false,
    filters: { "AppGen-X DSL": ["appgen", "ag", "ags"] },
    openLabel: "Select previous DSL"
  });
  if (!previous || !previous.length) {
    return;
  }
  return runAppGenJson(["migration-plan", previous[0].fsPath, current, "--backend", "postgresql", "--json"], "AppGen-X Migration Plan").then((result) => {
    showJsonPreview("AppGen-X Migration Plan", result.payload, renderMigrationPlan);
  });
}

async function naturalLanguagePlan() {
  const file = activeFile();
  const prompt = await vscode.window.showInputBox({
    title: "AppGen-X Natural Language Change",
    prompt: "Describe the tables, forms, workflows, agents, reports, or UI changes to plan.",
    ignoreFocusOut: true
  });
  if (!prompt || !prompt.trim()) {
    return;
  }
  return runAppGenJson(["nl-plan", file, "--prompt", prompt.trim(), "--backend", "postgresql", "--json"], "AppGen-X Natural Language Plan").then((result) => {
    showJsonPreview("AppGen-X Natural Language Plan", result.payload, renderNaturalLanguagePlan);
  });
}

async function agentHandoff() {
  const file = activeFile();
  const prompt = await vscode.window.showInputBox({
    title: "AppGen-X Coding Agent Handoff",
    prompt: "Describe the bounded AppGen-X operation for the coding agent handoff.",
    value: "Build or evolve this AppGen-X application.",
    ignoreFocusOut: true
  });
  if (!prompt || !prompt.trim()) {
    return;
  }
  const operation = await vscode.window.showInputBox({
    title: "AppGen-X Operation Kind",
    prompt: "Use a compact operation label for the handoff contract.",
    value: "bounded_dsl_change",
    ignoreFocusOut: true
  });
  if (!operation || !operation.trim()) {
    return;
  }
  const vector = await vscode.window.showQuickPick(
    ["all", "claude_code", "openai_codex", "opencode"],
    { title: "Coding Agent Vector", placeHolder: "Select the target coding agent vector." }
  );
  if (!vector) {
    return;
  }
  const backend = await vscode.window.showQuickPick(
    ["all", "api-key", "ollama", "vllm"],
    { title: "LLM Backend", placeHolder: "Select the model/backend path." }
  );
  if (!backend) {
    return;
  }
  return runAppGenJson(
    ["agent-handoff", file, "--prompt", prompt.trim(), "--operation", operation.trim(), "--vector", vector, "--backend", backend, "--json"],
    "AppGen-X Coding Agent Handoff"
  ).then((result) => {
    showJsonPreview("AppGen-X Coding Agent Handoff", result.payload, renderAgentHandoff);
  });
}

function verifyRelease() {
  const file = activeFile();
  return runAppGenJson(["verify", file, "--target", "all", "--json"], "AppGen-X Release Verification").then((result) => {
    showJsonPreview("AppGen-X Release Verification", result.payload, renderReleaseVerifier);
  });
}

function packageActiveFile() {
  const file = activeFile();
  const out = path.join(path.dirname(file), "dist");
  return runForActiveFile(["package", file, "--out", out, "--json"], "AppGen-X Package");
}

function doctorReport() {
  return runAppGenJson(["doctor", "--json"], "AppGen-X Doctor").then((result) => {
    showJsonPreview("AppGen-X Doctor", result.payload, renderToolingAudit);
  });
}

function toolingAudit() {
  return runAppGenJson(["tooling-audit", "--json"], "AppGen-X Tooling Audit").then((result) => {
    showJsonPreview("AppGen-X Tooling Audit", result.payload, renderToolingAudit);
  });
}

function contractSchemaCatalog() {
  return runAppGenJson(["contract-schema", "--json"], "AppGen-X Contract Schemas").then((result) => {
    showJsonPreview("AppGen-X Contract Schemas", result.payload, renderContractSchema);
  });
}

async function validateSemanticContract() {
  const file = activeFile();
  const semantic = await runAppGenJson(["semantic", file, "--json"], "AppGen-X Semantic Model");
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "appgen-contract-"));
  const semanticPath = path.join(tempDir, "semantic-model.json");
  fs.writeFileSync(semanticPath, JSON.stringify(semantic.payload, null, 2), "utf8");
  return runAppGenJson(
    ["contract-validate", semanticPath, "--format", "appgen.semantic-model.v1", "--json"],
    "AppGen-X Contract Validation"
  ).then((result) => {
    showJsonPreview("AppGen-X Contract Validation", result.payload, renderContractValidation);
  });
}

function browsePbcCatalog() {
  return runAppGenJson(["pbc", "list", "--json"], "AppGen-X PBC Catalog").then((result) => {
    showJsonPreview("AppGen-X PBC Catalog", result.payload, renderPbcCatalog);
  });
}

module.exports = {
  activate,
  deactivate
};
