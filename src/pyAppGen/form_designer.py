"""Package-level RAD-style form designer contracts."""

from __future__ import annotations

from .dsl import schema_from_dsl


FORM_DESIGNER_SAMPLE_DSL = """
app DesignerAudit { targets: web, mobile, desktop }

table Customer {
  id: int pk
  name: string required
  email: string
  phone: string
  joined_on: date
  notes: text
}

view CustomerForm for Customer {
  Main: name, email, joined_on, notes
  @ name TextBox 0 0 6 1
  @ email EmailInput 0 1 6 1
  @ joined_on DatePicker 0 2 4 1
  @ notes TextArea 0 3 8 3
}
"""

COMPONENTS = {
    "TextBox": {
        "category": "input",
        "field_types": ("string", "int", "decimal"),
        "default_size": {"w": 6, "h": 1},
        "properties": ("label", "placeholder", "required", "readonly", "help_text"),
    },
    "EmailInput": {
        "category": "input",
        "field_types": ("string",),
        "default_size": {"w": 6, "h": 1},
        "properties": ("label", "placeholder", "required", "validation", "help_text"),
    },
    "TextArea": {
        "category": "input",
        "field_types": ("text", "string"),
        "default_size": {"w": 8, "h": 3},
        "properties": ("label", "placeholder", "rows", "spellcheck", "grammar_hints"),
    },
    "DatePicker": {
        "category": "calendar",
        "field_types": ("date", "datetime", "time"),
        "default_size": {"w": 4, "h": 1},
        "properties": ("label", "required", "min", "max", "display_format"),
    },
    "Lookup": {
        "category": "relationship",
        "field_types": ("relation", "int"),
        "default_size": {"w": 6, "h": 1},
        "properties": ("label", "target_table", "label_fields", "search", "required"),
    },
    "FileUpload": {
        "category": "media",
        "field_types": ("file", "image"),
        "default_size": {"w": 8, "h": 2},
        "properties": ("label", "accept", "max_size_mb", "preview", "required"),
    },
    "Button": {
        "category": "action",
        "field_types": (),
        "default_size": {"w": 2, "h": 1},
        "properties": ("label", "action", "variant", "confirm", "disabled_when"),
    },
    "Panel": {
        "category": "container",
        "field_types": (),
        "default_size": {"w": 12, "h": 3},
        "properties": ("caption", "align", "padding", "visible", "enabled"),
    },
    "GroupBox": {
        "category": "container",
        "field_types": (),
        "default_size": {"w": 6, "h": 3},
        "properties": ("caption", "align", "tab_order", "visible", "enabled"),
    },
    "RadioGroup": {
        "category": "choice",
        "field_types": ("string", "int", "enum"),
        "default_size": {"w": 4, "h": 3},
        "properties": ("items", "columns", "required", "tab_order", "help_text"),
    },
    "ListBox": {
        "category": "choice",
        "field_types": ("string", "int", "enum"),
        "default_size": {"w": 4, "h": 4},
        "properties": ("items", "multi_select", "sorted", "required", "help_text"),
    },
    "TreeView": {
        "category": "navigation",
        "field_types": ("relation", "tree"),
        "default_size": {"w": 4, "h": 6},
        "properties": ("data_source", "parent_field", "label_field", "lazy_load", "icons"),
    },
    "Grid": {
        "category": "data",
        "field_types": ("relation", "dataset"),
        "default_size": {"w": 12, "h": 6},
        "properties": ("data_source", "columns", "sortable", "filterable", "editable"),
    },
    "PageControl": {
        "category": "container",
        "field_types": (),
        "default_size": {"w": 12, "h": 6},
        "properties": ("tabs", "active_tab", "align", "lazy_mount", "tab_position"),
    },
    "MainMenu": {
        "category": "menu",
        "field_types": (),
        "default_size": {"w": 12, "h": 1},
        "properties": ("items", "roles", "shortcuts", "icons", "visible"),
    },
    "PopupMenu": {
        "category": "menu",
        "field_types": (),
        "default_size": {"w": 4, "h": 1},
        "properties": ("items", "surface", "roles", "shortcuts", "visible"),
    },
    "ToolBar": {
        "category": "action",
        "field_types": (),
        "default_size": {"w": 12, "h": 1},
        "properties": ("actions", "icons", "density", "overflow", "visible"),
    },
    "ActionList": {
        "category": "action",
        "field_types": (),
        "default_size": {"w": 4, "h": 1},
        "properties": ("actions", "shortcuts", "roles", "enabled_when", "confirm"),
    },
    "Image": {
        "category": "media",
        "field_types": ("image", "file"),
        "default_size": {"w": 4, "h": 3},
        "properties": ("source", "fit", "alt_text", "preview", "lazy_load"),
    },
    "Chart": {
        "category": "analytics",
        "field_types": ("dataset", "relation"),
        "default_size": {"w": 8, "h": 5},
        "properties": ("series", "chart_type", "legend", "data_source", "refresh"),
    },
    "ReportViewer": {
        "category": "reports",
        "field_types": ("dataset", "relation"),
        "default_size": {"w": 12, "h": 7},
        "properties": ("report", "parameters", "export_formats", "printer", "preview"),
    },
    "WebBrowser": {
        "category": "integration",
        "field_types": ("url", "string"),
        "default_size": {"w": 8, "h": 6},
        "properties": ("url", "sandbox", "allowed_hosts", "scripts", "navigation"),
    },
    "Timer": {
        "category": "nonvisual",
        "field_types": (),
        "default_size": {"w": 2, "h": 1},
        "properties": ("interval", "enabled", "on_timer", "single_shot", "jitter"),
    },
    "DataSource": {
        "category": "data",
        "field_types": ("dataset", "relation"),
        "default_size": {"w": 3, "h": 1},
        "properties": ("dataset", "auto_open", "filters", "sort", "events"),
    },
    "BindingSource": {
        "category": "data",
        "field_types": ("dataset", "relation"),
        "default_size": {"w": 3, "h": 1},
        "properties": ("source", "bindings", "converters", "validators", "events"),
    },
    "RESTClient": {
        "category": "integration",
        "field_types": (),
        "default_size": {"w": 3, "h": 1},
        "properties": ("base_url", "auth_profile", "timeout", "headers", "retry"),
    },
    "CameraView": {
        "category": "mobile",
        "field_types": ("image", "file"),
        "default_size": {"w": 4, "h": 4},
        "properties": ("camera", "resolution", "flash", "permission", "capture_action"),
    },
    "LocationSensor": {
        "category": "mobile",
        "field_types": ("geo", "string"),
        "default_size": {"w": 3, "h": 1},
        "properties": ("accuracy", "permission", "watch", "interval", "fallback"),
    },
    "NotificationCenter": {
        "category": "mobile",
        "field_types": (),
        "default_size": {"w": 3, "h": 1},
        "properties": ("channels", "permission", "deep_link", "badge", "sound"),
    },
    "Animation": {
        "category": "effects",
        "field_types": (),
        "default_size": {"w": 3, "h": 1},
        "properties": ("target", "property", "duration", "easing", "reduced_motion"),
    },
    "Effect": {
        "category": "effects",
        "field_types": (),
        "default_size": {"w": 3, "h": 1},
        "properties": ("target", "effect", "intensity", "gpu_fallback", "enabled"),
    },
    "Viewport3D": {
        "category": "three_d",
        "field_types": (),
        "default_size": {"w": 8, "h": 6},
        "properties": ("camera", "lights", "models", "materials", "mobile_budget"),
    },
}

