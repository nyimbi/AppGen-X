"""Generated owned schema evidence for the order_routing_optimization PBC."""

SCHEMA_CONTRACT = {'format': 'appgen.order-routing-optimization-owned-schema-contract.v1', 'ok': True, 'tables': ({'logical_table': 'routing_rule', 'owned_table': 'order_routing_optimization_routing_rule', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'route_candidate', 'owned_table': 'order_routing_optimization_route_candidate', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'routing_rule_id', 'type': 'integer', 'required': True, 'references': 'order_routing_optimization_routing_rule.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'routing_rule_id', 'target_table': 'order_routing_optimization_routing_rule', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'capacity_snapshot', 'owned_table': 'order_routing_optimization_capacity_snapshot', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'routing_rule_id', 'type': 'integer', 'required': True, 'references': 'order_routing_optimization_routing_rule.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'routing_rule_id', 'target_table': 'order_routing_optimization_routing_rule', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'routing_decision', 'owned_table': 'order_routing_optimization_routing_decision', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'routing_rule_id', 'type': 'integer', 'required': True, 'references': 'order_routing_optimization_routing_rule.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'routing_rule_id', 'target_table': 'order_routing_optimization_routing_rule', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'relationships': ({'from': 'routing_plan_leg.plan_id', 'to': 'routing_plan.plan_id', 'type': 'owned_child'}, {'from': 'routing_node_calendar.node_id', 'to': 'routing_node.node_id', 'type': 'owned_calendar'}, {'from': 'routing_node_service.node_id', 'to': 'routing_node.node_id', 'type': 'owned_service'}, {'from': 'routing_node_capacity.node_id', 'to': 'routing_node.node_id', 'type': 'owned_capacity'}, {'from': 'routing_constraint.rule_id', 'to': 'routing_rule.rule_id', 'type': 'owned_constraint'}, {'from': 'routing_cost_component.decision_id', 'to': 'routing_decision.decision_id', 'type': 'owned_cost'}, {'from': 'routing_promise.decision_id', 'to': 'routing_decision.decision_id', 'type': 'owned_promise'}, {'from': 'split_shipment_leg.split_shipment_id', 'to': 'split_shipment.split_shipment_id', 'type': 'owned_split_leg'}, {'from': 'node_reservation.decision_id', 'to': 'routing_decision.decision_id', 'type': 'owned_reservation'}, {'from': 'route_simulation_scenario.simulation_id', 'to': 'route_simulation.simulation_id', 'type': 'owned_simulation'}, {'from': 'optimization_candidate.run_id', 'to': 'optimization_run.run_id', 'type': 'owned_optimization_candidate'}, {'from': 'exception_resolution.exception_id', 'to': 'routing_exception.exception_id', 'type': 'owned_resolution'}, {'from': 'routing_approval.decision_id', 'to': 'routing_decision.decision_id', 'type': 'owned_approval'}, {'from': 'routing_feedback.decision_id', 'to': 'routing_decision.decision_id', 'type': 'owned_feedback'}), 'migrations': ('migrations/001_initial.sql',), 'models': ({'class_name': 'OrderRoutingOptimizationRoutingRule', 'table': 'order_routing_optimization_routing_rule', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'OrderRoutingOptimizationRouteCandidate', 'table': 'order_routing_optimization_route_candidate', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'routing_rule_id', 'type': 'integer', 'required': True, 'references': 'order_routing_optimization_routing_rule.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'routing_rule_id', 'target_table': 'order_routing_optimization_routing_rule', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'OrderRoutingOptimizationCapacitySnapshot', 'table': 'order_routing_optimization_capacity_snapshot', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'routing_rule_id', 'type': 'integer', 'required': True, 'references': 'order_routing_optimization_routing_rule.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'routing_rule_id', 'target_table': 'order_routing_optimization_routing_rule', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'OrderRoutingOptimizationRoutingDecision', 'table': 'order_routing_optimization_routing_decision', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'routing_rule_id', 'type': 'integer', 'required': True, 'references': 'order_routing_optimization_routing_rule.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'routing_rule_id', 'target_table': 'order_routing_optimization_routing_rule', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'shared_table_access': False, 'pbc': 'order_routing_optimization', 'owned_tables': ('order_routing_optimization_routing_rule', 'order_routing_optimization_route_candidate', 'order_routing_optimization_capacity_snapshot', 'order_routing_optimization_routing_decision'), 'database_backends': ('postgresql',)}


def build_schema_contract():
    """Return generated owned schema, migration, and model evidence."""
    return dict(SCHEMA_CONTRACT)


def validate_schema_contract():
    """Validate owned table, migration, model, and datastore evidence."""
    contract = build_schema_contract()
    pbc = contract['pbc']
    owned_tables = tuple(contract.get('owned_tables', ()))
    raw_model_tables = tuple(
        model.get('table')
        for model in contract.get('models', ())
        if isinstance(model, dict) and model.get('table')
    )
    model_tables = tuple(
        table if table.startswith(f'{pbc}_') else f'{pbc}_{table}'
        for table in raw_model_tables
    )
    migration_paths = tuple(contract.get('migrations', ()))
    allowed_backends = {'postgresql', 'mysql', 'mariadb'}
    invalid_tables = tuple(table for table in owned_tables if not table.startswith(f'{pbc}_'))
    missing_models = tuple(table for table in owned_tables if model_tables and table not in model_tables)
    invalid_backends = tuple(
        backend for backend in contract.get('database_backends', ()) if backend not in allowed_backends
    )
    return {
        'ok': contract.get('ok') is True
        and bool(owned_tables)
        and bool(migration_paths)
        and not invalid_tables
        and not missing_models
        and not invalid_backends
        and contract.get('shared_table_access') is False,
        'pbc': pbc,
        'owned_tables': owned_tables,
        'raw_model_tables': raw_model_tables,
        'model_tables': model_tables,
        'migration_paths': migration_paths,
        'invalid_tables': invalid_tables,
        'missing_models': missing_models,
        'invalid_backends': invalid_backends,
        'side_effects': (),
    }


def smoke_test():
    """Exercise schema validation side-effect-free."""
    return validate_schema_contract()
