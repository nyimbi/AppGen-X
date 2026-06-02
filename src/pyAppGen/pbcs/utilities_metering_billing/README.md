# Utilities Metering and Billing PBC

`utilities_metering_billing` is a standalone AppGen-X packaged business capability for service point, meter, read-to-bill, tariff, billing, adjustment, dispute, and regulatory utility billing operations. It covers service point identity, energization, meter assets, meter exchanges, read provenance, validation ladders, interval completeness, estimates, tariffs, billing cycles, usage calculation, bill simulation, adjustments, payments-boundary evidence, disputes, exception workbenches, regulatory reporting, and governed assistant support.

## Owned Domain

The PBC owns service points, customer meter accounts, service orders, meter assets, meter installs/exchanges, meter reads, usage intervals, estimates, tariffs, billing cycles, utility bills, billing adjustments, customer charges, payment allocation evidence, exception cases, disputes, regulatory reports, rule/configuration records, governed model metadata, and AppGen-X event artifacts. Customer master, cash settlement, collections, field workforce, asset management, and external AMI/head-end platforms remain API/event/projection dependencies.

## Standalone Application Surface

The executable `UtilitiesMeteringBillingStandaloneApp` lives in `slice_app.py` and is exposed through `standalone.py`. It provides configuration, parameters, rules, schema extensions, idempotent event intake, service point creation, meter registration and exchange, meter read capture, validation, interval recording, estimate creation, tariff review, service-order approval, billing cycle creation, usage calculation, bill simulation, adjustment governance, customer charge/payment allocation evidence, exception/dispute workflows, regulatory report previews, UI contracts, agent contracts, and release evidence.

## UI and Agent

Forms, wizards, controls, queues, detail panels, and assistant contracts are PBC-local. The agent can explain reads, exceptions, tariff notices, adjustments, bill narratives, and regulatory scenarios, but all datastore mutations are previewed and confirmation-gated. The composed application receives a single-agent skill namespace, not a separate chatbot silo.

## Verification

See `implementation-status.md` for compile, pytest, diff-check, and focused audit evidence.