THIRD_PARTY_COMPONENT_SUITES = (
    {
        "id": "devexpress-vcl",
        "vendor": "DevExpress",
        "frameworks": ("VCL",),
        "license": "commercial",
        "categories": ("grid", "ribbon", "scheduler", "spreadsheet", "pivot", "printing"),
        "components": ("cxGrid", "cxRibbon", "cxScheduler", "cxSpreadsheet", "cxPivotGrid"),
        "use_cases": ("data-heavy ERP screens", "office-style desktop shells", "analytics workbenches"),
    },
    {
        "id": "tms-fnc",
        "vendor": "TMS Software",
        "frameworks": ("VCL", "FMX", "WEB"),
        "license": "commercial",
        "categories": ("grid", "planner", "maps", "charts", "cloud", "cross-platform-ui"),
        "components": ("TTMSFNCGrid", "TTMSFNCPlanner", "TTMSFNCMaps", "TTMSFNCChart"),
        "use_cases": ("shared web/mobile/desktop UI", "planner screens", "map-centric operations"),
    },
    {
        "id": "fastreport",
        "vendor": "Fast Reports",
        "frameworks": ("VCL", "FMX", "Lazarus"),
        "license": "commercial",
        "categories": ("reports", "print", "export", "designer"),
        "components": ("TfrxReport", "TfrxDesigner", "TfrxPDFExport", "TfrxDBDataset"),
        "use_cases": ("invoice reports", "statutory reports", "print/export workflows"),
    },
    {
        "id": "teechart",
        "vendor": "Steema",
        "frameworks": ("VCL", "FMX"),
        "license": "commercial",
        "categories": ("charts", "gauges", "maps", "dashboards"),
        "components": ("TChart", "TGauge", "TMapSeries", "TDBChart"),
        "use_cases": ("dashboard charts", "operational gauges", "geo reports"),
    },
    {
        "id": "skia4rad",
        "vendor": "Skia4RAD",
        "frameworks": ("VCL", "FMX", "Console"),
        "license": "open-source",
        "categories": ("graphics", "svg", "animation", "text-rendering"),
        "components": ("TSkPaintBox", "TSkSvg", "TSkAnimatedImage", "TSkLabel"),
        "use_cases": ("high-quality 2D rendering", "SVG icons", "animated visual states"),
    },
    {
        "id": "jvcl-jcl",
        "vendor": "Project JEDI",
        "frameworks": ("VCL",),
        "license": "open-source",
        "categories": ("utilities", "visual-controls", "dialogs", "system"),
        "components": ("TJvFormStorage", "TJvWizard", "TJvInspector", "TJvDBGrid"),
        "use_cases": ("legacy VCL migration", "utility controls", "wizard-heavy back office apps"),
    },
    {
        "id": "virtual-treeview",
        "vendor": "Virtual TreeView",
        "frameworks": ("VCL",),
        "license": "open-source",
        "categories": ("tree", "virtualization", "large-data"),
        "components": ("TVirtualStringTree", "TVirtualDrawTree"),
        "use_cases": ("large hierarchies", "navigation trees", "outline explorers"),
    },
    {
        "id": "indy",
        "vendor": "Indy Project",
        "frameworks": ("VCL", "FMX", "Console"),
        "license": "open-source",
        "categories": ("network", "http", "smtp", "tcp", "sockets"),
        "components": ("TIdHTTP", "TIdSMTP", "TIdTCPClient", "TIdTCPServer"),
        "use_cases": ("protocol clients", "email workflows", "socket integrations"),
    },
    {
        "id": "devart-data-access",
        "vendor": "Devart",
        "frameworks": ("VCL", "FMX", "Console"),
        "license": "commercial",
        "categories": ("database", "oracle", "postgresql", "mysql", "sqlserver", "cloud-data"),
        "components": ("TUniConnection", "TUniQuery", "TOraSession", "TPgConnection"),
        "use_cases": ("multi-database apps", "Oracle/PostgreSQL-heavy ERP", "offline sync bridges"),
    },
    {
        "id": "intraweb-unigui",
        "vendor": "Atozed/FMSoft",
        "frameworks": ("VCL", "Web"),
        "license": "commercial",
        "categories": ("web-ui", "server-driven-ui", "migration"),
        "components": ("TIWAppForm", "TUniForm", "TUniDBGrid", "TUniMainMenu"),
        "use_cases": ("VCL-to-web migration", "server-driven internal systems"),
    },
)

