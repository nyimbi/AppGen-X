# Telecom Subscription Lifecycle PBC

`telecom_subscription_lifecycle` is a standalone AppGen-X packaged business capability for telecom line and subscription operations. It supports subscriber aggregates, plan versioning, SIM and eSIM assignment, activation decomposition, provisioning readiness, number portability, usage threshold actions, roaming entitlement/spend protection, churn reason tracking, and governed assistant previews.

## Owned Domain

The PBC owns subscriber account, service plan, SIM profile, activation request, usage session, roaming event, churn risk, policy rule, runtime parameter, schema extension, control assertion, governed model, and AppGen-X event tables. Billing, invoice, customer master, network adapter, device fulfillment, courier, and partner systems are represented only through declared APIs/events/projections.

## Standalone Application Surface

`TelecomSubscriptionLifecycleStandaloneApp` exposes plan definition, subscription creation, SIM/eSIM assignment, activation request and completion, portability cases, usage threshold evaluation, roaming enablement, churn/save offers, and assistant mutation previews. The app contract includes forms, wizards, controls, workbench, routes, services, schema, permissions, and composed-agent metadata.

## UI and Agent

Forms and wizards surface new activation, eSIM install, SIM swap review, portability, roaming shock protection, retention, and assistant preview workflows. The agent contributes `telecom_subscription_lifecycle_skills`, can draft owned-table CRUD previews, and requires human confirmation for mutations.

## Verification

See `implementation-status.md` for compile, pytest, diff-check, and focused audit evidence.
