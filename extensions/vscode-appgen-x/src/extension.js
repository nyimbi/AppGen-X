"use strict";

const cp = require("child_process");
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
  registerCommand(context, "appgen.format", () => runForActiveFile(["format", activeFile(), "--write", "--json"], "AppGen-X Format"));
  registerCommand(context, "appgen.graph", () => runForActiveFile(["graph-suite", activeFile(), "--json"], "AppGen-X Graphs"));
  registerCommand(context, "appgen.previewGraph", previewGraph);
  registerCommand(context, "appgen.explain", explainActiveSymbol);
  registerCommand(context, "appgen.generate", generateActiveFile);
  registerCommand(context, "appgen.previewArtifacts", previewGeneratedArtifacts);
  registerCommand(context, "appgen.package", packageActiveFile);
  registerCommand(context, "appgen.pbcCatalog", browsePbcCatalog);
  registerCommand(context, "appgen.restartLanguageServer", () => client.restart());
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
      return client.request("textDocument/rename", { ...textParams(document, position), newName }).then(asWorkspaceEdit);
    }
  }));
  context.subscriptions.push(vscode.languages.registerWorkspaceSymbolProvider({
    provideWorkspaceSymbols(query) {
      return client.request("workspace/symbol", { query }).then((symbols) => (symbols || []).map(asSymbolInformation));
    }
  }));
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

function previewGeneratedArtifacts() {
  const file = activeFile();
  const out = path.join(path.dirname(file), ".appgen-preview");
  return runAppGenJson(["generate", file, "--out", out, "--allow-warnings", "--json"], "AppGen-X Artifact Preview").then((result) => {
    showJsonPreview("AppGen-X Generated Artifacts", result.payload, renderArtifactPreview);
  });
}

function packageActiveFile() {
  const file = activeFile();
  const out = path.join(path.dirname(file), "dist");
  return runForActiveFile(["package", file, "--out", out, "--json"], "AppGen-X Package");
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