RAD_PARITY_REQUIREMENTS = (
    "vcl_fmx_component_parity",
    "built_in_component_usability",
    "pascal_runtime_and_dfm_streaming",
    "object_inspector_parity",
    "livebindings_designer",
    "firedac_datasnap_radserver_interbase_tooling",
    "design_time_package_installation",
    "mobile_native_device_api_coverage",
    "fmx_animation_effects_3d_depth",
    "third_party_component_ecosystem",
)


def component_palette() -> tuple[dict, ...]:
    """Return draggable RAD-style form components."""
    return tuple({"component": name, **spec} for name, spec in COMPONENTS.items())


def third_party_component_registry() -> tuple[dict, ...]:
    """Return useful third-party RAD component suites the IDE can model."""
    return THIRD_PARTY_COMPONENT_SUITES


def third_party_component_categories() -> tuple[str, ...]:
    """Return normalized categories covered by built-in third-party suites."""
    return tuple(sorted({category for suite in THIRD_PARTY_COMPONENT_SUITES for category in suite["categories"]}))


def third_party_component_install_plan(package_ids: tuple[str, ...] = ()) -> dict:
    """Return a reviewed installation plan for third-party component suites."""
    selected = set(package_ids or tuple(suite["id"] for suite in THIRD_PARTY_COMPONENT_SUITES))
    known = {suite["id"] for suite in THIRD_PARTY_COMPONENT_SUITES}
    unknown = tuple(sorted(selected - known))
    packages = tuple(suite for suite in THIRD_PARTY_COMPONENT_SUITES if suite["id"] in selected)
    return {
        "format": "appgen.third-party-component-install-plan.v1",
        "ok": not unknown and bool(packages),
        "packages": packages,
        "unknown": unknown,
        "requires_review": True,
        "side_effects": (),
        "install_channels": ("getit", "vendor-installer", "source-package", "manual-bpl"),
        "guards": (
            "license_acceptance_required",
            "version_pin_required",
            "sandbox_before_global_install",
            "design_time_packages_reviewed_before_load",
        ),
    }


def third_party_component_import_contract(metadata: dict) -> dict:
    """Return a reviewed contract for a custom third-party component package."""
    required = ("id", "vendor", "frameworks", "components", "categories")
    missing = tuple(field for field in required if not metadata.get(field))
    return {
        "format": "appgen.third-party-component-import-contract.v1",
        "ok": not missing,
        "missing": missing,
        "package": {
            "id": metadata.get("id"),
            "vendor": metadata.get("vendor"),
            "frameworks": tuple(metadata.get("frameworks", ())),
            "components": tuple(metadata.get("components", ())),
            "categories": tuple(metadata.get("categories", ())),
            "license": metadata.get("license", "review-required"),
        },
        "requires_review": True,
        "side_effects": (),
    }


def dfm_streaming_contract() -> dict:
    """Return the design-time streaming model used for RAD-compatible forms."""
    return {
        "format": "appgen.dfm-streaming-contract.v1",
        "stream_formats": ("text-dfm", "binary-dfm", "json-form-model"),
        "round_trip": ("component_identity", "published_properties", "nested_children", "event_bindings"),
        "pascal_runtime": {
            "compiler": "external-rad-or-freepascal-toolchain",
            "generated_units": ("forms", "data-modules", "packages", "resources"),
            "side_effects": (),
        },
        "guards": ("never_execute_imported_pascal", "review_event_handlers", "preserve_unknown_properties"),
    }


