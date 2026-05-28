# Cross Border Trade PBC

`cross_border_trade` is the AppGen-X Packaged Business Capability for international trade execution. A generated app can include only this PBC and still provide a working trade compliance workspace with database-backed forms, wizards, release controls, workbench views, services, routes, AppGen-X events, and an assistant that turns trade documents into governed CRUD previews.

## Owned Boundary

The PBC owns HS classifications, landed-cost quotes, export-control checks, customs declarations, denied-party screenings, document packets, broker handoffs, carrier handoffs, compliance holds, country restriction policies, runtime rules, parameters, configuration, schema extensions, audit evidence, and AppGen-X inbox/outbox/dead-letter tables.

It does not share order, inventory, payment, broker, carrier, customer, or audit tables. Those dependencies are represented through declared APIs, consumed events, emitted events, and projections.

Supported ordinary datastore backends are PostgreSQL, MySQL, and MariaDB. Eventing is fixed to the AppGen-X event contract; there is no user-facing stream-engine picker.

## Application Surface

The standalone trade app exposes specialist forms for:

- HS classification readiness and approval.
- Landed-cost quote creation with duty, tax, fee, currency, and Incoterm trace.
- Restricted-party screening and fuzzy-match adjudication.
- Export-control and license requirement checks.
- Customs declaration filing and release.
- Compliance hold opening and resolution.

Guided wizards cover classification approval, landed-cost scenarios, restricted-party resolution, customs declaration release, and policy change impact. Controls block unsafe release when classification evidence, landed-cost trace, screening, export license, documents, broker handoff, carrier handoff, hold resolution, owned-boundary, or AppGen-X event requirements are missing.

## Workbench

`CrossBorderTradeWorkbench` is the command center for classifications, landed cost, export controls, declarations, broker submissions, trade documents, topology, exposure, exceptions, rules, parameters, configuration, eventing, and dead letters.

The rendered workbench includes cards for classification count, quote count, export control count, declaration count, compliance holds, dead letters, and rule coverage. It also carries form, wizard, control, and single-PBC app metadata so a generated one-PBC application can render the full domain surface without another PBC.

## Agent And Documents

`CrossBorderTradeAgent` contributes skills to the composed application assistant and can also operate in a one-PBC app. It plans document and instruction handling for invoices, packing lists, certificates, end-use statements, customs declarations, denied-party evidence, broker requests, carrier requests, duties, taxes, and Incoterms.

Every mutation plan stays side-effect-free, targets only owned tables, declares the proposed command, requires human confirmation, and uses AppGen-X event evidence.

## Developer Entry Points

- `runtime.py` contains the executable trade lifecycle, rules, parameters, schema extensions, event handling, release gates, controls, analytics, and smoke audit.
- `app_surface.py` contains the standalone forms, wizards, controls, document planning, and single-PBC app contract.
- `services.py` and `routes.py` expose route-bound service commands.
- `ui.py` exposes the workbench, forms, wizards, controls, and single-PBC metadata.
- `agent.py` exposes chatbot skills, document instruction planning, and governed CRUD plans.
- `release_evidence.py` includes the standalone app surface in readiness evidence.

## Validation

Run package tests:

```bash
./.venv/bin/pytest -q src/pyAppGen/pbcs/cross_border_trade/tests
```

Run release checks:

```bash
./.venv/bin/python - <<'PY'
from pyAppGen.pbc import pbc_generation_smoke_audit, pbc_implementation_release_audit
keys = ("cross_border_trade",)
print(pbc_implementation_release_audit(keys)["ok"])
print(pbc_generation_smoke_audit(keys)["ok"])
PY
```
