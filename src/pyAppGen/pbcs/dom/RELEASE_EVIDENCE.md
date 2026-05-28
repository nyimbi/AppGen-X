# Distributed Order Management Release Evidence

Directory: `src/pyAppGen/pbcs/dom`

## Executable surfaces

- `standalone.DomStandaloneApplication`
- `services.DomStandaloneService`
- `routes.dispatch_standalone_route`
- `ui.dom_ui_contract`
- `agent.document_instruction_plan`
- `audit.run_dom_pbc_audit`

## Release checks

- standalone_application
- standalone_service_methods
- ui_forms_wizards_controls
- agent_document_intake
- api_event_contract
- permissions_cover_commands
- documentation_present
- package_audit

## Fixed platform constraints

- `event_contract = AppGen-X`
- `event_topic = appgen.dom.events`
- `stream_engine_picker_visible = false`
- `allowed_backends = postgresql, mysql, mariadb`