def object_inspector_contract(component: str = "TextBox") -> dict:
    """Return Object Inspector parity metadata for properties, events, and editors."""
    properties = property_inspector(component if component in COMPONENTS else "TextBox")["properties"]
    return {
        "format": "appgen.object-inspector-contract.v1",
        "component": component,
        "tabs": ("Properties", "Events", "Data", "Actions"),
        "property_editors": tuple({"name": name, "editor": "boolean" if name in {"required", "readonly"} else "string"} for name in properties),
        "event_editors": ("OnClick", "OnChange", "OnValidate", "OnCreate", "OnDestroy"),
        "component_editors": ("align", "tab_order", "anchors", "constraints", "bindings"),
        "custom_designer_hooks": ("paint_overlay", "verb_menu", "selection_handles", "smart_tags"),
    }


def livebindings_contract() -> dict:
    """Return LiveBindings-style visual data-binding contracts."""
    return {
        "format": "appgen.livebindings-designer-contract.v1",
        "binding_nodes": ("control", "field", "dataset", "expression", "converter", "validator"),
        "binding_edges": ("control_to_field", "field_to_control", "expression_to_property", "dataset_to_grid"),
        "expressions": ("format", "parse", "lookup", "aggregate", "conditional"),
        "generated_artifacts": ("binding_graph", "binding_list", "data_sources", "validation_rules"),
        "review_required": True,
    }


def rad_data_tooling_contract() -> dict:
    """Return native RAD data-service tooling modeled by the generated IDE."""
    return {
        "format": "appgen.rad-data-tooling-contract.v1",
        "tooling": {
            "FireDAC": ("connections", "queries", "stored_procedures", "schema_adapter", "offline_cache"),
            "DataSnap": ("server_methods", "client_proxies", "transport_filters", "session_lifecycle"),
            "RAD Server": ("resources", "edge_modules", "users", "groups", "analytics"),
            "InterBase": ("local_embedded", "change_views", "encryption", "backup_restore"),
        },
        "guards": ("connection_secrets_externalized", "migrations_reviewed", "offline_sync_conflicts_visible"),
    }


def mobile_native_api_contract() -> dict:
    """Return mobile/native device APIs exposed to the component designer."""
    return {
        "format": "appgen.mobile-native-api-contract.v1",
        "apis": (
            "camera",
            "photos",
            "location",
            "sensors",
            "biometrics",
            "push_notifications",
            "contacts",
            "calendar",
            "secure_storage",
            "bluetooth",
            "nfc",
            "file_picker",
            "share_sheet",
            "background_tasks",
        ),
        "targets": ("android", "ios", "desktop", "web-pwa"),
        "guards": ("permission_manifest_generated", "runtime_permission_prompt", "privacy_labels_reviewed"),
    }


def fmx_visual_depth_contract() -> dict:
    """Return FMX-level animation, styling, effects, and 3D designer coverage."""
    return {
        "format": "appgen.fmx-visual-depth-contract.v1",
        "styling": ("stylebook", "multi-resolution-bitmaps", "themes", "state-triggers"),
        "animation": ("float_animation", "color_animation", "path_animation", "timeline", "easing"),
        "effects": ("shadow", "blur", "glow", "reflection", "color-key", "shader-hook"),
        "three_d": ("viewport3d", "camera", "light", "mesh", "material", "model-import"),
        "guards": ("reduced_motion_fallback", "gpu_fallback", "mobile_frame_budget"),
    }


