# Airport Operations Management

This package now contains a real executable airport operations slice for gate and stand compatibility planning. The implemented behavior focuses on backlog item 1 and produces operationally meaningful assignment decisions rather than generic contract placeholders.

## What The Slice Does

- evaluates candidate stands against an incoming flight profile
- selects the best viable stand when one exists
- returns machine-readable reject reasons when a stand is blocked
- records rejected assignments as explicit operational exceptions
- exposes decision-support metadata to runtime, service, UI, and agent surfaces

## Operational Constraints Currently Modeled

- aircraft family support
- wingspan code envelope
- international-arrival capability
- contact versus remote stand requirements
- hydrant fuel requirement
- ground power requirement
- preconditioned air requirement
- remote-stand bussing support
- adjacent stand shadow conflicts

## Primary Entry Points

- `compatibility.py`
  Core compatibility matrix and explanation logic.
- `runtime.py`
  `airport_operations_management_evaluate_gate_assignment_compatibility`
  `airport_operations_management_command_gate_assignment`
  `airport_operations_management_query_workbench`
- `services.py`
  `AirportOperationsManagementService().evaluate_gate_assignment_compatibility(...)`
- `agent.py`
  `gate_assignment_decision_rationale(...)`

## Example

```python
from pyAppGen.pbcs.airport_operations_management.runtime import (
    airport_operations_management_evaluate_gate_assignment_compatibility,
)

result = airport_operations_management_evaluate_gate_assignment_compatibility(
    {
        "flight_number": "AX220",
        "aircraft_family": "narrowbody",
        "wingspan_code": "C",
        "operation_type": "domestic",
    }
)
```

The result includes a recommended option when a stand is viable, otherwise a blocked outcome with machine-readable reason codes. All emitted event references remain on the AppGen-X contract.

## Current Boundaries

- No new dependencies were added.
- The slice remains package-local.
- Backends remain limited to PostgreSQL, MySQL, and MariaDB.
- The current implementation uses request-supplied or default stand fixtures rather than a persisted live airport stand inventory.
