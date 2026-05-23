# Deployment Guide

AppGen-generated applications include deployment and operations contracts for
containerized, orchestrated, and cloud-hosted releases.

## Generated Deployment Assets

Depending on the source and targets, generated output can include:

- `Dockerfile`
- `docker-compose.yml`
- `deploy/k8s.yaml`
- `deploy/k8s-autoscale.yaml`
- `deploy/terraform-aws.tf`
- `deploy/terraform-gcp.tf`
- `deploy/terraform-azure.tf`
- `deploy/Caddyfile`
- `deploy/appgen_https.py`
- `automation/appgen_node_red.py`
- `automation/node-red/flows.json`
- Backup, restore, search, and release-gate contracts.

Run the deployment and packaging audits:

```console
appgen --ops-release-audit
appgen --distribution-release-audit
```

## Local Container Workflow

Generate an app:

```console
appgen --dsl app.appgen --writedir generated/app/app
```

Review generated configuration:

```console
cd generated/app
ls Dockerfile docker-compose.yml deploy
```

Build and run with Compose:

```console
docker compose up --build
```

Use generated config workbench payloads to review database URLs, secrets,
feature flags, and deployment-specific settings before promoting the app.

## Database Configuration

Use `--wdatabase` to write a database URL or legacy PostgreSQL database name
into generated `config.py`:

```console
appgen --dsl app.appgen --writedir generated/app/app --wdatabase postgresql+psycopg2://user@host/db
```

For runtime environments, prefer environment variables and deployment secrets
over committed literal credentials.

## Kubernetes Workflow

Generate an app and inspect:

```console
appgen --dsl app.appgen --writedir generated/app/app
sed -n '1,220p' generated/app/deploy/k8s.yaml
```

The Kubernetes contract is intended as a starting point. Before production,
review:

- Image repository and tag policy.
- Database and cache service endpoints.
- Secret references.
- Ingress, TLS, and hostname configuration.
- Resource requests and limits.
- Autoscaling policy.
- Health checks and readiness checks.

## Terraform Workflow

Generated Terraform stubs provide cloud-specific starting points:

```text
deploy/terraform-aws.tf
deploy/terraform-gcp.tf
deploy/terraform-azure.tf
```

Review provider configuration, regions, networking, managed database choices,
secrets, IAM/service-account policy, and state backend before applying.

## HTTPS And Reverse Proxy

Generated deployments can include `deploy/Caddyfile` and HTTPS helper
contracts. Review:

- Hostnames.
- TLS automation policy.
- Upstream app port.
- Proxy headers.
- Static file behavior.
- Security headers.

## Node-RED Automation

Generated Node-RED exports live under:

```text
automation/appgen_node_red.py
automation/node-red/flows.json
```

Use them for integration workflows, webhook routing, approval automation, and
operations hooks. Validate the generated flow JSON before importing it into a
Node-RED runtime.

## Mobile And Desktop Releases

When `targets` includes `mobile` or `desktop`, generated native starters appear
under:

```text
native/mobile/
native/desktop/
```

Mobile release review should cover permissions, offline queues, push
notifications, camera/location access, platform packaging, and API endpoints.
Desktop release review should cover local cache, file access, sync replay,
keyboard navigation, packaging, and update policy.
Prepared-host native packaging should persist binary adapter transcripts with
tool, command, exit code, working directory, duration, and artifact paths. Feed
those transcripts plus artifact manifests into
`target_binary_adapter_execution_audit()` before claiming native package
execution succeeded.

Run:

```console
appgen --target-release-audit
appgen --target-binary-adapter-audit
```

CI can run the transcript audit directly through
`.github/workflows/native-package-transcripts.yml`. Use that workflow on
prepared hosts that can install the package and validate the generated binary
adapter transcript contract before publishing native artifacts.

## Agentic Runtime Configuration

Agentic apps can connect to local and API-backed LLMs. Local providers usually
need an endpoint such as Ollama:

```appgen
llm LocalModel {
  provider: ollama
  mode: local
  model: llama3
  endpoint: "http://localhost:11434"
}
```

API providers should reference environment variables:

```appgen
llm ApiModel {
  provider: openai
  mode: api
  model: gpt-4.1-mini
  api_key: OPENAI_API_KEY
}
```

Before deployment, check that required environment variables are configured and
that generated tool policies require review for application-changing actions:

```console
appgen --agentic-release-audit
```

## Release Checklist

Before a release:

1. Regenerate from committed source DSL/schema.
2. Run `appgen --lint-dsl` and `appgen --dsl-authoring-gate` for DSL sources.
3. Run source-specific audits such as `--source-intake-release-audit`.
4. Run target audits such as `--target-release-audit`.
5. Run security, config, reporting, integration, and ops audits for touched
   capabilities.
6. Run `appgen --package-goal-audit` for aggregate evidence.
7. Build the container or native package.
8. Smoke test the deployed app, generated Studio, and critical workflows.

## Troubleshooting

If generation fails:

- Run the DSL linter or source intake audit.
- Check relation targets and enum values.
- Confirm SQLAlchemy database URLs include the correct driver.
- Keep PonyORM scripts import-safe even though AppGen parses them statically.
- Inspect `appgen.json` for source fingerprint and known lossy areas.

If deployment fails:

- Validate environment variables and database URLs.
- Check container logs.
- Confirm generated deployment files reference the correct app paths.
- Review secrets and API-key provider configuration.
- Re-run `appgen --ops-release-audit` after changing deployment contracts.
