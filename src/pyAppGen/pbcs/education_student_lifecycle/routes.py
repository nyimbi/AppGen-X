from .services import EducationStudentLifecycleService, service_operation_manifest

PBC_KEY = "education_student_lifecycle"
ROUTE_DEFINITIONS = (
    {"route": "POST /student-applicants", "operation": "register_student_applicant", "required_permission": f"{PBC_KEY}.create"},
    {"route": "POST /applicant-documents", "operation": "review_applicant_documents", "required_permission": f"{PBC_KEY}.update"},
    {"route": "POST /enrollments", "operation": "activate_enrollment", "required_permission": f"{PBC_KEY}.approve"},
    {"route": "POST /curriculum-plans", "operation": "maintain_curriculum_plan", "required_permission": f"{PBC_KEY}.update"},
    {"route": "POST /course-attempts", "operation": "register_course_attempt", "required_permission": f"{PBC_KEY}.update"},
    {"route": "POST /advising-cases", "operation": "open_advising_case", "required_permission": f"{PBC_KEY}.update"},
    {"route": "POST /academic-petitions", "operation": "submit_academic_petition", "required_permission": f"{PBC_KEY}.create"},
    {"route": "POST /graduation-clearances", "operation": "prepare_graduation_clearance", "required_permission": f"{PBC_KEY}.approve"},
    {"route": "POST /credentials", "operation": "award_credential", "required_permission": f"{PBC_KEY}.approve"},
    {"route": "GET /education-student-lifecycle-workbench", "operation": "build_student_lifecycle_workbench", "required_permission": f"{PBC_KEY}.read"},
)
ROUTES = tuple(item["route"] for item in ROUTE_DEFINITIONS)


def api_route_contracts():
    contracts = tuple(
        {
            "route": item["route"],
            "method": item["route"].split()[0],
            "path": item["route"].split()[1],
            "operation": item["operation"],
            "pbc": PBC_KEY,
            "idempotency_key": f"{PBC_KEY}:{item['route']}",
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "required_permission": item["required_permission"],
        }
        for item in ROUTE_DEFINITIONS
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts():
    manifest = service_operation_manifest()
    known_ops = set(manifest["command_operations"] + manifest["query_operations"])
    contracts = api_route_contracts()["contracts"]
    return {
        "ok": all(contract["operation"] in known_ops for contract in contracts),
        "pbc": PBC_KEY,
        "service_mismatches": tuple(contract["route"] for contract in contracts if contract["operation"] not in known_ops),
        "missing_idempotency": tuple(contract for contract in contracts if not contract["idempotency_key"]),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route, payload=None):
    definition = next((item for item in ROUTE_DEFINITIONS if item["route"] == route), None)
    if definition is None:
        return {"ok": False, "route": route, "reason": "unknown_route", "side_effects": ()}
    service = EducationStudentLifecycleService()
    result = getattr(service, definition["operation"])(payload or {})
    return {"ok": result["ok"], "route": route, "payload": dict(payload or {}), "operation_contract": result["operation_contract"], "result": result, "side_effects": ()}


def smoke_test():
    return {"ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and dispatch_route(ROUTES[0], {"program_code": "BSCS", "required_documents": (), "application_stage": "accepted", "decision_status": "accepted"})["ok"], "side_effects": ()}
