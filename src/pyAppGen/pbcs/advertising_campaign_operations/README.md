# Advertising Campaign Operations

This PBC now includes an executable advertising-specific slice for campaign planning and launch control.

## Implemented Slice

- Canonical campaign brief normalization and validation.
- Deterministic campaign plan creation from a structured brief.
- Pre-launch readiness review with explicit blockers.
- Launch attempt handling that transitions plans to `ready_for_launch` or `launch_blocked`.
- Workbench command-center summary data for ready versus blocked launch plans.
- Assistant previews for campaign brief validation and launch readiness review.

## Package Entry Points

- `runtime.py`
  - `advertising_campaign_operations_create_campaign_plan`
  - `advertising_campaign_operations_review_launch_readiness`
  - `advertising_campaign_operations_attempt_launch_campaign`
- `services.py`
  - `AdvertisingCampaignOperationsService.create_campaign_plan`
  - `AdvertisingCampaignOperationsService.review_launch_readiness`
  - `AdvertisingCampaignOperationsService.attempt_launch_campaign`
- `ui.py`
  - `advertising_campaign_operations_render_workbench`
- `agent.py`
  - `campaign_brief_preview`
  - `launch_readiness_preview`

## Behavior Summary

`campaign_planning.py` provides the shared domain logic. It requires every campaign brief to include:

- `objective`
- `offer`
- `audience_promise`
- `channels`
- `primary_kpi`
- `guardrails`
- `launch_dependencies`

Equivalent briefs normalize to the same deterministic shape and fingerprint. Launch readiness stays blocked until:

- budget is approved,
- creative is approved,
- audience is ready,
- placements are ready,
- tracking is ready,
- suppliers are eligible,
- policy is compliant,
- and all declared launch dependencies are marked ready.

## Event Contract

The implemented slice stays on the AppGen-X event contract and emits only declared PBC event types:

- `AdvertisingCampaignOperationsCreated`
- `AdvertisingCampaignOperationsApproved`
- `AdvertisingCampaignOperationsExceptionOpened`

## Validation

Validated with:

- `./.venv/bin/python -m py_compile src/pyAppGen/pbcs/advertising_campaign_operations/campaign_planning.py src/pyAppGen/pbcs/advertising_campaign_operations/runtime.py src/pyAppGen/pbcs/advertising_campaign_operations/services.py src/pyAppGen/pbcs/advertising_campaign_operations/ui.py src/pyAppGen/pbcs/advertising_campaign_operations/agent.py tests/test_pbc_advertising_campaign_operations_implementation.py`
- `./.venv/bin/pytest tests/test_pbc_advertising_campaign_operations_implementation.py tests/test_pbc_advertising_campaign_operations_runtime.py src/pyAppGen/pbcs/advertising_campaign_operations/tests/test_contract.py`
