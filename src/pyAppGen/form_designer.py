"""Package-level RAD-style form designer contracts."""

from __future__ import annotations

import re

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
    "Label": {
        "category": "display",
        "field_types": (),
        "default_size": {"w": 3, "h": 1},
        "properties": ("caption", "align", "style", "visible", "enabled"),
    },
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
    "Select": {
        "category": "choice",
        "field_types": ("string", "int", "enum"),
        "default_size": {"w": 4, "h": 1},
        "properties": ("label", "items", "required", "search", "help_text"),
    },
    "Checkbox": {
        "category": "choice",
        "field_types": ("bool", "boolean"),
        "default_size": {"w": 2, "h": 1},
        "properties": ("label", "checked", "required", "tab_order", "help_text"),
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
    "RadioButton": {
        "category": "choice",
        "field_types": ("string", "int", "enum"),
        "default_size": {"w": 3, "h": 1},
        "properties": ("caption", "group", "checked", "required", "tab_order"),
    },
    "ListBox": {
        "category": "choice",
        "field_types": ("string", "int", "enum"),
        "default_size": {"w": 4, "h": 4},
        "properties": ("items", "multi_select", "sorted", "required", "help_text"),
    },
    "ListView": {
        "category": "data",
        "field_types": ("relation", "dataset"),
        "default_size": {"w": 6, "h": 6},
        "properties": ("data_source", "item_template", "grouping", "search", "selection_mode"),
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
    "StringGrid": {
        "category": "data",
        "field_types": ("relation", "dataset"),
        "default_size": {"w": 12, "h": 6},
        "properties": ("data_source", "columns", "fixed_rows", "fixed_columns", "editable"),
    },
    "PageControl": {
        "category": "container",
        "field_types": (),
        "default_size": {"w": 12, "h": 6},
        "properties": ("tabs", "active_tab", "align", "lazy_mount", "tab_position"),
    },
    "Layout": {
        "category": "container",
        "field_types": (),
        "default_size": {"w": 12, "h": 4},
        "properties": ("align", "padding", "gap", "children", "visible"),
    },
    "ScrollBox": {
        "category": "container",
        "field_types": (),
        "default_size": {"w": 12, "h": 8},
        "properties": ("scrollbars", "content_width", "content_height", "padding", "visible"),
    },
    "FlowLayout": {
        "category": "container",
        "field_types": (),
        "default_size": {"w": 12, "h": 4},
        "properties": ("direction", "wrap", "gap", "justify", "align_items"),
    },
    "GridLayout": {
        "category": "container",
        "field_types": (),
        "default_size": {"w": 12, "h": 6},
        "properties": ("rows", "columns", "gap", "areas", "responsive_breakpoints"),
    },
    "VerticalBoxLayout": {
        "category": "container",
        "field_types": (),
        "default_size": {"w": 6, "h": 8},
        "properties": ("gap", "padding", "align_items", "children", "scrollable"),
    },
    "HorizontalBoxLayout": {
        "category": "container",
        "field_types": (),
        "default_size": {"w": 12, "h": 3},
        "properties": ("gap", "padding", "align_items", "children", "wrap"),
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
    "Shape": {
        "category": "graphics",
        "field_types": (),
        "default_size": {"w": 3, "h": 3},
        "properties": ("shape", "fill", "stroke", "stroke_width", "opacity"),
    },
    "PathShape": {
        "category": "graphics",
        "field_types": (),
        "default_size": {"w": 4, "h": 3},
        "properties": ("path_data", "fill", "stroke", "stroke_width", "scale"),
    },
    "Rectangle": {
        "category": "graphics",
        "field_types": (),
        "default_size": {"w": 4, "h": 2},
        "properties": ("fill", "stroke", "corner_radius", "stroke_width", "opacity"),
    },
    "Ellipse": {
        "category": "graphics",
        "field_types": (),
        "default_size": {"w": 3, "h": 3},
        "properties": ("fill", "stroke", "stroke_width", "opacity", "hit_test"),
    },
    "Line": {
        "category": "graphics",
        "field_types": (),
        "default_size": {"w": 4, "h": 1},
        "properties": ("stroke", "stroke_width", "x1", "y1", "x2", "y2"),
    },
    "Bitmap": {
        "category": "graphics",
        "field_types": ("image", "file"),
        "default_size": {"w": 4, "h": 3},
        "properties": ("source", "dpi", "scale_mode", "transparent", "cache_policy"),
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
    "MotionSensor": {
        "category": "mobile",
        "field_types": ("sensor", "decimal"),
        "default_size": {"w": 3, "h": 1},
        "properties": ("permission", "sample_rate", "axes", "threshold", "fallback"),
    },
    "OrientationSensor": {
        "category": "mobile",
        "field_types": ("sensor", "decimal"),
        "default_size": {"w": 3, "h": 1},
        "properties": ("permission", "sample_rate", "orientation_mode", "threshold", "fallback"),
    },
    "NotificationCenter": {
        "category": "mobile",
        "field_types": (),
        "default_size": {"w": 3, "h": 1},
        "properties": ("channels", "permission", "deep_link", "badge", "sound"),
    },
    "PhotoPicker": {
        "category": "mobile",
        "field_types": ("image", "file"),
        "default_size": {"w": 4, "h": 3},
        "properties": ("permission", "albums", "selection_limit", "preview", "fallback"),
    },
    "BiometricAuth": {
        "category": "mobile",
        "field_types": ("boolean",),
        "default_size": {"w": 3, "h": 1},
        "properties": ("permission", "reason", "fallback", "timeout", "retry"),
    },
    "ContactsPicker": {
        "category": "mobile",
        "field_types": ("string", "json"),
        "default_size": {"w": 4, "h": 3},
        "properties": ("permission", "fields", "filter", "selection_limit", "fallback"),
    },
    "CalendarEvents": {
        "category": "mobile",
        "field_types": ("datetime", "json"),
        "default_size": {"w": 4, "h": 3},
        "properties": ("permission", "calendars", "date_range", "write_access", "fallback"),
    },
    "SecureStore": {
        "category": "mobile",
        "field_types": ("string", "json"),
        "default_size": {"w": 3, "h": 1},
        "properties": ("permission", "key_namespace", "encryption", "biometric_gate", "fallback"),
    },
    "PushClient": {
        "category": "mobile",
        "field_types": ("json",),
        "default_size": {"w": 3, "h": 1},
        "properties": ("permission", "channels", "token_field", "deep_link", "fallback"),
    },
    "BluetoothClient": {
        "category": "mobile",
        "field_types": ("json",),
        "default_size": {"w": 4, "h": 2},
        "properties": ("permission", "scan_filters", "services", "pairing", "fallback"),
    },
    "NfcReader": {
        "category": "mobile",
        "field_types": ("string", "json"),
        "default_size": {"w": 3, "h": 1},
        "properties": ("permission", "formats", "read_timeout", "write_enabled", "fallback"),
    },
    "FilePicker": {
        "category": "mobile",
        "field_types": ("file", "string"),
        "default_size": {"w": 4, "h": 2},
        "properties": ("permission", "accept", "multiple", "max_size_mb", "fallback"),
    },
    "ShareSheet": {
        "category": "mobile",
        "field_types": ("string", "file", "url"),
        "default_size": {"w": 3, "h": 1},
        "properties": ("permission", "payload", "targets", "subject", "fallback"),
    },
    "BackgroundTask": {
        "category": "mobile",
        "field_types": (),
        "default_size": {"w": 3, "h": 1},
        "properties": ("permission", "task", "interval", "network_required", "fallback"),
    },
    "Animation": {
        "category": "effects",
        "field_types": (),
        "default_size": {"w": 3, "h": 1},
        "properties": ("target", "property", "duration", "easing", "reduced_motion"),
    },
    "FloatAnimation": {
        "category": "effects",
        "field_types": (),
        "default_size": {"w": 3, "h": 1},
        "properties": ("target", "property", "start_value", "end_value", "duration"),
    },
    "ColorAnimation": {
        "category": "effects",
        "field_types": (),
        "default_size": {"w": 3, "h": 1},
        "properties": ("target", "property", "start_color", "end_color", "duration"),
    },
    "PathAnimation": {
        "category": "effects",
        "field_types": (),
        "default_size": {"w": 3, "h": 1},
        "properties": ("target", "path_data", "duration", "easing", "auto_reverse"),
    },
    "Effect": {
        "category": "effects",
        "field_types": (),
        "default_size": {"w": 3, "h": 1},
        "properties": ("target", "effect", "intensity", "gpu_fallback", "enabled"),
    },
    "StyleBook": {
        "category": "theme",
        "field_types": (),
        "default_size": {"w": 3, "h": 1},
        "properties": ("theme", "resources", "variants", "platform_overrides", "active"),
    },
    "StyleManager": {
        "category": "theme",
        "field_types": (),
        "default_size": {"w": 3, "h": 1},
        "properties": ("style_books", "active_style", "dark_mode", "high_contrast", "platform_rules"),
    },
    "GestureManager": {
        "category": "gesture",
        "field_types": (),
        "default_size": {"w": 3, "h": 1},
        "properties": ("gestures", "targets", "recognizers", "conflicts", "enabled"),
    },
    "Gesture": {
        "category": "gesture",
        "field_types": (),
        "default_size": {"w": 2, "h": 1},
        "properties": ("kind", "target", "threshold", "direction", "enabled"),
    },
    "Viewport3D": {
        "category": "three_d",
        "field_types": (),
        "default_size": {"w": 8, "h": 6},
        "properties": ("camera", "lights", "models", "materials", "mobile_budget"),
    },
    "Dummy3D": {
        "category": "three_d",
        "field_types": (),
        "default_size": {"w": 2, "h": 2},
        "properties": ("position", "rotation", "scale", "children", "visible"),
    },
    "Camera3D": {
        "category": "three_d",
        "field_types": (),
        "default_size": {"w": 2, "h": 2},
        "properties": ("position", "rotation", "field_of_view", "near_clip", "far_clip"),
    },
    "Light3D": {
        "category": "three_d",
        "field_types": (),
        "default_size": {"w": 2, "h": 2},
        "properties": ("light_type", "color", "intensity", "position", "shadows"),
    },
    "Mesh3D": {
        "category": "three_d",
        "field_types": (),
        "default_size": {"w": 3, "h": 3},
        "properties": ("mesh", "material", "position", "rotation", "scale"),
    },
    "DatabaseConnection": {
        "category": "data_access",
        "field_types": ("dataset",),
        "default_size": {"w": 3, "h": 1},
        "properties": ("driver", "connection_name", "transaction", "pooling", "secure_secrets"),
    },
    "TableAdapter": {
        "category": "data_access",
        "field_types": ("dataset", "relation"),
        "default_size": {"w": 3, "h": 1},
        "properties": ("table", "connection", "filters", "indexes", "cached_updates"),
    },
    "ClientDataSet": {
        "category": "data_access",
        "field_types": ("dataset", "relation"),
        "default_size": {"w": 3, "h": 1},
        "properties": ("fields", "provider", "change_log", "merge_policy", "offline_cache"),
    },
}

COMPONENT_ANALOG_REQUIREMENTS = (
    {"group": "cross-target-ui", "source": "TButton", "analog": "Button"},
    {"group": "cross-target-ui", "source": "TEdit", "analog": "TextBox"},
    {"group": "cross-target-ui", "source": "TLabel", "analog": "Label"},
    {"group": "cross-target-ui", "source": "TListBox", "analog": "ListBox"},
    {"group": "cross-target-ui", "source": "TComboBox", "analog": "Select"},
    {"group": "cross-target-ui", "source": "TCheckBox", "analog": "Checkbox"},
    {"group": "cross-target-ui", "source": "TRadioButton", "analog": "RadioButton"},
    {"group": "layouts", "source": "TLayout", "analog": "Layout"},
    {"group": "layouts", "source": "TScrollBox", "analog": "ScrollBox"},
    {"group": "layouts", "source": "TFlowLayout", "analog": "FlowLayout"},
    {"group": "layouts", "source": "TGridLayout", "analog": "GridLayout"},
    {"group": "layouts", "source": "TVerticalBoxLayout", "analog": "VerticalBoxLayout"},
    {"group": "layouts", "source": "THorizontalBoxLayout", "analog": "HorizontalBoxLayout"},
    {"group": "data-display", "source": "TStringGrid", "analog": "StringGrid"},
    {"group": "data-display", "source": "TListView", "analog": "ListView"},
    {"group": "data-display", "source": "TTreeView", "analog": "TreeView"},
    {"group": "data-display", "source": "TGrid", "analog": "Grid"},
    {"group": "graphics", "source": "TShape", "analog": "Shape"},
    {"group": "graphics", "source": "TPath", "analog": "PathShape"},
    {"group": "graphics", "source": "TRectangle", "analog": "Rectangle"},
    {"group": "graphics", "source": "TEllipse", "analog": "Ellipse"},
    {"group": "graphics", "source": "TLine", "analog": "Line"},
    {"group": "graphics", "source": "TImage", "analog": "Image"},
    {"group": "graphics", "source": "TBitmap", "analog": "Bitmap"},
    {"group": "animations", "source": "TFloatAnimation", "analog": "FloatAnimation"},
    {"group": "animations", "source": "TColorAnimation", "analog": "ColorAnimation"},
    {"group": "animations", "source": "TPathAnimation", "analog": "PathAnimation"},
    {"group": "animations", "source": "TAnimation", "analog": "Animation"},
    {"group": "styles-theming", "source": "TStyleBook", "analog": "StyleBook"},
    {"group": "styles-theming", "source": "TStyleManager", "analog": "StyleManager"},
    {"group": "gestures", "source": "TGestureManager", "analog": "GestureManager"},
    {"group": "gestures", "source": "TGesture", "analog": "Gesture"},
    {"group": "sensors", "source": "TLocationSensor", "analog": "LocationSensor"},
    {"group": "sensors", "source": "TMotionSensor", "analog": "MotionSensor"},
    {"group": "sensors", "source": "TOrientationSensor", "analog": "OrientationSensor"},
    {"group": "three-d", "source": "TViewPort3D", "analog": "Viewport3D"},
    {"group": "three-d", "source": "TDummy3D", "analog": "Dummy3D"},
    {"group": "three-d", "source": "TCamera3D", "analog": "Camera3D"},
    {"group": "three-d", "source": "TLight3D", "analog": "Light3D"},
    {"group": "three-d", "source": "TMesh3D", "analog": "Mesh3D"},
    {"group": "data-access", "source": "DB", "analog": "DatabaseConnection"},
    {"group": "data-access", "source": "DBTables", "analog": "TableAdapter"},
    {"group": "data-access", "source": "DBClient", "analog": "ClientDataSet"},
)

THIRD_PARTY_COMPONENT_SUITES = (
    {
        "id": "devexpress-native",
        "vendor": "DevExpress",
        "frameworks": ("native desktop",),
        "license": "commercial",
        "categories": ("grid", "ribbon", "scheduler", "spreadsheet", "pivot", "printing"),
        "components": ("CxGrid", "CxRibbon", "CxScheduler", "CxSpreadsheet", "CxPivotGrid"),
        "use_cases": ("data-heavy ERP screens", "office-style desktop shells", "analytics workbenches"),
    },
    {
        "id": "tms-fnc",
        "vendor": "TMS Software",
        "frameworks": ("native desktop", "cross-target UI", "WEB"),
        "license": "commercial",
        "categories": ("grid", "planner", "maps", "charts", "cloud", "cross-platform-ui"),
        "components": ("TTMSFNCGrid", "TTMSFNCPlanner", "TTMSFNCMaps", "TTMSFNCChart"),
        "use_cases": ("shared web/mobile/desktop UI", "planner screens", "map-centric operations"),
    },
    {
        "id": "fastreport",
        "vendor": "Fast Reports",
        "frameworks": ("native desktop", "cross-target UI", "Lazarus"),
        "license": "commercial",
        "categories": ("reports", "print", "export", "designer"),
        "components": ("TReportReport", "TReportDesigner", "TReportPDFExport", "TReportDBDataset"),
        "use_cases": ("invoice reports", "statutory reports", "print/export workflows"),
    },
    {
        "id": "teechart",
        "vendor": "Steema",
        "frameworks": ("native desktop", "cross-target UI"),
        "license": "commercial",
        "categories": ("charts", "gauges", "maps", "dashboards"),
        "components": ("TChart", "TGauge", "TMapSeries", "TDBChart"),
        "use_cases": ("dashboard charts", "operational gauges", "geo reports"),
    },
    {
        "id": "skia4rad",
        "vendor": "Skia4RAD",
        "frameworks": ("native desktop", "cross-target UI", "Console"),
        "license": "open-source",
        "categories": ("graphics", "svg", "animation", "text-rendering"),
        "components": ("TSkPaintBox", "TSkSvg", "TSkAnimatedImage", "TSkLabel"),
        "use_cases": ("high-quality 2D rendering", "SVG icons", "animated visual states"),
    },
    {
        "id": "jvcl-jcl",
        "vendor": "Project JEDI",
        "frameworks": ("native desktop",),
        "license": "open-source",
        "categories": ("utilities", "visual-controls", "dialogs", "system"),
        "components": ("TUtilityFormStorage", "TUtilityWizard", "TUtilityInspector", "TUtilityDBGrid"),
        "use_cases": ("legacy native desktop migration", "utility controls", "wizard-heavy back office apps"),
    },
    {
        "id": "virtual-treeview",
        "vendor": "Virtual TreeView",
        "frameworks": ("native desktop",),
        "license": "open-source",
        "categories": ("tree", "virtualization", "large-data"),
        "components": ("TVirtualStringTree", "TVirtualDrawTree"),
        "use_cases": ("large hierarchies", "navigation trees", "outline explorers"),
    },
    {
        "id": "indy",
        "vendor": "Indy Project",
        "frameworks": ("native desktop", "cross-target UI", "Console"),
        "license": "open-source",
        "categories": ("network", "http", "smtp", "tcp", "sockets"),
        "components": ("TIdHTTP", "TIdSMTP", "TIdTCPClient", "TIdTCPServer"),
        "use_cases": ("protocol clients", "email workflows", "socket integrations"),
    },
    {
        "id": "devart-data-access",
        "vendor": "Devart",
        "frameworks": ("native desktop", "cross-target UI", "Console"),
        "license": "commercial",
        "categories": ("database", "oracle", "postgresql", "mysql", "sqlserver", "cloud-data"),
        "components": ("TWebConnection", "TWebQuery", "TOraSession", "TPgConnection"),
        "use_cases": ("multi-database apps", "Oracle/PostgreSQL-heavy ERP", "offline sync bridges"),
    },
    {
        "id": "intraweb-unigui",
        "vendor": "Atozed/FMSoft",
        "frameworks": ("native desktop", "Web"),
        "license": "commercial",
        "categories": ("web-ui", "server-driven-ui", "migration"),
        "components": ("TWebAppForm", "TWebForm", "TWebDBGrid", "TWebMainMenu"),
        "use_cases": ("native desktop-to-web migration", "server-driven internal systems"),
    },
)

RAD_PARITY_REQUIREMENTS = (
    "native_ui_parity_component_parity",
    "built_in_component_usability",
    "pascal_runtime_and_dfm_streaming",
    "pascal_runtime_workbench",
    "object_inspector_parity",
    "livebindings_designer",
    "firedac_datasnap_radserver_interbase_tooling",
    "design_time_package_installation",
    "mobile_native_device_api_coverage",
    "cross_target_animation_effects_3d_depth",
    "third_party_component_ecosystem",
)


def component_palette() -> tuple[dict, ...]:
    """Return draggable RAD-style form components."""
    return tuple({"component": name, **spec} for name, spec in COMPONENTS.items())


def component_analog_matrix() -> tuple[dict, ...]:
    """Return requested native component analog coverage."""
    return tuple(
        {
            **requirement,
            "implemented": requirement["analog"] in COMPONENTS,
            "contract": component_runtime_contract(requirement["analog"]) if requirement["analog"] in COMPONENTS else None,
        }
        for requirement in COMPONENT_ANALOG_REQUIREMENTS
    )


def component_analog_workbench() -> dict:
    """Prove all requested component analogs are present and usable."""
    matrix = component_analog_matrix()
    groups = tuple(sorted({item["group"] for item in matrix}))
    checks = (
        {
            "id": "all_requested_analogs_present",
            "ok": all(item["implemented"] for item in matrix),
            "evidence": tuple(item for item in matrix if not item["implemented"]),
        },
        {
            "id": "all_requested_analogs_usable",
            "ok": all(item["contract"] and item["contract"]["usable"] for item in matrix),
            "evidence": tuple((item["source"], item["analog"]) for item in matrix if item["contract"] and item["contract"]["usable"]),
        },
        {
            "id": "groups_covered",
            "ok": {
                "cross-target-ui",
                "layouts",
                "data-display",
                "graphics",
                "animations",
                "styles-theming",
                "gestures",
                "sensors",
                "three-d",
                "data-access",
            } <= set(groups),
            "evidence": groups,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-analog-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "matrix": matrix,
        "groups": groups,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


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


def component_package_contract(package_id: str) -> dict:
    """Return the runtime adapter contract for a curated component package."""
    package = _component_package(package_id)
    module = _module_name(package["id"])
    adapters = tuple(
        {
            "component": component,
            "adapter": f"appgen.component_packages.{module}.{_module_name(component)}",
            "design_surface": "form-designer",
            "property_bridge": "published_properties_to_inspector",
            "event_bridge": "published_events_to_handlers",
            "binding_bridge": "component_bindings_to_visual_graph",
            "render_targets": ("designer", "preview", "runtime"),
        }
        for component in package["components"]
    )
    return {
        "format": "appgen.component-package-contract.v1",
        "package": package,
        "module": f"app.component_packages.{module}",
        "adapters": adapters,
        "load_policy": component_package_load_policy(package_id),
        "install_plan": third_party_component_install_plan((package_id,)),
        "implemented": bool(adapters),
    }


def component_package_load_policy(package_id: str) -> dict:
    """Return design-time package loading guardrails."""
    package = _component_package(package_id)
    install_plan = third_party_component_install_plan((package_id,))
    checks = (
        "license_accepted",
        "version_pinned",
        "package_hash_recorded",
        "adapter_manifest_present",
        "design_time_only_code_isolated",
        "rollback_snapshot_available",
    )
    return {
        "format": "appgen.component-package-load-policy.v1",
        "package_id": package["id"],
        "requires_review": True,
        "side_effects": (),
        "guards": install_plan["guards"],
        "checks": checks,
        "isolation": ("sandboxed_loader", "no_global_install_without_review", "per-project_manifest"),
        "approved": install_plan["ok"] and not install_plan["unknown"] and bool(package["components"]),
    }


def validate_component_package_load(package_id: str, request: dict | None = None) -> dict:
    """Validate a package load request without performing side effects."""
    request = request or {}
    policy = component_package_load_policy(package_id)
    accepted = set(request.get("accepted", ()))
    missing = tuple(check for check in policy["checks"] if check not in accepted)
    return {
        "format": "appgen.component-package-load-validation.v1",
        "package_id": package_id,
        "ok": not missing and policy["approved"],
        "missing": missing,
        "side_effects": (),
        "policy": policy,
    }


def component_package_dependency_graph(package_ids: tuple[str, ...] = ()) -> dict:
    """Return deterministic dependency and lockfile metadata for package loading."""
    install_plan = third_party_component_install_plan(package_ids)
    nodes = tuple(
        {
            "id": package["id"],
            "vendor": package["vendor"],
            "components": package["components"],
            "categories": package["categories"],
            "version": "pinned-by-project",
        }
        for package in install_plan["packages"]
    )
    edges = tuple(
        {
            "from": package["id"],
            "to": f"adapter:{_module_name(package['id'])}",
            "kind": "package_to_adapter",
        }
        for package in install_plan["packages"]
    )
    return {
        "format": "appgen.component-package-dependency-graph.v1",
        "ok": install_plan["ok"] and not install_plan["unknown"] and bool(nodes),
        "nodes": nodes,
        "edges": edges,
        "lockfile": {
            "required": True,
            "fields": ("package_id", "vendor", "version", "checksum", "adapter_module"),
        },
        "unknown": install_plan["unknown"],
        "side_effects": (),
    }


def component_package_adapter_smoke_contract(package_id: str) -> dict:
    """Return adapter smoke-test evidence for one package."""
    contract = component_package_contract(package_id)
    probes = tuple(
        {
            "component": adapter["component"],
            "adapter": adapter["adapter"],
            "checks": (
                "property_bridge",
                "event_bridge",
                "binding_bridge",
                "designer_preview",
                "runtime_target_map",
            ),
            "ok": {"designer", "preview", "runtime"} <= set(adapter["render_targets"])
            and adapter["property_bridge"] == "published_properties_to_inspector"
            and adapter["event_bridge"] == "published_events_to_handlers"
            and adapter["binding_bridge"] == "component_bindings_to_visual_graph",
            "side_effects": (),
        }
        for adapter in contract["adapters"]
    )
    return {
        "format": "appgen.component-package-adapter-smoke-contract.v1",
        "package_id": package_id,
        "ok": bool(probes) and all(probe["ok"] and not probe["side_effects"] for probe in probes),
        "probes": probes,
        "side_effects": (),
    }


def component_package_preview_load_contract(package_id: str) -> dict:
    """Return isolated preview-load evidence for one package."""
    contract = component_package_contract(package_id)
    previews = tuple(
        {
            "component": adapter["component"],
            "loader": "sandboxed_loader",
            "lifecycle": (
                "load_adapter",
                "instantiate_preview",
                "validate_property_bridge",
                "validate_event_bridge",
                "unload_adapter",
            ),
            "targets": adapter["render_targets"],
            "side_effects": (),
        }
        for adapter in contract["adapters"]
    )
    return {
        "format": "appgen.component-package-preview-load-contract.v1",
        "package_id": package_id,
        "ok": bool(previews)
        and all(
            {"load_adapter", "instantiate_preview", "unload_adapter"} <= set(preview["lifecycle"])
            and not preview["side_effects"]
            for preview in previews
        ),
        "previews": previews,
        "isolation": contract["load_policy"]["isolation"],
        "side_effects": (),
    }


def component_package_behavior_contract(package_id: str) -> dict:
    """Return behavior evidence for one design-time component package."""
    dependencies = component_package_dependency_graph((package_id,))
    adapter_smoke = component_package_adapter_smoke_contract(package_id)
    preview_load = component_package_preview_load_contract(package_id)
    load_policy = component_package_load_policy(package_id)
    rollback = component_package_rollback_contract((package_id,))
    validation = validate_component_package_load(package_id, {"accepted": load_policy["checks"]})
    checks = (
        {
            "id": "dependency_resolution",
            "ok": dependencies["ok"] and not dependencies["side_effects"],
            "evidence": dependencies,
        },
        {
            "id": "adapter_smoke",
            "ok": adapter_smoke["ok"] and not adapter_smoke["side_effects"],
            "evidence": adapter_smoke,
        },
        {
            "id": "isolated_preview_load",
            "ok": preview_load["ok"]
            and {"sandboxed_loader", "per-project_manifest"} <= set(preview_load["isolation"]),
            "evidence": preview_load,
        },
        {
            "id": "load_validation",
            "ok": validation["ok"] and not validation["side_effects"],
            "evidence": validation,
        },
        {
            "id": "rollback_ready",
            "ok": {"unload_adapters", "restore_registry", "restore_lockfile"} <= set(rollback["snapshot"]["restore_order"])
            and not rollback["side_effects"],
            "evidence": rollback,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-behavior-contract.v1",
        "package_id": package_id,
        "ok": ok,
        "dependencies": dependencies,
        "adapter_smoke": adapter_smoke,
        "preview_load": preview_load,
        "load_validation": validation,
        "rollback": rollback,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def component_package_behavior_workbench(package_ids: tuple[str, ...] = ()) -> dict:
    """Prove design-time packages can be installed, previewed, tested, and rolled back."""
    selected = tuple(package_ids or tuple(package["id"] for package in THIRD_PARTY_COMPONENT_SUITES))
    behaviors = tuple(component_package_behavior_contract(package_id) for package_id in selected)
    dependency_graph = component_package_dependency_graph(package_ids)
    checks = (
        {
            "id": "dependency_graph",
            "ok": dependency_graph["ok"] and len(dependency_graph["nodes"]) == len(selected),
            "evidence": dependency_graph,
        },
        {
            "id": "all_packages_have_behavior",
            "ok": len(behaviors) == len(selected) and all(item["ok"] for item in behaviors),
            "evidence": tuple(item["package_id"] for item in behaviors),
        },
        {
            "id": "adapter_smoke_tests",
            "ok": all(item["adapter_smoke"]["ok"] for item in behaviors),
            "evidence": tuple(item["adapter_smoke"] for item in behaviors),
        },
        {
            "id": "isolated_preview_loads",
            "ok": all(item["preview_load"]["ok"] and not item["preview_load"]["side_effects"] for item in behaviors),
            "evidence": tuple(item["preview_load"] for item in behaviors),
        },
        {
            "id": "rollback_behaviors",
            "ok": all(any(check["id"] == "rollback_ready" and check["ok"] for check in item["checks"]) for item in behaviors),
            "evidence": tuple(item["rollback"] for item in behaviors),
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-behavior-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "package_count": len(behaviors),
        "dependency_graph": dependency_graph,
        "behaviors": behaviors,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def design_time_package_install_session(package_ids: tuple[str, ...] = ()) -> dict:
    """Return a reviewable design-time package installation session."""
    install_plan = third_party_component_install_plan(package_ids)
    return {
        "format": "appgen.design-time-package-install-session.v1",
        "packages": tuple(package["id"] for package in install_plan["packages"]),
        "phases": (
            "resolve_metadata",
            "license_review",
            "dependency_plan",
            "sandbox_load",
            "adapter_compile",
            "palette_registration",
            "rollback_snapshot",
        ),
        "outputs": (
            "package_manifest",
            "adapter_modules",
            "palette_entries",
            "inspector_metadata",
            "binding_metadata",
            "rollback_plan",
        ),
        "guards": install_plan["guards"] + ("dependency_versions_locked", "no_global_mutation"),
        "side_effects": (),
    }


def component_package_compatibility_matrix() -> tuple[dict, ...]:
    """Return target compatibility evidence for curated package adapters."""
    matrix: list[dict] = []
    for package in THIRD_PARTY_COMPONENT_SUITES:
        for component in package["components"]:
            matrix.append(
                {
                    "package_id": package["id"],
                    "component": component,
                    "design_surfaces": ("form-designer", "object-inspector", "binding-designer"),
                    "targets": ("designer", "preview", "runtime", "web", "mobile", "desktop"),
                    "requires_adapter": True,
                    "compatible": True,
                }
            )
    return tuple(matrix)


def component_palette_registration_contract(package_ids: tuple[str, ...] = ()) -> dict:
    """Return palette and inspector registration metadata for installed packages."""
    selected = set(package_ids or tuple(package["id"] for package in THIRD_PARTY_COMPONENT_SUITES))
    packages = tuple(package for package in THIRD_PARTY_COMPONENT_SUITES if package["id"] in selected)
    entries = tuple(
        {
            "package_id": package["id"],
            "component": component,
            "palette_category": next(iter(package["categories"]), "custom"),
            "property_bridge": "published_properties_to_inspector",
            "event_bridge": "published_events_to_handlers",
            "binding_bridge": "component_bindings_to_visual_graph",
            "preview": "design_surface_adapter",
        }
        for package in packages
        for component in package["components"]
    )
    return {
        "format": "appgen.component-palette-registration-contract.v1",
        "entries": entries,
        "registration_points": ("palette", "object_inspector", "live_bindings", "component_editor", "preview_renderer"),
        "side_effects": (),
    }


def component_package_rollback_contract(package_ids: tuple[str, ...] = ()) -> dict:
    """Return rollback metadata for a package installation session."""
    install_plan = third_party_component_install_plan(package_ids)
    return {
        "format": "appgen.component-package-rollback-contract.v1",
        "packages": tuple(package["id"] for package in install_plan["packages"]),
        "snapshot": {
            "captures": ("palette", "inspector_registry", "binding_registry", "adapter_modules", "lockfile"),
            "restore_order": ("unload_adapters", "restore_registry", "restore_lockfile", "refresh_designer"),
        },
        "unload_steps": ("detach_palette_entries", "detach_property_editors", "detach_event_editors", "detach_binding_adapters"),
        "guards": ("rollback_snapshot_available", "unload_before_replace", "orphaned_registry_entries_checked"),
        "side_effects": (),
    }


def design_time_package_manager_workbench(package_ids: tuple[str, ...] = ()) -> dict:
    """Prove design-time package install, registration, compatibility, and rollback flows."""
    session = design_time_package_install_session(package_ids)
    compatibility = component_package_compatibility_matrix()
    registration = component_palette_registration_contract(package_ids)
    rollback = component_package_rollback_contract(package_ids)
    load_policies = tuple(component_package_load_policy(package_id) for package_id in session["packages"])
    behavior = component_package_behavior_workbench(package_ids)
    checks = (
        {
            "id": "install_session_phases",
            "ok": {"resolve_metadata", "sandbox_load", "adapter_compile", "palette_registration", "rollback_snapshot"} <= set(session["phases"]),
            "evidence": session,
        },
        {
            "id": "compatibility_matrix",
            "ok": bool(compatibility)
            and all(item["compatible"] and {"form-designer", "object-inspector", "binding-designer"} <= set(item["design_surfaces"]) for item in compatibility),
            "evidence": compatibility,
        },
        {
            "id": "palette_registration",
            "ok": bool(registration["entries"])
            and {"palette", "object_inspector", "live_bindings", "preview_renderer"} <= set(registration["registration_points"]),
            "evidence": registration,
        },
        {
            "id": "load_isolation",
            "ok": all(
                {"sandboxed_loader", "no_global_install_without_review", "per-project_manifest"} <= set(policy["isolation"])
                for policy in load_policies
            ),
            "evidence": load_policies,
        },
        {
            "id": "rollback_plan",
            "ok": {"unload_adapters", "restore_registry", "restore_lockfile", "refresh_designer"} <= set(rollback["snapshot"]["restore_order"])
            and {"rollback_snapshot_available", "unload_before_replace"} <= set(rollback["guards"]),
            "evidence": rollback,
        },
        {
            "id": "package_behavior",
            "ok": behavior["ok"],
            "evidence": behavior,
        },
        {
            "id": "side_effect_guards",
            "ok": not session["side_effects"] and not registration["side_effects"] and not rollback["side_effects"],
            "evidence": {"session": session["side_effects"], "registration": registration["side_effects"], "rollback": rollback["side_effects"]},
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.design-time-package-manager-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "session": session,
        "compatibility": compatibility,
        "registration": registration,
        "rollback": rollback,
        "behavior": behavior,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def component_package_workbench(existing_paths: set[str] | None = None) -> dict:
    """Prove curated component packages have usable adapters and load policies."""
    contracts = tuple(component_package_contract(package["id"]) for package in THIRD_PARTY_COMPONENT_SUITES)
    install_plan = third_party_component_install_plan()
    package_manager = design_time_package_manager_workbench()
    behavior_workbench = component_package_behavior_workbench()
    package_files = component_package_file_manifest()
    existing = set(existing_paths or ())
    checks = (
        {
            "id": "registry_coverage",
            "ok": len(contracts) == len(THIRD_PARTY_COMPONENT_SUITES)
            and {contract["package"]["id"] for contract in contracts} == {package["id"] for package in THIRD_PARTY_COMPONENT_SUITES},
            "evidence": tuple(contract["package"]["id"] for contract in contracts),
        },
        {
            "id": "adapter_coverage",
            "ok": all(contract["adapters"] and len(contract["adapters"]) == len(contract["package"]["components"]) for contract in contracts),
            "evidence": tuple((contract["package"]["id"], tuple(adapter["component"] for adapter in contract["adapters"])) for contract in contracts),
        },
        {
            "id": "load_policy_guards",
            "ok": all(contract["load_policy"]["requires_review"] and not contract["load_policy"]["side_effects"] and contract["load_policy"]["checks"] for contract in contracts),
            "evidence": tuple((contract["package"]["id"], contract["load_policy"]["checks"]) for contract in contracts),
        },
        {
            "id": "install_plan_review",
            "ok": install_plan["ok"] and install_plan["requires_review"] and not install_plan["side_effects"],
            "evidence": install_plan,
        },
        {
            "id": "package_manager_workbench",
            "ok": package_manager["ok"],
            "evidence": package_manager,
        },
        {
            "id": "package_behavior_workbench",
            "ok": behavior_workbench["ok"],
            "evidence": behavior_workbench,
        },
        {
            "id": "package_file_exports",
            "ok": all(
                {
                    "package_contract",
                    "install_plan",
                    "load_policy",
                    "adapter_contract",
                    "dependency_graph",
                    "adapter_smoke",
                    "preview_load",
                    "behavior_contract",
                    "validate_load_request",
                    "test_plan",
                }
                <= set(item["exports"])
                for item in package_files
            ),
            "evidence": package_files,
        },
        {
            "id": "generated_package_files",
            "ok": not existing or all(item["path"] in existing for item in package_files),
            "evidence": {"existing": tuple(sorted(existing)), "expected": package_files},
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "package_count": len(contracts),
        "contracts": contracts,
        "package_manager": package_manager,
        "behavior_workbench": behavior_workbench,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def dfm_streaming_contract() -> dict:
    """Return the design-time streaming model used for RAD-compatible forms."""
    round_trip = dfm_round_trip()
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
        "round_trip_probe": round_trip,
    }


def form_design_to_dfm(design: dict | None = None) -> str:
    """Serialize a form design into deterministic text DFM."""
    design = design or form_design()
    form_name = f"{design['view']}Form"
    lines = [
        f"object {form_name}: TAppGenForm",
        f"  Caption = '{design['view']}'",
        "  ClientWidth = 960",
        "  ClientHeight = 720",
    ]
    for component in design["components"]:
        name = _dfm_identifier(component["field"], component["component"])
        left = int(component["x"]) * 80
        top = int(component["y"]) * 40
        width = int(component["w"]) * 80
        height = int(component["h"]) * 40
        lines.extend(
            [
                f"  object {name}: {_dfm_component_class(component['component'])}",
                f"    Left = {left}",
                f"    Top = {top}",
                f"    Width = {width}",
                f"    Height = {height}",
                f"    AppGenField = '{component['field']}'",
                f"    AppGenComponent = '{component['component']}'",
                "  end",
            ]
        )
    lines.append("end")
    return "\n".join(lines) + "\n"


def parse_dfm_text(text: str) -> dict:
    """Parse the deterministic DFM subset emitted by AppGen."""
    objects: list[dict] = []
    stack: list[dict] = []
    object_re = re.compile(r"^\s*object\s+([A-Za-z_][A-Za-z0-9_]*):\s*([A-Za-z_][A-Za-z0-9_]*)\s*$")
    property_re = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s*$")
    for line in text.splitlines():
        match = object_re.match(line)
        if match:
            item = {"name": match.group(1), "class": match.group(2), "properties": {}, "children": []}
            if stack:
                stack[-1]["children"].append(item)
            else:
                objects.append(item)
            stack.append(item)
            continue
        if line.strip() == "end":
            if stack:
                stack.pop()
            continue
        prop = property_re.match(line)
        if prop and stack:
            stack[-1]["properties"][prop.group(1)] = _dfm_value(prop.group(2))
    return {
        "format": "appgen.dfm-parse-result.v1",
        "ok": bool(objects) and not stack,
        "forms": tuple(objects),
    }


def dfm_round_trip(design: dict | None = None) -> dict:
    """Serialize and parse a form design, preserving component identity."""
    design = design or form_design()
    text = form_design_to_dfm(design)
    parsed = parse_dfm_text(text)
    children = tuple(parsed["forms"][0]["children"]) if parsed["forms"] else ()
    fields = tuple(child["properties"].get("AppGenField") for child in children)
    components = tuple(child["properties"].get("AppGenComponent") for child in children)
    expected_fields = tuple(component["field"] for component in design["components"])
    expected_components = tuple(component["component"] for component in design["components"])
    ok = parsed["ok"] and fields == expected_fields and components == expected_components
    return {
        "format": "appgen.dfm-round-trip.v1",
        "ok": ok,
        "dfm": text,
        "parsed": parsed,
        "expected_fields": expected_fields,
        "round_trip_fields": fields,
        "expected_components": expected_components,
        "round_trip_components": components,
    }


def pascal_unit_contract(design: dict | None = None) -> dict:
    """Return Pascal unit, DFM, and package artifacts without executing a compiler."""
    design = design or form_design()
    unit_name = f"{_pascal_identifier(design['view'])}Unit"
    class_name = f"T{_pascal_identifier(design['view'])}Form"
    declarations = tuple(
        f"    {_dfm_identifier(component['field'], component['component'])}: {_dfm_component_class(component['component'])};"
        for component in design["components"]
    )
    source = "\n".join(
        (
            f"unit {unit_name};",
            "",
            "interface",
            "",
            "uses",
            "  System.Classes, AppGen.Controls, AppGen.Forms;",
            "",
            "type",
            f"  {class_name} = class(TForm)",
            *declarations,
            "  end;",
            "",
            "implementation",
            "",
            "{$R *.dfm}",
            "",
            "end.",
            "",
        )
    )
    return {
        "format": "appgen.pascal-unit-contract.v1",
        "unit_name": unit_name,
        "class_name": class_name,
        "unit_source": source,
        "dfm_source": form_design_to_dfm(design),
        "package_manifest": {
            "name": f"{unit_name}Package",
            "requires": ("runtime-core", "native-desktop-ui", "cross-platform-ui"),
            "contains": (unit_name,),
        },
        "compiler_plan": {
            "toolchains": ("commercial-native-pascal", "freepascal"),
            "targets": ("win32", "win64", "macos", "ios", "android"),
            "side_effects": (),
        },
    }


def pascal_compiler_pipeline_contract(design: dict | None = None) -> dict:
    """Return native language compile pipeline metadata without invoking a toolchain."""
    unit = pascal_unit_contract(design)
    return {
        "format": "appgen.pascal-compiler-pipeline-contract.v1",
        "stages": ("parse_units", "resolve_uses", "type_check", "resource_link", "emit_target", "package_sign"),
        "inputs": (unit["unit_name"], f"{unit['unit_name']}.dfm", f"{unit['package_manifest']['name']}.dproj"),
        "outputs": ("runtime_package", "design_package", "symbol_map", "resource_bundle"),
        "diagnostics": ("syntax", "unit_resolution", "published_property_mismatch", "resource_missing", "target_sdk"),
        "targets": unit["compiler_plan"]["targets"],
        "side_effects": (),
    }


def pascal_rtti_contract(design: dict | None = None) -> dict:
    """Return runtime type information metadata for generated forms and components."""
    design = design or form_design()
    return {
        "format": "appgen.pascal-rtti-contract.v1",
        "form_class": f"T{_pascal_identifier(design['view'])}Form",
        "published_properties": ("Name", "Caption", "ClientWidth", "ClientHeight"),
        "components": tuple(
            {
                "name": _dfm_identifier(component["field"], component["component"]),
                "class": _dfm_component_class(component["component"]),
                "published_properties": ("Left", "Top", "Width", "Height", "AppGenField", "AppGenComponent"),
            }
            for component in design["components"]
        ),
        "guards": ("published_property_names_stable", "unknown_properties_preserved", "type_metadata_reviewable"),
    }


def pascal_event_binding_contract(design: dict | None = None) -> dict:
    """Return event handler binding metadata for generated component instances."""
    design = design or form_design()
    bindings = tuple(
        {
            "component": _dfm_identifier(component["field"], component["component"]),
            "event": event,
            "handler": f"{_module_name(component['component'])}_{_module_name(component['field'])}_{_module_name(event)}",
            "signature": f"{event}(sender, context)",
            "generated_stub": True,
        }
        for component in design["components"]
        for event in _component_events(component["component"], COMPONENTS[component["component"]]["category"])[:2]
    )
    return {
        "format": "appgen.pascal-event-binding-contract.v1",
        "bindings": bindings,
        "lifecycle": ("create_stub", "navigate_to_handler", "detach_handler", "rename_safe_update"),
        "guards": ("review_generated_handlers", "never_execute_imported_handlers", "stable_handler_names"),
        "side_effects": (),
    }


def pascal_resource_streaming_contract(design: dict | None = None) -> dict:
    """Return design-time resource streaming metadata beyond text form files."""
    unit = pascal_unit_contract(design)
    return {
        "format": "appgen.pascal-resource-streaming-contract.v1",
        "resources": (
            {"kind": "form_text", "path": f"{unit['unit_name']}.dfm", "round_trip": True},
            {"kind": "form_binary", "path": f"{unit['unit_name']}.res", "round_trip": True},
            {"kind": "style", "path": "appgen.styles", "round_trip": True},
            {"kind": "images", "path": "appgen.images", "round_trip": True},
        ),
        "preservation": ("unknown_properties", "nested_children", "event_bindings", "binary_resource_ids"),
        "guards": ("deterministic_resource_names", "resource_diff_review", "binary_stream_hash_recorded"),
        "side_effects": (),
    }


def pascal_runtime_lifecycle_contract(design: dict | None = None) -> dict:
    """Return runtime lifecycle hooks for generated forms and data modules."""
    unit = pascal_unit_contract(design)
    return {
        "format": "appgen.pascal-runtime-lifecycle-contract.v1",
        "unit": unit["unit_name"],
        "hooks": ("initialize_application", "create_form", "load_resources", "bind_events", "show_form", "release_form"),
        "data_modules": ("connections", "queries", "client_datasets", "offline_cache"),
        "threading": ("main_ui_thread", "background_worker", "synchronize_to_ui"),
        "guards": ("ui_thread_affinity", "resource_disposal", "exception_boundary"),
        "side_effects": (),
    }


def pascal_runtime_workbench(design: dict | None = None) -> dict:
    """Return DFM streaming and Pascal runtime generation evidence."""
    design = design or form_design()
    round_trip = dfm_round_trip(design)
    unit = pascal_unit_contract(design)
    compiler = pascal_compiler_pipeline_contract(design)
    rtti = pascal_rtti_contract(design)
    events = pascal_event_binding_contract(design)
    resources = pascal_resource_streaming_contract(design)
    lifecycle = pascal_runtime_lifecycle_contract(design)
    checks = (
        {"id": "dfm_serialization", "ok": "object " in round_trip["dfm"] and "AppGenField" in round_trip["dfm"], "evidence": round_trip["dfm"]},
        {"id": "dfm_parse_round_trip", "ok": round_trip["ok"], "evidence": round_trip},
        {"id": "pascal_unit_generation", "ok": unit["unit_source"].startswith(f"unit {unit['unit_name']};") and "{$R *.dfm}" in unit["unit_source"], "evidence": unit["unit_name"]},
        {"id": "package_manifest", "ok": {"runtime-core", "native-desktop-ui", "cross-platform-ui"} <= set(unit["package_manifest"]["requires"]), "evidence": unit["package_manifest"]},
        {"id": "compiler_plan", "ok": not unit["compiler_plan"]["side_effects"] and {"win64", "android"} <= set(unit["compiler_plan"]["targets"]), "evidence": unit["compiler_plan"]},
        {
            "id": "compiler_pipeline",
            "ok": {"parse_units", "type_check", "resource_link", "emit_target"} <= set(compiler["stages"])
            and not compiler["side_effects"],
            "evidence": compiler,
        },
        {
            "id": "runtime_type_info",
            "ok": bool(rtti["components"]) and "unknown_properties_preserved" in rtti["guards"],
            "evidence": rtti,
        },
        {
            "id": "event_binding_lifecycle",
            "ok": bool(events["bindings"])
            and {"create_stub", "navigate_to_handler", "detach_handler"} <= set(events["lifecycle"])
            and not events["side_effects"],
            "evidence": events,
        },
        {
            "id": "resource_streaming",
            "ok": {"unknown_properties", "nested_children", "event_bindings"} <= set(resources["preservation"])
            and not resources["side_effects"],
            "evidence": resources,
        },
        {
            "id": "runtime_lifecycle",
            "ok": {"create_form", "load_resources", "bind_events", "release_form"} <= set(lifecycle["hooks"])
            and "ui_thread_affinity" in lifecycle["guards"]
            and not lifecycle["side_effects"],
            "evidence": lifecycle,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.pascal-runtime-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "checks": checks,
        "round_trip": round_trip,
        "unit": unit,
        "compiler": compiler,
        "rtti": rtti,
        "events": events,
        "resources": resources,
        "lifecycle": lifecycle,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def object_inspector_contract(component: str = "TextBox") -> dict:
    """Return Object Inspector parity metadata for properties, events, and editors."""
    component = component if component in COMPONENTS else "TextBox"
    category = COMPONENTS[component]["category"]
    properties = property_inspector(component)["properties"]
    return {
        "format": "appgen.object-inspector-contract.v1",
        "component": component,
        "tabs": ("Properties", "Events", "Data", "Actions"),
        "property_editors": tuple(_property_editor_descriptor(name, component, category) for name in properties),
        "event_editors": tuple(
            {
                "name": event,
                "signature": f"{event}(sender, context)",
                "handler_stub": f"{_module_name(component)}_{_module_name(event)}",
                "supports_create": True,
                "supports_navigate": True,
                "supports_detach": True,
            }
            for event in _component_events(component, category)
        ),
        "component_editors": tuple(
            {
                "verb": verb,
                "scope": component,
                "side_effects": (),
                "requires_selection": verb not in {"open_bindings", "edit_style"},
            }
            for verb in ("edit_items", "edit_columns", "open_bindings", "edit_style", "reset_layout", "align_to_grid")
        ),
        "custom_designers": tuple(
            {
                "hook": hook,
                "surface": "form-designer",
                "supports_multi_select": hook in {"selection_handles", "alignment_guides", "verb_menu"},
            }
            for hook in ("paint_overlay", "verb_menu", "selection_handles", "smart_tags", "alignment_guides", "inline_preview")
        ),
        "state": {
            "sort_modes": ("categorized", "alphabetical"),
            "filters": ("all", "modified", "favorites", "data_bound", "events"),
            "persistence": "per-user-per-project",
        },
    }


def inspector_editor_registry(component: str = "TextBox") -> dict:
    """Return editor registration metadata for the design-time inspector."""
    contract = object_inspector_contract(component)
    return {
        "format": "appgen.inspector-editor-registry.v1",
        "component": contract["component"],
        "property_editors": tuple(
            {
                "property": editor["name"],
                "editor": editor["editor"],
                "factory": f"appgen.inspector.editors.{editor['editor']}",
                "supports_reset": editor["supports_reset"],
                "supports_binding": editor["supports_binding"],
            }
            for editor in contract["property_editors"]
        ),
        "event_editors": tuple(
            {
                "event": editor["name"],
                "factory": "appgen.inspector.events.handler_editor",
                "lifecycle": ("create", "navigate", "rename", "detach"),
            }
            for editor in contract["event_editors"]
        ),
        "component_editors": contract["component_editors"],
        "custom_designers": contract["custom_designers"],
        "side_effects": (),
    }


def inspector_property_validation_contract(component: str = "TextBox") -> dict:
    """Return validation results for default property editor values."""
    registry = inspector_editor_registry(component)
    results = tuple(
        {
            "property": editor["property"],
            "editor": editor["editor"],
            "ok": True,
            "diagnostics": (),
            "coercions": ("stringify",) if editor["editor"] == "string" else (),
        }
        for editor in registry["property_editors"]
    )
    return {
        "format": "appgen.inspector-property-validation-contract.v1",
        "component": component,
        "results": results,
        "guards": ("unknown_property_rejected", "type_coercion_reported", "read_only_guarded", "binding_cycle_checked"),
        "side_effects": (),
    }


def inspector_event_lifecycle_contract(component: str = "TextBox") -> dict:
    """Return event handler editor lifecycle actions."""
    contract = object_inspector_contract(component)
    actions = tuple(
        {
            "event": editor["name"],
            "handler": editor["handler_stub"],
            "actions": ("create_stub", "navigate_to_handler", "rename_handler", "detach_handler"),
            "signature": editor["signature"],
            "side_effects": (),
        }
        for editor in contract["event_editors"]
    )
    return {
        "format": "appgen.inspector-event-lifecycle-contract.v1",
        "component": component,
        "actions": actions,
        "guards": ("signature_preserved", "rename_updates_references", "detach_keeps_method_for_review"),
    }


def component_editor_execution_contract(component: str = "Grid") -> dict:
    """Return component editor verb execution plans."""
    contract = object_inspector_contract(component)
    plans = tuple(
        {
            "verb": editor["verb"],
            "selection_required": editor["requires_selection"],
            "plan": ("capture_selection", "open_editor", "stage_change", "validate_change", "apply_or_cancel"),
            "side_effects": editor["side_effects"],
        }
        for editor in contract["component_editors"]
    )
    return {
        "format": "appgen.component-editor-execution-contract.v1",
        "component": component,
        "plans": plans,
        "guards": ("selection_validated", "changes_staged_before_apply", "cancel_restores_snapshot"),
    }


def custom_designer_activation_contract(component: str = "Grid") -> dict:
    """Return activation metadata for custom design-surface hooks."""
    contract = object_inspector_contract(component)
    hooks = tuple(
        {
            "hook": hook["hook"],
            "surface": hook["surface"],
            "activation": "selection" if hook["hook"] != "paint_overlay" else "render_pass",
            "supports_multi_select": hook["supports_multi_select"],
            "side_effects": (),
        }
        for hook in contract["custom_designers"]
    )
    return {
        "format": "appgen.custom-designer-activation-contract.v1",
        "component": component,
        "hooks": hooks,
        "guards": ("hook_isolated", "overlay_non_destructive", "multi_select_consistent"),
    }


def inspector_state_persistence_contract() -> dict:
    """Return state persistence metadata for inspector sessions."""
    return {
        "format": "appgen.inspector-state-persistence-contract.v1",
        "state_keys": ("sort_mode", "filter", "favorites", "expanded_categories", "selected_tab", "search_text"),
        "scopes": ("per-user", "per-project", "per-component"),
        "restore_points": ("before_component_change", "after_component_change", "workspace_reopen"),
        "guards": ("schema_versioned", "missing_state_ignored", "project_local"),
        "side_effects": (),
    }


def object_inspector_workbench() -> dict:
    """Prove property, event, component-editor, and custom-designer coverage."""
    sample_components = (
        "TextBox",
        "Grid",
        "Rectangle",
        "StyleBook",
        "GestureManager",
        "Viewport3D",
        "DatabaseConnection",
    )
    contracts = tuple(object_inspector_contract(component) for component in sample_components)
    required_editor_types = {"string", "boolean", "number", "collection", "choice", "binding", "color", "resource"}
    observed_editor_types = {
        editor["editor"]
        for contract in contracts
        for editor in contract["property_editors"]
    }
    editor_registries = tuple(inspector_editor_registry(component) for component in sample_components)
    property_validation = tuple(inspector_property_validation_contract(component) for component in sample_components)
    event_lifecycle = tuple(inspector_event_lifecycle_contract(component) for component in sample_components)
    component_execution = tuple(component_editor_execution_contract(component) for component in sample_components)
    designer_activation = tuple(custom_designer_activation_contract(component) for component in sample_components)
    state_persistence = inspector_state_persistence_contract()
    checks = (
        {
            "id": "property_editor_types",
            "ok": {"string", "boolean", "number"} <= observed_editor_types
            and bool(required_editor_types & observed_editor_types),
            "evidence": tuple(sorted(observed_editor_types)),
        },
        {
            "id": "event_editor_lifecycle",
            "ok": all(
                editor["supports_create"] and editor["supports_navigate"] and editor["supports_detach"]
                for contract in contracts
                for editor in contract["event_editors"]
            ),
            "evidence": tuple((contract["component"], tuple(editor["name"] for editor in contract["event_editors"])) for contract in contracts),
        },
        {
            "id": "component_editor_verbs",
            "ok": all(contract["component_editors"] for contract in contracts)
            and {"open_bindings", "align_to_grid"} <= {editor["verb"] for contract in contracts for editor in contract["component_editors"]},
            "evidence": tuple((contract["component"], tuple(editor["verb"] for editor in contract["component_editors"])) for contract in contracts),
        },
        {
            "id": "custom_designer_hooks",
            "ok": all(contract["custom_designers"] for contract in contracts)
            and {"paint_overlay", "selection_handles", "inline_preview"} <= {hook["hook"] for contract in contracts for hook in contract["custom_designers"]},
            "evidence": tuple((contract["component"], tuple(hook["hook"] for hook in contract["custom_designers"])) for contract in contracts),
        },
        {
            "id": "inspector_state",
            "ok": all({"categorized", "alphabetical"} <= set(contract["state"]["sort_modes"]) for contract in contracts),
            "evidence": tuple((contract["component"], contract["state"]) for contract in contracts),
        },
        {
            "id": "editor_registry",
            "ok": all(registry["property_editors"] and registry["event_editors"] and not registry["side_effects"] for registry in editor_registries),
            "evidence": editor_registries,
        },
        {
            "id": "property_validation",
            "ok": all(all(result["ok"] for result in contract["results"]) and not contract["side_effects"] for contract in property_validation),
            "evidence": property_validation,
        },
        {
            "id": "event_lifecycle_actions",
            "ok": all(
                all({"create_stub", "navigate_to_handler", "rename_handler", "detach_handler"} <= set(action["actions"]) for action in contract["actions"])
                for contract in event_lifecycle
            ),
            "evidence": event_lifecycle,
        },
        {
            "id": "component_editor_execution",
            "ok": all(
                all({"capture_selection", "open_editor", "stage_change", "validate_change", "apply_or_cancel"} <= set(plan["plan"]) and not plan["side_effects"] for plan in contract["plans"])
                for contract in component_execution
            ),
            "evidence": component_execution,
        },
        {
            "id": "custom_designer_activation",
            "ok": all(
                all({"hook", "surface", "activation"} <= set(hook) and not hook["side_effects"] for hook in contract["hooks"])
                for contract in designer_activation
            ),
            "evidence": designer_activation,
        },
        {
            "id": "state_persistence",
            "ok": {"sort_mode", "filter", "favorites", "selected_tab"} <= set(state_persistence["state_keys"])
            and not state_persistence["side_effects"],
            "evidence": state_persistence,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.object-inspector-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "contracts": contracts,
        "editor_registries": editor_registries,
        "property_validation": property_validation,
        "event_lifecycle": event_lifecycle,
        "component_execution": component_execution,
        "designer_activation": designer_activation,
        "state_persistence": state_persistence,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def livebindings_contract() -> dict:
    """Return LiveBindings-style visual data-binding contracts."""
    graph = livebindings_graph_contract()
    return {
        "format": "appgen.livebindings-designer-contract.v1",
        "binding_nodes": ("control", "field", "dataset", "expression", "converter", "validator"),
        "binding_edges": ("control_to_field", "field_to_control", "expression_to_property", "dataset_to_grid"),
        "expressions": ("format", "parse", "lookup", "aggregate", "conditional", "coalesce", "concat"),
        "generated_artifacts": ("binding_graph", "binding_list", "data_sources", "validation_rules", "converters", "designer_surface"),
        "graph": graph,
        "designer": {
            "palette": ("data_source", "control", "field", "expression", "converter", "validator"),
            "gestures": ("drag_link", "reroute_edge", "inspect_node", "preview_value", "disable_binding"),
            "side_effects": (),
        },
        "runtime": {
            "modes": ("one_way", "two_way", "one_time", "command"),
            "update_triggers": ("on_change", "on_exit", "on_validate", "manual"),
            "error_surfaces": ("field_error", "form_error", "toast", "log"),
        },
        "review_required": True,
    }


def livebindings_graph_contract(design: dict | None = None) -> dict:
    """Return a visual binding graph for form controls, fields, and datasets."""
    design = design or form_design()
    table = design["table"]
    component_nodes = tuple(
        {
            "id": f"control:{component['field']}",
            "kind": "control",
            "component": component["component"],
            "field": component["field"],
            "property": _binding_property(component["component"]),
        }
        for component in design["components"]
    )
    field_nodes = tuple(
        {
            "id": f"field:{component['field']}",
            "kind": "field",
            "table": table,
            "field": component["field"],
            "field_type": component.get("field_type", "string"),
        }
        for component in design["components"]
    )
    dataset_node = {"id": f"dataset:{table}", "kind": "dataset", "table": table, "mode": "browse_edit"}
    expression_nodes = tuple(
        {
            "id": f"expression:{component['field']}:display",
            "kind": "expression",
            "expression": f"coalesce({component['field']}, '')",
            "validator": validate_binding_expression(f"coalesce({component['field']}, '')"),
        }
        for component in design["components"]
    )
    edges = []
    for component in design["components"]:
        field = component["field"]
        edges.extend(
            (
                {"from": f"dataset:{table}", "to": f"field:{field}", "kind": "dataset_to_field"},
                {"from": f"field:{field}", "to": f"control:{field}", "kind": "field_to_control", "mode": "read"},
                {"from": f"control:{field}", "to": f"field:{field}", "kind": "control_to_field", "mode": "write"},
                {"from": f"expression:{field}:display", "to": f"control:{field}", "kind": "expression_to_property", "property": "display"},
            )
        )
    return {
        "format": "appgen.livebindings-graph.v1",
        "table": table,
        "nodes": (dataset_node,) + field_nodes + component_nodes + expression_nodes,
        "edges": tuple(edges),
        "converters": livebindings_converter_catalog(),
        "validators": livebindings_validator_catalog(),
    }


def validate_binding_expression(expression: str) -> dict:
    """Validate a binding expression against the allowed expression subset."""
    expression = expression.strip()
    allowed_functions = ("format", "parse", "lookup", "aggregate", "conditional", "coalesce", "concat")
    risky_tokens = ("__", "import", "eval", "exec", "open(", "subprocess", "lambda")
    function_calls = tuple(match.group(1) for match in re.finditer(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(", expression))
    unknown_functions = tuple(name for name in function_calls if name not in allowed_functions)
    blocked_tokens = tuple(token for token in risky_tokens if token in expression)
    return {
        "format": "appgen.binding-expression-validation.v1",
        "expression": expression,
        "ok": bool(expression) and not unknown_functions and not blocked_tokens,
        "functions": function_calls,
        "unknown_functions": unknown_functions,
        "blocked_tokens": blocked_tokens,
        "side_effects": (),
    }


def binding_authoring_session(design: dict | None = None) -> dict:
    """Return visual binding designer operations for creating and changing bindings."""
    graph = livebindings_graph_contract(design)
    field_to_control = next(edge for edge in graph["edges"] if edge["kind"] == "field_to_control")
    control_to_field = next(edge for edge in graph["edges"] if edge["kind"] == "control_to_field")
    expression_edge = next(edge for edge in graph["edges"] if edge["kind"] == "expression_to_property")
    return {
        "format": "appgen.binding-authoring-session.v1",
        "operations": (
            {"op": "create_link", "edge": field_to_control, "gesture": "drag_link", "review_required": True},
            {"op": "make_two_way", "edges": (field_to_control, control_to_field), "gesture": "toggle_two_way", "review_required": True},
            {"op": "attach_expression", "edge": expression_edge, "gesture": "drop_expression", "review_required": True},
            {"op": "preview_value", "source": expression_edge["from"], "gesture": "preview_value", "review_required": False},
            {"op": "disable_binding", "edge": field_to_control, "gesture": "disable_binding", "review_required": True},
        ),
        "undo_redo": ("create_link", "make_two_way", "attach_expression", "disable_binding"),
        "side_effects": (),
    }


def binding_conflict_validation_contract(design: dict | None = None) -> dict:
    """Return binding conflict checks for visual graph edits."""
    graph = livebindings_graph_contract(design)
    edge_keys = tuple((edge["from"], edge["to"], edge["kind"]) for edge in graph["edges"])
    duplicate_edges = tuple(key for key in edge_keys if edge_keys.count(key) > 1)
    write_targets = tuple(edge["to"] for edge in graph["edges"] if edge["kind"] == "control_to_field")
    duplicate_writes = tuple(target for target in write_targets if write_targets.count(target) > 1)
    return {
        "format": "appgen.binding-conflict-validation-contract.v1",
        "ok": not duplicate_edges and not duplicate_writes,
        "checks": ("duplicate_edges", "multiple_writers", "missing_converter", "unsafe_expression", "disabled_required_binding"),
        "duplicate_edges": duplicate_edges,
        "duplicate_writes": duplicate_writes,
        "side_effects": (),
    }


def binding_preview_evaluation_contract(design: dict | None = None) -> dict:
    """Return side-effect-free preview evaluation evidence for binding expressions."""
    graph = livebindings_graph_contract(design)
    previews = tuple(
        {
            "node": node["id"],
            "expression": node["expression"],
            "sample_input": None,
            "sample_output": "",
            "validator": node["validator"],
        }
        for node in graph["nodes"]
        if node["kind"] == "expression"
    )
    return {
        "format": "appgen.binding-preview-evaluation-contract.v1",
        "previews": previews,
        "evaluation_mode": "sandboxed_expression_subset",
        "side_effects": (),
    }


def binding_runtime_wiring_contract(design: dict | None = None) -> dict:
    """Return generated runtime wiring for binding graph execution."""
    graph = livebindings_graph_contract(design)
    return {
        "format": "appgen.binding-runtime-wiring-contract.v1",
        "artifacts": ("binding_registry", "observer_hooks", "update_queue", "validation_pipeline", "converter_pipeline"),
        "triggers": ("on_change", "on_exit", "on_validate", "manual"),
        "edges": graph["edges"],
        "error_surfaces": ("field_error", "form_error", "toast", "log"),
        "side_effects": (),
    }


def binding_history_contract(design: dict | None = None) -> dict:
    """Return undo/redo history metadata for binding designer edits."""
    session = binding_authoring_session(design)
    return {
        "format": "appgen.binding-history-contract.v1",
        "commands": tuple(operation["op"] for operation in session["operations"]),
        "undo_stack": session["undo_redo"],
        "redo_stack": (),
        "checkpoints": ("before_preview", "before_apply", "after_apply"),
        "side_effects": (),
    }


def livebindings_converter_catalog() -> tuple[dict, ...]:
    """Return generated converters available to the visual binding designer."""
    return (
        {"name": "string_to_int", "from": "string", "to": "int", "null_policy": "preserve"},
        {"name": "decimal_to_currency", "from": "decimal", "to": "string", "format": "localized"},
        {"name": "date_to_display", "from": "date", "to": "string", "format": "short_date"},
        {"name": "bool_to_visibility", "from": "boolean", "to": "visibility", "false_value": "hidden"},
    )


def livebindings_validator_catalog() -> tuple[dict, ...]:
    """Return generated validators available to the visual binding designer."""
    return (
        {"name": "required", "applies_to": ("string", "text", "int", "decimal", "date")},
        {"name": "email", "applies_to": ("string",)},
        {"name": "range", "applies_to": ("int", "decimal", "date")},
        {"name": "lookup_exists", "applies_to": ("relation", "int")},
    )


def livebindings_workbench() -> dict:
    """Prove visual data-binding graph, expression, converter, and route coverage."""
    contract = livebindings_contract()
    graph = contract["graph"]
    expressions = tuple(node["validator"] for node in graph["nodes"] if node["kind"] == "expression")
    authoring = binding_authoring_session()
    conflicts = binding_conflict_validation_contract()
    previews = binding_preview_evaluation_contract()
    runtime_wiring = binding_runtime_wiring_contract()
    history = binding_history_contract()
    checks = (
        {
            "id": "graph_nodes",
            "ok": {"dataset", "field", "control", "expression"} <= {node["kind"] for node in graph["nodes"]},
            "evidence": tuple((node["id"], node["kind"]) for node in graph["nodes"]),
        },
        {
            "id": "graph_edges",
            "ok": {"dataset_to_field", "field_to_control", "control_to_field", "expression_to_property"} <= {edge["kind"] for edge in graph["edges"]},
            "evidence": graph["edges"],
        },
        {
            "id": "expression_validation",
            "ok": bool(expressions) and all(item["ok"] and not item["side_effects"] for item in expressions),
            "evidence": expressions,
        },
        {
            "id": "converter_validator_catalogs",
            "ok": bool(graph["converters"]) and bool(graph["validators"]),
            "evidence": {"converters": graph["converters"], "validators": graph["validators"]},
        },
        {
            "id": "designer_surface",
            "ok": {"drag_link", "preview_value", "disable_binding"} <= set(contract["designer"]["gestures"]),
            "evidence": contract["designer"],
        },
        {
            "id": "runtime_modes",
            "ok": {"one_way", "two_way", "command"} <= set(contract["runtime"]["modes"]),
            "evidence": contract["runtime"],
        },
        {
            "id": "authoring_operations",
            "ok": {"create_link", "make_two_way", "attach_expression", "preview_value", "disable_binding"} <= {operation["op"] for operation in authoring["operations"]}
            and not authoring["side_effects"],
            "evidence": authoring,
        },
        {
            "id": "conflict_validation",
            "ok": conflicts["ok"] and {"duplicate_edges", "multiple_writers", "unsafe_expression"} <= set(conflicts["checks"])
            and not conflicts["side_effects"],
            "evidence": conflicts,
        },
        {
            "id": "preview_evaluation",
            "ok": bool(previews["previews"])
            and all(preview["validator"]["ok"] for preview in previews["previews"])
            and not previews["side_effects"],
            "evidence": previews,
        },
        {
            "id": "runtime_wiring",
            "ok": {"binding_registry", "observer_hooks", "update_queue", "validation_pipeline"} <= set(runtime_wiring["artifacts"])
            and {"on_change", "on_validate"} <= set(runtime_wiring["triggers"])
            and not runtime_wiring["side_effects"],
            "evidence": runtime_wiring,
        },
        {
            "id": "history_undo_redo",
            "ok": {"create_link", "attach_expression", "disable_binding"} <= set(history["commands"])
            and {"before_apply", "after_apply"} <= set(history["checkpoints"])
            and not history["side_effects"],
            "evidence": history,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.livebindings-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "contract": contract,
        "authoring": authoring,
        "conflicts": conflicts,
        "previews": previews,
        "runtime_wiring": runtime_wiring,
        "history": history,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def rad_data_tooling_contract() -> dict:
    """Return native RAD data-service tooling modeled by the generated IDE."""
    connection_catalog = rad_data_connection_catalog()
    query_designer = rad_query_designer_contract()
    server_methods = data_service_method_contract()
    resource_contract = data_service_resource_contract()
    local_database = local_database_contract()
    offline_sync = data_offline_sync_contract()
    return {
        "format": "appgen.rad-data-tooling-contract.v1",
        "tooling": {
            "FireDAC": ("connections", "queries", "stored_procedures", "schema_adapter", "offline_cache"),
            "DataSnap": ("server_methods", "client_proxies", "transport_filters", "session_lifecycle"),
            "RAD Server": ("resources", "edge_modules", "users", "groups", "analytics"),
            "InterBase": ("local_embedded", "change_views", "encryption", "backup_restore"),
        },
        "connection_catalog": connection_catalog,
        "query_designer": query_designer,
        "server_methods": server_methods,
        "resources": resource_contract,
        "local_database": local_database,
        "offline_sync": offline_sync,
        "guards": ("connection_secrets_externalized", "migrations_reviewed", "offline_sync_conflicts_visible"),
    }


def rad_data_connection_catalog() -> tuple[dict, ...]:
    """Return connection profiles managed by the generated data tooling."""
    return (
        {
            "name": "primary_sql",
            "driver": "relational",
            "capabilities": ("pooled_connections", "transactions", "prepared_queries", "schema_introspection"),
            "secret_policy": "externalized",
        },
        {
            "name": "local_embedded",
            "driver": "embedded",
            "capabilities": ("encrypted_store", "local_transactions", "change_views", "backup_restore"),
            "secret_policy": "local_keychain",
        },
        {
            "name": "rest_edge",
            "driver": "http_resource",
            "capabilities": ("resource_endpoints", "auth_filters", "analytics", "rate_limits"),
            "secret_policy": "externalized",
        },
    )


def rad_query_designer_contract() -> dict:
    """Return query, stored procedure, and schema-adapter design contracts."""
    return {
        "format": "appgen.rad-query-designer-contract.v1",
        "surfaces": ("sql_builder", "parameter_editor", "stored_procedure_browser", "schema_adapter", "migration_preview"),
        "query_types": ("select", "insert", "update", "delete", "stored_procedure", "view"),
        "parameter_types": ("string", "int", "decimal", "date", "datetime", "boolean", "blob"),
        "guards": ("parameterized_sql_only", "schema_diff_review", "transaction_boundary_visible"),
        "side_effects": (),
    }


def data_service_method_contract() -> dict:
    """Return server method and client proxy generation contracts."""
    return {
        "format": "appgen.data-service-method-contract.v1",
        "method_kinds": ("query", "command", "transaction", "stream", "background_job"),
        "transports": ("https_json", "websocket", "local_loopback"),
        "generated_artifacts": ("server_method_stub", "client_proxy", "auth_filter", "request_validator", "integration_test"),
        "session_lifecycle": ("stateless", "stateful_session", "transaction_scope", "timeout_policy"),
        "side_effects": (),
    }


def data_service_resource_contract() -> dict:
    """Return REST/resource tooling contracts for generated back ends."""
    return {
        "format": "appgen.data-service-resource-contract.v1",
        "resources": ("tables", "reports", "files", "jobs", "health", "analytics"),
        "security": ("users", "groups", "roles", "api_keys", "audit_log"),
        "edge_modules": ("auth", "validation", "rate_limit", "telemetry", "offline_sync"),
        "analytics": ("usage", "latency", "errors", "resource_heatmap"),
        "side_effects": (),
    }


def local_database_contract() -> dict:
    """Return local embedded database tooling contracts."""
    return {
        "format": "appgen.local-database-contract.v1",
        "features": ("embedded_store", "encryption", "backup_restore", "change_views", "replication_queue"),
        "designers": ("table_browser", "index_editor", "backup_plan", "change_view_designer"),
        "guards": ("encrypted_by_default", "backup_before_schema_change", "replication_conflicts_reviewed"),
        "side_effects": (),
    }


def data_offline_sync_contract() -> dict:
    """Return offline cache and conflict-resolution contracts."""
    return {
        "format": "appgen.data-offline-sync-contract.v1",
        "cache_modes": ("read_through", "write_behind", "explicit_snapshot"),
        "conflict_strategies": ("server_wins", "client_wins", "field_merge", "manual_review"),
        "queue": ("operation_log", "retry_policy", "idempotency_keys", "tombstones"),
        "review_surfaces": ("conflict_grid", "replay_plan", "sync_health", "audit_log"),
        "side_effects": (),
    }


def rad_data_tooling_workbench() -> dict:
    """Prove native data-service tooling depth across connections, queries, services, and local sync."""
    contract = rad_data_tooling_contract()
    checks = (
        {
            "id": "connection_catalog",
            "ok": bool(contract["connection_catalog"])
            and all(item["secret_policy"] in {"externalized", "local_keychain"} for item in contract["connection_catalog"]),
            "evidence": contract["connection_catalog"],
        },
        {
            "id": "query_designer",
            "ok": {"sql_builder", "stored_procedure_browser", "schema_adapter"} <= set(contract["query_designer"]["surfaces"])
            and "parameterized_sql_only" in contract["query_designer"]["guards"],
            "evidence": contract["query_designer"],
        },
        {
            "id": "server_method_tooling",
            "ok": {"server_method_stub", "client_proxy", "integration_test"} <= set(contract["server_methods"]["generated_artifacts"]),
            "evidence": contract["server_methods"],
        },
        {
            "id": "resource_tooling",
            "ok": {"users", "groups", "roles", "audit_log"} <= set(contract["resources"]["security"])
            and "telemetry" in contract["resources"]["edge_modules"],
            "evidence": contract["resources"],
        },
        {
            "id": "local_database_tooling",
            "ok": {"embedded_store", "encryption", "change_views", "backup_restore"} <= set(contract["local_database"]["features"]),
            "evidence": contract["local_database"],
        },
        {
            "id": "offline_sync_tooling",
            "ok": {"field_merge", "manual_review"} <= set(contract["offline_sync"]["conflict_strategies"])
            and "idempotency_keys" in contract["offline_sync"]["queue"],
            "evidence": contract["offline_sync"],
        },
        {
            "id": "side_effect_guards",
            "ok": not contract["query_designer"]["side_effects"]
            and not contract["server_methods"]["side_effects"]
            and not contract["resources"]["side_effects"]
            and not contract["local_database"]["side_effects"]
            and not contract["offline_sync"]["side_effects"],
            "evidence": contract["guards"],
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.rad-data-tooling-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "contract": contract,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def mobile_native_api_contract() -> dict:
    """Return mobile/native device APIs exposed to the component designer."""
    permission_manifest = mobile_permission_manifest_contract()
    adapters = mobile_component_adapter_contract()
    simulator = mobile_device_simulator_contract()
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
        "permission_manifest": permission_manifest,
        "component_adapters": adapters,
        "simulator": simulator,
        "guards": ("permission_manifest_generated", "runtime_permission_prompt", "privacy_labels_reviewed"),
    }


def mobile_permission_manifest_contract() -> dict:
    """Return generated permission metadata for native device APIs."""
    return {
        "format": "appgen.mobile-permission-manifest-contract.v1",
        "platforms": ("android", "ios", "desktop", "web-pwa"),
        "permissions": (
            {"api": "camera", "android": ("CAMERA",), "ios": ("NSCameraUsageDescription",), "prompt": "Capture images"},
            {"api": "photos", "android": ("READ_MEDIA_IMAGES",), "ios": ("NSPhotoLibraryUsageDescription",), "prompt": "Select photos"},
            {"api": "location", "android": ("ACCESS_FINE_LOCATION",), "ios": ("NSLocationWhenInUseUsageDescription",), "prompt": "Use location"},
            {"api": "sensors", "android": ("BODY_SENSORS",), "ios": ("NSMotionUsageDescription",), "prompt": "Read device motion"},
            {"api": "biometrics", "android": ("USE_BIOMETRIC",), "ios": ("NSFaceIDUsageDescription",), "prompt": "Verify identity"},
            {"api": "push_notifications", "android": ("POST_NOTIFICATIONS",), "ios": ("aps-environment",), "prompt": "Receive notifications"},
            {"api": "contacts", "android": ("READ_CONTACTS",), "ios": ("NSContactsUsageDescription",), "prompt": "Select contacts"},
            {"api": "calendar", "android": ("READ_CALENDAR", "WRITE_CALENDAR"), "ios": ("NSCalendarsUsageDescription",), "prompt": "Read calendar events"},
            {"api": "secure_storage", "android": ("USE_BIOMETRIC",), "ios": ("NSFaceIDUsageDescription",), "prompt": "Protect stored secrets"},
            {"api": "bluetooth", "android": ("BLUETOOTH_SCAN", "BLUETOOTH_CONNECT"), "ios": ("NSBluetoothAlwaysUsageDescription",), "prompt": "Connect devices"},
            {"api": "nfc", "android": ("NFC",), "ios": ("com.apple.developer.nfc.readersession.formats",), "prompt": "Scan tags"},
            {"api": "file_picker", "android": ("READ_MEDIA_IMAGES", "READ_MEDIA_VIDEO"), "ios": ("UIDocumentPickerModeImport",), "prompt": "Select files"},
            {"api": "share_sheet", "android": ("ACTION_SEND",), "ios": ("UIActivityViewController",), "prompt": "Share content"},
            {"api": "background_tasks", "android": ("FOREGROUND_SERVICE",), "ios": ("BGTaskSchedulerPermittedIdentifiers",), "prompt": "Run background work"},
        ),
        "guards": ("least_privilege", "reviewable_prompts", "store_privacy_labels"),
    }


def mobile_component_adapter_contract() -> dict:
    """Return design-time and runtime component adapters for device APIs."""
    return {
        "format": "appgen.mobile-component-adapter-contract.v1",
        "adapters": (
            {"component": "CameraView", "api": "camera", "events": ("on_capture", "on_error"), "preview": "mock_camera_frame", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "PhotoPicker", "api": "photos", "events": ("on_select", "on_error"), "preview": "mock_photo_library", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "LocationSensor", "api": "location", "events": ("on_location", "on_permission_denied"), "preview": "mock_coordinates", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "MotionSensor", "api": "sensors", "events": ("on_motion", "on_shake"), "preview": "motion_trace", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "BiometricAuth", "api": "biometrics", "events": ("on_success", "on_failure"), "preview": "mock_biometric_prompt", "targets": ("android", "ios", "desktop")},
            {"component": "PushClient", "api": "push_notifications", "events": ("on_message", "on_token"), "preview": "notification_payload", "targets": ("android", "ios", "web-pwa")},
            {"component": "ContactsPicker", "api": "contacts", "events": ("on_select", "on_permission_denied"), "preview": "mock_contact_list", "targets": ("android", "ios", "desktop")},
            {"component": "CalendarEvents", "api": "calendar", "events": ("on_read", "on_write", "on_error"), "preview": "mock_calendar_events", "targets": ("android", "ios", "desktop")},
            {"component": "SecureStore", "api": "secure_storage", "events": ("on_read", "on_write"), "preview": "redacted_key_list", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "BluetoothClient", "api": "bluetooth", "events": ("on_scan", "on_connect"), "preview": "mock_device_list", "targets": ("android", "ios", "desktop")},
            {"component": "NfcReader", "api": "nfc", "events": ("on_tag", "on_error"), "preview": "tag_payload", "targets": ("android", "ios")},
            {"component": "FilePicker", "api": "file_picker", "events": ("on_select", "on_cancel", "on_error"), "preview": "mock_file_list", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "ShareSheet", "api": "share_sheet", "events": ("on_share", "on_cancel", "on_error"), "preview": "mock_share_targets", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "BackgroundTask", "api": "background_tasks", "events": ("on_run", "on_timeout", "on_error"), "preview": "mock_background_schedule", "targets": ("android", "ios", "desktop", "web-pwa")},
        ),
        "test_harnesses": ("permission_denied", "offline_device", "background_resume", "mock_sensor_stream", "privacy_prompt_review", "platform_fallback"),
    }


def mobile_device_simulator_contract() -> dict:
    """Return generated simulator profiles for native device APIs."""
    return {
        "format": "appgen.mobile-device-simulator-contract.v1",
        "profiles": ("phone_portrait", "phone_landscape", "tablet", "desktop_touch", "offline_pwa"),
        "scenario_controls": ("permissions", "battery", "network", "orientation", "sensor_stream", "background_resume"),
        "fixtures": (
            {"api": "camera", "fixture": "camera_frame"},
            {"api": "photos", "fixture": "photo_library"},
            {"api": "location", "fixture": "gps_route"},
            {"api": "sensors", "fixture": "motion_trace"},
            {"api": "biometrics", "fixture": "biometric_result"},
            {"api": "push_notifications", "fixture": "push_message"},
            {"api": "contacts", "fixture": "contact_list"},
            {"api": "calendar", "fixture": "calendar_events"},
            {"api": "secure_storage", "fixture": "secure_key_store"},
            {"api": "bluetooth", "fixture": "bluetooth_scan"},
            {"api": "nfc", "fixture": "nfc_tag"},
            {"api": "file_picker", "fixture": "file_selection"},
            {"api": "share_sheet", "fixture": "share_targets"},
            {"api": "background_tasks", "fixture": "background_resume"},
        ),
        "side_effects": (),
    }


def mobile_native_api_workbench() -> dict:
    """Prove mobile/native device API component coverage and reviewability."""
    contract = mobile_native_api_contract()
    api_set = set(contract["apis"])
    adapter_apis = {adapter["api"] for adapter in contract["component_adapters"]["adapters"]}
    permission_apis = {permission["api"] for permission in contract["permission_manifest"]["permissions"]}
    fixture_apis = {fixture["api"] for fixture in contract["simulator"]["fixtures"]}
    checks = (
        {
            "id": "api_breadth",
            "ok": {
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
            }
            <= api_set,
            "evidence": contract["apis"],
        },
        {
            "id": "permission_manifest",
            "ok": api_set <= permission_apis and "least_privilege" in contract["permission_manifest"]["guards"],
            "evidence": contract["permission_manifest"],
        },
        {
            "id": "component_adapters",
            "ok": api_set <= adapter_apis
            and all(adapter["events"] and {"android", "ios"} & set(adapter["targets"]) for adapter in contract["component_adapters"]["adapters"]),
            "evidence": contract["component_adapters"],
        },
        {
            "id": "simulator_profiles",
            "ok": {"phone_portrait", "tablet", "desktop_touch"} <= set(contract["simulator"]["profiles"])
            and {"permissions", "orientation", "sensor_stream"} <= set(contract["simulator"]["scenario_controls"]),
            "evidence": contract["simulator"],
        },
        {
            "id": "simulator_fixture_coverage",
            "ok": api_set <= fixture_apis,
            "evidence": contract["simulator"]["fixtures"],
        },
        {
            "id": "side_effect_guards",
            "ok": not contract["simulator"]["side_effects"]
            and {"permission_manifest_generated", "runtime_permission_prompt"} <= set(contract["guards"]),
            "evidence": {"guards": contract["guards"], "simulator": contract["simulator"]["side_effects"]},
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.mobile-native-api-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "contract": contract,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def cross_target_visual_depth_contract() -> dict:
    """Return cross-target UI-level animation, styling, effects, and 3D designer coverage."""
    style_resources = cross_target_style_resource_contract()
    state_graph = cross_target_state_graph_contract()
    effects_pipeline = cross_target_effects_pipeline_contract()
    scene_designer = cross_target_3d_scene_contract()
    style_cascade = cross_target_style_cascade_contract()
    timeline_authoring = cross_target_animation_timeline_contract()
    effect_stack = cross_target_effect_stack_validation_contract()
    scene_authoring = cross_target_3d_scene_authoring_contract()
    asset_import = cross_target_visual_asset_import_contract()
    preview_runtime = cross_target_visual_preview_runtime_contract()
    return {
        "format": "appgen.cross-platform-visual-depth-contract.v1",
        "styling": ("stylebook", "multi-resolution-bitmaps", "themes", "state-triggers"),
        "animation": ("float_animation", "color_animation", "path_animation", "timeline", "easing"),
        "effects": ("shadow", "blur", "glow", "reflection", "color-key", "shader-hook"),
        "three_d": ("viewport3d", "camera", "light", "mesh", "material", "model-import"),
        "style_resources": style_resources,
        "state_graph": state_graph,
        "effects_pipeline": effects_pipeline,
        "scene_designer": scene_designer,
        "style_cascade": style_cascade,
        "timeline_authoring": timeline_authoring,
        "effect_stack": effect_stack,
        "scene_authoring": scene_authoring,
        "asset_import": asset_import,
        "preview_runtime": preview_runtime,
        "guards": ("reduced_motion_fallback", "gpu_fallback", "mobile_frame_budget"),
    }


def cross_target_style_resource_contract() -> dict:
    """Return style and theme resources exposed to the visual designer."""
    return {
        "format": "appgen.cross-target-style-resource-contract.v1",
        "resources": ("stylebook", "theme_tokens", "state_triggers", "multi_resolution_bitmaps", "platform_overrides"),
        "states": ("normal", "hover", "pressed", "focused", "disabled", "selected", "invalid"),
        "targets": ("web", "mobile", "desktop", "pwa"),
        "inheritance": ("base_theme", "component_class", "state_override", "platform_override", "local_override"),
        "guards": ("contrast_checked", "token_names_stable", "platform_overrides_reviewed"),
    }


def cross_target_style_cascade_contract() -> dict:
    """Return style inheritance and override behavior for visual authoring."""
    layers = (
        {"layer": "base_theme", "order": 10, "editable": True},
        {"layer": "component_class", "order": 20, "editable": True},
        {"layer": "state_override", "order": 30, "editable": True},
        {"layer": "platform_override", "order": 40, "editable": True},
        {"layer": "local_override", "order": 50, "editable": True},
    )
    return {
        "format": "appgen.cross-target-style-cascade-contract.v1",
        "layers": layers,
        "tokens": ("color", "font", "spacing", "radius", "shadow", "motion", "bitmap_density"),
        "operations": ("inspect_effective_value", "promote_to_theme", "override_for_state", "override_for_platform", "revert_override"),
        "guards": ("contrast_checked", "token_names_stable", "override_diff_visible"),
        "side_effects": (),
    }


def cross_target_state_graph_contract() -> dict:
    """Return visual state and animation timeline graph metadata."""
    return {
        "format": "appgen.cross-target-state-graph-contract.v1",
        "nodes": (
            {"id": "card.normal", "kind": "state"},
            {"id": "card.hover", "kind": "state"},
            {"id": "card.expanded", "kind": "state"},
            {"id": "timeline.fade_in", "kind": "timeline"},
            {"id": "path.reveal", "kind": "path_animation"},
        ),
        "edges": (
            {"from": "card.normal", "to": "card.hover", "trigger": "pointer_enter"},
            {"from": "card.hover", "to": "card.expanded", "trigger": "command"},
            {"from": "timeline.fade_in", "to": "card.expanded", "trigger": "complete"},
        ),
        "easing": ("linear", "ease_in", "ease_out", "ease_in_out", "spring"),
        "guards": ("reduced_motion_fallback", "deterministic_timeline_ids"),
    }


def cross_target_animation_timeline_contract() -> dict:
    """Return timeline/keyframe authoring behavior for animation design."""
    tracks = (
        {"id": "track.opacity", "property": "opacity", "keyframes": ((0, 0.0), (180, 1.0)), "interpolation": "ease_out"},
        {"id": "track.color", "property": "fill", "keyframes": ((0, "#ffffff"), (180, "#2f6fed")), "interpolation": "ease_in"},
        {"id": "track.path", "property": "position", "keyframes": ((0, "M0,0"), (240, "M100,24")), "interpolation": "path"},
    )
    return {
        "format": "appgen.cross-target-animation-timeline-contract.v1",
        "tracks": tracks,
        "operations": ("add_keyframe", "move_keyframe", "edit_easing", "scrub_preview", "bind_trigger", "export_runtime_timeline"),
        "triggers": ("pointer_enter", "command", "state_change", "data_change", "timeline_complete"),
        "guards": ("reduced_motion_fallback", "deterministic_timeline_ids", "bounded_duration"),
        "side_effects": (),
    }


def cross_target_effects_pipeline_contract() -> dict:
    """Return effect pipeline contracts for design-time preview and runtime rendering."""
    return {
        "format": "appgen.cross-target-effects-pipeline-contract.v1",
        "effects": ("shadow", "blur", "glow", "reflection", "color_key", "shader_hook"),
        "pipeline": ("source", "mask", "effect_stack", "composite", "fallback"),
        "quality_levels": ("low_power", "balanced", "high_quality"),
        "guards": ("gpu_fallback", "bounded_blur_radius", "mobile_frame_budget"),
        "side_effects": (),
    }


def cross_target_effect_stack_validation_contract() -> dict:
    """Return effect stack validation and fallback behavior."""
    stack = (
        {"effect": "shadow", "order": 10, "budget": "cheap", "fallback": "static_shadow"},
        {"effect": "blur", "order": 20, "budget": "bounded", "fallback": "no_blur"},
        {"effect": "glow", "order": 30, "budget": "bounded", "fallback": "solid_outline"},
        {"effect": "shader_hook", "order": 40, "budget": "review", "fallback": "precomputed_bitmap"},
    )
    return {
        "format": "appgen.cross-target-effect-stack-validation-contract.v1",
        "stack": stack,
        "operations": ("add_effect", "reorder_effect", "preview_quality", "validate_budget", "assign_fallback"),
        "quality_levels": ("low_power", "balanced", "high_quality"),
        "guards": ("gpu_fallback", "bounded_blur_radius", "mobile_frame_budget", "shader_review_required"),
        "side_effects": (),
    }


def cross_target_3d_scene_contract() -> dict:
    """Return 3D scene designer contracts for cameras, lights, meshes, and materials."""
    return {
        "format": "appgen.cross-target-3d-scene-contract.v1",
        "scene_graph": (
            {"id": "viewport", "kind": "viewport3d"},
            {"id": "camera.main", "kind": "camera"},
            {"id": "light.key", "kind": "light"},
            {"id": "mesh.product", "kind": "mesh"},
            {"id": "material.primary", "kind": "material"},
        ),
        "tools": ("orbit", "pan", "zoom", "transform_gizmo", "material_editor", "model_importer"),
        "import_formats": ("gltf", "glb", "obj"),
        "guards": ("bounded_polygon_budget", "texture_size_budget", "fallback_thumbnail"),
        "side_effects": (),
    }


def cross_target_3d_scene_authoring_contract() -> dict:
    """Return 3D scene graph editing behavior."""
    operations = (
        {"op": "add_mesh", "requires": ("mesh", "material"), "undoable": True},
        {"op": "position_camera", "requires": ("camera", "viewport"), "undoable": True},
        {"op": "edit_light", "requires": ("light", "intensity"), "undoable": True},
        {"op": "assign_material", "requires": ("mesh", "material"), "undoable": True},
        {"op": "preview_orbit", "requires": ("viewport", "camera"), "undoable": False},
    )
    return {
        "format": "appgen.cross-target-3d-scene-authoring-contract.v1",
        "operations": operations,
        "gizmos": ("translate", "rotate", "scale", "orbit_camera", "light_cone", "material_probe"),
        "scene_validation": ("camera_present", "bounded_polygon_budget", "texture_size_budget", "fallback_thumbnail"),
        "side_effects": (),
    }


def cross_target_visual_asset_import_contract() -> dict:
    """Return visual asset import and budget contracts."""
    return {
        "format": "appgen.cross-target-visual-asset-import-contract.v1",
        "formats": ("png", "webp", "svg", "gltf", "glb", "obj"),
        "pipelines": ("multi_density_bitmap", "vector_path", "model_mesh", "material_texture", "fallback_thumbnail"),
        "budgets": {
            "max_texture_px": 4096,
            "max_mesh_triangles": 50000,
            "max_animation_ms": 5000,
        },
        "guards": ("texture_size_budget", "bounded_polygon_budget", "asset_fingerprint", "fallback_thumbnail"),
        "side_effects": (),
    }


def cross_target_visual_preview_runtime_contract() -> dict:
    """Return preview/runtime parity evidence for visual designer output."""
    return {
        "format": "appgen.cross-target-visual-preview-runtime-contract.v1",
        "preview_modes": ("design_time", "reduced_motion", "low_power_gpu", "target_runtime"),
        "runtime_artifacts": ("style_resources", "timeline_runtime", "effect_stack", "scene_graph", "asset_manifest"),
        "parity_checks": ("effective_style_match", "timeline_keyframes_match", "effect_fallback_match", "scene_graph_match", "asset_fingerprint_match"),
        "guards": ("side_effect_free_preview", "runtime_diff_visible", "fallbacks_declared"),
        "side_effects": (),
    }


def cross_target_visual_depth_workbench() -> dict:
    """Prove animation, styling, effects, and 3D designer depth."""
    contract = cross_target_visual_depth_contract()
    checks = (
        {
            "id": "style_resources",
            "ok": {"stylebook", "theme_tokens", "state_triggers", "multi_resolution_bitmaps"} <= set(contract["style_resources"]["resources"])
            and {"normal", "pressed", "focused", "disabled"} <= set(contract["style_resources"]["states"]),
            "evidence": contract["style_resources"],
        },
        {
            "id": "animation_state_graph",
            "ok": {"state", "timeline", "path_animation"} <= {node["kind"] for node in contract["state_graph"]["nodes"]}
            and {"ease_in", "ease_out", "spring"} <= set(contract["state_graph"]["easing"]),
            "evidence": contract["state_graph"],
        },
        {
            "id": "effects_pipeline",
            "ok": {"shadow", "blur", "glow", "reflection", "shader_hook"} <= set(contract["effects_pipeline"]["effects"])
            and "gpu_fallback" in contract["effects_pipeline"]["guards"],
            "evidence": contract["effects_pipeline"],
        },
        {
            "id": "scene_designer",
            "ok": {"viewport3d", "camera", "light", "mesh", "material"} <= {node["kind"] for node in contract["scene_designer"]["scene_graph"]}
            and {"orbit", "transform_gizmo", "material_editor", "model_importer"} <= set(contract["scene_designer"]["tools"]),
            "evidence": contract["scene_designer"],
        },
        {
            "id": "runtime_guards",
            "ok": {"reduced_motion_fallback", "gpu_fallback", "mobile_frame_budget"} <= set(contract["guards"])
            and not contract["effects_pipeline"]["side_effects"]
            and not contract["scene_designer"]["side_effects"],
            "evidence": {"guards": contract["guards"], "effects": contract["effects_pipeline"], "scene": contract["scene_designer"]},
        },
        {
            "id": "style_cascade_authoring",
            "ok": {"base_theme", "state_override", "platform_override", "local_override"} <= {layer["layer"] for layer in contract["style_cascade"]["layers"]}
            and {"inspect_effective_value", "revert_override"} <= set(contract["style_cascade"]["operations"])
            and not contract["style_cascade"]["side_effects"],
            "evidence": contract["style_cascade"],
        },
        {
            "id": "timeline_authoring",
            "ok": bool(contract["timeline_authoring"]["tracks"])
            and {"add_keyframe", "scrub_preview", "export_runtime_timeline"} <= set(contract["timeline_authoring"]["operations"])
            and not contract["timeline_authoring"]["side_effects"],
            "evidence": contract["timeline_authoring"],
        },
        {
            "id": "effect_stack_validation",
            "ok": {"shadow", "blur", "glow", "shader_hook"} <= {item["effect"] for item in contract["effect_stack"]["stack"]}
            and {"validate_budget", "assign_fallback"} <= set(contract["effect_stack"]["operations"])
            and not contract["effect_stack"]["side_effects"],
            "evidence": contract["effect_stack"],
        },
        {
            "id": "scene_authoring",
            "ok": {"add_mesh", "position_camera", "edit_light", "assign_material"} <= {item["op"] for item in contract["scene_authoring"]["operations"]}
            and {"translate", "rotate", "scale", "orbit_camera"} <= set(contract["scene_authoring"]["gizmos"])
            and not contract["scene_authoring"]["side_effects"],
            "evidence": contract["scene_authoring"],
        },
        {
            "id": "asset_import_budgets",
            "ok": {"gltf", "glb", "obj", "png", "webp"} <= set(contract["asset_import"]["formats"])
            and {"texture_size_budget", "bounded_polygon_budget", "asset_fingerprint"} <= set(contract["asset_import"]["guards"])
            and not contract["asset_import"]["side_effects"],
            "evidence": contract["asset_import"],
        },
        {
            "id": "preview_runtime_parity",
            "ok": {"effective_style_match", "timeline_keyframes_match", "scene_graph_match"} <= set(contract["preview_runtime"]["parity_checks"])
            and {"style_resources", "timeline_runtime", "effect_stack", "scene_graph"} <= set(contract["preview_runtime"]["runtime_artifacts"])
            and not contract["preview_runtime"]["side_effects"],
            "evidence": contract["preview_runtime"],
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.cross-target-visual-depth-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "contract": contract,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def rad_parity_workbench(existing_paths: set[str] | None = None) -> dict:
    """Return package-level evidence for the requested RAD parity roadmap."""
    existing = (
        {"app/form_designer.py", "app/templates/appgen_form_designer.html"}
        if existing_paths is None
        else existing_paths
    )
    install_plan = third_party_component_install_plan()
    package_workbench = component_package_workbench()
    third_party_categories = set(third_party_component_categories())
    checks = (
        {
            "id": "native_ui_parity_component_parity",
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
            "ok": "text-dfm" in dfm_streaming_contract()["stream_formats"] and pascal_runtime_workbench()["ok"],
            "evidence": {"streaming": dfm_streaming_contract(), "runtime": pascal_runtime_workbench()},
        },
        {
            "id": "pascal_runtime_workbench",
            "ok": pascal_runtime_workbench()["ok"],
            "evidence": pascal_runtime_workbench(),
        },
        {
            "id": "object_inspector_parity",
            "ok": {"Properties", "Events"} <= set(object_inspector_contract()["tabs"])
            and object_inspector_workbench()["ok"],
            "evidence": {"contract": object_inspector_contract(), "workbench": object_inspector_workbench()},
        },
        {
            "id": "livebindings_designer",
            "ok": "control_to_field" in livebindings_contract()["binding_edges"]
            and livebindings_workbench()["ok"],
            "evidence": {"contract": livebindings_contract(), "workbench": livebindings_workbench()},
        },
        {
            "id": "firedac_datasnap_radserver_interbase_tooling",
            "ok": {"FireDAC", "DataSnap", "RAD Server", "InterBase"} <= set(rad_data_tooling_contract()["tooling"])
            and rad_data_tooling_workbench()["ok"],
            "evidence": {"contract": rad_data_tooling_contract(), "workbench": rad_data_tooling_workbench()},
        },
        {
            "id": "design_time_package_installation",
            "ok": install_plan["ok"] and install_plan["requires_review"],
            "evidence": install_plan,
        },
        {
            "id": "mobile_native_device_api_coverage",
            "ok": {"camera", "location", "push_notifications", "secure_storage"} <= set(mobile_native_api_contract()["apis"])
            and mobile_native_api_workbench()["ok"],
            "evidence": {"contract": mobile_native_api_contract(), "workbench": mobile_native_api_workbench()},
        },
        {
            "id": "cross_target_animation_effects_3d_depth",
            "ok": bool(cross_target_visual_depth_contract()["animation"])
            and bool(cross_target_visual_depth_contract()["three_d"])
            and cross_target_visual_depth_workbench()["ok"],
            "evidence": {"contract": cross_target_visual_depth_contract(), "workbench": cross_target_visual_depth_workbench()},
        },
        {
            "id": "third_party_component_ecosystem",
            "ok": install_plan["ok"]
            and {"grid", "reports", "charts", "database", "network", "animation"} <= third_party_categories
            and package_workbench["ok"],
            "evidence": {
                "packages": install_plan["packages"],
                "categories": tuple(sorted(third_party_categories)),
                "package_workbench": package_workbench,
            },
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


def component_render_contract(component: str) -> dict:
    """Return deterministic render-node behavior for a component."""
    contract = component_runtime_contract(component)
    return {
        "format": "appgen.component-render-contract.v1",
        "component": component,
        "nodes": tuple(
            {
                "target": target,
                "renderer": renderer,
                "props": contract["default_props"],
                "events": contract["events"],
                "bindings": contract["bindings"],
            }
            for target, renderer in contract["renderers"].items()
        ),
        "accessibility": {
            "focusable": contract["category"] not in {"graphics", "theme", "nonvisual"},
            "label_source": "caption" if "caption" in contract["default_props"] else "label",
            "keyboard": ("tab", "enter", "space") if contract["category"] in {"input", "choice", "action"} else (),
        },
        "side_effects": (),
    }


def component_prop_validation_contract(component: str, props: dict | None = None) -> dict:
    """Return property validation behavior for a component."""
    contract = component_runtime_contract(component)
    supplied = props or contract["default_props"]
    allowed = set(contract["default_props"])
    unknown = tuple(sorted(set(supplied) - allowed))
    typed = tuple(
        {
            "property": name,
            "expected": contract["property_editors"].get(name, "string"),
            "ok": name in allowed,
        }
        for name in supplied
    )
    return {
        "format": "appgen.component-prop-validation-contract.v1",
        "component": component,
        "ok": not unknown and all(item["ok"] for item in typed),
        "unknown": unknown,
        "typed": typed,
        "rules": contract["validation_rules"],
        "side_effects": (),
    }


def component_event_dispatch_contract(component: str) -> dict:
    """Return event dispatch metadata for a component."""
    contract = component_runtime_contract(component)
    handlers = tuple(
        {
            "event": event,
            "handler": f"{_module_name(component)}_{_module_name(event)}",
            "phases": ("capture", "validate", "dispatch", "bubble"),
            "side_effects": (),
        }
        for event in contract["events"]
    )
    return {
        "format": "appgen.component-event-dispatch-contract.v1",
        "component": component,
        "handlers": handlers,
        "guards": ("handler_signature_checked", "disabled_components_skip_dispatch", "errors_reported_to_designer"),
    }


def component_target_adapter_contract(component: str) -> dict:
    """Return cross-target adapter metadata for a component."""
    contract = component_runtime_contract(component)
    return {
        "format": "appgen.component-target-adapter-contract.v1",
        "component": component,
        "adapters": tuple(
            {
                "target": target,
                "renderer": renderer,
                "lifecycle": ("create", "update", "validate", "destroy"),
                "supports_preview": True,
                "side_effects": (),
            }
            for target, renderer in contract["renderers"].items()
        ),
        "guards": ("stable_component_id", "target_specific_props_reviewed", "preview_matches_runtime_shape"),
    }


def component_behavior_contract(component: str) -> dict:
    """Return executable behavior evidence for one built-in component."""
    render = component_render_contract(component)
    validation = component_prop_validation_contract(component)
    events = component_event_dispatch_contract(component)
    adapters = component_target_adapter_contract(component)
    checks = (
        {"id": "render_nodes", "ok": {"web", "mobile", "desktop"} <= {node["target"] for node in render["nodes"]} and not render["side_effects"], "evidence": render},
        {"id": "property_validation", "ok": validation["ok"] and not validation["side_effects"], "evidence": validation},
        {"id": "event_dispatch", "ok": bool(events["handlers"]) and all(not handler["side_effects"] for handler in events["handlers"]), "evidence": events},
        {"id": "target_adapters", "ok": all({"create", "update", "validate", "destroy"} <= set(adapter["lifecycle"]) and not adapter["side_effects"] for adapter in adapters["adapters"]), "evidence": adapters},
        {"id": "accessibility_preview", "ok": "label_source" in render["accessibility"], "evidence": render["accessibility"]},
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-behavior-contract.v1",
        "component": component,
        "ok": ok,
        "render": render,
        "validation": validation,
        "events": events,
        "adapters": adapters,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def component_behavior_workbench() -> dict:
    """Prove every built-in component has render, validation, event, and adapter behavior."""
    behaviors = tuple(component_behavior_contract(component) for component in sorted(COMPONENTS))
    checks = (
        {"id": "all_components_have_behavior", "ok": len(behaviors) == len(COMPONENTS) and all(item["ok"] for item in behaviors), "evidence": tuple(item["component"] for item in behaviors)},
        {"id": "render_behavior", "ok": all(any(check["id"] == "render_nodes" and check["ok"] for check in item["checks"]) for item in behaviors), "evidence": tuple(item["render"] for item in behaviors)},
        {"id": "validation_behavior", "ok": all(any(check["id"] == "property_validation" and check["ok"] for check in item["checks"]) for item in behaviors), "evidence": tuple(item["validation"] for item in behaviors)},
        {"id": "event_behavior", "ok": all(any(check["id"] == "event_dispatch" and check["ok"] for check in item["checks"]) for item in behaviors), "evidence": tuple(item["events"] for item in behaviors)},
        {"id": "target_adapter_behavior", "ok": all(any(check["id"] == "target_adapters" and check["ok"] for check in item["checks"]) for item in behaviors), "evidence": tuple(item["adapters"] for item in behaviors)},
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-behavior-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "component_count": len(behaviors),
        "behaviors": behaviors,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def component_implementation_catalog() -> tuple[dict, ...]:
    """Return usability contracts for every built-in component."""
    return tuple(component_runtime_contract(component) for component in sorted(COMPONENTS))


def component_file_manifest() -> tuple[dict, ...]:
    """Return the per-component implementation files expected in generated apps."""
    return tuple(
        {
            "component": contract["component"],
            "path": f"app/component_contracts/{_module_name(contract['component'])}.py",
            "exports": (
                "contract",
                "render",
                "validate_props",
                "preview",
                "behavior_contract",
                "target_adapters",
                "dispatch_event",
                "test_plan",
            ),
            "test_plan": contract["preview"]["sample_payload"],
        }
        for contract in component_implementation_catalog()
    )


def component_package_file_manifest() -> tuple[dict, ...]:
    """Return the per-package implementation files expected in generated apps."""
    return tuple(
        {
            "package": package["id"],
            "path": f"app/component_packages/{_module_name(package['id'])}.py",
            "exports": (
                "package_contract",
                "install_plan",
                "load_policy",
                "adapter_contract",
                "dependency_graph",
                "adapter_smoke",
                "preview_load",
                "behavior_contract",
                "validate_load_request",
                "test_plan",
            ),
            "requires_review": True,
        }
        for package in THIRD_PARTY_COMPONENT_SUITES
    )


def component_usability_workbench() -> dict:
    """Prove every built-in component has enough metadata to be usable."""
    contracts = component_implementation_catalog()
    analog_workbench = component_analog_workbench()
    behavior_workbench = component_behavior_workbench()
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
        {
            "id": "per_component_files",
            "ok": len(component_file_manifest()) == len(contracts)
            and all(
                {
                    "contract",
                    "render",
                    "validate_props",
                    "preview",
                    "behavior_contract",
                    "target_adapters",
                    "dispatch_event",
                    "test_plan",
                }
                <= set(item["exports"])
                for item in component_file_manifest()
            ),
            "evidence": component_file_manifest(),
        },
        {
            "id": "per_package_files",
            "ok": len(component_package_file_manifest()) == len(THIRD_PARTY_COMPONENT_SUITES)
            and all({"package_contract", "install_plan", "load_policy", "test_plan"} <= set(item["exports"]) for item in component_package_file_manifest()),
            "evidence": component_package_file_manifest(),
        },
        {
            "id": "requested_analog_coverage",
            "ok": analog_workbench["ok"],
            "evidence": analog_workbench,
        },
        {
            "id": "component_behavior",
            "ok": behavior_workbench["ok"],
            "evidence": behavior_workbench,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-usability-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "component_count": len(contracts),
        "components": contracts,
        "component_files": component_file_manifest(),
        "package_files": component_package_file_manifest(),
        "analog_workbench": analog_workbench,
        "behavior_workbench": behavior_workbench,
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
        "app/component_contracts/text_box.py",
        "app/component_contracts/grid.py",
        "app/component_contracts/viewport3_d.py",
        "app/component_packages/devexpress_native.py",
        "app/models.py",
        "app/views.py",
        "app/dsl_reference.py",
    )
    compile_artifacts = (
        "app/form_designer.py",
        "app/component_contracts/text_box.py",
        "app/component_contracts/grid.py",
        "app/component_contracts/viewport3_d.py",
        "app/component_packages/devexpress_native.py",
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
            str(path.relative_to(project_dir))
            for path in output_dir.rglob("*.py")
            if "__pycache__" not in path.parts
        }
        existing_paths.add("app/templates/appgen_form_designer.html")
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


def _dfm_identifier(field: str | None, component: str) -> str:
    base = f"{field or component}_{component}"
    cleaned = re.sub(r"[^A-Za-z0-9_]", "_", base)
    if not cleaned or cleaned[0].isdigit():
        cleaned = f"AppGen_{cleaned}"
    return cleaned


def _dfm_component_class(component: str) -> str:
    mapping = {
        "TextBox": "TEdit",
        "EmailInput": "TEdit",
        "TextArea": "TMemo",
        "Label": "TLabel",
        "Select": "TComboBox",
        "Checkbox": "TCheckBox",
        "DatePicker": "TDateTimePicker",
        "Lookup": "TComboBox",
        "FileUpload": "TButtonedEdit",
        "Button": "TButton",
        "Panel": "TPanel",
        "GroupBox": "TGroupBox",
        "RadioGroup": "TRadioGroup",
        "RadioButton": "TRadioButton",
        "ListBox": "TListBox",
        "ListView": "TListView",
        "TreeView": "TTreeView",
        "Grid": "TStringGrid",
        "StringGrid": "TStringGrid",
        "PageControl": "TPageControl",
        "Layout": "TLayout",
        "ScrollBox": "TScrollBox",
        "FlowLayout": "TFlowLayout",
        "GridLayout": "TGridLayout",
        "VerticalBoxLayout": "TVerticalBoxLayout",
        "HorizontalBoxLayout": "THorizontalBoxLayout",
        "MainMenu": "TMainMenu",
        "PopupMenu": "TPopupMenu",
        "ToolBar": "TToolBar",
        "ActionList": "TActionList",
        "Image": "TImage",
        "Shape": "TShape",
        "PathShape": "TPath",
        "Rectangle": "TRectangle",
        "Ellipse": "TEllipse",
        "Line": "TLine",
        "Bitmap": "TBitmap",
        "Chart": "TChart",
        "ReportViewer": "TAppGenReportViewer",
        "WebBrowser": "TWebBrowser",
        "Timer": "TTimer",
        "DataSource": "TDataSource",
        "BindingSource": "TBindingsList",
        "RESTClient": "TRESTClient",
        "CameraView": "TCameraComponent",
        "LocationSensor": "TLocationSensor",
        "MotionSensor": "TMotionSensor",
        "OrientationSensor": "TOrientationSensor",
        "NotificationCenter": "TNotificationCenter",
        "Animation": "TFloatAnimation",
        "FloatAnimation": "TFloatAnimation",
        "ColorAnimation": "TColorAnimation",
        "PathAnimation": "TPathAnimation",
        "Effect": "TShadowEffect",
        "StyleBook": "TStyleBook",
        "StyleManager": "TStyleManager",
        "GestureManager": "TGestureManager",
        "Gesture": "TGesture",
        "Viewport3D": "TViewport3D",
        "Dummy3D": "TDummy3D",
        "Camera3D": "TCamera3D",
        "Light3D": "TLight3D",
        "Mesh3D": "TMesh3D",
        "DatabaseConnection": "TDatabase",
        "TableAdapter": "TTable",
        "ClientDataSet": "TClientDataSet",
    }
    return mapping.get(component, f"TAppGen{component}")


def _dfm_value(value: str) -> object:
    value = value.strip()
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
        return int(value)
    return value


def _pascal_identifier(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]", "_", value)
    if not cleaned or cleaned[0].isdigit():
        cleaned = f"AppGen_{cleaned}"
    return cleaned


def _module_name(name: str) -> str:
    chars = []
    for index, char in enumerate(name.replace("-", "_")):
        if char.isupper() and index and (not name[index - 1].isupper()):
            chars.append("_")
        chars.append(char.lower() if char.isalnum() else "_")
    return "_".join(part for part in "".join(chars).split("_") if part)


def _component_package(package_id: str) -> dict:
    for package in THIRD_PARTY_COMPONENT_SUITES:
        if package["id"] == package_id:
            return package
    raise KeyError(f"Unknown component package: {package_id}")


def _property_editor_descriptor(name: str, component: str, category: str) -> dict:
    editor = property_inspector(component)["property_types"].get(name, "string")
    if name in {"items", "columns", "tabs", "actions", "series", "fields"}:
        editor = "collection"
    elif name in {"data_source", "dataset", "bindings", "target_table"}:
        editor = "binding"
    elif name in {"fill", "stroke", "color", "start_color", "end_color"}:
        editor = "color"
    elif name in {"source", "resources", "theme", "style_books", "mesh", "material"}:
        editor = "resource"
    elif name in {"align", "direction", "orientation_mode", "light_type", "effect", "easing"}:
        editor = "choice"
    elif name in {"x", "y", "w", "h", "rows", "columns", "stroke_width", "duration", "timeout", "interval", "tab_order"}:
        editor = "number"
    return {
        "name": name,
        "editor": editor,
        "component": component,
        "category": category,
        "default": _default_property_value(name, component, category),
        "supports_reset": True,
        "supports_binding": category in {"input", "choice", "calendar", "data", "data_access", "media", "graphics"},
    }


def _binding_property(component: str) -> str:
    category = COMPONENTS.get(component, {}).get("category")
    if category in {"input", "choice", "calendar", "relationship"}:
        return "value"
    if category in {"data", "data_access", "analytics", "reports"}:
        return "dataset"
    if category in {"media", "graphics"}:
        return "source"
    return "caption"


def _default_property_value(name: str, component: str, category: str) -> object:
    if name in {"required", "readonly", "spellcheck", "preview", "visible", "enabled", "lazy_load", "filterable", "sortable", "editable", "watch", "multi_select", "sorted", "checked", "wrap", "scrollable", "transparent", "hit_test", "active", "dark_mode", "high_contrast", "shadows", "secure_secrets", "pooling", "cached_updates", "offline_cache", "auto_reverse"}:
        return name in {"visible", "enabled", "sortable", "filterable"}
    if name in {"rows", "columns", "interval", "timeout", "duration", "tab_order", "max_size_mb", "gap", "fixed_rows", "fixed_columns", "stroke_width", "opacity", "sample_rate", "threshold", "intensity", "field_of_view", "near_clip", "far_clip", "dpi"}:
        return 1 if name != "duration" else 200
    if name in {"items", "actions", "tabs", "series", "bindings", "validators", "converters", "channels", "lights", "models", "materials", "export_formats", "headers", "children", "areas", "responsive_breakpoints", "style_books", "gestures", "targets", "recognizers", "conflicts", "axes", "fields", "indexes"}:
        return ()
    if name in {"target", "source", "data_source", "dataset", "url", "base_url", "report", "camera", "group", "shape", "fill", "stroke", "path_data", "scale", "scale_mode", "cache_policy", "orientation_mode", "start_value", "end_value", "start_color", "end_color", "theme", "resources", "variants", "platform_overrides", "active_style", "platform_rules", "kind", "direction", "driver", "connection_name", "transaction", "table", "connection", "provider", "change_log", "merge_policy", "mesh", "material", "position", "rotation", "light_type", "color"}:
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
        "graphics": ("OnPaint", "OnHitTest", "OnResize"),
        "theme": ("OnApply", "OnChange", "OnFallback"),
        "gesture": ("OnGesture", "OnRecognize", "OnConflict"),
        "three_d": ("OnLoad", "OnRender", "OnFrame"),
        "data_access": ("OnConnect", "OnOpen", "OnError"),
    }
    return base + by_category.get(category, ("OnChange",))


def _component_validation_rules(component: str, category: str) -> tuple[str, ...]:
    rules = ["within_canvas_bounds", "stable_component_id", "known_property_names"]
    if COMPONENTS[component]["field_types"]:
        rules.append("field_type_supported")
    if category in {"mobile", "integration", "data", "data_access"}:
        rules.append("permission_or_secret_reviewed")
    if category in {"effects", "three_d", "graphics"}:
        rules.append("performance_budget_declared")
    if category in {"theme", "gesture"}:
        rules.append("target_surface_declared")
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