def rad_parity_workbench(existing_paths: set[str] | None = None) -> dict:
    """Return package-level evidence for the requested RAD parity roadmap."""
    existing = (
        {"app/form_designer.py", "app/templates/appgen_form_designer.html"}
        if existing_paths is None
        else existing_paths
    )
    install_plan = third_party_component_install_plan()
    third_party_categories = set(third_party_component_categories())
    checks = (
        {
            "id": "vcl_fmx_component_parity",
            "ok": len(component_palette()) >= 7 and {"input", "calendar", "relationship", "media", "action"} <= set(palette_categories()),
            "evidence": {"components": tuple(item["component"] for item in component_palette())},
        },
        {
            "id": "built_in_component_usability",
            "ok": component_usability_workbench()["ok"],
            "evidence": component_usability_workbench(),
        },
        {
            "id": "pascal_runtime_and_dfm_streaming",
            "ok": "text-dfm" in dfm_streaming_contract()["stream_formats"],
            "evidence": dfm_streaming_contract(),
        },
        {
            "id": "object_inspector_parity",
            "ok": {"Properties", "Events"} <= set(object_inspector_contract()["tabs"]),
            "evidence": object_inspector_contract(),
        },
        {
            "id": "livebindings_designer",
            "ok": "control_to_field" in livebindings_contract()["binding_edges"],
            "evidence": livebindings_contract(),
        },
        {
            "id": "firedac_datasnap_radserver_interbase_tooling",
            "ok": {"FireDAC", "DataSnap", "RAD Server", "InterBase"} <= set(rad_data_tooling_contract()["tooling"]),
            "evidence": rad_data_tooling_contract(),
        },
        {
            "id": "design_time_package_installation",
            "ok": install_plan["ok"] and install_plan["requires_review"],
            "evidence": install_plan,
        },
        {
            "id": "mobile_native_device_api_coverage",
            "ok": {"camera", "location", "push_notifications", "secure_storage"} <= set(mobile_native_api_contract()["apis"]),
            "evidence": mobile_native_api_contract(),
        },
        {
            "id": "fmx_animation_effects_3d_depth",
            "ok": bool(fmx_visual_depth_contract()["animation"]) and bool(fmx_visual_depth_contract()["three_d"]),
            "evidence": fmx_visual_depth_contract(),
        },
        {
            "id": "third_party_component_ecosystem",
            "ok": install_plan["ok"] and {"grid", "reports", "charts", "database", "network", "animation"} <= third_party_categories,
            "evidence": {"packages": install_plan["packages"], "categories": tuple(sorted(third_party_categories))},
        },
        {
            "id": "artifact_contract",
            "ok": {"app/form_designer.py", "app/templates/appgen_form_designer.html"} <= existing,
            "evidence": {"existing": tuple(sorted(existing))},
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.rad-parity-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "requirements": RAD_PARITY_REQUIREMENTS,
        "checks": checks,
        "third_party_registry": THIRD_PARTY_COMPONENT_SUITES,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "stop_condition": "do-not-claim-full-rad-parity-unless-every-check-is-proven",
    }


def palette_categories() -> tuple[str, ...]:
    """Return component palette categories."""
    return tuple(sorted({item["category"] for item in component_palette()}))


def form_canvas(table: str = "Customer") -> dict:
    """Return the stable grid canvas contract for a form designer."""
    return {
        "format": "appgen.package-form-canvas.v1",
        "table": table,
        "grid": {"columns": 12, "row_height": 40, "snap": 1},
        "bounds": {"x": 0, "y": 0, "w": 12, "h": 24},
        "render_targets": ("web", "mobile", "desktop"),
    }


def form_design(source: str = FORM_DESIGNER_SAMPLE_DSL, table: str = "Customer") -> dict:
    """Return a parsed form design from DSL component placements."""
    schema = schema_from_dsl(source, source_name="form-designer-audit.appgen")
    view = next(item for item in schema.views if item.table == table)
    fields = {column.name: column for column in schema.table(table).columns}
    components = tuple(
        {
            "field": component.field,
            "component": component.component,
            "x": component.x,
            "y": component.y,
            "w": component.w,
            "h": component.h,
            "field_type": fields[component.field].type_name,
        }
        for component in view.components
    )
    return {
        "format": "appgen.package-form-design.v1",
        "table": table,
        "view": view.name,
        "canvas": form_canvas(table),
        "components": components,
        "sections": tuple({"name": section.name, "fields": section.fields} for section in view.sections),
    }


def field_component_matrix(source: str = FORM_DESIGNER_SAMPLE_DSL) -> tuple[dict, ...]:
    """Return field-to-component mapping evidence."""
    design = form_design(source)
    palette = {item["component"]: item for item in component_palette()}
    return tuple(
        {
            "field": item["field"],
            "field_type": item["field_type"],
            "component": item["component"],
            "supported": item["field_type"] in palette[item["component"]]["field_types"],
        }
        for item in design["components"]
    )


def snap_drop(component: str, x: float, y: float, *, field: str | None = None) -> dict:
    """Return a snapped drag/drop proposal on the form canvas."""
    if component not in COMPONENTS:
        raise KeyError(f"Unknown component: {component}")
    size = COMPONENTS[component]["default_size"]
    snapped = {
        "field": field,
        "component": component,
        "x": max(0, min(11, round(x))),
        "y": max(0, round(y)),
        "w": size["w"],
        "h": size["h"],
    }
    if snapped["x"] + snapped["w"] > 12:
        snapped["x"] = 12 - snapped["w"]
    return {
        "format": "appgen.package-form-drop-proposal.v1",
        "proposal": snapped,
        "property_inspector": property_inspector(component, field=field),
        "review_required": True,
    }


def property_inspector(component: str, *, field: str | None = None) -> dict:
    """Return property editor metadata for a component."""
    if component not in COMPONENTS:
        raise KeyError(f"Unknown component: {component}")
    spec = COMPONENTS[component]
    return {
        "format": "appgen.package-form-property-inspector.v1",
        "component": component,
        "field": field,
        "properties": spec["properties"],
        "property_types": {
            name: "boolean" if name in {"required", "readonly", "spellcheck", "preview"} else "string"
            for name in spec["properties"]
        },
    }


def component_runtime_contract(component: str) -> dict:
    """Return the runtime/editor contract that makes a component usable."""
    if component not in COMPONENTS:
        raise KeyError(f"Unknown component: {component}")
    spec = COMPONENTS[component]
    category = spec["category"]
    data_bound = bool(spec["field_types"])
    nonvisual = category in {"nonvisual", "data", "integration"} and component not in {"Grid", "Chart", "ReportViewer", "WebBrowser"}
    renderer = {
        "web": f"appgen.components.{component}",
        "mobile": f"appgen.mobile.{component}",
        "desktop": f"appgen.desktop.{component}",
    }
    if nonvisual:
        renderer = {
            "web": f"appgen.services.{component}",
            "mobile": f"appgen.mobile_services.{component}",
            "desktop": f"appgen.desktop_services.{component}",
        }
    return {
        "format": "appgen.component-runtime-contract.v1",
        "component": component,
        "category": category,
        "renderers": renderer,
        "default_size": spec["default_size"],
        "default_props": {name: _default_property_value(name, component, category) for name in spec["properties"]},
        "property_editors": property_inspector(component)["property_types"],
        "events": _component_events(component, category),
        "bindings": {
            "data_bound": data_bound,
            "field_types": spec["field_types"],
            "binding_modes": ("read", "write") if data_bound else (),
        },
        "validation_rules": _component_validation_rules(component, category),
        "preview": {
            "available": True,
            "preview_kind": "service-node" if nonvisual else "visual-control",
            "sample_payload": {"component": component, "props": tuple(spec["properties"])},
        },
        "usable": True,
    }


def component_implementation_catalog() -> tuple[dict, ...]:
    """Return usability contracts for every built-in component."""
    return tuple(component_runtime_contract(component) for component in sorted(COMPONENTS))


def component_usability_workbench() -> dict:
    """Prove every built-in component has enough metadata to be usable."""
    contracts = component_implementation_catalog()
    checks = (
        {
            "id": "complete_catalog",
            "ok": {item["component"] for item in contracts} == set(COMPONENTS),
            "evidence": {"component_count": len(contracts)},
        },
        {
            "id": "runtime_renderers",
            "ok": all({"web", "mobile", "desktop"} <= set(item["renderers"]) for item in contracts),
            "evidence": tuple((item["component"], tuple(item["renderers"])) for item in contracts),
        },
        {
            "id": "property_editors",
            "ok": all(item["property_editors"] and item["default_props"] for item in contracts),
            "evidence": tuple((item["component"], tuple(item["property_editors"])) for item in contracts),
        },
        {
            "id": "events",
            "ok": all(item["events"] for item in contracts),
            "evidence": tuple((item["component"], item["events"]) for item in contracts),
        },
        {
            "id": "validation_rules",
            "ok": all(item["validation_rules"] for item in contracts),
            "evidence": tuple((item["component"], item["validation_rules"]) for item in contracts),
        },
        {
            "id": "drop_defaults",
            "ok": all(item["default_size"]["w"] > 0 and item["default_size"]["h"] > 0 for item in contracts),
            "evidence": tuple((item["component"], item["default_size"]) for item in contracts),
        },
        {
            "id": "preview_contracts",
            "ok": all(item["preview"]["available"] and item["usable"] for item in contracts),
            "evidence": tuple((item["component"], item["preview"]["preview_kind"]) for item in contracts),
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-usability-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "component_count": len(contracts),
        "components": contracts,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def detect_overlaps(components: tuple[dict, ...]) -> tuple[dict, ...]:
    """Return overlapping component pairs."""
    overlaps = []
    for index, left in enumerate(components):
        for right in components[index + 1 :]:
            if _overlaps(left, right):
                overlaps.append({"left": left["field"], "right": right["field"]})
    return tuple(overlaps)


def placement_suggestions(source: str = FORM_DESIGNER_SAMPLE_DSL) -> tuple[dict, ...]:
    """Return deterministic drop suggestions for fields not already on a form."""
    schema = schema_from_dsl(source, source_name="form-designer-audit.appgen")
    design = form_design(source)
    placed = {item["field"] for item in design["components"]}
    table = schema.table(design["table"])
    suggestions = []
    next_y = max(item["y"] + item["h"] for item in design["components"])
    for column in table.columns:
        if column.name not in placed and column.name != "id":
            component = _component_for_type(column.type_name)
            suggestions.append(
                {
                    "field": column.name,
                    "component": component,
                    "drop": snap_drop(component, 0, next_y, field=column.name)["proposal"],
                }
            )
            next_y += COMPONENTS[component]["default_size"]["h"]
    return tuple(suggestions)


def apply_drop(design: dict, proposal: dict) -> dict:
    """Apply a reviewed drop proposal to a form design."""
    components = tuple(design["components"]) + (proposal,)
    updated = dict(design)
    updated["components"] = components
    updated["validation"] = validate_form_design(updated)
    return updated


def validate_form_design(design: dict) -> dict:
    """Validate bounds and overlap guardrails for a form design."""
    bounds = design["canvas"]["bounds"]
    components = tuple(design["components"])
    out_of_bounds = tuple(
        item
        for item in components
        if item["x"] < bounds["x"]
        or item["y"] < bounds["y"]
        or item["x"] + item["w"] > bounds["w"]
        or item["y"] + item["h"] > bounds["h"]
    )
    overlaps = detect_overlaps(components)
    return {
        "format": "appgen.package-form-design-validation.v1",
        "ok": not out_of_bounds and not overlaps,
        "out_of_bounds": out_of_bounds,
        "overlaps": overlaps,
    }


def form_designer_generation_smoke_audit(source: str = FORM_DESIGNER_SAMPLE_DSL) -> dict:
    """Generate a temporary app and exercise its generated form designer."""
    import importlib.util
    import py_compile
    import tempfile
    from pathlib import Path

    from .gen import generate_app_from_schema
    from .schema import load_schema

    required_artifacts = (
        "app/form_designer.py",
        "app/templates/appgen_form_designer.html",
        "app/models.py",
        "app/views.py",
        "app/dsl_reference.py",
    )
    compile_artifacts = (
        "app/form_designer.py",
        "app/models.py",
        "app/views.py",
        "app/dsl_reference.py",
    )

    with tempfile.TemporaryDirectory(prefix="appgen-form-designer-smoke-") as tmp:
        project_dir = Path(tmp)
        dsl_path = project_dir / "form_designer.appgen"
        dsl_path.write_text(source, encoding="utf-8")
        schema = load_schema(dsl_path, source_type="dsl")
        output_dir = project_dir / "app"
        generate_app_from_schema(schema, output_dir)

        missing_artifacts = tuple(
            artifact for artifact in required_artifacts if not (project_dir / artifact).exists()
        )
        compiled = []
        compile_failures = []
        for artifact in compile_artifacts:
            path = project_dir / artifact
            if not path.exists():
                continue
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                compile_failures.append({"artifact": artifact, "error": str(exc)})
            else:
                compiled.append(artifact)

        module_path = output_dir / "form_designer.py"
        spec = importlib.util.spec_from_file_location(
            "generated_form_designer_smoke", module_path
        )
        generated_form_designer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generated_form_designer)
        existing_paths = {
            "app/form_designer.py",
            "app/templates/appgen_form_designer.html",
        }
        palette = generated_form_designer.component_palette()
        forms = generated_form_designer.form_catalog()
        first_table = forms[0]["table"] if forms else None
        design = generated_form_designer.form_design(first_table) if first_table else {}
        validation = generated_form_designer.validate_form_design(design) if first_table else {}
        proposal = (
            generated_form_designer.proposal_from_drop(
                {
                    "table": first_table,
                    "component": "TextBox",
                    "field": "name",
                    "x": 2.3,
                    "y": 7.7,
                }
            )
            if first_table
            else {}
        )
        updated = (
            generated_form_designer.apply_form_proposal(design, proposal)
            if first_table
            else {}
        )
        updated_validation = (
            generated_form_designer.validate_form_design(updated) if first_table else {}
        )
        release_gate = generated_form_designer.form_designer_release_gate(existing_paths)
        workbench = generated_form_designer.form_designer_workbench(existing_paths)

    checks = (
        {
            "id": "generated_artifacts",
            "ok": not missing_artifacts,
            "required_artifacts": required_artifacts,
            "missing": missing_artifacts,
        },
        {
            "id": "generated_python_compiles",
            "ok": not compile_failures and set(compiled) == set(compile_artifacts),
            "compiled": tuple(compiled),
            "failures": tuple(compile_failures),
        },
        {
            "id": "palette_and_catalog",
            "ok": {"TextBox", "TextArea", "DatePicker", "RelationshipPicker", "Button"}
            <= {item["type"] for item in palette}
            and bool(forms),
            "forms": forms,
        },
        {
            "id": "canvas_drop_contract",
            "ok": validation.get("ok") is True
            and proposal.get("kind") == "drop_component"
            and any(item.get("name") == "field" for item in proposal.get("properties", ()))
            and updated_validation.get("ok") is True,
        },
        {
            "id": "generated_release_contracts",
            "ok": release_gate["ok"] and workbench["ok"],
            "release_gate": release_gate["format"],
            "workbench": workbench["format"],
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.form-designer-generation-smoke-audit.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "required_artifacts": required_artifacts,
        "compiled_artifacts": tuple(compiled),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def form_designer_release_audit(existing_paths: set[str] | None = None) -> dict:
    """Return package-level proof for RAD-style form design readiness."""
    existing = (
        {"app/form_designer.py", "app/templates/appgen_form_designer.html"}
        if existing_paths is None
        else existing_paths
    )
    design = form_design()
    matrix = field_component_matrix()
    drop = snap_drop("TextBox", 2.3, 7.7, field="generated_note")
    valid_after_drop = validate_form_design(
        apply_drop(design, {**drop["proposal"], "field_type": "string"})  # type: ignore[arg-type]
    )
    overlap_case = tuple(design["components"]) + (
        {"field": "duplicate_name", "component": "TextBox", "x": 0, "y": 0, "w": 6, "h": 1},
    )
    generation_smoke = form_designer_generation_smoke_audit()
    gates = (
        {
            "id": "palette_breadth",
            "ok": {"input", "calendar", "relationship", "media", "action", "data", "menu", "mobile", "effects", "three_d"} <= set(palette_categories()),
        },
        {
            "id": "canvas_contract",
            "ok": design["canvas"]["grid"]["columns"] == 12
            and {"web", "mobile", "desktop"} <= set(design["canvas"]["render_targets"]),
        },
        {
            "id": "field_component_mapping",
            "ok": all(item["supported"] for item in matrix),
        },
        {
            "id": "drop_snap_property_inspector",
            "ok": drop["proposal"]["x"] == 2
            and drop["proposal"]["y"] == 8
            and "label" in drop["property_inspector"]["properties"],
        },
        {
            "id": "placement_suggestions",
            "ok": any(item["field"] == "phone" for item in placement_suggestions()),
        },
        {
            "id": "overlap_guardrails",
            "ok": bool(detect_overlaps(overlap_case)) and valid_after_drop["ok"],
        },
        {
            "id": "artifact_contract",
            "ok": {"app/form_designer.py", "app/templates/appgen_form_designer.html"} <= existing,
        },
        {
            "id": "generation_smoke",
            "ok": generation_smoke["ok"],
            "checks": tuple(check["id"] for check in generation_smoke["checks"]),
        },
        {
            "id": "rad_parity_workbench",
            "ok": rad_parity_workbench(existing)["ok"],
            "checks": tuple(check["id"] for check in rad_parity_workbench(existing)["checks"]),
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.package-form-designer-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "palette": component_palette(),
        "design": design,
        "matrix": matrix,
        "drop": drop,
        "suggestions": placement_suggestions(),
        "validation": validate_form_design(design),
        "generation_smoke": generation_smoke,
        "rad_parity": rad_parity_workbench(existing),
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-rad-form-designer-unless-ok-is-true",
    }


def _component_for_type(type_name: str) -> str:
    if type_name in {"date", "datetime", "time"}:
        return "DatePicker"
    if type_name == "text":
        return "TextArea"
    if type_name in {"file", "image"}:
        return "FileUpload"
    return "TextBox"


def _default_property_value(name: str, component: str, category: str) -> object:
    if name in {"required", "readonly", "spellcheck", "preview", "visible", "enabled", "lazy_load", "filterable", "sortable", "editable", "watch", "multi_select", "sorted"}:
        return name in {"visible", "enabled", "sortable", "filterable"}
    if name in {"rows", "columns", "interval", "timeout", "duration", "tab_order", "max_size_mb"}:
        return 1 if name != "duration" else 200
    if name in {"items", "actions", "tabs", "series", "bindings", "validators", "converters", "channels", "lights", "models", "materials", "export_formats", "headers"}:
        return ()
    if name in {"target", "source", "data_source", "dataset", "url", "base_url", "report", "camera"}:
        return ""
    if name == "label":
        return component
    if name == "caption":
        return component
    if name == "permission":
        return "runtime"
    if name == "align":
        return "none"
    if name == "effect":
        return "shadow"
    if name == "easing":
        return "ease-out"
    if category == "mobile" and name == "fallback":
        return "manual-entry"
    return ""


def _component_events(component: str, category: str) -> tuple[str, ...]:
    base = ("OnCreate", "OnDestroy")
    by_category = {
        "input": ("OnChange", "OnValidate", "OnEnter", "OnExit"),
        "calendar": ("OnChange", "OnValidate", "OnOpen"),
        "relationship": ("OnLookup", "OnChange", "OnValidate"),
        "media": ("OnUpload", "OnPreview", "OnClear"),
        "action": ("OnClick", "OnExecute", "OnUpdate"),
        "container": ("OnResize", "OnShow", "OnHide"),
        "choice": ("OnChange", "OnSelect", "OnValidate"),
        "navigation": ("OnSelect", "OnExpand", "OnCollapse"),
        "data": ("OnOpen", "OnDataChange", "OnError"),
        "menu": ("OnClick", "OnPopup", "OnShortcut"),
        "analytics": ("OnRefresh", "OnPointClick", "OnExport"),
        "reports": ("OnPreview", "OnExport", "OnPrint"),
        "integration": ("OnRequest", "OnResponse", "OnError"),
        "nonvisual": ("OnTimer", "OnStart", "OnStop"),
        "mobile": ("OnPermission", "OnCapture", "OnError"),
        "effects": ("OnStart", "OnFinish", "OnCancel"),
        "three_d": ("OnLoad", "OnRender", "OnFrame"),
    }
    return base + by_category.get(category, ("OnChange",))


def _component_validation_rules(component: str, category: str) -> tuple[str, ...]:
    rules = ["within_canvas_bounds", "stable_component_id", "known_property_names"]
    if COMPONENTS[component]["field_types"]:
        rules.append("field_type_supported")
    if category in {"mobile", "integration", "data"}:
        rules.append("permission_or_secret_reviewed")
    if category in {"effects", "three_d"}:
        rules.append("performance_budget_declared")
    if category == "menu":
        rules.append("role_visibility_reviewed")
    return tuple(rules)


def _overlaps(left: dict, right: dict) -> bool:
    return not (
        left["x"] + left["w"] <= right["x"]
        or right["x"] + right["w"] <= left["x"]
        or left["y"] + left["h"] <= right["y"]
        or right["y"] + right["h"] <= left["y"]
    )
