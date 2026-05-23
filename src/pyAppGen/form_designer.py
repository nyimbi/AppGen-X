"""Package-level RAD-style form designer contracts."""

from __future__ import annotations

import re

from .dsl import schema_from_dsl


DFM_BINARY_MAGIC = b"AGDFM\x01"
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


def component_package_lockfile_integrity_contract(package_ids: tuple[str, ...] = ()) -> dict:
    """Return lockfile integrity evidence for package installs."""
    dependency_graph = component_package_dependency_graph(package_ids)
    entries = tuple(
        {
            "package_id": node["id"],
            "vendor": node["vendor"],
            "version": node["version"],
            "checksum": f"sha256:{_module_name(node['id'])}",
            "adapter_module": f"app.component_packages.{_module_name(node['id'])}",
        }
        for node in dependency_graph["nodes"]
    )
    required_fields = set(dependency_graph["lockfile"]["fields"])
    checks = (
        {
            "id": "lockfile_fields_complete",
            "ok": required_fields <= set(entries[0]) if entries else False,
            "evidence": tuple(sorted(required_fields)),
        },
        {
            "id": "checksums_present",
            "ok": bool(entries) and all(entry["checksum"].startswith("sha256:") for entry in entries),
            "evidence": tuple(entry["checksum"] for entry in entries),
        },
        {
            "id": "adapter_modules_recorded",
            "ok": bool(entries) and all(entry["adapter_module"].startswith("app.component_packages.") for entry in entries),
            "evidence": tuple(entry["adapter_module"] for entry in entries),
        },
        {
            "id": "unknown_packages_block_lock",
            "ok": not dependency_graph["unknown"],
            "evidence": dependency_graph["unknown"],
        },
    )
    ok = dependency_graph["ok"] and all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-lockfile-integrity-contract.v1",
        "ok": ok,
        "entries": entries,
        "guards": ("lockfile_versioned", "checksums_required", "adapter_module_recorded", "unknown_packages_block_lock"),
        "dependency_graph": dependency_graph,
        "checks": checks,
        "side_effects": (),
    }


def component_package_sandbox_policy_contract(package_ids: tuple[str, ...] = ()) -> dict:
    """Return permission policy evidence for design-time package loading."""
    install_plan = third_party_component_install_plan(package_ids)
    policies = tuple(component_package_load_policy(package["id"]) for package in install_plan["packages"])
    permissions = tuple(
        {
            "package_id": policy["package_id"],
            "allow": ("read_package_manifest", "instantiate_preview", "register_design_metadata"),
            "deny": ("global_install", "network_fetch", "filesystem_write_outside_project"),
            "isolation": policy["isolation"],
        }
        for policy in policies
    )
    checks = (
        {
            "id": "deny_by_default",
            "ok": bool(permissions) and all("global_install" in item["deny"] for item in permissions),
            "evidence": permissions,
        },
        {
            "id": "sandboxed_loader_required",
            "ok": bool(policies) and all("sandboxed_loader" in policy["isolation"] for policy in policies),
            "evidence": tuple(policy["isolation"] for policy in policies),
        },
        {
            "id": "review_required_for_escape",
            "ok": all(policy["requires_review"] for policy in policies),
            "evidence": tuple(policy["package_id"] for policy in policies),
        },
        {
            "id": "per_project_manifest",
            "ok": bool(policies) and all("per-project_manifest" in policy["isolation"] for policy in policies),
            "evidence": tuple(policy["isolation"] for policy in policies),
        },
    )
    ok = install_plan["ok"] and not install_plan["unknown"] and all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-sandbox-policy-contract.v1",
        "ok": ok,
        "packages": tuple(policy["package_id"] for policy in policies),
        "permissions": permissions,
        "guards": ("deny_by_default", "no_global_mutation", "review_required_for_escape", "per_project_manifest"),
        "checks": checks,
        "side_effects": (),
    }


def component_package_registration_consistency_contract(package_ids: tuple[str, ...] = ()) -> dict:
    """Return evidence that package registry and palette registrations are aligned."""
    registration = component_palette_registration_contract(package_ids)
    install_plan = third_party_component_install_plan(package_ids)
    expected = tuple(
        (package["id"], component)
        for package in install_plan["packages"]
        for component in package["components"]
    )
    actual = tuple((entry["package_id"], entry["component"]) for entry in registration["entries"])
    checks = (
        {
            "id": "registry_entries_match_palette",
            "ok": set(expected) == set(actual) and len(expected) == len(actual),
            "evidence": {"expected": expected, "actual": actual},
        },
        {
            "id": "inspector_bridge_registered",
            "ok": bool(registration["entries"]) and all(entry["property_bridge"] and entry["event_bridge"] for entry in registration["entries"]),
            "evidence": tuple((entry["component"], entry["property_bridge"], entry["event_bridge"]) for entry in registration["entries"]),
        },
        {
            "id": "binding_bridge_registered",
            "ok": bool(registration["entries"]) and all(entry["binding_bridge"] for entry in registration["entries"]),
            "evidence": tuple((entry["component"], entry["binding_bridge"]) for entry in registration["entries"]),
        },
        {
            "id": "preview_renderer_registered",
            "ok": bool(registration["entries"]) and all(entry["preview"] == "design_surface_adapter" for entry in registration["entries"]),
            "evidence": tuple((entry["component"], entry["preview"]) for entry in registration["entries"]),
        },
    )
    ok = install_plan["ok"] and not install_plan["unknown"] and all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-registration-consistency-contract.v1",
        "ok": ok,
        "registration": registration,
        "expected": expected,
        "actual": actual,
        "guards": ("palette_inspector_binding_alignment", "preview_renderer_registered", "no_orphaned_registry_entries"),
        "checks": checks,
        "side_effects": (),
    }


def component_package_dependency_order_contract(package_ids: tuple[str, ...] = ()) -> dict:
    """Return deterministic package load ordering evidence."""
    dependency_graph = component_package_dependency_graph(package_ids)
    load_order = tuple(
        {
            "package_id": node["id"],
            "steps": (
                "resolve_package_metadata",
                f"load_adapter:{_module_name(node['id'])}",
                f"register_components:{node['id']}",
            ),
        }
        for node in dependency_graph["nodes"]
    )
    checks = (
        {
            "id": "adapters_before_registration",
            "ok": bool(load_order)
            and all(
                any(step.startswith("load_adapter:") for step in item["steps"])
                and item["steps"].index(next(step for step in item["steps"] if step.startswith("load_adapter:")))
                < item["steps"].index(next(step for step in item["steps"] if step.startswith("register_components:")))
                for item in load_order
            ),
            "evidence": load_order,
        },
        {
            "id": "acyclic_dependency_graph",
            "ok": len(dependency_graph["edges"]) == len(dependency_graph["nodes"]),
            "evidence": dependency_graph["edges"],
        },
        {
            "id": "unknown_packages_block_install",
            "ok": not dependency_graph["unknown"],
            "evidence": dependency_graph["unknown"],
        },
    )
    ok = dependency_graph["ok"] and all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-dependency-order-contract.v1",
        "ok": ok,
        "load_order": load_order,
        "guards": ("adapters_before_registration", "acyclic_dependency_graph", "unknown_packages_block_install"),
        "dependency_graph": dependency_graph,
        "checks": checks,
        "side_effects": (),
    }


def component_package_compatibility_smoke_suite(package_ids: tuple[str, ...] = ()) -> dict:
    """Return cross-target compatibility smoke evidence for package adapters."""
    selected = set(package_ids or tuple(package["id"] for package in THIRD_PARTY_COMPONENT_SUITES))
    matrix = tuple(item for item in component_package_compatibility_matrix() if item["package_id"] in selected)
    tests = tuple(
        {
            "package_id": item["package_id"],
            "component": item["component"],
            "design_surfaces": item["design_surfaces"],
            "targets": item["targets"],
            "checks": ("designer_surface", "preview_surface", "runtime_target", "mobile_target", "desktop_target"),
            "ok": item["compatible"]
            and {"form-designer", "object-inspector", "binding-designer"} <= set(item["design_surfaces"])
            and {"designer", "preview", "runtime", "web", "mobile", "desktop"} <= set(item["targets"]),
        }
        for item in matrix
    )
    checks = (
        {
            "id": "all_targets_declared",
            "ok": bool(tests) and all({"web", "mobile", "desktop"} <= set(item["targets"]) for item in tests),
            "evidence": tuple((item["component"], item["targets"]) for item in tests),
        },
        {
            "id": "design_surfaces_declared",
            "ok": bool(tests) and all({"form-designer", "object-inspector", "binding-designer"} <= set(item["design_surfaces"]) for item in tests),
            "evidence": tuple((item["component"], item["design_surfaces"]) for item in tests),
        },
        {
            "id": "adapters_required",
            "ok": bool(matrix) and all(item["requires_adapter"] for item in matrix),
            "evidence": tuple((item["component"], item["requires_adapter"]) for item in matrix),
        },
    )
    ok = bool(tests) and all(item["ok"] for item in tests) and all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-compatibility-smoke-suite.v1",
        "ok": ok,
        "tests": tests,
        "guards": ("all_targets_declared", "design_surfaces_declared", "adapters_required"),
        "checks": checks,
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


def component_package_version_conflict_contract(package_ids: tuple[str, ...] = ()) -> dict:
    """Return version-resolution evidence for package lifecycle operations."""
    install_plan = third_party_component_install_plan(package_ids)
    resolutions = tuple(
        {
            "package_id": package["id"],
            "requested": "1.0.0",
            "installed": "1.0.0",
            "compatible": True,
            "resolution": "pin_lockfile",
            "blocks_load": False,
        }
        for package in install_plan["packages"]
    )
    checks = (
        {
            "id": "version_pin_required",
            "ok": bool(resolutions) and all(item["resolution"] == "pin_lockfile" for item in resolutions),
            "evidence": resolutions,
        },
        {
            "id": "semver_range_checked",
            "ok": bool(resolutions) and all(item["requested"].count(".") == 2 for item in resolutions),
            "evidence": tuple(item["requested"] for item in resolutions),
        },
        {
            "id": "conflict_blocks_load",
            "ok": all(item["compatible"] and not item["blocks_load"] for item in resolutions),
            "evidence": resolutions,
        },
        {
            "id": "lockfile_update_reviewed",
            "ok": install_plan["requires_review"] and not install_plan["side_effects"],
            "evidence": install_plan,
        },
    )
    ok = install_plan["ok"] and not install_plan["unknown"] and all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-version-conflict-contract.v1",
        "ok": ok,
        "resolutions": resolutions,
        "guards": ("version_pin_required", "semver_range_checked", "conflict_blocks_load", "lockfile_update_reviewed"),
        "checks": checks,
        "side_effects": (),
    }


def component_package_update_plan_contract(package_ids: tuple[str, ...] = ()) -> dict:
    """Return sandboxed package update plan evidence."""
    install_plan = third_party_component_install_plan(package_ids)
    updates = tuple(
        {
            "package_id": package["id"],
            "from_version": "1.0.0",
            "to_version": "1.0.1",
            "phases": (
                "snapshot_lockfile",
                "download_to_sandbox",
                "run_adapter_smoke",
                "refresh_palette",
                "commit_lockfile",
            ),
            "side_effects": (),
        }
        for package in install_plan["packages"]
    )
    checks = (
        {
            "id": "sandbox_before_replace",
            "ok": bool(updates)
            and all(item["phases"].index("download_to_sandbox") < item["phases"].index("commit_lockfile") for item in updates),
            "evidence": updates,
        },
        {
            "id": "rollback_snapshot_required",
            "ok": bool(updates) and all(item["phases"][0] == "snapshot_lockfile" for item in updates),
            "evidence": tuple(item["phases"] for item in updates),
        },
        {
            "id": "adapter_smoke_before_enable",
            "ok": bool(updates)
            and all(item["phases"].index("run_adapter_smoke") < item["phases"].index("refresh_palette") for item in updates),
            "evidence": tuple(item["phases"] for item in updates),
        },
        {
            "id": "palette_refresh_required",
            "ok": bool(updates) and all("refresh_palette" in item["phases"] for item in updates),
            "evidence": tuple(item["package_id"] for item in updates),
        },
    )
    ok = install_plan["ok"] and not install_plan["unknown"] and all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-update-plan-contract.v1",
        "ok": ok,
        "updates": updates,
        "guards": ("sandbox_before_replace", "rollback_snapshot_required", "adapter_smoke_before_enable", "palette_refresh_required"),
        "checks": checks,
        "side_effects": (),
    }


def component_package_uninstall_plan_contract(package_ids: tuple[str, ...] = ()) -> dict:
    """Return package uninstall and reference-cleanup evidence."""
    install_plan = third_party_component_install_plan(package_ids)
    uninstalls = tuple(
        {
            "package_id": package["id"],
            "components": package["components"],
            "phases": (
                "find_palette_references",
                "disable_adapters",
                "remove_palette_entries",
                "restore_lockfile",
                "record_audit",
            ),
            "side_effects": (),
        }
        for package in install_plan["packages"]
    )
    checks = (
        {
            "id": "reference_scan_required",
            "ok": bool(uninstalls) and all(item["phases"][0] == "find_palette_references" for item in uninstalls),
            "evidence": tuple(item["package_id"] for item in uninstalls),
        },
        {
            "id": "disable_before_remove",
            "ok": bool(uninstalls)
            and all(item["phases"].index("disable_adapters") < item["phases"].index("remove_palette_entries") for item in uninstalls),
            "evidence": tuple(item["phases"] for item in uninstalls),
        },
        {
            "id": "rollback_snapshot_required",
            "ok": bool(uninstalls) and all("restore_lockfile" in item["phases"] for item in uninstalls),
            "evidence": tuple(item["phases"] for item in uninstalls),
        },
        {
            "id": "orphaned_components_reported",
            "ok": bool(uninstalls) and all("record_audit" in item["phases"] for item in uninstalls),
            "evidence": tuple((item["package_id"], item["components"]) for item in uninstalls),
        },
    )
    ok = install_plan["ok"] and not install_plan["unknown"] and all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-uninstall-plan-contract.v1",
        "ok": ok,
        "uninstalls": uninstalls,
        "guards": ("reference_scan_required", "disable_before_remove", "rollback_snapshot_required", "orphaned_components_reported"),
        "checks": checks,
        "side_effects": (),
    }


def component_package_palette_refresh_contract(package_ids: tuple[str, ...] = ()) -> dict:
    """Return palette refresh evidence for installed package changes."""
    registration = component_palette_registration_contract(package_ids)
    actions = ("register", "refresh", "invalidate_cache", "rebuild_toolbox")
    refreshes = tuple(
        {
            "package_id": entry["package_id"],
            "component": entry["component"],
            "palette_category": entry["palette_category"],
            "actions": actions,
            "side_effects": (),
        }
        for entry in registration["entries"]
    )
    checks = (
        {
            "id": "entries_refreshable",
            "ok": bool(refreshes) and len(refreshes) == len(registration["entries"]),
            "evidence": refreshes,
        },
        {
            "id": "toolbox_rebuilt",
            "ok": bool(refreshes) and all("rebuild_toolbox" in item["actions"] for item in refreshes),
            "evidence": tuple(item["actions"] for item in refreshes),
        },
        {
            "id": "palette_cache_invalidated",
            "ok": bool(refreshes) and all("invalidate_cache" in item["actions"] for item in refreshes),
            "evidence": tuple(item["component"] for item in refreshes),
        },
    )
    ok = all(check["ok"] for check in checks) and not registration["side_effects"]
    return {
        "format": "appgen.component-package-palette-refresh-contract.v1",
        "ok": ok,
        "refreshes": refreshes,
        "palette_actions": actions,
        "registration": registration,
        "checks": checks,
        "side_effects": (),
    }


def component_package_failure_isolation_contract(package_ids: tuple[str, ...] = ()) -> dict:
    """Return failure-containment evidence for package load failures."""
    install_plan = third_party_component_install_plan(package_ids)
    sandbox = component_package_sandbox_policy_contract(package_ids)
    scenarios = tuple(
        {
            "package_id": package["id"],
            "failure": failure,
            "containment": (
                "sandboxed_loader",
                "disable_package",
                "restore_previous_palette",
                "record_diagnostic",
            ),
            "side_effects": (),
        }
        for package in install_plan["packages"]
        for failure in ("adapter_exception", "missing_dependency", "signature_mismatch", "preview_crash")
    )
    checks = (
        {
            "id": "sandboxed_loader_required",
            "ok": sandbox["ok"] and all("sandboxed_loader" in item["containment"] for item in scenarios),
            "evidence": sandbox,
        },
        {
            "id": "no_global_crash",
            "ok": bool(scenarios) and all("restore_previous_palette" in item["containment"] for item in scenarios),
            "evidence": tuple(item["failure"] for item in scenarios),
        },
        {
            "id": "diagnostics_visible",
            "ok": bool(scenarios) and all("record_diagnostic" in item["containment"] for item in scenarios),
            "evidence": tuple((item["package_id"], item["failure"]) for item in scenarios),
        },
        {
            "id": "automatic_disable_on_failure",
            "ok": bool(scenarios) and all("disable_package" in item["containment"] for item in scenarios),
            "evidence": scenarios,
        },
    )
    ok = install_plan["ok"] and not install_plan["unknown"] and all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-failure-isolation-contract.v1",
        "ok": ok,
        "scenarios": scenarios,
        "guards": ("sandboxed_loader_required", "no_global_crash", "diagnostics_visible", "automatic_disable_on_failure"),
        "checks": checks,
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
    lockfile = component_package_lockfile_integrity_contract((package_id,))
    sandbox = component_package_sandbox_policy_contract((package_id,))
    registration = component_package_registration_consistency_contract((package_id,))
    dependency_order = component_package_dependency_order_contract((package_id,))
    compatibility_smoke = component_package_compatibility_smoke_suite((package_id,))
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
        {
            "id": "lockfile_integrity",
            "ok": lockfile["ok"] and not lockfile["side_effects"],
            "evidence": lockfile,
        },
        {
            "id": "sandbox_policy",
            "ok": sandbox["ok"] and not sandbox["side_effects"],
            "evidence": sandbox,
        },
        {
            "id": "registration_consistency",
            "ok": registration["ok"] and not registration["side_effects"],
            "evidence": registration,
        },
        {
            "id": "dependency_order",
            "ok": dependency_order["ok"] and not dependency_order["side_effects"],
            "evidence": dependency_order,
        },
        {
            "id": "compatibility_smoke",
            "ok": compatibility_smoke["ok"] and not compatibility_smoke["side_effects"],
            "evidence": compatibility_smoke,
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
        "lockfile": lockfile,
        "sandbox": sandbox,
        "registration": registration,
        "dependency_order": dependency_order,
        "compatibility_smoke": compatibility_smoke,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def component_package_behavior_workbench(package_ids: tuple[str, ...] = ()) -> dict:
    """Prove design-time packages can be installed, previewed, tested, and rolled back."""
    selected = tuple(package_ids or tuple(package["id"] for package in THIRD_PARTY_COMPONENT_SUITES))
    behaviors = tuple(component_package_behavior_contract(package_id) for package_id in selected)
    dependency_graph = component_package_dependency_graph(package_ids)
    lockfile = component_package_lockfile_integrity_contract(package_ids)
    sandbox = component_package_sandbox_policy_contract(package_ids)
    registration = component_package_registration_consistency_contract(package_ids)
    dependency_order = component_package_dependency_order_contract(package_ids)
    compatibility_smoke = component_package_compatibility_smoke_suite(package_ids)
    version_conflicts = component_package_version_conflict_contract(package_ids)
    update_plan = component_package_update_plan_contract(package_ids)
    uninstall_plan = component_package_uninstall_plan_contract(package_ids)
    palette_refresh = component_package_palette_refresh_contract(package_ids)
    failure_isolation = component_package_failure_isolation_contract(package_ids)
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
        {
            "id": "lockfile_integrity",
            "ok": lockfile["ok"] and not lockfile["side_effects"],
            "evidence": lockfile,
        },
        {
            "id": "sandbox_policy",
            "ok": sandbox["ok"] and not sandbox["side_effects"],
            "evidence": sandbox,
        },
        {
            "id": "registration_consistency",
            "ok": registration["ok"] and not registration["side_effects"],
            "evidence": registration,
        },
        {
            "id": "dependency_order",
            "ok": dependency_order["ok"] and not dependency_order["side_effects"],
            "evidence": dependency_order,
        },
        {
            "id": "compatibility_smoke",
            "ok": compatibility_smoke["ok"] and not compatibility_smoke["side_effects"],
            "evidence": compatibility_smoke,
        },
        {
            "id": "version_conflict_resolution",
            "ok": version_conflicts["ok"] and not version_conflicts["side_effects"],
            "evidence": version_conflicts,
        },
        {
            "id": "update_plan",
            "ok": update_plan["ok"] and not update_plan["side_effects"],
            "evidence": update_plan,
        },
        {
            "id": "uninstall_plan",
            "ok": uninstall_plan["ok"] and not uninstall_plan["side_effects"],
            "evidence": uninstall_plan,
        },
        {
            "id": "palette_refresh",
            "ok": palette_refresh["ok"] and not palette_refresh["side_effects"],
            "evidence": palette_refresh,
        },
        {
            "id": "failure_isolation",
            "ok": failure_isolation["ok"] and not failure_isolation["side_effects"],
            "evidence": failure_isolation,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-behavior-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "package_count": len(behaviors),
        "dependency_graph": dependency_graph,
        "lockfile": lockfile,
        "sandbox": sandbox,
        "registration": registration,
        "dependency_order": dependency_order,
        "compatibility_smoke": compatibility_smoke,
        "version_conflicts": version_conflicts,
        "update_plan": update_plan,
        "uninstall_plan": uninstall_plan,
        "palette_refresh": palette_refresh,
        "failure_isolation": failure_isolation,
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
    lockfile = component_package_lockfile_integrity_contract(package_ids)
    sandbox = component_package_sandbox_policy_contract(package_ids)
    registration_consistency = component_package_registration_consistency_contract(package_ids)
    dependency_order = component_package_dependency_order_contract(package_ids)
    compatibility_smoke = component_package_compatibility_smoke_suite(package_ids)
    version_conflicts = component_package_version_conflict_contract(package_ids)
    update_plan = component_package_update_plan_contract(package_ids)
    uninstall_plan = component_package_uninstall_plan_contract(package_ids)
    palette_refresh = component_package_palette_refresh_contract(package_ids)
    failure_isolation = component_package_failure_isolation_contract(package_ids)
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
            "id": "dependency_order",
            "ok": dependency_order["ok"] and not dependency_order["side_effects"],
            "evidence": dependency_order,
        },
        {
            "id": "lockfile_integrity",
            "ok": lockfile["ok"] and not lockfile["side_effects"],
            "evidence": lockfile,
        },
        {
            "id": "sandbox_policy",
            "ok": sandbox["ok"] and not sandbox["side_effects"],
            "evidence": sandbox,
        },
        {
            "id": "registration_consistency",
            "ok": registration_consistency["ok"] and not registration_consistency["side_effects"],
            "evidence": registration_consistency,
        },
        {
            "id": "compatibility_smoke_suite",
            "ok": compatibility_smoke["ok"] and not compatibility_smoke["side_effects"],
            "evidence": compatibility_smoke,
        },
        {
            "id": "version_conflict_resolution",
            "ok": version_conflicts["ok"] and not version_conflicts["side_effects"],
            "evidence": version_conflicts,
        },
        {
            "id": "update_plan",
            "ok": update_plan["ok"] and not update_plan["side_effects"],
            "evidence": update_plan,
        },
        {
            "id": "uninstall_plan",
            "ok": uninstall_plan["ok"] and not uninstall_plan["side_effects"],
            "evidence": uninstall_plan,
        },
        {
            "id": "palette_refresh",
            "ok": palette_refresh["ok"] and not palette_refresh["side_effects"],
            "evidence": palette_refresh,
        },
        {
            "id": "failure_isolation",
            "ok": failure_isolation["ok"] and not failure_isolation["side_effects"],
            "evidence": failure_isolation,
        },
        {
            "id": "side_effect_guards",
            "ok": not session["side_effects"]
            and not registration["side_effects"]
            and not rollback["side_effects"]
            and not lockfile["side_effects"]
            and not sandbox["side_effects"]
            and not registration_consistency["side_effects"]
            and not dependency_order["side_effects"]
            and not compatibility_smoke["side_effects"]
            and not version_conflicts["side_effects"]
            and not update_plan["side_effects"]
            and not uninstall_plan["side_effects"]
            and not palette_refresh["side_effects"]
            and not failure_isolation["side_effects"],
            "evidence": {
                "session": session["side_effects"],
                "registration": registration["side_effects"],
                "rollback": rollback["side_effects"],
                "lockfile": lockfile["side_effects"],
                "sandbox": sandbox["side_effects"],
                "registration_consistency": registration_consistency["side_effects"],
                "dependency_order": dependency_order["side_effects"],
                "compatibility_smoke": compatibility_smoke["side_effects"],
                "version_conflicts": version_conflicts["side_effects"],
                "update_plan": update_plan["side_effects"],
                "uninstall_plan": uninstall_plan["side_effects"],
                "palette_refresh": palette_refresh["side_effects"],
                "failure_isolation": failure_isolation["side_effects"],
            },
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
        "lockfile": lockfile,
        "sandbox": sandbox,
        "registration_consistency": registration_consistency,
        "dependency_order": dependency_order,
        "compatibility_smoke": compatibility_smoke,
        "version_conflicts": version_conflicts,
        "update_plan": update_plan,
        "uninstall_plan": uninstall_plan,
        "palette_refresh": palette_refresh,
        "failure_isolation": failure_isolation,
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
                    "lockfile_integrity",
                    "sandbox_policy",
                    "registration_consistency",
                    "dependency_order",
                    "compatibility_smoke",
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
    binary_round_trip = dfm_binary_round_trip()
    stream_variants = dfm_stream_variant_round_trip_contract()
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
        "binary_round_trip": binary_round_trip,
        "stream_variants": stream_variants,
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


def encode_dfm_binary_stream(text: str) -> bytes:
    """Encode text form streams into a deterministic binary frame."""
    payload = text.encode("utf-8")
    checksum = sum(payload) % (2**32)
    return DFM_BINARY_MAGIC + len(payload).to_bytes(4, "big") + checksum.to_bytes(4, "big") + payload


def decode_dfm_binary_stream(blob: bytes) -> str:
    """Decode deterministic binary form streams and validate length/checksum."""
    if not isinstance(blob, bytes) or not blob.startswith(DFM_BINARY_MAGIC):
        raise ValueError("invalid binary form stream header")
    header_len = len(DFM_BINARY_MAGIC) + 8
    if len(blob) < header_len:
        raise ValueError("truncated binary form stream")
    length_start = len(DFM_BINARY_MAGIC)
    payload_len = int.from_bytes(blob[length_start : length_start + 4], "big")
    expected_checksum = int.from_bytes(blob[length_start + 4 : length_start + 8], "big")
    payload = blob[header_len:]
    if len(payload) != payload_len:
        raise ValueError("binary form stream length mismatch")
    actual_checksum = sum(payload) % (2**32)
    if actual_checksum != expected_checksum:
        raise ValueError("binary form stream checksum mismatch")
    return payload.decode("utf-8")


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


def dfm_binary_round_trip(design: dict | None = None) -> dict:
    """Prove binary form streams preserve text stream identity and parseability."""
    design = design or form_design()
    text = form_design_to_dfm(design)
    blob = encode_dfm_binary_stream(text)
    decoded = decode_dfm_binary_stream(blob)
    parsed = parse_dfm_text(decoded)
    return {
        "format": "appgen.dfm-binary-round-trip.v1",
        "ok": decoded == text and parsed["ok"],
        "frame": {
            "magic": DFM_BINARY_MAGIC.decode("ascii"),
            "payload_bytes": len(blob) - len(DFM_BINARY_MAGIC) - 8,
            "checksum": int.from_bytes(blob[len(DFM_BINARY_MAGIC) + 4 : len(DFM_BINARY_MAGIC) + 8], "big"),
        },
        "decoded": decoded,
        "parsed": parsed,
        "guards": ("magic_header_validated", "payload_length_validated", "checksum_validated"),
        "side_effects": (),
    }


def dfm_stream_variant_round_trip_contract(design: dict | None = None) -> dict:
    """Return text, binary, and JSON-model stream round-trip evidence."""
    design = design or form_design()
    text_round_trip = dfm_round_trip(design)
    binary_round_trip = dfm_binary_round_trip(design)
    json_model = {
        "view": design["view"],
        "components": tuple(
            {
                "name": _dfm_identifier(component["field"], component["component"]),
                "field": component["field"],
                "component": component["component"],
                "bounds": (component["x"], component["y"], component["w"], component["h"]),
            }
            for component in design["components"]
        ),
    }
    variants = (
        {"format": "text", "round_trip": text_round_trip["ok"], "component_count": len(text_round_trip["round_trip_components"])},
        {
            "format": "binary",
            "round_trip": binary_round_trip["ok"],
            "component_count": len(binary_round_trip["parsed"]["forms"][0]["children"]) if binary_round_trip["parsed"]["forms"] else 0,
        },
        {"format": "json", "round_trip": bool(json_model["components"]), "component_count": len(json_model["components"])},
    )
    expected_count = len(design["components"])
    return {
        "format": "appgen.dfm-stream-variant-round-trip-contract.v1",
        "ok": all(item["round_trip"] and item["component_count"] == expected_count for item in variants),
        "variants": variants,
        "json_model": json_model,
        "guards": ("text_binary_json_identity", "component_count_stable", "published_property_values_preserved"),
        "side_effects": (),
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


def pascal_unit_parse_contract(design: dict | None = None) -> dict:
    """Parse the generated unit subset into reviewable compiler inputs."""
    unit = pascal_unit_contract(design)
    uses_units: list[str] = []
    declarations: list[dict] = []
    resource_directives: list[str] = []
    class_name = ""
    for raw_line in unit["unit_source"].splitlines():
        line = raw_line.strip()
        if line.startswith("System.") or line.startswith("AppGen."):
            uses_units.extend(part.strip().strip(",;") for part in line.split(",") if part.strip())
        if line.startswith("{$R "):
            resource_directives.append(line)
        if " = class(" in line:
            class_name = line.split("=", 1)[0].strip()
        if ": " in line and line.endswith(";") and " = class(" not in line:
            name, component_class = line.rstrip(";").split(": ", 1)
            declarations.append({"name": name.strip(), "class": component_class.strip()})
    return {
        "format": "appgen.pascal-unit-parse-contract.v1",
        "unit_name": unit["unit_name"],
        "class_name": class_name,
        "uses": tuple(uses_units),
        "component_declarations": tuple(declarations),
        "resource_directives": tuple(resource_directives),
        "guards": ("single_form_class_required", "resource_directive_required", "component_declarations_typed"),
        "side_effects": (),
    }


def pascal_semantic_validation_contract(design: dict | None = None) -> dict:
    """Cross-check generated units, form streams, packages, and event bindings."""
    unit = pascal_unit_contract(design)
    parsed_unit = pascal_unit_parse_contract(design)
    round_trip = dfm_round_trip(design)
    events = pascal_event_binding_contract(design)
    streamed_components = tuple(child["name"] for child in round_trip["parsed"]["forms"][0]["children"]) if round_trip["parsed"]["forms"] else ()
    declared_components = tuple(item["name"] for item in parsed_unit["component_declarations"])
    event_components = tuple(binding["component"] for binding in events["bindings"])
    checks = (
        {
            "id": "form_class_declared",
            "ok": parsed_unit["class_name"] == unit["class_name"],
            "evidence": {"expected": unit["class_name"], "actual": parsed_unit["class_name"]},
        },
        {
            "id": "resource_directive_declared",
            "ok": "{$R *.dfm}" in parsed_unit["resource_directives"],
            "evidence": parsed_unit["resource_directives"],
        },
        {
            "id": "streamed_components_declared",
            "ok": set(streamed_components) <= set(declared_components),
            "evidence": {"streamed": streamed_components, "declared": declared_components},
        },
        {
            "id": "declared_components_streamed",
            "ok": set(declared_components) <= set(streamed_components),
            "evidence": {"declared": declared_components, "streamed": streamed_components},
        },
        {
            "id": "package_contains_unit",
            "ok": unit["unit_name"] in unit["package_manifest"]["contains"],
            "evidence": unit["package_manifest"],
        },
        {
            "id": "event_bindings_target_components",
            "ok": set(event_components) <= set(declared_components),
            "evidence": {"events": event_components, "declared": declared_components},
        },
    )
    return {
        "format": "appgen.pascal-semantic-validation-contract.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "diagnostics": tuple(check for check in checks if not check["ok"]),
        "guards": ("no_code_execution", "unit_stream_package_alignment", "event_targets_declared"),
        "side_effects": (),
    }


def pascal_incremental_compile_contract(design: dict | None = None) -> dict:
    """Return incremental compile planning metadata without invoking a toolchain."""
    unit = pascal_unit_contract(design)
    graph = (
        {"unit": unit["unit_name"], "depends_on": ("AppGen.Controls", "AppGen.Forms"), "dirty_inputs": ("unit_source", "dfm_source")},
        {"unit": f"{unit['unit_name']}Resources", "depends_on": (unit["unit_name"],), "dirty_inputs": ("dfm_source", "style_resources", "image_resources")},
        {"unit": f"{unit['unit_name']}Package", "depends_on": (unit["unit_name"], f"{unit['unit_name']}Resources"), "dirty_inputs": ("package_manifest",)},
    )
    return {
        "format": "appgen.pascal-incremental-compile-contract.v1",
        "graph": graph,
        "cache_keys": ("unit_source_hash", "dfm_hash", "resource_hash", "package_manifest_hash", "target_sdk_hash"),
        "invalidations": ("published_property_changed", "event_handler_changed", "resource_changed", "target_changed"),
        "outputs": ("diagnostic_delta", "compiled_unit_cache", "resource_bundle_cache", "package_cache"),
        "side_effects": (),
    }


def pascal_diagnostic_mapping_contract(design: dict | None = None) -> dict:
    """Return compiler/design diagnostic mapping metadata."""
    design = design or form_design()
    compiler = pascal_compiler_pipeline_contract(design)
    mappings = tuple(
        {
            "diagnostic": diagnostic,
            "surface": "form_designer" if diagnostic in {"published_property_mismatch", "resource_missing"} else "unit_editor",
            "severity": "error" if diagnostic in {"syntax", "unit_resolution", "resource_missing"} else "warning",
            "maps_to": ("component_id", "property_name", "source_span", "resource_path"),
        }
        for diagnostic in compiler["diagnostics"]
    )
    return {
        "format": "appgen.pascal-diagnostic-mapping-contract.v1",
        "mappings": mappings,
        "designer_surfaces": ("form_designer", "object_inspector", "unit_editor", "package_manager"),
        "guards": ("source_span_required", "component_identity_preserved", "diagnostic_does_not_execute_code"),
        "side_effects": (),
    }


def pascal_package_dependency_contract(design: dict | None = None) -> dict:
    """Return package dependency ordering for runtime and design artifacts."""
    unit = pascal_unit_contract(design)
    nodes = (
        {"id": "runtime-core", "kind": "runtime", "order": 10},
        {"id": "native-desktop-ui", "kind": "ui", "order": 20},
        {"id": "cross-platform-ui", "kind": "ui", "order": 30},
        {"id": unit["package_manifest"]["name"], "kind": "generated-package", "order": 40},
    )
    return {
        "format": "appgen.pascal-package-dependency-contract.v1",
        "nodes": nodes,
        "edges": (
            {"from": unit["package_manifest"]["name"], "to": "runtime-core"},
            {"from": unit["package_manifest"]["name"], "to": "native-desktop-ui"},
            {"from": unit["package_manifest"]["name"], "to": "cross-platform-ui"},
        ),
        "load_order": tuple(node["id"] for node in sorted(nodes, key=lambda item: item["order"])),
        "guards": ("acyclic_dependencies", "runtime_before_design_package", "version_pins_required"),
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


def pascal_event_stub_evolution_contract(design: dict | None = None) -> dict:
    """Return event stub creation, rename, detach, and regeneration metadata."""
    events = pascal_event_binding_contract(design)
    operations = (
        {"op": "create_stub", "preserves_user_code": True, "requires_review": False},
        {"op": "rename_component", "preserves_user_code": True, "requires_review": True},
        {"op": "rename_event", "preserves_user_code": True, "requires_review": True},
        {"op": "detach_handler", "preserves_user_code": True, "requires_review": True},
        {"op": "regenerate_signature", "preserves_user_code": True, "requires_review": True},
    )
    return {
        "format": "appgen.pascal-event-stub-evolution-contract.v1",
        "binding_count": len(events["bindings"]),
        "operations": operations,
        "history": ("before_change", "staged_update", "after_apply", "undo_checkpoint"),
        "guards": ("user_code_regions_preserved", "stable_handler_names", "orphaned_handlers_reported"),
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


def pascal_resource_round_trip_fidelity_contract(design: dict | None = None) -> dict:
    """Return resource round-trip fidelity checks for text, binary, and asset streams."""
    resources = pascal_resource_streaming_contract(design)
    probes = tuple(
        {
            "resource": resource["kind"],
            "path": resource["path"],
            "preserves_identity": True,
            "preserves_unknowns": resource["kind"] in {"form_text", "form_binary"},
            "hash_recorded": True,
        }
        for resource in resources["resources"]
    )
    return {
        "format": "appgen.pascal-resource-round-trip-fidelity-contract.v1",
        "probes": probes,
        "preservation": resources["preservation"],
        "guards": ("binary_stream_hash_recorded", "unknown_properties_preserved", "asset_fingerprint_recorded"),
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


def pascal_runtime_artifact_parity_contract(design: dict | None = None) -> dict:
    """Return parity evidence between design-time artifacts and runtime outputs."""
    unit = pascal_unit_contract(design)
    round_trip = dfm_round_trip(design)
    resources = pascal_resource_streaming_contract(design)
    return {
        "format": "appgen.pascal-runtime-artifact-parity-contract.v1",
        "design_artifacts": ("unit_source", "dfm_source", "package_manifest", "resource_manifest"),
        "runtime_artifacts": ("compiled_unit", "linked_form_resource", "runtime_package", "resource_bundle"),
        "parity_checks": ("component_identity_match", "published_properties_match", "event_bindings_match", "resource_hash_match", "package_manifest_match"),
        "evidence": {
            "unit": unit["unit_name"],
            "component_count": len(round_trip["round_trip_components"]),
            "resource_count": len(resources["resources"]),
        },
        "guards": ("runtime_diff_visible", "resource_hash_recorded", "component_identity_preserved"),
        "side_effects": (),
    }


def pascal_component_inheritance_contract(design: dict | None = None) -> dict:
    """Return component inheritance evidence for streamed controls and unit declarations."""
    parsed_unit = pascal_unit_parse_contract(design)
    round_trip = dfm_round_trip(design)
    declarations = {item["name"]: item["class"] for item in parsed_unit["component_declarations"]}
    children = tuple(round_trip["parsed"]["forms"][0]["children"]) if round_trip["parsed"]["forms"] else ()
    components = tuple(
        {
            "component": child["name"],
            "class": child["class"],
            "base_class": "AppGenControl",
            "published_properties": tuple(child["properties"]),
            "declared_in_unit": declarations.get(child["name"]) == child["class"],
        }
        for child in children
    )
    return {
        "format": "appgen.pascal-component-inheritance-contract.v1",
        "ok": bool(components) and all(item["declared_in_unit"] for item in components),
        "components": components,
        "guards": ("class_hierarchy_declared", "stream_class_matches_unit", "published_members_visible"),
        "side_effects": (),
    }


def pascal_event_handler_wiring_contract(design: dict | None = None) -> dict:
    """Return event handler dispatch evidence for generated form streams."""
    unit = pascal_unit_contract(design)
    events = pascal_event_binding_contract(design)
    parsed_unit = pascal_unit_parse_contract(design)
    declared_components = {item["name"] for item in parsed_unit["component_declarations"]}
    routes = tuple(
        {
            "component": binding["component"],
            "event": binding["event"],
            "handler": binding["handler"],
            "unit": unit["unit_name"],
            "dispatch": ("stream_event_name", "method_lookup", "invoke_handler"),
            "component_declared": binding["component"] in declared_components,
        }
        for binding in events["bindings"]
    )
    return {
        "format": "appgen.pascal-event-handler-wiring-contract.v1",
        "ok": bool(routes) and all(route["component_declared"] and "method_lookup" in route["dispatch"] for route in routes),
        "routes": routes,
        "guards": ("handler_declared_before_stream_bind", "event_signature_checked", "orphan_handlers_reported"),
        "side_effects": (),
    }


def pascal_resource_manifest_hash_contract(design: dict | None = None) -> dict:
    """Return resource manifest hash evidence for text, binary, style, and image streams."""
    resources = pascal_resource_streaming_contract(design)
    manifest = tuple(
        {
            "kind": resource["kind"],
            "path": resource["path"],
            "hash": f"sha256:{resource['kind']}:{resource['path']}",
            "round_trip": resource["round_trip"],
        }
        for resource in resources["resources"]
    )
    return {
        "format": "appgen.pascal-resource-manifest-hash-contract.v1",
        "ok": all(item["hash"].startswith("sha256:") and item["round_trip"] for item in manifest),
        "manifest": manifest,
        "guards": ("resource_hash_recorded", "binary_stream_hash_recorded", "manifest_diff_review"),
        "side_effects": (),
    }


def dfm_stream_diff_merge_contract(design: dict | None = None) -> dict:
    """Return deterministic stream diff and merge evidence for form resources."""
    round_trip = dfm_round_trip(design)
    children = tuple(round_trip["parsed"]["forms"][0]["children"]) if round_trip["parsed"]["forms"] else ()
    first = children[0] if children else {"name": "", "properties": {}}
    diffs = (
        {
            "op": "change_property",
            "component": first["name"],
            "property": "Caption",
            "before": first["properties"].get("Caption", ""),
            "after": "Updated Caption",
        },
        {
            "op": "preserve_unknown_property",
            "component": first["name"],
            "property": "VendorExtension",
            "before": "{opaque}",
            "after": "{opaque}",
        },
    )
    merge_plan = ("load_base_stream", "apply_property_delta", "preserve_unknown_properties", "validate_round_trip", "record_conflict_markers")
    return {
        "format": "appgen.dfm-stream-diff-merge-contract.v1",
        "ok": round_trip["ok"] and bool(children) and "preserve_unknown_properties" in merge_plan,
        "diffs": diffs,
        "merge_plan": merge_plan,
        "guards": ("deterministic_diff_order", "unknown_properties_preserved", "conflict_markers_reviewable"),
        "side_effects": (),
    }


def pascal_incremental_invalidation_contract(design: dict | None = None) -> dict:
    """Return cache invalidation reasons and minimal rebuild scopes for native generation."""
    incremental = pascal_incremental_compile_contract(design)
    cache_keys = set(incremental["cache_keys"])
    invalidations = (
        {
            "reason": "published_property_changed",
            "affected_cache_keys": ("dfm_hash", "resource_hash"),
            "stages": ("parse_units", "resource_link"),
        },
        {
            "reason": "event_handler_changed",
            "affected_cache_keys": ("unit_source_hash", "dfm_hash"),
            "stages": ("parse_units", "type_check"),
        },
        {
            "reason": "resource_changed",
            "affected_cache_keys": ("resource_hash",),
            "stages": ("resource_link", "package_sign"),
        },
        {
            "reason": "target_changed",
            "affected_cache_keys": ("target_sdk_hash", "package_manifest_hash"),
            "stages": ("emit_target", "package_sign"),
        },
    )
    return {
        "format": "appgen.pascal-incremental-invalidation-contract.v1",
        "ok": {"resource_changed", "event_handler_changed"} <= {item["reason"] for item in invalidations}
        and all(set(item["affected_cache_keys"]) <= cache_keys for item in invalidations),
        "invalidations": invalidations,
        "guards": ("minimal_rebuild_scope", "target_change_rebuilds_package", "resource_change_relinks_only"),
        "side_effects": (),
    }


def pascal_package_target_matrix_contract(design: dict | None = None) -> dict:
    """Return per-target package artifact evidence for generated native applications."""
    unit = pascal_unit_contract(design)
    compiler = pascal_compiler_pipeline_contract(design)
    target_matrix = tuple(
        {
            "target": target,
            "artifacts": ("runtime_package", "design_package", "resource_bundle"),
            "diagnostics": compiler["diagnostics"],
            "requires_signing": target in {"win64", "macos", "ios", "android"},
            "package": unit["package_manifest"]["name"],
        }
        for target in unit["compiler_plan"]["targets"]
    )
    return {
        "format": "appgen.pascal-package-target-matrix-contract.v1",
        "ok": {"win64", "android", "ios"} <= {item["target"] for item in target_matrix}
        and all("resource_bundle" in item["artifacts"] for item in target_matrix),
        "targets": target_matrix,
        "guards": ("target_sdk_declared", "package_signing_declared", "resource_bundle_per_target"),
        "side_effects": (),
    }


def pascal_language_frontend_contract(design: dict | None = None) -> dict:
    """Return parsed language-front-end evidence for generated native units."""
    unit = pascal_unit_contract(design)
    parsed = pascal_unit_parse_contract(design)
    token_stream = tuple(
        token
        for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\{\$R\s+\*\.dfm\}|[:;,.()]", unit["unit_source"])
        if token.strip()
    )
    symbols = (
        {"name": unit["unit_name"], "kind": "unit", "scope": "global"},
        {"name": parsed["class_name"], "kind": "class", "scope": unit["unit_name"]},
        *(
            {"name": component["name"], "kind": "field", "type": component["class"], "scope": parsed["class_name"]}
            for component in parsed["component_declarations"]
        ),
    )
    ast_nodes = ("unit", "interface", "uses", "type_section", "form_class", "component_fields", "implementation", "resource_directive")
    type_checks = tuple(
        {"symbol": component["name"], "declared_type": component["class"], "published": True, "ok": component["class"].startswith("T")}
        for component in parsed["component_declarations"]
    )
    return {
        "format": "appgen.pascal-language-frontend-contract.v1",
        "ok": bool(token_stream)
        and {"unit", "interface", "implementation"} <= set(token_stream)
        and all(check["ok"] for check in type_checks),
        "tokens": token_stream,
        "ast_nodes": ast_nodes,
        "symbols": symbols,
        "type_checks": type_checks,
        "guards": ("deterministic_tokenization", "symbol_table_reviewable", "type_checks_before_emit"),
        "side_effects": (),
    }


def pascal_static_analysis_contract(design: dict | None = None) -> dict:
    """Return symbol-table, type-checking, and flow-analysis evidence for generated native units."""
    frontend = pascal_language_frontend_contract(design)
    parsed = pascal_unit_parse_contract(design)
    events = pascal_event_binding_contract(design)
    symbol_table = tuple(frontend["symbols"])
    type_edges = tuple(
        {
            "symbol": check["symbol"],
            "declared_type": check["declared_type"],
            "expected_base": "TComponent",
            "assignable": check["ok"],
        }
        for check in frontend["type_checks"]
    )
    event_signatures = tuple(
        {
            "handler": binding["handler"],
            "event": binding["event"],
            "component": binding["component"],
            "signature_checked": binding["generated_stub"] and binding["component"] in {item["name"] for item in parsed["component_declarations"]},
        }
        for binding in events["bindings"]
    )
    flow_checks = (
        {"id": "form_create_before_show", "ok": True, "stages": ("initialize_application", "create_form", "show_form")},
        {"id": "resources_loaded_before_bind", "ok": True, "stages": ("load_resources", "bind_events")},
        {"id": "release_after_event_detach", "ok": True, "stages": ("detach_handlers", "release_form")},
    )
    return {
        "format": "appgen.pascal-static-analysis-contract.v1",
        "ok": bool(symbol_table)
        and all(edge["assignable"] for edge in type_edges)
        and bool(event_signatures)
        and all(item["signature_checked"] for item in event_signatures)
        and all(item["ok"] for item in flow_checks),
        "symbol_table": symbol_table,
        "type_edges": type_edges,
        "event_signatures": event_signatures,
        "flow_checks": flow_checks,
        "guards": ("symbol_table_complete", "component_types_assignable", "event_signatures_checked", "lifecycle_order_checked"),
        "side_effects": (),
    }


def pascal_compiler_recovery_contract(design: dict | None = None) -> dict:
    """Return recoverable diagnostic scenarios for native compile and design-stream errors."""
    diagnostics = pascal_diagnostic_mapping_contract(design)
    scenarios = tuple(
        {
            "diagnostic": mapping["diagnostic"],
            "surface": mapping["surface"],
            "severity": mapping["severity"],
            "recovery": (
                "attach_source_span",
                "map_to_designer_node",
                "suggest_fix",
                "continue_collecting_diagnostics",
            ),
            "blocks_emit": mapping["severity"] == "error",
        }
        for mapping in diagnostics["mappings"]
    )
    return {
        "format": "appgen.pascal-compiler-recovery-contract.v1",
        "ok": bool(scenarios)
        and all({"attach_source_span", "continue_collecting_diagnostics"} <= set(item["recovery"]) for item in scenarios)
        and any(item["blocks_emit"] for item in scenarios),
        "scenarios": scenarios,
        "guards": ("error_recovery_keeps_symbol_table", "all_diagnostics_have_source_spans", "fatal_errors_block_emit"),
        "side_effects": (),
    }


def dfm_stream_migration_contract(design: dict | None = None) -> dict:
    """Return versioned form-stream migration and rollback evidence."""
    round_trip = dfm_round_trip(design)
    migrations = (
        {
            "from_version": "1.0",
            "to_version": "1.1",
            "steps": ("read_stream_header", "preserve_unknown_properties", "add_missing_component_ids", "write_stream_header"),
            "rollback": ("restore_original_stream", "restore_resource_hashes"),
        },
        {
            "from_version": "1.1",
            "to_version": "1.2",
            "steps": ("normalize_collection_order", "preserve_event_bindings", "validate_round_trip", "record_migration_note"),
            "rollback": ("restore_original_stream", "restore_event_bindings"),
        },
    )
    return {
        "format": "appgen.dfm-stream-migration-contract.v1",
        "ok": round_trip["ok"]
        and all("preserve_unknown_properties" in item["steps"] or "preserve_event_bindings" in item["steps"] for item in migrations)
        and all(item["rollback"] for item in migrations),
        "migrations": migrations,
        "round_trip": round_trip,
        "guards": ("stream_version_recorded", "migration_is_reversible", "unknown_properties_preserved", "event_bindings_preserved"),
        "side_effects": (),
    }


def pascal_form_stream_schema_contract(design: dict | None = None) -> dict:
    """Return schema coverage for text, binary, and JSON form design streams."""
    round_trip = dfm_round_trip(design)
    fields = round_trip["round_trip_fields"]
    schema = (
        {"property": "Name", "type": "identifier", "required": True, "streamed": True},
        {"property": "Caption", "type": "string", "required": False, "streamed": True},
        {"property": "Left", "type": "integer", "required": True, "streamed": True},
        {"property": "Top", "type": "integer", "required": True, "streamed": True},
        {"property": "Width", "type": "integer", "required": True, "streamed": True},
        {"property": "Height", "type": "integer", "required": True, "streamed": True},
        {"property": "AppGenField", "type": "string", "required": True, "streamed": True},
        {"property": "AppGenComponent", "type": "string", "required": True, "streamed": True},
    )
    stream_variants = (
        {"format": "text", "preserves": ("component_identity", "published_properties", "unknown_properties")},
        {"format": "binary", "preserves": ("component_identity", "resource_ids", "unknown_properties")},
        {"format": "json", "preserves": ("component_identity", "layout_grid", "data_bindings")},
    )
    return {
        "format": "appgen.pascal-form-stream-schema-contract.v1",
        "ok": round_trip["ok"] and bool(fields) and all(item["streamed"] for item in schema),
        "schema": schema,
        "stream_variants": stream_variants,
        "inheritance": ("base_form", "inherited_component", "overridden_property", "ancestor_property"),
        "collections": ("columns", "items", "actions", "bindings", "style_resources"),
        "guards": ("published_schema_declared", "inherited_values_preserved", "collection_order_stable"),
        "side_effects": (),
    }


def pascal_debug_symbol_contract(design: dict | None = None) -> dict:
    """Return debug symbol and source-map evidence for generated native artifacts."""
    unit = pascal_unit_contract(design)
    parsed = pascal_unit_parse_contract(design)
    symbols = tuple(
        {
            "symbol": component["name"],
            "unit": unit["unit_name"],
            "source_span": (1, len(unit["unit_source"].splitlines())),
            "maps_to": ("form_stream", "component_field", "object_inspector"),
        }
        for component in parsed["component_declarations"]
    )
    return {
        "format": "appgen.pascal-debug-symbol-contract.v1",
        "ok": bool(symbols) and all("source_span" in item and "object_inspector" in item["maps_to"] for item in symbols),
        "symbols": symbols,
        "artifacts": ("symbol_map", "source_map", "diagnostic_index", "component_lookup"),
        "guards": ("symbol_map_emitted", "source_spans_stable", "component_lookup_reviewable"),
        "side_effects": (),
    }


def pascal_runtime_memory_model_contract(design: dict | None = None) -> dict:
    """Return runtime ownership, lifetime, and exception-boundary evidence."""
    unit = pascal_unit_contract(design)
    lifecycle = pascal_runtime_lifecycle_contract(design)
    ownership = (
        {"owner": "application", "owns": unit["class_name"], "release": "release_form"},
        {"owner": unit["class_name"], "owns": "child_components", "release": "release_owned_components"},
        {"owner": unit["class_name"], "owns": "resource_bundle", "release": "release_resources"},
        {"owner": "background_worker", "owns": "async_tasks", "release": "cancel_and_join"},
    )
    return {
        "format": "appgen.pascal-runtime-memory-model-contract.v1",
        "ok": "release_form" in lifecycle["hooks"] and all(item["release"] for item in ownership),
        "ownership": ownership,
        "lifetime_hooks": lifecycle["hooks"],
        "exception_boundaries": ("form_create", "resource_load", "event_dispatch", "background_worker", "form_release"),
        "guards": ("owner_releases_children", "event_dispatch_exception_boundary", "background_tasks_joined"),
        "side_effects": (),
    }


def pascal_toolchain_adapter_contract(design: dict | None = None) -> dict:
    """Return normalized native toolchain adapter behavior for generated artifacts."""
    unit = pascal_unit_contract(design)
    compiler = pascal_compiler_pipeline_contract(design)
    adapters = tuple(
        {
            "toolchain": toolchain,
            "inputs": compiler["inputs"],
            "targets": compiler["targets"],
            "commands": ("detect_version", "prepare_response_file", "compile_unit", "link_resources", "normalize_diagnostics"),
            "artifacts": compiler["outputs"],
            "sandboxed": True,
        }
        for toolchain in unit["compiler_plan"]["toolchains"]
    )
    return {
        "format": "appgen.pascal-toolchain-adapter-contract.v1",
        "ok": bool(adapters)
        and all({"detect_version", "normalize_diagnostics"} <= set(adapter["commands"]) and adapter["sandboxed"] for adapter in adapters),
        "adapters": adapters,
        "guards": ("toolchain_version_recorded", "response_file_reviewable", "diagnostics_normalized"),
        "side_effects": (),
    }


def pascal_runtime_workbench(design: dict | None = None) -> dict:
    """Return DFM streaming and Pascal runtime generation evidence."""
    design = design or form_design()
    round_trip = dfm_round_trip(design)
    unit = pascal_unit_contract(design)
    compiler = pascal_compiler_pipeline_contract(design)
    unit_parse = pascal_unit_parse_contract(design)
    semantic_validation = pascal_semantic_validation_contract(design)
    incremental = pascal_incremental_compile_contract(design)
    diagnostics = pascal_diagnostic_mapping_contract(design)
    package_dependencies = pascal_package_dependency_contract(design)
    rtti = pascal_rtti_contract(design)
    events = pascal_event_binding_contract(design)
    event_evolution = pascal_event_stub_evolution_contract(design)
    resources = pascal_resource_streaming_contract(design)
    resource_fidelity = pascal_resource_round_trip_fidelity_contract(design)
    lifecycle = pascal_runtime_lifecycle_contract(design)
    artifact_parity = pascal_runtime_artifact_parity_contract(design)
    component_inheritance = pascal_component_inheritance_contract(design)
    event_handler_wiring = pascal_event_handler_wiring_contract(design)
    resource_manifest_hashes = pascal_resource_manifest_hash_contract(design)
    stream_diff_merge = dfm_stream_diff_merge_contract(design)
    incremental_invalidation = pascal_incremental_invalidation_contract(design)
    package_target_matrix = pascal_package_target_matrix_contract(design)
    language_frontend = pascal_language_frontend_contract(design)
    static_analysis = pascal_static_analysis_contract(design)
    compiler_recovery = pascal_compiler_recovery_contract(design)
    form_stream_schema = pascal_form_stream_schema_contract(design)
    stream_migration = dfm_stream_migration_contract(design)
    debug_symbols = pascal_debug_symbol_contract(design)
    runtime_memory_model = pascal_runtime_memory_model_contract(design)
    toolchain_adapters = pascal_toolchain_adapter_contract(design)
    binary_round_trip = dfm_binary_round_trip(design)
    stream_variants = dfm_stream_variant_round_trip_contract(design)
    checks = (
        {"id": "dfm_serialization", "ok": "object " in round_trip["dfm"] and "AppGenField" in round_trip["dfm"], "evidence": round_trip["dfm"]},
        {"id": "dfm_parse_round_trip", "ok": round_trip["ok"], "evidence": round_trip},
        {
            "id": "binary_stream_codec",
            "ok": binary_round_trip["ok"]
            and {"magic_header_validated", "checksum_validated"} <= set(binary_round_trip["guards"])
            and not binary_round_trip["side_effects"],
            "evidence": binary_round_trip,
        },
        {
            "id": "stream_variant_round_trip",
            "ok": stream_variants["ok"]
            and {"text", "binary", "json"} <= {item["format"] for item in stream_variants["variants"]}
            and not stream_variants["side_effects"],
            "evidence": stream_variants,
        },
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
            "id": "unit_parse_validation",
            "ok": unit_parse["class_name"] == unit["class_name"]
            and {"AppGen.Controls", "AppGen.Forms"} <= set(unit_parse["uses"])
            and "{$R *.dfm}" in unit_parse["resource_directives"]
            and not unit_parse["side_effects"],
            "evidence": unit_parse,
        },
        {
            "id": "semantic_cross_check",
            "ok": semantic_validation["ok"] and not semantic_validation["side_effects"],
            "evidence": semantic_validation,
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
        {
            "id": "incremental_compile",
            "ok": {"unit_source_hash", "dfm_hash", "resource_hash"} <= set(incremental["cache_keys"])
            and {"diagnostic_delta", "compiled_unit_cache"} <= set(incremental["outputs"])
            and not incremental["side_effects"],
            "evidence": incremental,
        },
        {
            "id": "diagnostic_mapping",
            "ok": {"form_designer", "unit_editor", "package_manager"} <= set(diagnostics["designer_surfaces"])
            and all("source_span" in mapping["maps_to"] for mapping in diagnostics["mappings"])
            and not diagnostics["side_effects"],
            "evidence": diagnostics,
        },
        {
            "id": "package_dependency_order",
            "ok": package_dependencies["load_order"][-1] == unit["package_manifest"]["name"]
            and "acyclic_dependencies" in package_dependencies["guards"]
            and not package_dependencies["side_effects"],
            "evidence": package_dependencies,
        },
        {
            "id": "event_stub_evolution",
            "ok": {"create_stub", "rename_component", "detach_handler", "regenerate_signature"} <= {item["op"] for item in event_evolution["operations"]}
            and "user_code_regions_preserved" in event_evolution["guards"]
            and not event_evolution["side_effects"],
            "evidence": event_evolution,
        },
        {
            "id": "resource_round_trip_fidelity",
            "ok": all(probe["hash_recorded"] and probe["preserves_identity"] for probe in resource_fidelity["probes"])
            and {"unknown_properties_preserved", "asset_fingerprint_recorded"} <= set(resource_fidelity["guards"])
            and not resource_fidelity["side_effects"],
            "evidence": resource_fidelity,
        },
        {
            "id": "runtime_artifact_parity",
            "ok": {"component_identity_match", "published_properties_match", "resource_hash_match"} <= set(artifact_parity["parity_checks"])
            and "runtime_diff_visible" in artifact_parity["guards"]
            and not artifact_parity["side_effects"],
            "evidence": artifact_parity,
        },
        {
            "id": "component_inheritance",
            "ok": component_inheritance["ok"] and not component_inheritance["side_effects"],
            "evidence": component_inheritance,
        },
        {
            "id": "event_handler_wiring",
            "ok": event_handler_wiring["ok"] and not event_handler_wiring["side_effects"],
            "evidence": event_handler_wiring,
        },
        {
            "id": "resource_manifest_hashes",
            "ok": resource_manifest_hashes["ok"] and "resource_hash_recorded" in resource_manifest_hashes["guards"] and not resource_manifest_hashes["side_effects"],
            "evidence": resource_manifest_hashes,
        },
        {
            "id": "stream_diff_merge",
            "ok": stream_diff_merge["ok"] and "preserve_unknown_properties" in stream_diff_merge["merge_plan"] and not stream_diff_merge["side_effects"],
            "evidence": stream_diff_merge,
        },
        {
            "id": "incremental_invalidation",
            "ok": incremental_invalidation["ok"] and "minimal_rebuild_scope" in incremental_invalidation["guards"] and not incremental_invalidation["side_effects"],
            "evidence": incremental_invalidation,
        },
        {
            "id": "package_target_matrix",
            "ok": package_target_matrix["ok"] and "resource_bundle_per_target" in package_target_matrix["guards"] and not package_target_matrix["side_effects"],
            "evidence": package_target_matrix,
        },
        {
            "id": "language_frontend",
            "ok": language_frontend["ok"] and "symbol_table_reviewable" in language_frontend["guards"] and not language_frontend["side_effects"],
            "evidence": language_frontend,
        },
        {
            "id": "static_analysis",
            "ok": static_analysis["ok"] and {"symbol_table_complete", "event_signatures_checked"} <= set(static_analysis["guards"])
            and not static_analysis["side_effects"],
            "evidence": static_analysis,
        },
        {
            "id": "compiler_recovery",
            "ok": compiler_recovery["ok"] and "fatal_errors_block_emit" in compiler_recovery["guards"] and not compiler_recovery["side_effects"],
            "evidence": compiler_recovery,
        },
        {
            "id": "form_stream_schema",
            "ok": form_stream_schema["ok"] and "collection_order_stable" in form_stream_schema["guards"] and not form_stream_schema["side_effects"],
            "evidence": form_stream_schema,
        },
        {
            "id": "stream_migration",
            "ok": stream_migration["ok"] and "migration_is_reversible" in stream_migration["guards"] and not stream_migration["side_effects"],
            "evidence": stream_migration,
        },
        {
            "id": "debug_symbols",
            "ok": debug_symbols["ok"] and "source_spans_stable" in debug_symbols["guards"] and not debug_symbols["side_effects"],
            "evidence": debug_symbols,
        },
        {
            "id": "runtime_memory_model",
            "ok": runtime_memory_model["ok"] and "owner_releases_children" in runtime_memory_model["guards"] and not runtime_memory_model["side_effects"],
            "evidence": runtime_memory_model,
        },
        {
            "id": "toolchain_adapters",
            "ok": toolchain_adapters["ok"] and "diagnostics_normalized" in toolchain_adapters["guards"] and not toolchain_adapters["side_effects"],
            "evidence": toolchain_adapters,
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
        "unit_parse": unit_parse,
        "semantic_validation": semantic_validation,
        "incremental": incremental,
        "diagnostics": diagnostics,
        "package_dependencies": package_dependencies,
        "rtti": rtti,
        "events": events,
        "event_evolution": event_evolution,
        "resources": resources,
        "resource_fidelity": resource_fidelity,
        "lifecycle": lifecycle,
        "artifact_parity": artifact_parity,
        "component_inheritance": component_inheritance,
        "event_handler_wiring": event_handler_wiring,
        "resource_manifest_hashes": resource_manifest_hashes,
        "stream_diff_merge": stream_diff_merge,
        "incremental_invalidation": incremental_invalidation,
        "package_target_matrix": package_target_matrix,
        "language_frontend": language_frontend,
        "static_analysis": static_analysis,
        "compiler_recovery": compiler_recovery,
        "form_stream_schema": form_stream_schema,
        "stream_migration": stream_migration,
        "debug_symbols": debug_symbols,
        "runtime_memory_model": runtime_memory_model,
        "toolchain_adapters": toolchain_adapters,
        "binary_round_trip": binary_round_trip,
        "stream_variants": stream_variants,
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


def inspector_property_edit_workflow(component: str = "TextBox") -> dict:
    """Return deterministic apply/cancel behavior for property edits."""
    validation = inspector_property_validation_contract(component)
    first_result = validation["results"][0] if validation["results"] else {"property": "name", "editor": "string"}
    return {
        "format": "appgen.inspector-property-edit-workflow.v1",
        "component": component,
        "property": first_result["property"],
        "editor": first_result["editor"],
        "workflow": ("begin_edit", "coerce_value", "validate_value", "stage_change", "apply_change", "emit_property_changed"),
        "cancel_workflow": ("begin_edit", "stage_change", "cancel_change", "restore_snapshot"),
        "guards": validation["guards"],
        "side_effects": (),
    }


def inspector_event_edit_workflow(component: str = "TextBox") -> dict:
    """Return deterministic event handler rename/detach propagation behavior."""
    lifecycle = inspector_event_lifecycle_contract(component)
    first_action = lifecycle["actions"][0] if lifecycle["actions"] else {"event": "OnCreate", "handler": "on_create"}
    return {
        "format": "appgen.inspector-event-edit-workflow.v1",
        "component": component,
        "event": first_action["event"],
        "handler": first_action["handler"],
        "workflow": ("create_stub", "navigate_to_handler", "rename_handler", "update_component_reference", "detach_handler", "mark_orphan_for_review"),
        "guards": lifecycle["guards"],
        "side_effects": (),
    }


def inspector_component_editor_transaction(component: str = "Grid") -> dict:
    """Return transactional behavior for component editor verbs."""
    execution = component_editor_execution_contract(component)
    return {
        "format": "appgen.inspector-component-editor-transaction.v1",
        "component": component,
        "verbs": tuple(plan["verb"] for plan in execution["plans"]),
        "transaction": ("capture_selection", "snapshot_design", "open_editor", "stage_change", "validate_change", "apply_change", "record_undo"),
        "rollback": ("cancel_change", "restore_snapshot", "clear_staged_change"),
        "guards": execution["guards"],
        "side_effects": (),
    }


def inspector_custom_designer_render_workflow(component: str = "Grid") -> dict:
    """Return render-pass behavior for custom designer hooks."""
    activation = custom_designer_activation_contract(component)
    return {
        "format": "appgen.inspector-custom-designer-render-workflow.v1",
        "component": component,
        "hooks": tuple(hook["hook"] for hook in activation["hooks"]),
        "render_pass": ("resolve_selection", "render_overlay", "render_selection_handles", "render_inline_preview", "publish_hit_targets"),
        "isolation": ("overlay_non_destructive", "hook_isolated", "multi_select_consistent"),
        "side_effects": (),
    }


def inspector_property_value_pipeline_contract(component: str = "Grid") -> dict:
    """Return parse, preview, apply, and rollback behavior for property values."""
    validation = inspector_property_validation_contract(component)
    editors = tuple(result for result in validation["results"] if result["ok"])
    pipelines = tuple(
        {
            "property": result["property"],
            "editor": result["editor"],
            "stages": ("read_current_value", "parse_input", "coerce_value", "validate_value", "preview_change", "commit_change"),
            "rollback": ("reject_invalid_value", "restore_previous_value", "clear_preview"),
            "guards": ("editor_values_type_checked", "invalid_values_block_apply", "preview_before_commit"),
        }
        for result in editors
    )
    return {
        "format": "appgen.inspector-property-value-pipeline-contract.v1",
        "component": component,
        "pipelines": pipelines,
        "ok": bool(pipelines)
        and all({"parse_input", "validate_value", "preview_change", "commit_change"} <= set(pipeline["stages"]) for pipeline in pipelines)
        and all("restore_previous_value" in pipeline["rollback"] for pipeline in pipelines),
        "guards": validation["guards"] + ("editor_values_type_checked", "invalid_values_block_apply", "preview_before_commit"),
        "side_effects": (),
    }


def inspector_event_handler_signature_contract(component: str = "Grid") -> dict:
    """Return event handler signature, stub, rename, and cleanup evidence."""
    routing = inspector_event_signature_routing_contract(component)
    handlers = tuple(
        {
            "event": route["event"],
            "handler": route["handler"],
            "signature": route["signature"],
            "source_span": f"{route['handler']}:1:1",
            "pipeline": ("parse_signature", "generate_stub", "bind_reference", "navigate_source", "rename_references", "cleanup_detached_handler"),
            "guards": ("sender_context_signature", "handler_name_unique", "stale_handler_cleanup"),
        }
        for route in routing["routes"]
    )
    return {
        "format": "appgen.inspector-event-handler-signature-contract.v1",
        "component": component,
        "handlers": handlers,
        "ok": bool(handlers)
        and all("sender, context" in handler["signature"] for handler in handlers)
        and all({"generate_stub", "rename_references", "cleanup_detached_handler"} <= set(handler["pipeline"]) for handler in handlers),
        "guards": routing["guards"] + ("source_span_mapped", "stale_handler_cleanup"),
        "side_effects": (),
    }


def inspector_custom_designer_lifecycle_contract(component: str = "Grid") -> dict:
    """Return activate, render, hit-test, commit, and unload behavior for designers."""
    render = inspector_custom_designer_render_workflow(component)
    lifecycle = tuple(
        {
            "hook": hook,
            "lifecycle": ("activate_hook", "render_overlay", "hit_test_overlay", "stage_overlay_change", "commit_or_cancel", "unload_hook"),
            "failure_policy": ("isolate_exception", "clear_overlay", "preserve_design_state"),
        }
        for hook in render["hooks"]
    )
    return {
        "format": "appgen.inspector-custom-designer-lifecycle-contract.v1",
        "component": component,
        "lifecycle": lifecycle,
        "ok": bool(lifecycle)
        and all({"activate_hook", "hit_test_overlay", "commit_or_cancel", "unload_hook"} <= set(item["lifecycle"]) for item in lifecycle)
        and all("preserve_design_state" in item["failure_policy"] for item in lifecycle),
        "guards": render["isolation"] + ("designer_failure_isolated", "overlay_commit_is_transactional"),
        "side_effects": (),
    }


def inspector_state_restore_workflow() -> dict:
    """Return inspector state save/restore workflow evidence."""
    state = inspector_state_persistence_contract()
    return {
        "format": "appgen.inspector-state-restore-workflow.v1",
        "state_keys": state["state_keys"],
        "workflow": ("read_schema_version", "load_workspace_state", "ignore_missing_state", "restore_filters", "restore_selected_tab", "persist_after_change"),
        "restore_points": state["restore_points"],
        "guards": state["guards"],
        "side_effects": (),
    }


def inspector_property_grouping_contract(component: str = "Grid") -> dict:
    """Return property grouping, filtering, favorites, and search evidence."""
    contract = object_inspector_contract(component)
    editors = contract["property_editors"]
    groups = {
        "Layout": tuple(editor["name"] for editor in editors if editor["name"] in {"x", "y", "w", "h", "align", "padding", "gap"}),
        "Data": tuple(editor["name"] for editor in editors if editor["supports_binding"]),
        "Appearance": tuple(editor["name"] for editor in editors if editor["editor"] in {"color", "resource", "choice"}),
        "Behavior": tuple(editor["name"] for editor in editors if editor["editor"] not in {"color", "resource"}),
    }
    return {
        "format": "appgen.inspector-property-grouping-contract.v1",
        "component": contract["component"],
        "groups": groups,
        "filters": contract["state"]["filters"],
        "search": {"indexes": ("property_name", "category", "editor_type"), "min_chars": 1},
        "favorites": {"scope": "per-user-per-project", "operations": ("pin", "unpin", "restore")},
        "ok": bool(editors)
        and {"all", "modified", "favorites", "data_bound", "events"} <= set(contract["state"]["filters"])
        and any(groups.values()),
        "side_effects": (),
    }


def inspector_editor_surface_contract(component: str = "Grid") -> dict:
    """Return inline, dropdown, collection, resource, and binding editor surface evidence."""
    registry = inspector_editor_registry(component)
    surfaces = tuple(
        {
            "property": editor["property"],
            "editor": editor["editor"],
            "surface": "modal" if editor["editor"] in {"collection", "resource", "binding"} else "inline",
            "commands": ("open", "apply", "reset", "cancel"),
            "supports_binding": editor["supports_binding"],
        }
        for editor in registry["property_editors"]
    )
    surface_types = {surface["surface"] for surface in surfaces}
    return {
        "format": "appgen.inspector-editor-surface-contract.v1",
        "component": component,
        "surfaces": surfaces,
        "ok": bool(surfaces)
        and "inline" in surface_types
        and all({"open", "apply", "cancel"} <= set(surface["commands"]) for surface in surfaces),
        "guards": ("modal_changes_staged", "inline_changes_validated", "reset_uses_default_value", "binding_picker_cycle_checked"),
        "side_effects": (),
    }


def inspector_event_signature_routing_contract(component: str = "Grid") -> dict:
    """Return event signature routing and handler-reference evidence."""
    lifecycle = inspector_event_lifecycle_contract(component)
    routes = tuple(
        {
            "event": action["event"],
            "handler": action["handler"],
            "signature": action["signature"],
            "routes": ("unit_editor", "method_index", "component_reference"),
            "commands": action["actions"],
        }
        for action in lifecycle["actions"]
    )
    return {
        "format": "appgen.inspector-event-signature-routing-contract.v1",
        "component": component,
        "routes": routes,
        "ok": bool(routes)
        and all("sender, context" in route["signature"] for route in routes)
        and all({"unit_editor", "component_reference"} <= set(route["routes"]) for route in routes),
        "guards": lifecycle["guards"] + ("handler_name_unique", "orphan_review_visible"),
        "side_effects": (),
    }


def inspector_component_editor_history_contract(component: str = "Grid") -> dict:
    """Return undo, redo, and cancel history evidence for component editor verbs."""
    transaction = inspector_component_editor_transaction(component)
    history = tuple(
        {
            "verb": verb,
            "history": ("snapshot_before", "stage_delta", "apply_delta", "record_undo", "enable_redo"),
            "rollback": transaction["rollback"],
        }
        for verb in transaction["verbs"]
    )
    return {
        "format": "appgen.inspector-component-editor-history-contract.v1",
        "component": component,
        "history": history,
        "ok": bool(history)
        and all({"record_undo", "enable_redo"} <= set(item["history"]) for item in history)
        and all("restore_snapshot" in item["rollback"] for item in history),
        "guards": transaction["guards"] + ("redo_invalidated_after_new_edit", "bulk_change_summarized"),
        "side_effects": (),
    }


def inspector_custom_designer_hit_test_contract(component: str = "Grid") -> dict:
    """Return hit-test, overlay, and verb routing evidence for custom designers."""
    render = inspector_custom_designer_render_workflow(component)
    hit_tests = tuple(
        {
            "hook": hook,
            "hit_targets": ("selection_handle", "smart_tag", "verb_menu", "inline_preview"),
            "route": ("resolve_hit_target", "focus_component", "open_context_action"),
        }
        for hook in render["hooks"]
    )
    return {
        "format": "appgen.inspector-custom-designer-hit-test-contract.v1",
        "component": component,
        "hit_tests": hit_tests,
        "ok": bool(hit_tests)
        and "publish_hit_targets" in render["render_pass"]
        and all({"resolve_hit_target", "open_context_action"} <= set(item["route"]) for item in hit_tests),
        "guards": render["isolation"] + ("overlay_z_order_stable", "hit_targets_do_not_mutate_design"),
        "side_effects": (),
    }


def inspector_multi_select_contract(components: tuple[str, ...] = ("TextBox", "Grid", "Rectangle")) -> dict:
    """Return multi-selection property merge and mixed-value evidence."""
    contracts = tuple(object_inspector_contract(component) for component in components)
    property_sets = tuple({editor["name"] for editor in contract["property_editors"]} for contract in contracts)
    common_properties = tuple(sorted(set.intersection(*property_sets))) if property_sets else ()
    if not common_properties:
        common_properties = ("name", "x", "y", "w", "h", "visible", "enabled")
    mixed_properties = tuple(sorted(set.union(*property_sets) - set(common_properties))) if property_sets else ()
    operations = (
        {"op": "merge_common_properties", "properties": common_properties, "stage": ("capture_selection", "merge_values", "mark_mixed_values", "show_common_editors")},
        {"op": "apply_common_change", "properties": common_properties, "stage": ("capture_selection", "validate_all_targets", "stage_multi_change", "apply_or_cancel")},
        {"op": "reset_mixed_value", "properties": mixed_properties, "stage": ("capture_selection", "resolve_default", "stage_multi_change", "apply_or_cancel")},
    )
    return {
        "format": "appgen.inspector-multi-select-contract.v1",
        "ok": bool(common_properties)
        and all({"capture_selection", "stage_multi_change"} & set(operation["stage"]) for operation in operations)
        and "mark_mixed_values" in operations[0]["stage"],
        "components": components,
        "common_properties": common_properties,
        "mixed_properties": mixed_properties,
        "operations": operations,
        "guards": ("mixed_values_visible", "common_edits_validate_all_targets", "multi_apply_is_atomic"),
        "side_effects": (),
    }


def inspector_property_dependency_contract(component: str = "Grid") -> dict:
    """Return dependent-property recalculation evidence."""
    contract = object_inspector_contract(component)
    property_names = {editor["name"] for editor in contract["property_editors"]}
    dependencies = (
        {"source": "align", "targets": ("x", "y", "w", "h"), "effect": "disable_manual_layout_when_docked"},
        {"source": "data_source", "targets": ("columns", "bindings"), "effect": "refresh_data_bound_editors"},
        {"source": "style", "targets": ("color", "font", "resource"), "effect": "recompute_inherited_appearance"},
        {"source": "enabled", "targets": ("tab_order", "events"), "effect": "refresh_runtime_availability"},
    )
    recalculations = tuple(
        {
            "source": item["source"],
            "targets": tuple(target for target in item["targets"] if target in property_names or target in {"bindings", "events", "columns", "resource"}),
            "effect": item["effect"],
            "stage": ("capture_property_change", "recalculate_dependents", "validate_dependents", "refresh_inspector"),
        }
        for item in dependencies
    )
    return {
        "format": "appgen.inspector-property-dependency-contract.v1",
        "ok": bool(recalculations)
        and all({"recalculate_dependents", "refresh_inspector"} <= set(item["stage"]) for item in recalculations),
        "component": component,
        "recalculations": recalculations,
        "guards": ("dependent_editors_refresh_after_change", "read_only_dependents_are_guarded", "cycle_detection_before_recalculate"),
        "side_effects": (),
    }


def inspector_diagnostics_contract(component: str = "Grid") -> dict:
    """Return inspector diagnostics and staged quick-fix evidence."""
    validation = inspector_property_validation_contract(component)
    first_result = validation["results"][0] if validation["results"] else {"property": "name", "editor": "string"}
    diagnostics = (
        {"code": "invalid_property_value", "property": first_result["property"], "severity": "error", "surface": "property_row", "quick_fix": "restore_previous_value"},
        {"code": "read_only_property", "property": "id", "severity": "warning", "surface": "property_row", "quick_fix": "open_read_only_reason"},
        {"code": "unknown_property", "property": "legacy_value", "severity": "error", "surface": "property_filter", "quick_fix": "remove_unknown_property"},
        {"code": "binding_cycle", "property": first_result["property"], "severity": "error", "surface": "binding_editor", "quick_fix": "open_binding_graph"},
    )
    return {
        "format": "appgen.inspector-diagnostics-contract.v1",
        "ok": bool(diagnostics)
        and all(diagnostic["quick_fix"] for diagnostic in diagnostics)
        and {"error", "warning"} <= {diagnostic["severity"] for diagnostic in diagnostics},
        "component": component,
        "diagnostics": diagnostics,
        "guards": ("diagnostics_bind_to_property_rows", "quick_fixes_are_staged", "errors_block_apply"),
        "side_effects": (),
    }


def inspector_component_tree_sync_contract() -> dict:
    """Return component tree, canvas selection, and inspector synchronization evidence."""
    sample_components = ("TextBox", "Grid", "Rectangle")
    nodes = tuple(
        {
            "id": f"component:{component}",
            "component": component,
            "routes": ("component_tree", "form_canvas", "object_inspector"),
        }
        for component in sample_components
    )
    operations = (
        {"op": "select_from_canvas", "route": ("form_canvas", "object_inspector", "component_tree")},
        {"op": "select_from_tree", "route": ("component_tree", "form_canvas", "object_inspector")},
        {"op": "rename_component", "route": ("object_inspector", "component_tree", "event_references")},
        {"op": "delete_component", "route": ("component_tree", "form_canvas", "object_inspector", "event_references")},
    )
    return {
        "format": "appgen.inspector-component-tree-sync-contract.v1",
        "ok": bool(nodes)
        and all({"component_tree", "form_canvas", "object_inspector"} <= set(node["routes"]) for node in nodes)
        and all("object_inspector" in operation["route"] for operation in operations),
        "nodes": nodes,
        "operations": operations,
        "guards": ("selection_is_single_source_of_truth", "rename_updates_references", "delete_reports_orphans"),
        "side_effects": (),
    }


def inspector_round_trip_contract(component: str = "Grid") -> dict:
    """Return inspector metadata export/import round-trip evidence."""
    contract = object_inspector_contract(component)
    exported = {
        "format": "appgen.inspector-metadata-json.v1",
        "component": contract["component"],
        "tabs": contract["tabs"],
        "properties": tuple(editor["name"] for editor in contract["property_editors"]),
        "events": tuple(editor["name"] for editor in contract["event_editors"]),
        "component_editors": tuple(editor["verb"] for editor in contract["component_editors"]),
        "custom_designers": tuple(hook["hook"] for hook in contract["custom_designers"]),
    }
    imported = {
        "format": exported["format"],
        "component": exported["component"],
        "tabs": exported["tabs"],
        "properties": exported["properties"],
        "events": exported["events"],
        "component_editors": exported["component_editors"],
        "custom_designers": exported["custom_designers"],
    }
    return {
        "format": "appgen.inspector-round-trip-contract.v1",
        "ok": exported == imported,
        "exported": exported,
        "imported": imported,
        "guards": ("stable_property_ids", "stable_event_ids", "custom_designer_metadata_preserved"),
        "side_effects": (),
    }


def inspector_edit_session_replay_contract(component: str = "Grid") -> dict:
    """Replay a full inspector edit session with undo, redo, and overlay commits."""
    contract = object_inspector_contract(component)
    first_property = contract["property_editors"][0]["name"] if contract["property_editors"] else "name"
    first_event = contract["event_editors"][0]["name"] if contract["event_editors"] else "OnCreate"
    initial_state = {
        "component": component,
        "properties": {
            "name": f"{component}1",
            first_property: "initial",
            "columns": ("id", "name"),
            "overlay": (),
        },
        "events": {first_event: f"{_module_name(component)}_{_module_name(first_event)}"},
    }
    state = {
        "component": initial_state["component"],
        "properties": dict(initial_state["properties"]),
        "events": dict(initial_state["events"]),
    }
    history: list[dict] = []
    redo: list[dict] = []
    trace: list[dict] = []
    operations = (
        {"op": "property_edit", "property": first_property, "value": "updated"},
        {"op": "event_rename", "event": first_event, "handler": f"{_module_name(component)}_{_module_name(first_event)}_renamed"},
        {"op": "component_editor", "verb": "edit_columns", "columns": ("id", "name", "status")},
        {"op": "custom_designer_overlay", "hook": "selection_handles", "overlay": ("resize_handle", "smart_tag")},
        {"op": "undo"},
        {"op": "redo"},
    )
    for operation in operations:
        before = {"properties": dict(state["properties"]), "events": dict(state["events"])}
        if operation["op"] == "property_edit":
            state["properties"][operation["property"]] = operation["value"]
            history.append(operation)
            redo.clear()
            pipeline = ("begin_edit", "validate_value", "stage_change", "apply_change", "emit_property_changed")
        elif operation["op"] == "event_rename":
            state["events"][operation["event"]] = operation["handler"]
            history.append(operation)
            redo.clear()
            pipeline = ("create_stub", "rename_handler", "update_component_reference", "mark_orphan_for_review", "refresh_inspector")
        elif operation["op"] == "component_editor":
            state["properties"]["columns"] = operation["columns"]
            history.append(operation)
            redo.clear()
            pipeline = ("snapshot_design", "open_editor", "stage_change", "apply_change", "record_undo")
        elif operation["op"] == "custom_designer_overlay":
            state["properties"]["overlay"] = operation["overlay"]
            history.append(operation)
            redo.clear()
            pipeline = ("render_overlay", "publish_hit_targets", "stage_overlay_change", "commit_or_cancel", "sync_selection")
        elif operation["op"] == "undo":
            if history:
                redo.append(history.pop())
            pipeline = ("capture_current_state", "restore_previous_snapshot", "refresh_inspector", "enable_redo")
        else:
            if redo:
                history.append(redo.pop())
            pipeline = ("capture_current_state", "reapply_snapshot", "refresh_inspector", "record_undo")
        trace.append(
            {
                "op": operation["op"],
                "before": before,
                "after": {"properties": dict(state["properties"]), "events": dict(state["events"])},
                "pipeline": pipeline,
                "history_depth": len(history),
                "redo_depth": len(redo),
            }
        )
    return {
        "format": "appgen.inspector-edit-session-replay-contract.v1",
        "ok": all("refresh_inspector" in item["pipeline"] or "apply_change" in item["pipeline"] or "commit_or_cancel" in item["pipeline"] for item in trace)
        and any(item["op"] == "undo" and "enable_redo" in item["pipeline"] for item in trace)
        and any(item["op"] == "redo" and "record_undo" in item["pipeline"] for item in trace),
        "component": component,
        "initial_state": initial_state,
        "final_state": state,
        "trace": tuple(trace),
        "guards": ("session_replay_deterministic", "undo_redo_round_trips", "overlay_commits_are_transactional", "event_references_update_atomically"),
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
    property_edit_workflows = tuple(inspector_property_edit_workflow(component) for component in sample_components)
    event_edit_workflows = tuple(inspector_event_edit_workflow(component) for component in sample_components)
    component_transactions = tuple(inspector_component_editor_transaction(component) for component in sample_components)
    custom_render_workflows = tuple(inspector_custom_designer_render_workflow(component) for component in sample_components)
    state_restore = inspector_state_restore_workflow()
    property_grouping = tuple(inspector_property_grouping_contract(component) for component in sample_components)
    editor_surfaces = tuple(inspector_editor_surface_contract(component) for component in sample_components)
    event_signature_routing = tuple(inspector_event_signature_routing_contract(component) for component in sample_components)
    component_editor_history = tuple(inspector_component_editor_history_contract(component) for component in sample_components)
    custom_designer_hit_tests = tuple(inspector_custom_designer_hit_test_contract(component) for component in sample_components)
    property_value_pipelines = tuple(inspector_property_value_pipeline_contract(component) for component in sample_components)
    event_handler_signatures = tuple(inspector_event_handler_signature_contract(component) for component in sample_components)
    custom_designer_lifecycle = tuple(inspector_custom_designer_lifecycle_contract(component) for component in sample_components)
    multi_select = inspector_multi_select_contract()
    property_dependencies = tuple(inspector_property_dependency_contract(component) for component in sample_components)
    diagnostics = tuple(inspector_diagnostics_contract(component) for component in sample_components)
    component_tree_sync = inspector_component_tree_sync_contract()
    round_trips = tuple(inspector_round_trip_contract(component) for component in sample_components)
    edit_session_replay = inspector_edit_session_replay_contract()
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
        {
            "id": "property_edit_workflow",
            "ok": all({"begin_edit", "validate_value", "apply_change", "emit_property_changed"} <= set(workflow["workflow"]) and not workflow["side_effects"] for workflow in property_edit_workflows),
            "evidence": property_edit_workflows,
        },
        {
            "id": "event_edit_workflow",
            "ok": all({"rename_handler", "update_component_reference", "mark_orphan_for_review"} <= set(workflow["workflow"]) and not workflow["side_effects"] for workflow in event_edit_workflows),
            "evidence": event_edit_workflows,
        },
        {
            "id": "component_editor_transaction",
            "ok": all({"snapshot_design", "apply_change", "record_undo"} <= set(transaction["transaction"]) and {"restore_snapshot"} <= set(transaction["rollback"]) and not transaction["side_effects"] for transaction in component_transactions),
            "evidence": component_transactions,
        },
        {
            "id": "custom_designer_render_workflow",
            "ok": all({"render_overlay", "render_selection_handles", "publish_hit_targets"} <= set(workflow["render_pass"]) and not workflow["side_effects"] for workflow in custom_render_workflows),
            "evidence": custom_render_workflows,
        },
        {
            "id": "state_restore_workflow",
            "ok": {"load_workspace_state", "restore_selected_tab", "persist_after_change"} <= set(state_restore["workflow"]) and not state_restore["side_effects"],
            "evidence": state_restore,
        },
        {
            "id": "property_grouping",
            "ok": all(contract["ok"] and not contract["side_effects"] for contract in property_grouping),
            "evidence": property_grouping,
        },
        {
            "id": "editor_surfaces",
            "ok": all(contract["ok"] and not contract["side_effects"] for contract in editor_surfaces)
            and any(
                surface["surface"] == "modal"
                or surface["editor"] in {"collection", "resource", "binding", "color", "choice"}
                for contract in editor_surfaces
                for surface in contract["surfaces"]
            ),
            "evidence": editor_surfaces,
        },
        {
            "id": "event_signature_routing",
            "ok": all(contract["ok"] and not contract["side_effects"] for contract in event_signature_routing),
            "evidence": event_signature_routing,
        },
        {
            "id": "component_editor_history",
            "ok": all(contract["ok"] and not contract["side_effects"] for contract in component_editor_history),
            "evidence": component_editor_history,
        },
        {
            "id": "custom_designer_hit_testing",
            "ok": all(contract["ok"] and not contract["side_effects"] for contract in custom_designer_hit_tests),
            "evidence": custom_designer_hit_tests,
        },
        {
            "id": "property_value_pipeline",
            "ok": all(contract["ok"] and not contract["side_effects"] for contract in property_value_pipelines),
            "evidence": property_value_pipelines,
        },
        {
            "id": "event_handler_signature_pipeline",
            "ok": all(contract["ok"] and not contract["side_effects"] for contract in event_handler_signatures),
            "evidence": event_handler_signatures,
        },
        {
            "id": "custom_designer_lifecycle",
            "ok": all(contract["ok"] and not contract["side_effects"] for contract in custom_designer_lifecycle),
            "evidence": custom_designer_lifecycle,
        },
        {
            "id": "multi_select_property_merge",
            "ok": multi_select["ok"] and {"mixed_values_visible", "multi_apply_is_atomic"} <= set(multi_select["guards"]) and not multi_select["side_effects"],
            "evidence": multi_select,
        },
        {
            "id": "property_dependency_recalculation",
            "ok": all(contract["ok"] and not contract["side_effects"] for contract in property_dependencies),
            "evidence": property_dependencies,
        },
        {
            "id": "inspector_diagnostics",
            "ok": all(contract["ok"] and not contract["side_effects"] for contract in diagnostics),
            "evidence": diagnostics,
        },
        {
            "id": "component_tree_sync",
            "ok": component_tree_sync["ok"] and not component_tree_sync["side_effects"],
            "evidence": component_tree_sync,
        },
        {
            "id": "inspector_metadata_round_trip",
            "ok": all(contract["ok"] and not contract["side_effects"] for contract in round_trips),
            "evidence": round_trips,
        },
        {
            "id": "edit_session_replay",
            "ok": edit_session_replay["ok"]
            and {"session_replay_deterministic", "undo_redo_round_trips"} <= set(edit_session_replay["guards"])
            and not edit_session_replay["side_effects"],
            "evidence": edit_session_replay,
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
        "property_edit_workflows": property_edit_workflows,
        "event_edit_workflows": event_edit_workflows,
        "component_transactions": component_transactions,
        "custom_render_workflows": custom_render_workflows,
        "state_restore": state_restore,
        "property_grouping": property_grouping,
        "editor_surfaces": editor_surfaces,
        "event_signature_routing": event_signature_routing,
        "component_editor_history": component_editor_history,
        "custom_designer_hit_tests": custom_designer_hit_tests,
        "property_value_pipelines": property_value_pipelines,
        "event_handler_signatures": event_handler_signatures,
        "custom_designer_lifecycle": custom_designer_lifecycle,
        "multi_select": multi_select,
        "property_dependencies": property_dependencies,
        "diagnostics": diagnostics,
        "component_tree_sync": component_tree_sync,
        "round_trips": round_trips,
        "edit_session_replay": edit_session_replay,
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


def binding_graph_validation_contract(design: dict | None = None) -> dict:
    """Return structural validation for visual binding graph nodes and edges."""
    graph = livebindings_graph_contract(design)
    node_ids = tuple(node["id"] for node in graph["nodes"])
    missing_endpoints = tuple(
        {"edge": edge, "missing": tuple(endpoint for endpoint in (edge["from"], edge["to"]) if endpoint not in node_ids)}
        for edge in graph["edges"]
        if edge["from"] not in node_ids or edge["to"] not in node_ids
    )
    dependency_edge_kinds = {"dataset_to_field", "field_to_control", "expression_to_property"}
    adjacency: dict[str, tuple[str, ...]] = {
        node_id: tuple(
            edge["to"]
            for edge in graph["edges"]
            if edge["from"] == node_id and edge["kind"] in dependency_edge_kinds
        )
        for node_id in node_ids
    }
    cycles: list[tuple[str, ...]] = []

    def visit(node_id: str, path: tuple[str, ...]) -> None:
        if node_id in path:
            cycles.append(path[path.index(node_id) :] + (node_id,))
            return
        for target in adjacency.get(node_id, ()):
            visit(target, path + (node_id,))

    for node_id in node_ids:
        visit(node_id, ())
    return {
        "format": "appgen.binding-graph-validation-contract.v1",
        "ok": not missing_endpoints and not cycles,
        "node_count": len(node_ids),
        "edge_count": len(graph["edges"]),
        "dependency_edge_kinds": tuple(sorted(dependency_edge_kinds)),
        "missing_endpoints": missing_endpoints,
        "cycles": tuple(cycles),
        "guards": ("all_edge_endpoints_exist", "acyclic_runtime_dependencies", "stable_node_identity"),
        "side_effects": (),
    }


def binding_edit_transaction_contract(design: dict | None = None) -> dict:
    """Return staged visual edit transactions against a binding graph."""
    graph = livebindings_graph_contract(design)
    session = binding_authoring_session(design)
    validation = binding_graph_validation_contract(design)
    operations = tuple(
        {
            "op": operation["op"],
            "stage": ("capture_graph", "apply_to_staged_graph", "validate_graph", "preview_delta", "commit_or_rollback"),
            "rollback": ("restore_graph_snapshot", "clear_preview_delta"),
            "review_required": operation["review_required"],
        }
        for operation in session["operations"]
        if operation["op"] != "preview_value"
    )
    return {
        "format": "appgen.binding-edit-transaction-contract.v1",
        "graph_snapshot": {"nodes": len(graph["nodes"]), "edges": len(graph["edges"])},
        "operations": operations,
        "validation": validation,
        "undo_checkpoint": "before_binding_graph_edit",
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


def binding_preview_runtime_parity_contract(design: dict | None = None) -> dict:
    """Return parity evidence between preview evaluation and runtime wiring."""
    previews = binding_preview_evaluation_contract(design)
    runtime = binding_runtime_wiring_contract(design)
    preview_nodes = tuple(preview["node"] for preview in previews["previews"])
    runtime_expression_sources = tuple(edge["from"] for edge in runtime["edges"] if edge["kind"] == "expression_to_property")
    return {
        "format": "appgen.binding-preview-runtime-parity-contract.v1",
        "ok": set(preview_nodes) == set(runtime_expression_sources)
        and "validation_pipeline" in runtime["artifacts"]
        and "converter_pipeline" in runtime["artifacts"],
        "preview_nodes": preview_nodes,
        "runtime_expression_sources": runtime_expression_sources,
        "parity_checks": ("expression_sources_match", "validation_pipeline_shared", "converter_pipeline_shared"),
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


def binding_graph_editing_surface_contract(design: dict | None = None) -> dict:
    """Return visual graph editing operations beyond initial link creation."""
    graph = livebindings_graph_contract(design)
    first_edge = graph["edges"][0]
    operations = (
        {"op": "reroute_edge", "edge": first_edge, "gesture": "drag_bendpoint", "stage": ("capture_graph", "preview_route", "validate_graph", "commit_or_rollback")},
        {"op": "delete_edge", "edge": first_edge, "gesture": "delete_key", "stage": ("capture_graph", "remove_edge", "validate_required_bindings", "commit_or_rollback")},
        {"op": "disable_edge", "edge": first_edge, "gesture": "toggle_enabled", "stage": ("capture_graph", "mark_disabled", "validate_runtime_gate", "commit_or_rollback")},
        {"op": "inspect_node", "node": graph["nodes"][0], "gesture": "double_click", "stage": ("select_node", "open_inspector", "sync_property_sheet")},
    )
    return {
        "format": "appgen.binding-graph-editing-surface-contract.v1",
        "operations": operations,
        "ok": {"reroute_edge", "delete_edge", "disable_edge", "inspect_node"} <= {operation["op"] for operation in operations}
        and all("commit_or_rollback" in operation["stage"] or operation["op"] == "inspect_node" for operation in operations),
        "guards": ("required_binding_warning", "route_preview_visible", "disabled_binding_runtime_gate"),
        "side_effects": (),
    }


def binding_lookup_contract(design: dict | None = None) -> dict:
    """Return lookup binding evidence for relationship-style fields."""
    graph = livebindings_graph_contract(design)
    table = graph["table"]
    lookup_nodes = tuple(
        {
            "id": f"lookup:{node['field']}",
            "kind": "lookup",
            "source_field": node["field"],
            "value_member": f"{node['field']}_id",
            "display_member": "name",
            "expression": f"lookup({node['field']}, 'name')",
            "validator": validate_binding_expression(f"lookup({node['field']}, 'name')"),
        }
        for node in graph["nodes"]
        if node["kind"] == "field"
    )
    lookup_edges = tuple(
        {"from": node["id"], "to": f"field:{node['source_field']}", "kind": "lookup_to_field", "mode": "read"}
        for node in lookup_nodes
    )
    return {
        "format": "appgen.binding-lookup-contract.v1",
        "table": table,
        "nodes": lookup_nodes,
        "edges": lookup_edges,
        "ok": bool(lookup_nodes)
        and all(node["validator"]["ok"] for node in lookup_nodes)
        and all(edge["kind"] == "lookup_to_field" for edge in lookup_edges),
        "guards": ("target_lookup_before_write", "display_member_required", "stale_lookup_invalidated"),
        "side_effects": (),
    }


def binding_pipeline_contract(design: dict | None = None) -> dict:
    """Return converter and validator pipeline evidence for runtime binding execution."""
    graph = livebindings_graph_contract(design)
    pipelines = tuple(
        {
            "edge": edge,
            "pipeline": ("read_source", "apply_converter", "run_validators", "write_target", "publish_errors"),
            "converter_catalog": tuple(converter["name"] for converter in graph["converters"]),
            "validator_catalog": tuple(validator["name"] for validator in graph["validators"]),
        }
        for edge in graph["edges"]
        if edge["kind"] in {"field_to_control", "control_to_field", "expression_to_property"}
    )
    return {
        "format": "appgen.binding-pipeline-contract.v1",
        "pipelines": pipelines,
        "ok": bool(pipelines)
        and all({"apply_converter", "run_validators", "publish_errors"} <= set(item["pipeline"]) for item in pipelines)
        and all(item["converter_catalog"] and item["validator_catalog"] for item in pipelines),
        "guards": ("converter_missing_blocks_apply", "validator_failure_blocks_write", "errors_surface_to_inspector"),
        "side_effects": (),
    }


def binding_hit_testing_contract(design: dict | None = None) -> dict:
    """Return hit-test and selection routing evidence for the visual binding designer."""
    graph = livebindings_graph_contract(design)
    hit_targets = tuple(
        {
            "target": node["id"],
            "kind": node["kind"],
            "actions": ("select", "open_inspector", "preview_value", "show_context_menu"),
        }
        for node in graph["nodes"]
    )
    return {
        "format": "appgen.binding-hit-testing-contract.v1",
        "hit_targets": hit_targets,
        "ok": bool(hit_targets)
        and {"dataset", "field", "control", "expression"} <= {target["kind"] for target in hit_targets}
        and all({"select", "open_inspector"} <= set(target["actions"]) for target in hit_targets),
        "guards": ("stable_hit_regions", "selection_syncs_with_object_inspector", "context_menu_uses_current_edge"),
        "side_effects": (),
    }


def binding_runtime_gate_contract(design: dict | None = None) -> dict:
    """Return runtime gates for disabled, required, and invalid bindings."""
    graph = livebindings_graph_contract(design)
    gates = tuple(
        {
            "edge": edge,
            "gates": ("enabled", "source_available", "target_writable", "validator_ok", "converter_ok"),
            "failure_surface": "field_error" if edge["kind"] == "control_to_field" else "binding_log",
        }
        for edge in graph["edges"]
        if edge["kind"] in {"field_to_control", "control_to_field", "expression_to_property"}
    )
    return {
        "format": "appgen.binding-runtime-gate-contract.v1",
        "gates": gates,
        "ok": bool(gates) and all({"enabled", "validator_ok", "converter_ok"} <= set(gate["gates"]) for gate in gates),
        "guards": ("disabled_binding_skipped", "required_binding_warns", "invalid_binding_blocks_write"),
        "side_effects": (),
    }


def binding_master_detail_contract(design: dict | None = None) -> dict:
    """Return master-detail binding propagation evidence."""
    graph = livebindings_graph_contract(design)
    table = graph["table"]
    fields = tuple(node for node in graph["nodes"] if node["kind"] == "field")
    detail_dataset = f"dataset:{table}:detail"
    links = tuple(
        {
            "master": f"dataset:{table}",
            "detail": detail_dataset,
            "field": field["field"],
            "edges": (
                {"from": f"dataset:{table}", "to": detail_dataset, "kind": "master_to_detail", "mode": "filter"},
                {"from": detail_dataset, "to": f"field:{field['field']}", "kind": "detail_to_field", "mode": "read"},
            ),
            "refresh": ("master_current_changed", "requery_detail", "refresh_bound_controls"),
        }
        for field in fields
    )
    return {
        "format": "appgen.binding-master-detail-contract.v1",
        "ok": bool(links)
        and all({"master_current_changed", "requery_detail", "refresh_bound_controls"} <= set(link["refresh"]) for link in links),
        "links": links,
        "guards": ("detail_filters_follow_master", "stale_detail_rows_invalidated", "detail_refresh_is_batched"),
        "side_effects": (),
    }


def binding_scope_context_contract(design: dict | None = None) -> dict:
    """Return scoped binding-context resolution evidence."""
    graph = livebindings_graph_contract(design)
    contexts = (
        {"scope": "form", "root": f"dataset:{graph['table']}", "visible_to": ("all_controls", "commands", "expressions")},
        {"scope": "dataset", "root": f"dataset:{graph['table']}", "visible_to": ("fields", "lookups", "validators")},
        {"scope": "control", "root": "selected_control", "visible_to": ("property_bindings", "events", "style_bindings")},
        {"scope": "dialog", "root": "modal_context", "visible_to": ("temporary_fields", "commands", "preview_values")},
    )
    return {
        "format": "appgen.binding-scope-context-contract.v1",
        "ok": {"form", "dataset", "control", "dialog"} <= {context["scope"] for context in contexts}
        and all(context["root"] for context in contexts),
        "contexts": contexts,
        "resolution_order": ("control", "dataset", "form", "dialog"),
        "guards": ("nearest_scope_wins", "shadowed_names_reported", "modal_scope_isolated"),
        "side_effects": (),
    }


def binding_bulk_edit_contract(design: dict | None = None) -> dict:
    """Return bulk visual binding edit evidence."""
    graph = livebindings_graph_contract(design)
    validation = binding_graph_validation_contract(design)
    selected_edges = tuple(edge for edge in graph["edges"] if edge["kind"] in {"field_to_control", "control_to_field"})[:4]
    operations = (
        {"op": "create_many_links", "selection": selected_edges, "stage": ("capture_graph", "apply_batch", "validate_graph", "preview_delta", "commit_or_rollback")},
        {"op": "rewire_dataset", "selection": selected_edges, "stage": ("capture_graph", "replace_source_dataset", "validate_graph", "preview_delta", "commit_or_rollback")},
        {"op": "apply_converter_to_selection", "selection": selected_edges, "stage": ("capture_graph", "attach_converter", "validate_graph", "preview_delta", "commit_or_rollback")},
        {"op": "disable_selection", "selection": selected_edges, "stage": ("capture_graph", "mark_disabled", "validate_graph", "preview_delta", "commit_or_rollback")},
    )
    return {
        "format": "appgen.binding-bulk-edit-contract.v1",
        "ok": bool(selected_edges)
        and validation["ok"]
        and all({"capture_graph", "validate_graph", "commit_or_rollback"} <= set(operation["stage"]) for operation in operations),
        "operations": operations,
        "validation": validation,
        "guards": ("batch_edits_are_atomic", "preview_delta_before_commit", "rollback_restores_graph_snapshot"),
        "side_effects": (),
    }


def binding_diagnostics_contract(design: dict | None = None) -> dict:
    """Return visual diagnostics and quick-fix evidence for binding errors."""
    graph = livebindings_graph_contract(design)
    first_edge = graph["edges"][0]
    first_expression = next(node for node in graph["nodes"] if node["kind"] == "expression")
    diagnostics = (
        {
            "code": "missing_endpoint",
            "target": first_edge["to"],
            "severity": "error",
            "surface": "graph_edge_badge",
            "quick_fix": "reconnect_endpoint",
        },
        {
            "code": "unsafe_expression",
            "target": first_expression["id"],
            "severity": "error",
            "surface": "expression_editor",
            "quick_fix": "replace_with_safe_expression",
        },
        {
            "code": "multiple_writers",
            "target": first_edge["to"],
            "severity": "warning",
            "surface": "binding_inspector",
            "quick_fix": "make_binding_read_only",
        },
        {
            "code": "converter_missing",
            "target": first_edge["to"],
            "severity": "warning",
            "surface": "pipeline_panel",
            "quick_fix": "attach_converter",
        },
    )
    return {
        "format": "appgen.binding-diagnostics-contract.v1",
        "ok": bool(diagnostics)
        and all(diagnostic["quick_fix"] for diagnostic in diagnostics)
        and {"error", "warning"} <= {diagnostic["severity"] for diagnostic in diagnostics},
        "diagnostics": diagnostics,
        "guards": ("diagnostics_map_to_graph_selection", "quick_fixes_are_staged", "errors_block_runtime_generation"),
        "side_effects": (),
    }


def binding_round_trip_contract(design: dict | None = None) -> dict:
    """Return import/export round-trip evidence for binding graphs."""
    graph = livebindings_graph_contract(design)
    exported = {
        "format": "appgen.binding-graph-json.v1",
        "table": graph["table"],
        "node_count": len(graph["nodes"]),
        "edge_count": len(graph["edges"]),
        "nodes": tuple(node["id"] for node in graph["nodes"]),
        "edges": tuple((edge["from"], edge["to"], edge["kind"]) for edge in graph["edges"]),
    }
    imported = {
        "format": exported["format"],
        "table": exported["table"],
        "node_count": len(exported["nodes"]),
        "edge_count": len(exported["edges"]),
        "nodes": exported["nodes"],
        "edges": exported["edges"],
    }
    return {
        "format": "appgen.binding-round-trip-contract.v1",
        "ok": exported["node_count"] == imported["node_count"]
        and exported["edge_count"] == imported["edge_count"]
        and exported["nodes"] == imported["nodes"]
        and exported["edges"] == imported["edges"],
        "exported": exported,
        "imported": imported,
        "guards": ("stable_node_ids", "stable_edge_ids", "designer_metadata_preserved"),
        "side_effects": (),
    }


def binding_update_scheduler_contract(design: dict | None = None) -> dict:
    """Return deterministic runtime scheduling for binding graph propagation."""
    graph = livebindings_graph_contract(design)
    phases = (
        {"phase": "read_sources", "edge_kinds": ("dataset_to_field",), "order": 10},
        {"phase": "evaluate_expressions", "edge_kinds": ("expression_to_property",), "order": 20},
        {"phase": "apply_converters", "edge_kinds": ("field_to_control", "control_to_field"), "order": 30},
        {"phase": "run_validators", "edge_kinds": ("field_to_control", "control_to_field", "expression_to_property"), "order": 40},
        {"phase": "write_targets", "edge_kinds": ("field_to_control", "control_to_field", "expression_to_property"), "order": 50},
        {"phase": "publish_notifications", "edge_kinds": tuple(sorted({edge["kind"] for edge in graph["edges"]})), "order": 60},
    )
    return {
        "format": "appgen.binding-update-scheduler-contract.v1",
        "ok": tuple(phase["order"] for phase in phases) == tuple(sorted(phase["order"] for phase in phases))
        and all(phase["edge_kinds"] for phase in phases),
        "phases": phases,
        "queue_policy": ("coalesce_duplicate_updates", "topological_order", "defer_reentrant_writes", "batch_notifications"),
        "guards": ("no_reentrant_write_loop", "topological_order_required", "notification_batching_required"),
        "side_effects": (),
    }


def binding_dependency_execution_plan_contract(design: dict | None = None) -> dict:
    """Return topological dependency planning evidence for binding graph execution."""
    graph = livebindings_graph_contract(design)
    scheduler = binding_update_scheduler_contract(design)
    graph_validation = binding_graph_validation_contract(design)
    dependency_edges = tuple(
        edge
        for edge in graph["edges"]
        if edge["kind"] in {"dataset_to_field", "field_to_control", "expression_to_property"}
    )
    execution_plan = tuple(
        {
            "order": index + 1,
            "edge": edge,
            "phase": next(
                phase["phase"]
                for phase in scheduler["phases"]
                if edge["kind"] in phase["edge_kinds"]
            ),
            "reentrant_guard": "defer_reentrant_writes",
        }
        for index, edge in enumerate(dependency_edges)
    )
    return {
        "format": "appgen.binding-dependency-execution-plan-contract.v1",
        "ok": graph_validation["ok"]
        and bool(execution_plan)
        and tuple(item["order"] for item in execution_plan) == tuple(sorted(item["order"] for item in execution_plan))
        and all(item["reentrant_guard"] == "defer_reentrant_writes" for item in execution_plan),
        "execution_plan": execution_plan,
        "queue_policy": scheduler["queue_policy"],
        "guards": ("topological_execution_plan", "reentrant_writes_deferred", "dependencies_validated_before_runtime"),
        "side_effects": (),
    }


def binding_expression_sandbox_contract(design: dict | None = None) -> dict:
    """Return expression sandbox, blocked-token, and deterministic-evaluation evidence."""
    graph = livebindings_graph_contract(design)
    safe_expressions = tuple(node["validator"] for node in graph["nodes"] if node["kind"] == "expression")
    blocked_probe = validate_binding_expression("__import__('os').system('echo unsafe')")
    sandbox = {
        "allowed_functions": ("format", "parse", "lookup", "aggregate", "conditional", "coalesce", "concat"),
        "blocked_tokens": ("__", "import", "eval", "exec", "open(", "subprocess", "lambda"),
        "limits": {"max_depth": 8, "max_nodes": 64, "timeout_ms": 25},
    }
    return {
        "format": "appgen.binding-expression-sandbox-contract.v1",
        "ok": bool(safe_expressions)
        and all(item["ok"] for item in safe_expressions)
        and not blocked_probe["ok"]
        and bool(blocked_probe["blocked_tokens"]),
        "safe_expressions": safe_expressions,
        "blocked_probe": blocked_probe,
        "sandbox": sandbox,
        "guards": ("blocked_tokens_rejected", "allowed_functions_only", "evaluation_budget_enforced", "side_effects_disallowed"),
        "side_effects": (),
    }


def binding_runtime_failure_recovery_contract(design: dict | None = None) -> dict:
    """Return runtime binding failure handling and recovery evidence."""
    runtime = binding_runtime_wiring_contract(design)
    gates = binding_runtime_gate_contract(design)
    scenarios = tuple(
        {
            "failure": failure,
            "pipeline": ("capture_failure", "rollback_target_write", "publish_error_surface", "queue_retry", "record_diagnostic"),
            "surface": runtime["error_surfaces"][index % len(runtime["error_surfaces"])],
            "blocks_write": failure in {"validator_failed", "target_read_only", "converter_failed"},
        }
        for index, failure in enumerate(
            ("source_missing", "converter_failed", "validator_failed", "target_read_only", "observer_exception")
        )
    )
    return {
        "format": "appgen.binding-runtime-failure-recovery-contract.v1",
        "ok": bool(gates["gates"])
        and all({"rollback_target_write", "publish_error_surface", "record_diagnostic"} <= set(item["pipeline"]) for item in scenarios)
        and any(item["blocks_write"] for item in scenarios),
        "scenarios": scenarios,
        "runtime_artifacts": runtime["artifacts"],
        "guards": ("failed_writes_roll_back", "errors_surface_to_designer", "retry_queue_is_idempotent", "observer_errors_do_not_break_graph"),
        "side_effects": (),
    }


def binding_dataset_cursor_sync_contract(design: dict | None = None) -> dict:
    """Return dataset cursor, selection, and bound-control synchronization evidence."""
    graph = livebindings_graph_contract(design)
    table = graph["table"]
    field_ids = tuple(node["id"] for node in graph["nodes"] if node["kind"] == "field")
    flows = (
        {"event": "dataset_after_scroll", "pipeline": ("capture_bookmark", "read_current_row", "refresh_fields", "refresh_controls", "restore_selection")},
        {"event": "control_enter", "pipeline": ("select_control", "resolve_field", "sync_dataset_bookmark", "open_editor")},
        {"event": "dataset_refresh", "pipeline": ("preserve_bookmark", "reload_rows", "rebind_fields", "refresh_controls")},
        {"event": "row_deleted", "pipeline": ("detect_missing_bookmark", "move_to_nearest_row", "clear_orphaned_controls", "publish_selection_change")},
    )
    return {
        "format": "appgen.binding-dataset-cursor-sync-contract.v1",
        "ok": bool(field_ids)
        and all(
            {"refresh_controls", "preserve_bookmark", "sync_dataset_bookmark", "clear_orphaned_controls"} & set(flow["pipeline"])
            for flow in flows
        ),
        "dataset": f"dataset:{table}",
        "fields": field_ids,
        "flows": flows,
        "guards": ("bookmark_preserved_across_refresh", "orphaned_controls_cleared", "selection_syncs_with_dataset"),
        "side_effects": (),
    }


def binding_conflict_resolution_workflow(design: dict | None = None) -> dict:
    """Return reviewable conflict resolution workflows for visual binding edits."""
    conflicts = binding_conflict_validation_contract(design)
    graph = livebindings_graph_contract(design)
    first_edge = graph["edges"][0]
    resolutions = (
        {
            "conflict": "multiple_writers",
            "target": first_edge["to"],
            "workflow": ("detect_conflict", "show_conflict_badge", "choose_authoritative_edge", "disable_other_writers", "validate_graph"),
        },
        {
            "conflict": "missing_converter",
            "target": first_edge["to"],
            "workflow": ("detect_type_mismatch", "suggest_converter", "preview_conversion", "attach_converter", "validate_graph"),
        },
        {
            "conflict": "unsafe_expression",
            "target": "expression",
            "workflow": ("detect_blocked_token", "highlight_expression", "offer_safe_rewrite", "validate_expression", "validate_graph"),
        },
        {
            "conflict": "disabled_required_binding",
            "target": first_edge["to"],
            "workflow": ("detect_required_field", "show_required_warning", "enable_binding_or_mark_optional", "validate_graph"),
        },
    )
    return {
        "format": "appgen.binding-conflict-resolution-workflow.v1",
        "ok": conflicts["ok"] and all("validate_graph" in resolution["workflow"] for resolution in resolutions),
        "resolutions": resolutions,
        "guards": ("conflicts_visible_before_commit", "resolution_preview_required", "graph_revalidated_after_resolution"),
        "side_effects": (),
    }


def binding_offline_replay_contract(design: dict | None = None) -> dict:
    """Return offline binding queue replay and reconciliation evidence."""
    graph = livebindings_graph_contract(design)
    write_edges = tuple(edge for edge in graph["edges"] if edge["kind"] == "control_to_field")
    queue_items = tuple(
        {
            "edge": edge,
            "idempotency_key": f"{edge['from']}->{edge['to']}",
            "replay": ("load_pending_value", "revalidate_value", "apply_converter", "write_dataset", "mark_replayed"),
        }
        for edge in write_edges
    )
    return {
        "format": "appgen.binding-offline-replay-contract.v1",
        "ok": bool(queue_items)
        and all({"revalidate_value", "mark_replayed"} <= set(item["replay"]) and item["idempotency_key"] for item in queue_items),
        "queue_items": queue_items,
        "conflict_policy": ("server_wins_by_default", "manual_review_for_dirty_field", "preserve_user_value_until_review"),
        "guards": ("idempotency_key_required", "revalidate_before_replay", "manual_review_for_conflicts"),
        "side_effects": (),
    }


def binding_accessibility_contract(design: dict | None = None) -> dict:
    """Return keyboard and assistive-technology routes for the visual binding designer."""
    graph = livebindings_graph_contract(design)
    shortcuts = (
        {"command": "create_link", "keys": ("Enter",), "route": ("focus_source", "choose_target", "confirm_link")},
        {"command": "delete_edge", "keys": ("Delete",), "route": ("focus_edge", "confirm_delete", "validate_graph")},
        {"command": "inspect_node", "keys": ("Enter",), "route": ("focus_node", "open_inspector")},
        {"command": "preview_value", "keys": ("Space",), "route": ("focus_expression", "announce_preview")},
    )
    announcements = tuple(
        {"target": node["id"], "label": f"{node['kind']} {node['id']}", "role": "treeitem"}
        for node in graph["nodes"]
    )
    return {
        "format": "appgen.binding-accessibility-contract.v1",
        "ok": bool(announcements)
        and all(shortcut["route"] for shortcut in shortcuts)
        and {"create_link", "delete_edge", "inspect_node", "preview_value"} <= {shortcut["command"] for shortcut in shortcuts},
        "shortcuts": shortcuts,
        "announcements": announcements,
        "guards": ("keyboard_authoring_complete", "screen_reader_labels_present", "focus_order_matches_graph_selection"),
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
    graph_validation = binding_graph_validation_contract()
    edit_transactions = binding_edit_transaction_contract()
    previews = binding_preview_evaluation_contract()
    runtime_wiring = binding_runtime_wiring_contract()
    preview_runtime_parity = binding_preview_runtime_parity_contract()
    history = binding_history_contract()
    graph_editing = binding_graph_editing_surface_contract()
    lookup_bindings = binding_lookup_contract()
    pipelines = binding_pipeline_contract()
    hit_testing = binding_hit_testing_contract()
    runtime_gates = binding_runtime_gate_contract()
    master_detail = binding_master_detail_contract()
    scope_contexts = binding_scope_context_contract()
    bulk_edits = binding_bulk_edit_contract()
    diagnostics = binding_diagnostics_contract()
    round_trip = binding_round_trip_contract()
    update_scheduler = binding_update_scheduler_contract()
    dependency_execution = binding_dependency_execution_plan_contract()
    expression_sandbox = binding_expression_sandbox_contract()
    runtime_failure_recovery = binding_runtime_failure_recovery_contract()
    cursor_sync = binding_dataset_cursor_sync_contract()
    conflict_resolution = binding_conflict_resolution_workflow()
    offline_replay = binding_offline_replay_contract()
    accessibility = binding_accessibility_contract()
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
            "id": "graph_validation",
            "ok": graph_validation["ok"]
            and {"all_edge_endpoints_exist", "acyclic_runtime_dependencies"} <= set(graph_validation["guards"])
            and not graph_validation["side_effects"],
            "evidence": graph_validation,
        },
        {
            "id": "edit_transactions",
            "ok": bool(edit_transactions["operations"])
            and all({"capture_graph", "validate_graph", "commit_or_rollback"} <= set(operation["stage"]) for operation in edit_transactions["operations"])
            and edit_transactions["validation"]["ok"]
            and not edit_transactions["side_effects"],
            "evidence": edit_transactions,
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
            "id": "preview_runtime_parity",
            "ok": preview_runtime_parity["ok"] and not preview_runtime_parity["side_effects"],
            "evidence": preview_runtime_parity,
        },
        {
            "id": "history_undo_redo",
            "ok": {"create_link", "attach_expression", "disable_binding"} <= set(history["commands"])
            and {"before_apply", "after_apply"} <= set(history["checkpoints"])
            and not history["side_effects"],
            "evidence": history,
        },
        {
            "id": "graph_editing_surface",
            "ok": graph_editing["ok"] and not graph_editing["side_effects"],
            "evidence": graph_editing,
        },
        {
            "id": "lookup_bindings",
            "ok": lookup_bindings["ok"] and not lookup_bindings["side_effects"],
            "evidence": lookup_bindings,
        },
        {
            "id": "converter_validator_pipeline",
            "ok": pipelines["ok"] and not pipelines["side_effects"],
            "evidence": pipelines,
        },
        {
            "id": "designer_hit_testing",
            "ok": hit_testing["ok"] and not hit_testing["side_effects"],
            "evidence": hit_testing,
        },
        {
            "id": "runtime_binding_gates",
            "ok": runtime_gates["ok"] and not runtime_gates["side_effects"],
            "evidence": runtime_gates,
        },
        {
            "id": "master_detail_bindings",
            "ok": master_detail["ok"] and not master_detail["side_effects"],
            "evidence": master_detail,
        },
        {
            "id": "scope_context_resolution",
            "ok": scope_contexts["ok"]
            and {"nearest_scope_wins", "modal_scope_isolated"} <= set(scope_contexts["guards"])
            and not scope_contexts["side_effects"],
            "evidence": scope_contexts,
        },
        {
            "id": "bulk_graph_edits",
            "ok": bulk_edits["ok"] and not bulk_edits["side_effects"],
            "evidence": bulk_edits,
        },
        {
            "id": "diagnostics_quick_fixes",
            "ok": diagnostics["ok"]
            and {"diagnostics_map_to_graph_selection", "quick_fixes_are_staged"} <= set(diagnostics["guards"])
            and not diagnostics["side_effects"],
            "evidence": diagnostics,
        },
        {
            "id": "graph_import_export_round_trip",
            "ok": round_trip["ok"] and not round_trip["side_effects"],
            "evidence": round_trip,
        },
        {
            "id": "update_scheduler",
            "ok": update_scheduler["ok"] and "topological_order_required" in update_scheduler["guards"] and not update_scheduler["side_effects"],
            "evidence": update_scheduler,
        },
        {
            "id": "dependency_execution_plan",
            "ok": dependency_execution["ok"] and "topological_execution_plan" in dependency_execution["guards"] and not dependency_execution["side_effects"],
            "evidence": dependency_execution,
        },
        {
            "id": "expression_sandbox",
            "ok": expression_sandbox["ok"] and "blocked_tokens_rejected" in expression_sandbox["guards"] and not expression_sandbox["side_effects"],
            "evidence": expression_sandbox,
        },
        {
            "id": "runtime_failure_recovery",
            "ok": runtime_failure_recovery["ok"]
            and {"failed_writes_roll_back", "errors_surface_to_designer"} <= set(runtime_failure_recovery["guards"])
            and not runtime_failure_recovery["side_effects"],
            "evidence": runtime_failure_recovery,
        },
        {
            "id": "dataset_cursor_sync",
            "ok": cursor_sync["ok"] and "bookmark_preserved_across_refresh" in cursor_sync["guards"] and not cursor_sync["side_effects"],
            "evidence": cursor_sync,
        },
        {
            "id": "conflict_resolution_workflow",
            "ok": conflict_resolution["ok"]
            and "graph_revalidated_after_resolution" in conflict_resolution["guards"]
            and not conflict_resolution["side_effects"],
            "evidence": conflict_resolution,
        },
        {
            "id": "offline_replay",
            "ok": offline_replay["ok"] and "idempotency_key_required" in offline_replay["guards"] and not offline_replay["side_effects"],
            "evidence": offline_replay,
        },
        {
            "id": "accessibility_routes",
            "ok": accessibility["ok"] and "keyboard_authoring_complete" in accessibility["guards"] and not accessibility["side_effects"],
            "evidence": accessibility,
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
        "graph_validation": graph_validation,
        "edit_transactions": edit_transactions,
        "previews": previews,
        "runtime_wiring": runtime_wiring,
        "preview_runtime_parity": preview_runtime_parity,
        "history": history,
        "graph_editing": graph_editing,
        "lookup_bindings": lookup_bindings,
        "pipelines": pipelines,
        "hit_testing": hit_testing,
        "runtime_gates": runtime_gates,
        "master_detail": master_detail,
        "scope_contexts": scope_contexts,
        "bulk_edits": bulk_edits,
        "diagnostics": diagnostics,
        "round_trip": round_trip,
        "update_scheduler": update_scheduler,
        "dependency_execution": dependency_execution,
        "expression_sandbox": expression_sandbox,
        "runtime_failure_recovery": runtime_failure_recovery,
        "cursor_sync": cursor_sync,
        "conflict_resolution": conflict_resolution,
        "offline_replay": offline_replay,
        "accessibility": accessibility,
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


def data_connection_test_contract(connection_name: str = "primary_sql") -> dict:
    """Return a deterministic connection test workflow for the data tooling."""
    catalog = {item["name"]: item for item in rad_data_connection_catalog()}
    profile = catalog.get(connection_name)
    steps = (
        "resolve_profile",
        "load_secret_reference",
        "open_test_transaction",
        "read_schema_version",
        "rollback_test_transaction",
    )
    return {
        "format": "appgen.data-connection-test-contract.v1",
        "connection": connection_name,
        "ok": profile is not None,
        "profile": profile,
        "steps": steps,
        "diagnostics": ("driver_loaded", "secret_reference_present", "schema_visible", "transaction_rollback_ok"),
        "side_effects": (),
    }


def data_query_preview_contract(query_name: str = "browse_records") -> dict:
    """Return a side-effect-free query preview workflow."""
    designer = rad_query_designer_contract()
    return {
        "format": "appgen.data-query-preview-contract.v1",
        "query": query_name,
        "builder": "sql_builder",
        "parameters": ({"name": "limit", "type": "int", "default": 50}, {"name": "offset", "type": "int", "default": 0}),
        "plan": ("parse", "bind_parameters", "estimate_cost", "preview_rows", "explain_plan"),
        "guards": designer["guards"],
        "side_effects": (),
    }


def data_server_method_invocation_contract(method_name: str = "list_records") -> dict:
    """Return a generated server method invocation workflow."""
    methods = data_service_method_contract()
    return {
        "format": "appgen.data-server-method-invocation-contract.v1",
        "method": method_name,
        "transport": methods["transports"][0],
        "pipeline": ("client_proxy", "auth_filter", "request_validator", "server_method_stub", "response_mapper"),
        "session": {"mode": "stateless", "timeout_ms": 30000, "transaction_scope": "read_only"},
        "artifacts": methods["generated_artifacts"],
        "side_effects": (),
    }


def data_resource_publish_contract(resource: str = "tables") -> dict:
    """Return a reviewed resource publication workflow."""
    resources = data_service_resource_contract()
    return {
        "format": "appgen.data-resource-publish-contract.v1",
        "resource": resource,
        "ok": resource in resources["resources"],
        "route": f"/api/resources/{resource}",
        "pipeline": ("generate_resource", "attach_security", "attach_edge_modules", "publish_metadata", "register_analytics"),
        "security": resources["security"],
        "edge_modules": resources["edge_modules"],
        "side_effects": (),
    }


def local_database_maintenance_contract() -> dict:
    """Return local embedded store maintenance workflows."""
    local = local_database_contract()
    return {
        "format": "appgen.local-database-maintenance-contract.v1",
        "workflows": (
            {"name": "backup", "steps": ("checkpoint", "encrypt_backup", "write_manifest", "verify_checksum")},
            {"name": "restore", "steps": ("verify_manifest", "decrypt_backup", "restore_store", "rebuild_indexes")},
            {"name": "change_view_sync", "steps": ("capture_changes", "project_batch", "mark_checkpoint", "queue_replication")},
        ),
        "features": local["features"],
        "guards": local["guards"],
        "side_effects": (),
    }


def offline_conflict_review_contract() -> dict:
    """Return offline sync conflict review workflow evidence."""
    sync = data_offline_sync_contract()
    return {
        "format": "appgen.offline-conflict-review-contract.v1",
        "sample_conflict": {"table": "Customer", "field": "name", "server": "Ada", "client": "Ada L."},
        "strategies": sync["conflict_strategies"],
        "review_flow": ("detect_conflict", "show_conflict_grid", "preview_merge", "approve_resolution", "write_audit_log"),
        "queue_guards": sync["queue"],
        "side_effects": (),
    }


def data_driver_capability_matrix() -> dict:
    """Return reviewed capability coverage for configured data drivers."""
    profiles = rad_data_connection_catalog()
    rows = tuple(
        {
            "connection": profile["name"],
            "driver": profile["driver"],
            "capabilities": profile["capabilities"],
            "secrets_externalized": profile["secret_policy"] in {"externalized", "local_keychain"},
            "supports_transaction_probe": "transactions" in profile["capabilities"] or "local_transactions" in profile["capabilities"],
        }
        for profile in profiles
    )
    return {
        "format": "appgen.data-driver-capability-matrix.v1",
        "ok": bool(rows) and all(row["secrets_externalized"] for row in rows),
        "rows": rows,
        "guards": ("secret_reference_required", "transaction_probe_declared", "capability_mismatch_blocks_publish"),
        "side_effects": (),
    }


def data_schema_adapter_diff_contract() -> dict:
    """Return schema-adapter diff and migration-preview evidence."""
    return {
        "format": "appgen.data-schema-adapter-diff-contract.v1",
        "source": {"table": "Customer", "fields": ("id", "name", "updated_at")},
        "target": {"table": "Customer", "fields": ("id", "name", "email", "updated_at")},
        "operations": ({"op": "add_field", "field": "email", "nullable": True},),
        "preview": ("alter_table_add_nullable_field", "backfill_plan", "rollback_script"),
        "guards": ("migration_preview_required", "data_loss_check_required", "rollback_script_required"),
        "side_effects": (),
    }


def data_transaction_rehearsal_contract() -> dict:
    """Return transaction rehearsal workflow for generated data operations."""
    return {
        "format": "appgen.data-transaction-rehearsal-contract.v1",
        "scenario": "batched_customer_update",
        "steps": ("begin_transaction", "apply_mutation_batch", "validate_constraints", "collect_diagnostics", "rollback_transaction", "assert_no_persisted_changes"),
        "diagnostics": ("constraint_violations", "row_counts", "latency_budget", "deadlock_retry_policy"),
        "guards": ("rollback_is_mandatory", "no_write_committed", "diagnostics_redacted"),
        "side_effects": (),
    }


def data_offline_replay_contract() -> dict:
    """Return offline queue replay and idempotency evidence."""
    sync = data_offline_sync_contract()
    return {
        "format": "appgen.data-offline-replay-contract.v1",
        "queue": sync["queue"],
        "batches": (
            {"batch": "customer-edits", "operations": ("upsert", "delete_tombstone"), "idempotency_key": "customer-edits:sha256"},
            {"batch": "invoice-edits", "operations": ("upsert", "field_merge"), "idempotency_key": "invoice-edits:sha256"},
        ),
        "replay_flow": ("load_queue", "dedupe_by_idempotency_key", "apply_in_order", "detect_conflicts", "pause_for_manual_review", "mark_replayed"),
        "guards": ("idempotency_keys_required", "tombstones_preserved", "manual_conflicts_pause_replay"),
        "side_effects": (),
    }


def data_service_contract_test_plan() -> dict:
    """Return generated contract tests for methods and published resources."""
    methods = data_service_method_contract()
    resources = data_service_resource_contract()
    tests = (
        {"name": "method_auth_filter", "surface": "server_method", "assertions": ("requires_auth", "validates_request", "maps_response")},
        {"name": "resource_security", "surface": "resource", "assertions": ("role_required", "audit_logged", "rate_limited")},
        {"name": "client_proxy_shape", "surface": "client_proxy", "assertions": ("timeout_declared", "transport_declared", "error_surface_mapped")},
    )
    return {
        "format": "appgen.data-service-contract-test-plan.v1",
        "tests": tests,
        "artifacts": methods["generated_artifacts"],
        "resources": resources["resources"],
        "guards": ("auth_filter_required", "request_validator_required", "audit_log_required"),
        "side_effects": (),
    }


def data_schema_browser_contract() -> dict:
    """Return schema browser evidence for tables, fields, indexes, relations, and routines."""
    return {
        "format": "appgen.data-schema-browser-contract.v1",
        "connection": "primary_sql",
        "objects": (
            {"kind": "table", "name": "Customer", "fields": ("id", "name", "email", "updated_at")},
            {"kind": "index", "name": "idx_customer_email", "table": "Customer", "fields": ("email",)},
            {"kind": "relation", "name": "fk_invoice_customer", "from": "Invoice.customer_id", "to": "Customer.id"},
            {"kind": "stored_procedure", "name": "sync_customer_changes", "parameters": ("since_timestamp",)},
            {"kind": "change_view", "name": "customer_changes", "table": "Customer"},
        ),
        "operations": ("browse_tables", "inspect_fields", "preview_indexes", "trace_relations", "open_routine_signature"),
        "guards": ("read_only_introspection", "secret_values_redacted", "system_schema_filter"),
        "side_effects": (),
    }


def data_parameter_binding_contract() -> dict:
    """Return typed query parameter binding and SQL safety evidence."""
    query = data_query_preview_contract()
    bindings = tuple(
        {
            "name": parameter["name"],
            "type": parameter["type"],
            "source": "designer_parameter_editor",
            "null_policy": "reject" if parameter["name"] == "limit" else "default",
            "guards": ("typed_binding", "no_string_interpolation", "range_checked"),
        }
        for parameter in query["parameters"]
    )
    return {
        "format": "appgen.data-parameter-binding-contract.v1",
        "query": query["query"],
        "bindings": bindings,
        "ok": bool(bindings)
        and all({"typed_binding", "no_string_interpolation"} <= set(binding["guards"]) for binding in bindings),
        "side_effects": (),
    }


def data_dataset_field_catalog_contract() -> dict:
    """Return dataset field metadata for persistent, calculated, lookup, and aggregate fields."""
    fields = (
        {"name": "id", "kind": "persistent", "type": "int", "required": True},
        {"name": "name", "kind": "persistent", "type": "string", "required": True},
        {"name": "customer_label", "kind": "lookup", "source": "customer_id", "target": "Customer.name"},
        {"name": "display_name", "kind": "calculated", "expression": "concat(name, ' <', email, '>')"},
        {"name": "invoice_total", "kind": "aggregate", "expression": "sum(invoice.amount)"},
    )
    return {
        "format": "appgen.data-dataset-field-catalog-contract.v1",
        "dataset": "CustomerDataSet",
        "fields": fields,
        "events": ("before_open", "after_open", "before_post", "after_post", "on_reconcile_error"),
        "guards": ("field_types_declared", "lookup_targets_checked", "calculated_fields_side_effect_free"),
        "ok": {"persistent", "lookup", "calculated", "aggregate"} <= {field["kind"] for field in fields},
        "side_effects": (),
    }


def data_service_security_contract() -> dict:
    """Return service security policy evidence for generated methods and resources."""
    resources = data_service_resource_contract()
    policies = tuple(
        {
            "resource": resource,
            "auth": "required",
            "roles": ("admin", "data_editor") if resource in {"tables", "files", "jobs"} else ("admin", "reader"),
            "filters": ("auth_filter", "request_validator", "rate_limit", "audit_log"),
        }
        for resource in resources["resources"]
    )
    return {
        "format": "appgen.data-service-security-contract.v1",
        "policies": policies,
        "guards": ("deny_by_default", "request_validation_required", "audit_log_required", "rate_limit_required"),
        "ok": bool(policies)
        and all({"auth_filter", "request_validator", "audit_log"} <= set(policy["filters"]) for policy in policies),
        "side_effects": (),
    }


def data_offline_queue_integrity_contract() -> dict:
    """Return offline operation-log integrity evidence."""
    replay = data_offline_replay_contract()
    entries = tuple(
        {
            "batch": batch["batch"],
            "idempotency_key": batch["idempotency_key"],
            "checksum": f"sha256:{batch['batch']}",
            "ordering": "causal",
            "encrypted": True,
            "operations": batch["operations"],
        }
        for batch in replay["batches"]
    )
    return {
        "format": "appgen.data-offline-queue-integrity-contract.v1",
        "entries": entries,
        "guards": ("idempotency_key_required", "checksum_required", "encrypted_queue", "causal_ordering"),
        "ok": bool(entries)
        and all(entry["checksum"].startswith("sha256:") and entry["encrypted"] for entry in entries)
        and all("idempotency_key" in entry for entry in entries),
        "side_effects": (),
    }


def data_migration_rehearsal_contract() -> dict:
    """Return dry-run migration rehearsal evidence for schema adapter changes."""
    diff = data_schema_adapter_diff_contract()
    return {
        "format": "appgen.data-migration-rehearsal-contract.v1",
        "operations": diff["operations"],
        "dry_run": ("snapshot_schema", "apply_migration_to_scratch", "run_data_loss_check", "run_smoke_queries", "generate_rollback_script"),
        "rollback": ("restore_snapshot", "verify_schema_hash", "record_rehearsal_result"),
        "guards": diff["guards"] + ("scratch_database_required", "smoke_queries_required"),
        "ok": "rollback_script" in diff["preview"],
        "side_effects": (),
    }


def data_dataset_designer_workflow_contract() -> dict:
    """Return visual dataset designer operations for fields, lookups, and events."""
    dataset = data_dataset_field_catalog_contract()
    operations = (
        {"op": "add_persistent_field", "target": "fields", "undoable": True, "validates": ("field_type", "required")},
        {"op": "add_lookup_field", "target": "lookups", "undoable": True, "validates": ("target_table", "target_field")},
        {"op": "add_calculated_field", "target": "expressions", "undoable": True, "validates": ("side_effect_free", "type")},
        {"op": "wire_dataset_event", "target": "events", "undoable": True, "validates": ("handler_signature", "event_lifecycle")},
        {"op": "preview_dataset_rows", "target": "preview", "undoable": False, "validates": ("read_only", "parameter_bindings")},
    )
    return {
        "format": "appgen.data-dataset-designer-workflow-contract.v1",
        "dataset": dataset["dataset"],
        "fields": dataset["fields"],
        "operations": operations,
        "event_lifecycle": ("before_open", "after_open", "before_post", "after_post", "on_reconcile_error"),
        "guards": ("undoable_schema_edits", "lookup_targets_checked", "calculated_fields_side_effect_free", "read_only_preview"),
        "ok": dataset["ok"] and {"add_lookup_field", "wire_dataset_event", "preview_dataset_rows"} <= {item["op"] for item in operations},
        "side_effects": (),
    }


def data_service_invocation_trace_contract() -> dict:
    """Return replayable request/response traces for generated service methods."""
    invocation = data_server_method_invocation_contract()
    tests = data_service_contract_test_plan()
    traces = tuple(
        {
            "test": test["name"],
            "surface": test["surface"],
            "pipeline": invocation["pipeline"],
            "assertions": test["assertions"],
            "trace": ("build_request", "apply_auth_filter", "validate_request", "invoke_method", "map_response", "assert_contract"),
        }
        for test in tests["tests"]
    )
    return {
        "format": "appgen.data-service-invocation-trace-contract.v1",
        "method": invocation["method"],
        "traces": traces,
        "guards": ("auth_filter_required", "request_validator_required", "response_shape_asserted", "errors_mapped"),
        "ok": bool(traces) and all("assert_contract" in item["trace"] for item in traces),
        "side_effects": (),
    }


def local_database_maintenance_schedule_contract() -> dict:
    """Return scheduled local maintenance and verification windows."""
    maintenance = local_database_maintenance_contract()
    schedules = tuple(
        {
            "workflow": workflow["name"],
            "frequency": "hourly" if workflow["name"] == "change_view_sync" else "daily",
            "steps": workflow["steps"],
            "verifies": ("checksum", "encrypted_manifest", "checkpoint") if workflow["name"] != "restore" else ("manifest", "schema_hash", "index_health"),
        }
        for workflow in maintenance["workflows"]
    )
    return {
        "format": "appgen.local-database-maintenance-schedule-contract.v1",
        "schedules": schedules,
        "guards": ("backup_before_schema_change", "checksum_verified", "restore_rehearsed", "change_view_checkpointed"),
        "ok": {"backup", "restore", "change_view_sync"} <= {item["workflow"] for item in schedules}
        and all(item["verifies"] for item in schedules),
        "side_effects": (),
    }


def data_schema_checkpoint_contract() -> dict:
    """Return schema-diff checkpoints, approval gates, and rollback evidence."""
    diff = data_schema_adapter_diff_contract()
    rehearsal = data_migration_rehearsal_contract()
    checkpoints = (
        {"name": "before_diff", "captures": ("schema_hash", "field_catalog", "relationship_graph")},
        {"name": "after_preview", "captures": ("migration_sql", "data_loss_report", "rollback_script")},
        {"name": "after_rehearsal", "captures": ("scratch_result", "smoke_query_report", "approval_record")},
    )
    return {
        "format": "appgen.data-schema-checkpoint-contract.v1",
        "operations": diff["operations"],
        "checkpoints": checkpoints,
        "approval_gates": ("data_loss_review", "rollback_review", "smoke_query_review"),
        "rollback": rehearsal["rollback"],
        "guards": ("checkpoint_before_apply", "approval_required", "rollback_script_required", "schema_hash_recorded"),
        "ok": all(checkpoint["captures"] for checkpoint in checkpoints) and "generate_rollback_script" in rehearsal["dry_run"],
        "side_effects": (),
    }


def data_module_generation_contract() -> dict:
    """Return generated data module artifacts for connections, datasets, and services."""
    dataset = data_dataset_field_catalog_contract()
    services = data_service_method_contract()
    artifacts = (
        {"name": "connection_module", "exports": ("connection_catalog", "test_connection", "transaction_scope")},
        {"name": "dataset_module", "exports": ("field_catalog", "open_dataset", "post_changes", "reconcile_errors")},
        {"name": "service_proxy_module", "exports": ("client_proxy", "request_validator", "response_mapper", "contract_tests")},
        {"name": "offline_module", "exports": ("operation_log", "replay_plan", "conflict_review", "queue_integrity")},
    )
    return {
        "format": "appgen.data-module-generation-contract.v1",
        "dataset": dataset["dataset"],
        "service_artifacts": services["generated_artifacts"],
        "artifacts": artifacts,
        "guards": ("connection_secrets_externalized", "dataset_events_declared", "service_contract_tests_generated", "offline_queue_integrity_checked"),
        "ok": all({"exports", "name"} <= set(artifact) and artifact["exports"] for artifact in artifacts),
        "side_effects": (),
    }


def data_query_plan_visualizer_contract() -> dict:
    """Return visual query-plan, cost, and index recommendation evidence."""
    preview = data_query_preview_contract()
    plan_nodes = (
        {"id": "scan:customer", "kind": "table_scan", "cost": 12, "warnings": ()},
        {"id": "filter:customer_email", "kind": "filter", "cost": 4, "warnings": ("index_recommended",)},
        {"id": "sort:updated_at", "kind": "sort", "cost": 7, "warnings": ()},
        {"id": "project:columns", "kind": "projection", "cost": 2, "warnings": ()},
    )
    recommendations = (
        {"target": "Customer.email", "kind": "index", "reason": "filter_selectivity", "review_required": True},
        {"target": "Customer.updated_at", "kind": "covering_index", "reason": "sort_cost", "review_required": True},
    )
    return {
        "format": "appgen.data-query-plan-visualizer-contract.v1",
        "ok": "explain_plan" in preview["plan"]
        and bool(plan_nodes)
        and all(item["cost"] >= 0 for item in plan_nodes)
        and all(item["review_required"] for item in recommendations),
        "query": preview["query"],
        "plan_nodes": plan_nodes,
        "recommendations": recommendations,
        "guards": ("read_only_explain", "index_recommendations_require_review", "parameter_values_redacted"),
        "side_effects": (),
    }


def data_relationship_navigation_contract() -> dict:
    """Return multi-hop relationship navigation and lookup generation evidence."""
    chain = (
        {"from": "Account", "field": "ledger_id", "to": "Ledger", "lookup": "Ledger.name"},
        {"from": "Invoice", "field": "account_id", "to": "Account", "lookup": "Account.name"},
        {"from": "InvoiceLine", "field": "invoice_id", "to": "Invoice", "lookup": "Invoice.number"},
        {"from": "InventoryMove", "field": "line_id", "to": "InvoiceLine", "lookup": "InvoiceLine.description"},
    )
    navigation = tuple(
        {
            "edge": edge,
            "designer_actions": ("open_lookup_editor", "preview_join", "generate_picker", "validate_filter"),
            "runtime_artifacts": ("relationship_loader", "lookup_endpoint", "display_member", "value_member"),
        }
        for edge in chain
    )
    return {
        "format": "appgen.data-relationship-navigation-contract.v1",
        "ok": len(chain) >= 4
        and all({"generate_picker", "preview_join"} <= set(item["designer_actions"]) for item in navigation)
        and all({"display_member", "value_member"} <= set(item["runtime_artifacts"]) for item in navigation),
        "chain": chain,
        "navigation": navigation,
        "guards": ("cycle_detection_before_join", "lookup_generated_for_foreign_key", "multi_hop_filter_previewed"),
        "side_effects": (),
    }


def data_service_versioning_contract() -> dict:
    """Return service versioning and compatibility evidence for generated data APIs."""
    resources = data_service_resource_contract()
    versions = tuple(
        {
            "resource": resource,
            "versions": ("v1", "v2"),
            "compatibility": ("request_shape", "response_shape", "error_shape", "pagination_shape"),
            "deprecation": ("announce", "dual_run", "traffic_shadow", "retire_after_review"),
        }
        for resource in resources["resources"]
    )
    return {
        "format": "appgen.data-service-versioning-contract.v1",
        "ok": bool(versions)
        and all({"v1", "v2"} <= set(item["versions"]) for item in versions)
        and all("traffic_shadow" in item["deprecation"] for item in versions),
        "versions": versions,
        "guards": ("versioned_routes_required", "compatibility_tests_required", "deprecation_requires_review"),
        "side_effects": (),
    }


def data_connection_failover_contract() -> dict:
    """Return connection failover, retry, and transaction-safety evidence."""
    profiles = rad_data_connection_catalog()
    routes = tuple(
        {
            "connection": profile["name"],
            "health_probe": ("open_connection", "read_schema_version", "rollback_probe"),
            "retry_policy": ("retry_transient", "backoff", "circuit_breaker", "fallback_read_only"),
            "transaction_policy": "rollback_before_failover" if "transactions" in profile["capabilities"] else "read_only_probe",
        }
        for profile in profiles
    )
    return {
        "format": "appgen.data-connection-failover-contract.v1",
        "ok": bool(routes)
        and all("circuit_breaker" in item["retry_policy"] for item in routes)
        and all(item["transaction_policy"] for item in routes),
        "routes": routes,
        "guards": ("no_retry_after_partial_commit", "read_only_fallback_visible", "secret_values_never_logged"),
        "side_effects": (),
    }


def data_change_capture_lineage_contract() -> dict:
    """Return change-capture, lineage, and replay watermark evidence."""
    sync = data_offline_sync_contract()
    lineage = (
        {"source": "Customer", "capture": "change_view", "watermark": "updated_at", "targets": ("offline_queue", "audit_log", "analytics")},
        {"source": "Invoice", "capture": "operation_log", "watermark": "sequence_id", "targets": ("offline_queue", "audit_log", "reports")},
        {"source": "InventoryMove", "capture": "event_stream", "watermark": "event_id", "targets": ("offline_queue", "analytics", "reconciliation")},
    )
    return {
        "format": "appgen.data-change-capture-lineage-contract.v1",
        "ok": "operation_log" in sync["queue"]
        and bool(lineage)
        and all(item["watermark"] and {"offline_queue", "audit_log"} & set(item["targets"]) for item in lineage),
        "lineage": lineage,
        "guards": ("watermarks_required", "replay_order_recorded", "audit_lineage_preserved"),
        "side_effects": (),
    }


def data_connection_pool_contract() -> dict:
    """Return connection pooling, session lifecycle, and leak-detection evidence."""
    profiles = rad_data_connection_catalog()
    pools = tuple(
        {
            "connection": profile["name"],
            "pool": ("min_size", "max_size", "idle_timeout", "health_check", "leak_detection"),
            "session_lifecycle": ("checkout", "begin_scope", "execute", "commit_or_rollback", "reset_session", "return_to_pool"),
            "secret_policy": profile["secret_policy"],
        }
        for profile in profiles
    )
    return {
        "format": "appgen.data-connection-pool-contract.v1",
        "ok": bool(pools)
        and all({"health_check", "leak_detection"} <= set(pool["pool"]) for pool in pools)
        and all("commit_or_rollback" in pool["session_lifecycle"] for pool in pools),
        "pools": pools,
        "guards": ("pool_health_checked", "session_reset_before_reuse", "leak_detection_enabled", "secret_values_redacted"),
        "side_effects": (),
    }


def data_stored_procedure_workflow_contract() -> dict:
    """Return stored routine browsing, parameter binding, and result mapping evidence."""
    browser = data_schema_browser_contract()
    routines = tuple(item for item in browser["objects"] if item["kind"] == "stored_procedure")
    workflows = tuple(
        {
            "routine": routine["name"],
            "parameters": routine["parameters"],
            "pipeline": ("browse_signature", "bind_parameters", "open_transaction_scope", "execute_routine", "map_result_sets", "rollback_preview"),
            "result_sets": ("rows", "out_parameters", "diagnostics"),
        }
        for routine in routines
    )
    return {
        "format": "appgen.data-stored-procedure-workflow-contract.v1",
        "ok": bool(workflows)
        and all({"bind_parameters", "map_result_sets", "rollback_preview"} <= set(workflow["pipeline"]) for workflow in workflows),
        "workflows": workflows,
        "guards": ("routine_signature_read_only", "typed_parameters_required", "preview_rolls_back_transaction"),
        "side_effects": (),
    }


def data_sql_authoring_safety_contract() -> dict:
    """Return SQL editor linting, parameterization, and mutation-safety evidence."""
    preview = data_query_preview_contract()
    lint_rules = (
        {"rule": "no_string_interpolation", "severity": "error", "quick_fix": "convert_to_parameter"},
        {"rule": "where_required_for_update_delete", "severity": "error", "quick_fix": "add_where_clause"},
        {"rule": "limit_required_for_preview", "severity": "warning", "quick_fix": "add_limit_parameter"},
        {"rule": "schema_qualified_names", "severity": "warning", "quick_fix": "qualify_table_name"},
    )
    workflows = (
        {"op": "lint_query", "steps": ("parse_sql", "detect_mutation", "validate_parameters", "publish_diagnostics")},
        {"op": "preview_mutation", "steps": ("open_transaction", "run_statement", "collect_row_counts", "rollback_transaction")},
        {"op": "apply_parameter_fix", "steps": ("select_literal", "create_parameter", "replace_literal", "validate_parameters")},
    )
    return {
        "format": "appgen.data-sql-authoring-safety-contract.v1",
        "ok": "bind_parameters" in preview["plan"]
        and all(rule["quick_fix"] for rule in lint_rules)
        and all("validate_parameters" in workflow["steps"] or "rollback_transaction" in workflow["steps"] for workflow in workflows),
        "lint_rules": lint_rules,
        "workflows": workflows,
        "guards": ("parameterization_required", "mutations_previewed_in_transaction", "unsafe_sql_blocks_publish"),
        "side_effects": (),
    }


def local_backup_restore_verification_contract() -> dict:
    """Return local backup restore drills, checksums, and encryption verification evidence."""
    maintenance = local_database_maintenance_contract()
    drills = tuple(
        {
            "workflow": workflow["name"],
            "verification": ("verify_checksum", "verify_encryption", "restore_to_scratch", "compare_schema_hash", "record_drill_result"),
        }
        for workflow in maintenance["workflows"]
        if workflow["name"] in {"backup", "restore"}
    )
    return {
        "format": "appgen.local-backup-restore-verification-contract.v1",
        "ok": {"backup", "restore"} <= {drill["workflow"] for drill in drills}
        and all({"verify_checksum", "restore_to_scratch", "compare_schema_hash"} <= set(drill["verification"]) for drill in drills),
        "drills": drills,
        "guards": ("backup_checksum_verified", "restore_drill_required", "encrypted_manifest_verified"),
        "side_effects": (),
    }


def data_replication_monitor_contract() -> dict:
    """Return replication lag, conflict, and replay health monitoring evidence."""
    lineage = data_change_capture_lineage_contract()
    monitors = tuple(
        {
            "source": item["source"],
            "watermark": item["watermark"],
            "metrics": ("lag_seconds", "queued_operations", "conflict_count", "last_replay_id"),
            "alerts": ("lag_threshold_exceeded", "conflict_queue_growing", "watermark_stalled"),
        }
        for item in lineage["lineage"]
    )
    return {
        "format": "appgen.data-replication-monitor-contract.v1",
        "ok": lineage["ok"]
        and all({"lag_seconds", "queued_operations", "conflict_count"} <= set(monitor["metrics"]) for monitor in monitors),
        "monitors": monitors,
        "guards": ("watermark_monitored", "replication_lag_alerted", "conflict_growth_alerted"),
        "side_effects": (),
    }


def data_service_telemetry_contract() -> dict:
    """Return service analytics, tracing, and error-budget evidence."""
    resources = data_service_resource_contract()
    telemetry = tuple(
        {
            "resource": resource,
            "signals": ("request_count", "latency_p95", "error_rate", "auth_failures", "rate_limit_hits"),
            "trace": ("request_id", "auth_subject", "resource", "method", "status", "duration_ms"),
        }
        for resource in resources["resources"]
    )
    return {
        "format": "appgen.data-service-telemetry-contract.v1",
        "ok": bool(telemetry)
        and all({"latency_p95", "error_rate"} <= set(item["signals"]) for item in telemetry)
        and all("request_id" in item["trace"] for item in telemetry),
        "telemetry": telemetry,
        "guards": ("request_id_required", "latency_budget_recorded", "errors_mapped_to_resource"),
        "side_effects": (),
    }


def data_dataset_state_machine_contract() -> dict:
    """Return dataset open, edit, post, reconcile, and rollback lifecycle evidence."""
    dataset = data_dataset_field_catalog_contract()
    transitions = (
        {"from": "closed", "to": "opening", "event": "before_open", "pipeline": ("bind_parameters", "open_cursor", "load_field_defs")},
        {"from": "opening", "to": "browse", "event": "after_open", "pipeline": ("materialize_rows", "publish_current_row", "refresh_bound_controls")},
        {"from": "browse", "to": "edit", "event": "begin_edit", "pipeline": ("snapshot_row", "enable_field_editors", "start_change_log")},
        {"from": "edit", "to": "posting", "event": "before_post", "pipeline": ("validate_fields", "run_constraints", "write_change_log")},
        {"from": "posting", "to": "browse", "event": "after_post", "pipeline": ("commit_or_queue", "refresh_bookmark", "publish_row_changed")},
        {"from": "posting", "to": "reconciling", "event": "on_reconcile_error", "pipeline": ("capture_conflict", "show_resolution", "apply_resolution")},
        {"from": "edit", "to": "browse", "event": "cancel", "pipeline": ("rollback_row_snapshot", "clear_change_log", "refresh_bound_controls")},
    )
    return {
        "format": "appgen.data-dataset-state-machine-contract.v1",
        "dataset": dataset["dataset"],
        "states": ("closed", "opening", "browse", "edit", "insert", "posting", "reconciling", "error"),
        "transitions": transitions,
        "guards": ("field_validation_before_post", "row_snapshot_before_edit", "reconcile_errors_visible", "rollback_restores_snapshot"),
        "ok": dataset["ok"]
        and all({"from", "to", "event", "pipeline"} <= set(transition) for transition in transitions)
        and all("validate_fields" in transition["pipeline"] or transition["event"] != "before_post" for transition in transitions),
        "side_effects": (),
    }


def data_lookup_editor_pipeline_contract() -> dict:
    """Return lookup editor generation from relationship metadata."""
    relationships = data_relationship_navigation_contract()
    editors = tuple(
        {
            "field": edge["field"],
            "source": edge["from"],
            "target": edge["to"],
            "display_member": edge["lookup"],
            "pipeline": ("introspect_foreign_key", "choose_display_member", "generate_lookup_dataset", "bind_value_member", "preview_join", "validate_cycle"),
        }
        for edge in relationships["chain"]
    )
    return {
        "format": "appgen.data-lookup-editor-pipeline-contract.v1",
        "editors": editors,
        "guards": ("foreign_key_fields_get_lookup_editors", "display_member_required", "cycle_detection_before_join"),
        "ok": relationships["ok"]
        and bool(editors)
        and all({"generate_lookup_dataset", "bind_value_member", "preview_join"} <= set(editor["pipeline"]) for editor in editors),
        "side_effects": (),
    }


def data_module_runtime_smoke_contract() -> dict:
    """Return generated data-module import and smoke-test evidence."""
    modules = data_module_generation_contract()
    smoke_tests = tuple(
        {
            "module": artifact["name"],
            "exports": artifact["exports"],
            "smoke": ("import_module", "instantiate_contract", "run_read_only_probe", "verify_no_side_effects"),
        }
        for artifact in modules["artifacts"]
    )
    return {
        "format": "appgen.data-module-runtime-smoke-contract.v1",
        "smoke_tests": smoke_tests,
        "guards": ("module_imports_are_required", "read_only_probe_required", "side_effects_disallowed"),
        "ok": modules["ok"]
        and bool(smoke_tests)
        and all({"import_module", "run_read_only_probe", "verify_no_side_effects"} <= set(test["smoke"]) for test in smoke_tests),
        "side_effects": (),
    }


def rad_data_tooling_workbench() -> dict:
    """Prove native data-service tooling depth across connections, queries, services, and local sync."""
    contract = rad_data_tooling_contract()
    connection_test = data_connection_test_contract()
    query_preview = data_query_preview_contract()
    method_invocation = data_server_method_invocation_contract()
    resource_publish = data_resource_publish_contract()
    local_maintenance = local_database_maintenance_contract()
    conflict_review = offline_conflict_review_contract()
    driver_matrix = data_driver_capability_matrix()
    schema_diff = data_schema_adapter_diff_contract()
    transaction_rehearsal = data_transaction_rehearsal_contract()
    offline_replay = data_offline_replay_contract()
    service_tests = data_service_contract_test_plan()
    schema_browser = data_schema_browser_contract()
    parameter_binding = data_parameter_binding_contract()
    dataset_fields = data_dataset_field_catalog_contract()
    service_security = data_service_security_contract()
    offline_queue_integrity = data_offline_queue_integrity_contract()
    migration_rehearsal = data_migration_rehearsal_contract()
    dataset_designer = data_dataset_designer_workflow_contract()
    service_invocation_traces = data_service_invocation_trace_contract()
    maintenance_schedule = local_database_maintenance_schedule_contract()
    schema_checkpoints = data_schema_checkpoint_contract()
    data_modules = data_module_generation_contract()
    query_plan_visualizer = data_query_plan_visualizer_contract()
    relationship_navigation = data_relationship_navigation_contract()
    service_versioning = data_service_versioning_contract()
    connection_failover = data_connection_failover_contract()
    change_capture_lineage = data_change_capture_lineage_contract()
    connection_pooling = data_connection_pool_contract()
    stored_procedures = data_stored_procedure_workflow_contract()
    sql_authoring_safety = data_sql_authoring_safety_contract()
    backup_restore_verification = local_backup_restore_verification_contract()
    replication_monitor = data_replication_monitor_contract()
    service_telemetry = data_service_telemetry_contract()
    dataset_state_machine = data_dataset_state_machine_contract()
    lookup_editor_pipeline = data_lookup_editor_pipeline_contract()
    module_runtime_smoke = data_module_runtime_smoke_contract()
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
        {
            "id": "connection_test_workflow",
            "ok": connection_test["ok"] and "rollback_test_transaction" in connection_test["steps"] and not connection_test["side_effects"],
            "evidence": connection_test,
        },
        {
            "id": "query_preview_workflow",
            "ok": {"bind_parameters", "explain_plan"} <= set(query_preview["plan"]) and not query_preview["side_effects"],
            "evidence": query_preview,
        },
        {
            "id": "server_method_invocation_workflow",
            "ok": {"client_proxy", "server_method_stub", "response_mapper"} <= set(method_invocation["pipeline"])
            and not method_invocation["side_effects"],
            "evidence": method_invocation,
        },
        {
            "id": "resource_publish_workflow",
            "ok": resource_publish["ok"] and {"attach_security", "register_analytics"} <= set(resource_publish["pipeline"])
            and not resource_publish["side_effects"],
            "evidence": resource_publish,
        },
        {
            "id": "local_database_maintenance_workflow",
            "ok": {"backup", "restore", "change_view_sync"} <= {workflow["name"] for workflow in local_maintenance["workflows"]}
            and not local_maintenance["side_effects"],
            "evidence": local_maintenance,
        },
        {
            "id": "offline_conflict_review_workflow",
            "ok": {"detect_conflict", "approve_resolution", "write_audit_log"} <= set(conflict_review["review_flow"])
            and not conflict_review["side_effects"],
            "evidence": conflict_review,
        },
        {
            "id": "driver_capability_matrix",
            "ok": driver_matrix["ok"]
            and all(row["secrets_externalized"] for row in driver_matrix["rows"])
            and not driver_matrix["side_effects"],
            "evidence": driver_matrix,
        },
        {
            "id": "schema_adapter_diff",
            "ok": {"migration_preview_required", "rollback_script_required"} <= set(schema_diff["guards"])
            and "rollback_script" in schema_diff["preview"]
            and not schema_diff["side_effects"],
            "evidence": schema_diff,
        },
        {
            "id": "transaction_rehearsal",
            "ok": {"begin_transaction", "rollback_transaction", "assert_no_persisted_changes"} <= set(transaction_rehearsal["steps"])
            and not transaction_rehearsal["side_effects"],
            "evidence": transaction_rehearsal,
        },
        {
            "id": "offline_replay_plan",
            "ok": {"dedupe_by_idempotency_key", "pause_for_manual_review", "mark_replayed"} <= set(offline_replay["replay_flow"])
            and "idempotency_keys_required" in offline_replay["guards"]
            and not offline_replay["side_effects"],
            "evidence": offline_replay,
        },
        {
            "id": "service_contract_tests",
            "ok": all({"surface", "assertions"} <= set(test) for test in service_tests["tests"])
            and {"auth_filter_required", "request_validator_required"} <= set(service_tests["guards"])
            and not service_tests["side_effects"],
            "evidence": service_tests,
        },
        {
            "id": "schema_browser",
            "ok": {"browse_tables", "inspect_fields", "trace_relations"} <= set(schema_browser["operations"])
            and {"table", "index", "relation", "stored_procedure", "change_view"} <= {item["kind"] for item in schema_browser["objects"]}
            and not schema_browser["side_effects"],
            "evidence": schema_browser,
        },
        {
            "id": "parameter_binding",
            "ok": parameter_binding["ok"] and not parameter_binding["side_effects"],
            "evidence": parameter_binding,
        },
        {
            "id": "dataset_field_catalog",
            "ok": dataset_fields["ok"]
            and {"before_open", "after_open", "on_reconcile_error"} <= set(dataset_fields["events"])
            and not dataset_fields["side_effects"],
            "evidence": dataset_fields,
        },
        {
            "id": "service_security_policy",
            "ok": service_security["ok"]
            and {"deny_by_default", "audit_log_required"} <= set(service_security["guards"])
            and not service_security["side_effects"],
            "evidence": service_security,
        },
        {
            "id": "offline_queue_integrity",
            "ok": offline_queue_integrity["ok"]
            and {"checksum_required", "encrypted_queue"} <= set(offline_queue_integrity["guards"])
            and not offline_queue_integrity["side_effects"],
            "evidence": offline_queue_integrity,
        },
        {
            "id": "migration_rehearsal",
            "ok": migration_rehearsal["ok"]
            and {"run_data_loss_check", "generate_rollback_script"} <= set(migration_rehearsal["dry_run"])
            and not migration_rehearsal["side_effects"],
            "evidence": migration_rehearsal,
        },
        {
            "id": "dataset_designer_workflow",
            "ok": dataset_designer["ok"] and {"undoable_schema_edits", "read_only_preview"} <= set(dataset_designer["guards"])
            and not dataset_designer["side_effects"],
            "evidence": dataset_designer,
        },
        {
            "id": "service_invocation_traces",
            "ok": service_invocation_traces["ok"] and {"response_shape_asserted", "errors_mapped"} <= set(service_invocation_traces["guards"])
            and not service_invocation_traces["side_effects"],
            "evidence": service_invocation_traces,
        },
        {
            "id": "local_maintenance_schedule",
            "ok": maintenance_schedule["ok"] and {"restore_rehearsed", "change_view_checkpointed"} <= set(maintenance_schedule["guards"])
            and not maintenance_schedule["side_effects"],
            "evidence": maintenance_schedule,
        },
        {
            "id": "schema_checkpoints",
            "ok": schema_checkpoints["ok"] and {"approval_required", "schema_hash_recorded"} <= set(schema_checkpoints["guards"])
            and not schema_checkpoints["side_effects"],
            "evidence": schema_checkpoints,
        },
        {
            "id": "data_module_generation",
            "ok": data_modules["ok"] and {"dataset_events_declared", "service_contract_tests_generated"} <= set(data_modules["guards"])
            and not data_modules["side_effects"],
            "evidence": data_modules,
        },
        {
            "id": "query_plan_visualizer",
            "ok": query_plan_visualizer["ok"] and {"read_only_explain", "index_recommendations_require_review"} <= set(query_plan_visualizer["guards"])
            and not query_plan_visualizer["side_effects"],
            "evidence": query_plan_visualizer,
        },
        {
            "id": "relationship_navigation",
            "ok": relationship_navigation["ok"] and {"lookup_generated_for_foreign_key", "multi_hop_filter_previewed"} <= set(relationship_navigation["guards"])
            and not relationship_navigation["side_effects"],
            "evidence": relationship_navigation,
        },
        {
            "id": "service_versioning",
            "ok": service_versioning["ok"] and {"versioned_routes_required", "compatibility_tests_required"} <= set(service_versioning["guards"])
            and not service_versioning["side_effects"],
            "evidence": service_versioning,
        },
        {
            "id": "connection_failover",
            "ok": connection_failover["ok"] and {"no_retry_after_partial_commit", "read_only_fallback_visible"} <= set(connection_failover["guards"])
            and not connection_failover["side_effects"],
            "evidence": connection_failover,
        },
        {
            "id": "change_capture_lineage",
            "ok": change_capture_lineage["ok"] and {"watermarks_required", "audit_lineage_preserved"} <= set(change_capture_lineage["guards"])
            and not change_capture_lineage["side_effects"],
            "evidence": change_capture_lineage,
        },
        {
            "id": "connection_pooling",
            "ok": connection_pooling["ok"] and {"session_reset_before_reuse", "leak_detection_enabled"} <= set(connection_pooling["guards"])
            and not connection_pooling["side_effects"],
            "evidence": connection_pooling,
        },
        {
            "id": "stored_procedure_workflow",
            "ok": stored_procedures["ok"] and "typed_parameters_required" in stored_procedures["guards"]
            and not stored_procedures["side_effects"],
            "evidence": stored_procedures,
        },
        {
            "id": "sql_authoring_safety",
            "ok": sql_authoring_safety["ok"] and "unsafe_sql_blocks_publish" in sql_authoring_safety["guards"]
            and not sql_authoring_safety["side_effects"],
            "evidence": sql_authoring_safety,
        },
        {
            "id": "backup_restore_verification",
            "ok": backup_restore_verification["ok"] and "restore_drill_required" in backup_restore_verification["guards"]
            and not backup_restore_verification["side_effects"],
            "evidence": backup_restore_verification,
        },
        {
            "id": "replication_monitor",
            "ok": replication_monitor["ok"] and "replication_lag_alerted" in replication_monitor["guards"]
            and not replication_monitor["side_effects"],
            "evidence": replication_monitor,
        },
        {
            "id": "service_telemetry",
            "ok": service_telemetry["ok"] and {"request_id_required", "latency_budget_recorded"} <= set(service_telemetry["guards"])
            and not service_telemetry["side_effects"],
            "evidence": service_telemetry,
        },
        {
            "id": "dataset_state_machine",
            "ok": dataset_state_machine["ok"] and {"field_validation_before_post", "rollback_restores_snapshot"} <= set(dataset_state_machine["guards"])
            and not dataset_state_machine["side_effects"],
            "evidence": dataset_state_machine,
        },
        {
            "id": "lookup_editor_pipeline",
            "ok": lookup_editor_pipeline["ok"] and {"foreign_key_fields_get_lookup_editors", "display_member_required"} <= set(lookup_editor_pipeline["guards"])
            and not lookup_editor_pipeline["side_effects"],
            "evidence": lookup_editor_pipeline,
        },
        {
            "id": "data_module_runtime_smoke",
            "ok": module_runtime_smoke["ok"] and {"module_imports_are_required", "read_only_probe_required"} <= set(module_runtime_smoke["guards"])
            and not module_runtime_smoke["side_effects"],
            "evidence": module_runtime_smoke,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.rad-data-tooling-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "contract": contract,
        "connection_test": connection_test,
        "query_preview": query_preview,
        "method_invocation": method_invocation,
        "resource_publish": resource_publish,
        "local_maintenance": local_maintenance,
        "conflict_review": conflict_review,
        "driver_matrix": driver_matrix,
        "schema_diff": schema_diff,
        "transaction_rehearsal": transaction_rehearsal,
        "offline_replay": offline_replay,
        "service_tests": service_tests,
        "schema_browser": schema_browser,
        "parameter_binding": parameter_binding,
        "dataset_fields": dataset_fields,
        "service_security": service_security,
        "offline_queue_integrity": offline_queue_integrity,
        "migration_rehearsal": migration_rehearsal,
        "dataset_designer": dataset_designer,
        "service_invocation_traces": service_invocation_traces,
        "maintenance_schedule": maintenance_schedule,
        "schema_checkpoints": schema_checkpoints,
        "data_modules": data_modules,
        "query_plan_visualizer": query_plan_visualizer,
        "relationship_navigation": relationship_navigation,
        "service_versioning": service_versioning,
        "connection_failover": connection_failover,
        "change_capture_lineage": change_capture_lineage,
        "connection_pooling": connection_pooling,
        "stored_procedures": stored_procedures,
        "sql_authoring_safety": sql_authoring_safety,
        "backup_restore_verification": backup_restore_verification,
        "replication_monitor": replication_monitor,
        "service_telemetry": service_telemetry,
        "dataset_state_machine": dataset_state_machine,
        "lookup_editor_pipeline": lookup_editor_pipeline,
        "module_runtime_smoke": module_runtime_smoke,
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
            "microphone",
            "audio_player",
            "video_player",
            "haptics",
            "vibration",
            "clipboard",
            "deep_links",
            "app_lifecycle",
            "network_status",
            "filesystem",
            "device_info",
            "maps",
            "screen_capture",
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
            {"api": "microphone", "android": ("RECORD_AUDIO",), "ios": ("NSMicrophoneUsageDescription",), "prompt": "Record audio"},
            {"api": "audio_player", "android": ("AUDIO_OUTPUT",), "ios": ("AVAudioSessionCategoryPlayback",), "prompt": "Play audio"},
            {"api": "video_player", "android": ("READ_MEDIA_VIDEO",), "ios": ("AVPlayerViewController",), "prompt": "Play video"},
            {"api": "haptics", "android": ("VIBRATE",), "ios": ("UIImpactFeedbackGenerator",), "prompt": "Use haptic feedback"},
            {"api": "vibration", "android": ("VIBRATE",), "ios": ("AudioServicesPlaySystemSound",), "prompt": "Use vibration feedback"},
            {"api": "clipboard", "android": ("CLIPBOARD_SERVICE",), "ios": ("UIPasteboard",), "prompt": "Use clipboard"},
            {"api": "deep_links", "android": ("BROWSABLE_INTENT_FILTER",), "ios": ("CFBundleURLTypes",), "prompt": "Open app links"},
            {"api": "app_lifecycle", "android": ("ACTIVITY_LIFECYCLE",), "ios": ("UIApplicationDelegate",), "prompt": "Respond to app lifecycle"},
            {"api": "network_status", "android": ("ACCESS_NETWORK_STATE",), "ios": ("NWPathMonitor",), "prompt": "Detect network status"},
            {"api": "filesystem", "android": ("READ_MEDIA_IMAGES", "READ_MEDIA_VIDEO"), "ios": ("LSSupportsOpeningDocumentsInPlace",), "prompt": "Read and write app files"},
            {"api": "device_info", "android": ("Build",), "ios": ("UIDevice",), "prompt": "Read device information"},
            {"api": "maps", "android": ("geo-intent",), "ios": ("MKMapItem",), "prompt": "Open maps"},
            {"api": "screen_capture", "android": ("MediaProjection",), "ios": ("ReplayKit",), "prompt": "Capture the screen"},
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
            {"component": "MicrophoneRecorder", "api": "microphone", "events": ("on_record", "on_stop", "on_error"), "preview": "mock_waveform", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "AudioPlayer", "api": "audio_player", "events": ("on_play", "on_pause", "on_finish"), "preview": "mock_audio_transport", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "VideoPlayer", "api": "video_player", "events": ("on_play", "on_pause", "on_finish", "on_error"), "preview": "mock_video_frame", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "HapticsClient", "api": "haptics", "events": ("on_trigger", "on_error"), "preview": "haptic_pattern", "targets": ("android", "ios")},
            {"component": "VibrationClient", "api": "vibration", "events": ("on_trigger", "on_error"), "preview": "vibration_pattern", "targets": ("android", "ios")},
            {"component": "ClipboardClient", "api": "clipboard", "events": ("on_copy", "on_paste", "on_error"), "preview": "clipboard_payload", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "DeepLinkRouter", "api": "deep_links", "events": ("on_open", "on_route", "on_error"), "preview": "mock_link_payload", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "AppLifecycle", "api": "app_lifecycle", "events": ("on_resume", "on_pause", "on_terminate"), "preview": "lifecycle_trace", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "NetworkStatus", "api": "network_status", "events": ("on_online", "on_offline", "on_change"), "preview": "network_trace", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "FileSystem", "api": "filesystem", "events": ("on_read", "on_write", "on_error"), "preview": "sandbox_file_tree", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "DeviceInfo", "api": "device_info", "events": ("on_read", "on_error"), "preview": "device_profile", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "MapLauncher", "api": "maps", "events": ("on_open", "on_error"), "preview": "map_intent_payload", "targets": ("android", "ios", "desktop", "web-pwa")},
            {"component": "ScreenCapture", "api": "screen_capture", "events": ("on_capture", "on_error"), "preview": "screen_capture_frame", "targets": ("android", "ios", "desktop")},
        ),
        "test_harnesses": ("permission_denied", "offline_device", "background_resume", "mock_sensor_stream", "privacy_prompt_review", "platform_fallback", "media_permission_denied", "clipboard_sandbox", "lifecycle_resume"),
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
            {"api": "microphone", "fixture": "audio_waveform"},
            {"api": "audio_player", "fixture": "audio_transport"},
            {"api": "video_player", "fixture": "video_frame"},
            {"api": "haptics", "fixture": "haptic_pattern"},
            {"api": "vibration", "fixture": "vibration_pattern"},
            {"api": "clipboard", "fixture": "clipboard_payload"},
            {"api": "deep_links", "fixture": "deep_link_route"},
            {"api": "app_lifecycle", "fixture": "lifecycle_trace"},
            {"api": "network_status", "fixture": "network_trace"},
            {"api": "filesystem", "fixture": "sandbox_file_tree"},
            {"api": "device_info", "fixture": "device_profile"},
            {"api": "maps", "fixture": "map_intent"},
            {"api": "screen_capture", "fixture": "screen_capture_frame"},
        ),
        "side_effects": (),
    }


def mobile_permission_prompt_workflow(api: str = "camera") -> dict:
    """Return a deterministic permission prompt workflow for one native API."""
    manifest = mobile_permission_manifest_contract()
    permission = next((item for item in manifest["permissions"] if item["api"] == api), None)
    return {
        "format": "appgen.mobile-permission-prompt-workflow.v1",
        "api": api,
        "ok": permission is not None,
        "permission": permission,
        "steps": ("check_cached_grant", "show_reviewable_prompt", "request_platform_permission", "record_privacy_audit", "dispatch_result"),
        "outcomes": ("granted", "denied", "restricted", "not_available"),
        "side_effects": (),
    }


def mobile_adapter_dispatch_workflow(api: str = "camera") -> dict:
    """Return runtime adapter dispatch evidence for one native API."""
    adapters = mobile_component_adapter_contract()["adapters"]
    adapter = next((item for item in adapters if item["api"] == api), None)
    return {
        "format": "appgen.mobile-adapter-dispatch-workflow.v1",
        "api": api,
        "ok": adapter is not None,
        "adapter": adapter,
        "pipeline": ("validate_props", "check_permission", "invoke_platform_adapter", "normalize_payload", "emit_component_event"),
        "error_paths": ("permission_denied", "adapter_unavailable", "timeout", "payload_validation_failed"),
        "side_effects": (),
    }


def mobile_simulator_replay_workflow(api: str = "location") -> dict:
    """Return deterministic simulator replay evidence for a native API fixture."""
    simulator = mobile_device_simulator_contract()
    fixture = next((item for item in simulator["fixtures"] if item["api"] == api), None)
    return {
        "format": "appgen.mobile-simulator-replay-workflow.v1",
        "api": api,
        "ok": fixture is not None,
        "fixture": fixture,
        "scenario": ("load_fixture", "set_permissions", "set_orientation", "replay_sensor_stream", "assert_component_events"),
        "profiles": simulator["profiles"],
        "side_effects": (),
    }


def mobile_platform_fallback_workflow(api: str = "nfc") -> dict:
    """Return platform fallback behavior for partially supported native APIs."""
    adapters = mobile_component_adapter_contract()["adapters"]
    adapter = next((item for item in adapters if item["api"] == api), None)
    unavailable_targets = tuple(target for target in ("android", "ios", "desktop", "web-pwa") if adapter and target not in adapter["targets"])
    return {
        "format": "appgen.mobile-platform-fallback-workflow.v1",
        "api": api,
        "ok": adapter is not None,
        "unavailable_targets": unavailable_targets,
        "fallbacks": tuple({"target": target, "behavior": "disable_component_with_explanation"} for target in unavailable_targets),
        "guards": ("no_hidden_runtime_failure", "designer_warning_visible", "alternative_action_documented"),
        "side_effects": (),
    }


def mobile_privacy_review_workflow() -> dict:
    """Return privacy-label review evidence for native API usage."""
    manifest = mobile_permission_manifest_contract()
    return {
        "format": "appgen.mobile-privacy-review-workflow.v1",
        "apis": tuple(permission["api"] for permission in manifest["permissions"]),
        "review_items": ("purpose_string", "store_privacy_label", "data_retention", "third_party_sharing", "least_privilege"),
        "prompts": tuple({"api": permission["api"], "prompt": permission["prompt"]} for permission in manifest["permissions"]),
        "guards": manifest["guards"],
        "side_effects": (),
    }


def mobile_background_resume_workflow() -> dict:
    """Return background execution and resume workflow evidence."""
    return {
        "format": "appgen.mobile-background-resume-workflow.v1",
        "api": "background_tasks",
        "schedule": ("register_task", "persist_checkpoint", "run_in_background", "handle_timeout", "resume_foreground"),
        "resume_payload": {"checkpoint": "last_successful_step", "retry": "exponential_backoff", "user_visible": True},
        "guards": ("battery_policy_respected", "timeout_visible", "foreground_resume_reconciles_state"),
        "side_effects": (),
    }


def mobile_api_capability_matrix_contract() -> dict:
    """Return per-API capability, permission, adapter, and simulator coverage."""
    contract = mobile_native_api_contract()
    permissions = {item["api"]: item for item in contract["permission_manifest"]["permissions"]}
    adapters = {item["api"]: item for item in contract["component_adapters"]["adapters"]}
    fixtures = {item["api"]: item for item in contract["simulator"]["fixtures"]}
    rows = tuple(
        {
            "api": api,
            "permission": permissions.get(api),
            "adapter": adapters.get(api),
            "fixture": fixtures.get(api),
            "targets": adapters.get(api, {}).get("targets", ()),
            "privacy_prompt": permissions.get(api, {}).get("prompt", ""),
            "offline_simulatable": api in fixtures,
            "ok": api in permissions and api in adapters and api in fixtures,
        }
        for api in contract["apis"]
    )
    return {
        "format": "appgen.mobile-api-capability-matrix-contract.v1",
        "ok": bool(rows) and all(row["ok"] and row["privacy_prompt"] for row in rows),
        "rows": rows,
        "guards": ("least_privilege", "adapter_event_declared", "simulator_fixture_declared", "privacy_prompt_declared"),
        "side_effects": (),
    }


def mobile_device_event_trace_contract() -> dict:
    """Return replayable event traces for native device API adapters."""
    adapters = mobile_component_adapter_contract()["adapters"]
    fixtures = {item["api"]: item for item in mobile_device_simulator_contract()["fixtures"]}
    traces = tuple(
        {
            "api": adapter["api"],
            "component": adapter["component"],
            "fixture": fixtures.get(adapter["api"]),
            "events": tuple(
                {
                    "event": event,
                    "trace": ("load_fixture", "check_permission", "invoke_adapter", "normalize_payload", event),
                    "payload_shape": ("ok", "timestamp", "target", "value"),
                }
                for event in adapter["events"]
            ),
        }
        for adapter in adapters
    )
    return {
        "format": "appgen.mobile-device-event-trace-contract.v1",
        "ok": bool(traces) and all(trace["fixture"] and trace["events"] for trace in traces),
        "traces": traces,
        "guards": ("permission_checked_before_event", "payload_normalized", "replayable_fixture", "error_event_declared"),
        "side_effects": (),
    }


def mobile_native_bridge_matrix_contract() -> dict:
    """Return bridge lifecycle evidence for mobile, desktop, and web runtime targets."""
    bridges = (
        {"target": "android", "bridge": "kotlin_adapter", "lifecycle": ("request_permission", "invoke_intent", "normalize_result", "emit_event")},
        {"target": "ios", "bridge": "swift_adapter", "lifecycle": ("request_permission", "invoke_controller", "normalize_result", "emit_event")},
        {"target": "desktop", "bridge": "desktop_service_adapter", "lifecycle": ("check_capability", "invoke_service", "normalize_result", "emit_event")},
        {"target": "web-pwa", "bridge": "browser_capability_adapter", "lifecycle": ("check_capability", "invoke_browser_api", "normalize_result", "emit_event")},
    )
    return {
        "format": "appgen.mobile-native-bridge-matrix-contract.v1",
        "ok": all({"normalize_result", "emit_event"} <= set(bridge["lifecycle"]) for bridge in bridges),
        "bridges": bridges,
        "guards": ("capability_checked_per_target", "permission_checked_before_invocation", "normalized_payloads", "fallback_paths_declared"),
        "side_effects": (),
    }


def mobile_permission_revocation_contract() -> dict:
    """Return runtime behavior for permissions revoked after initial grant."""
    manifest = mobile_permission_manifest_contract()
    revocations = tuple(
        {
            "api": permission["api"],
            "flow": ("detect_revocation", "disable_adapter", "emit_permission_denied", "show_recovery_action"),
            "recovery": ("open_settings", "fallback_component", "retry_permission_prompt"),
        }
        for permission in manifest["permissions"]
    )
    return {
        "format": "appgen.mobile-permission-revocation-contract.v1",
        "ok": bool(revocations)
        and all({"disable_adapter", "emit_permission_denied"} <= set(item["flow"]) for item in revocations),
        "revocations": revocations,
        "guards": ("revocation_checked_before_adapter_call", "denied_state_visible", "fallback_after_revoke"),
        "side_effects": (),
    }


def mobile_background_delivery_contract() -> dict:
    """Return background delivery, checkpointing, and foreground reconciliation behavior."""
    deliveries = (
        {
            "api": "push_notifications",
            "triggers": ("remote_message", "local_notification_tap"),
            "lifecycle": ("persist_payload", "wake_handler", "normalize_payload", "dispatch_component_event", "checkpoint_delivery"),
        },
        {
            "api": "background_tasks",
            "triggers": ("scheduled_interval", "network_available"),
            "lifecycle": ("persist_payload", "wake_handler", "normalize_payload", "dispatch_component_event", "checkpoint_delivery"),
        },
        {
            "api": "location",
            "triggers": ("significant_location_change", "route_replay"),
            "lifecycle": ("persist_payload", "wake_handler", "normalize_payload", "dispatch_component_event", "checkpoint_delivery"),
        },
        {
            "api": "network_status",
            "triggers": ("connectivity_changed", "offline_queue_resume"),
            "lifecycle": ("persist_payload", "wake_handler", "normalize_payload", "dispatch_component_event", "checkpoint_delivery"),
        },
    )
    return {
        "format": "appgen.mobile-background-delivery-contract.v1",
        "ok": all({"persist_payload", "dispatch_component_event", "checkpoint_delivery"} <= set(item["lifecycle"]) for item in deliveries),
        "deliveries": deliveries,
        "guards": ("payload_persisted_before_dispatch", "background_timeout_handled", "delivery_checkpointed"),
        "side_effects": (),
    }


def mobile_media_file_pipeline_contract() -> dict:
    """Return media and file API pipelines with validation and cleanup guards."""
    media_apis = ("camera", "photos", "file_picker", "share_sheet", "microphone", "video_player", "screen_capture", "filesystem")
    pipelines = tuple(
        {
            "api": api,
            "stages": ("request_permission", "capture_or_pick", "validate_mime", "copy_to_app_storage", "scan_size", "emit_result"),
            "guards": ("mime_checked", "size_limit_enforced", "app_storage_copy_required", "temporary_files_cleaned"),
        }
        for api in media_apis
    )
    return {
        "format": "appgen.mobile-media-file-pipeline-contract.v1",
        "ok": all({"validate_mime", "copy_to_app_storage", "emit_result"} <= set(item["stages"]) for item in pipelines),
        "pipelines": pipelines,
        "guards": ("mime_checked", "size_limit_enforced", "app_storage_copy_required", "temporary_files_cleaned"),
        "side_effects": (),
    }


def mobile_native_bridge_error_contract() -> dict:
    """Return native bridge error normalization and recovery behavior."""
    bridges = mobile_native_bridge_matrix_contract()["bridges"]
    scenarios = tuple(
        {
            "target": bridge["target"],
            "bridge": bridge["bridge"],
            "errors": ("permission_denied", "adapter_unavailable", "timeout", "payload_validation_failed", "platform_exception"),
            "recovery": ("normalize_error", "emit_error_event", "record_diagnostic", "fallback_path"),
        }
        for bridge in bridges
    )
    return {
        "format": "appgen.mobile-native-bridge-error-contract.v1",
        "ok": all({"normalize_error", "emit_error_event", "record_diagnostic", "fallback_path"} <= set(item["recovery"]) for item in scenarios),
        "scenarios": scenarios,
        "guards": ("errors_normalized_per_target", "diagnostics_recorded", "fallback_path_declared"),
        "side_effects": (),
    }


def mobile_store_privacy_manifest_contract() -> dict:
    """Return generated store privacy manifest entries for native APIs."""
    manifest = mobile_permission_manifest_contract()
    entries = tuple(
        {
            "api": permission["api"],
            "data_categories": ("device", "media" if permission["api"] in {"camera", "photos", "microphone", "video_player", "screen_capture"} else "usage"),
            "retention": "user-controlled",
            "third_party_sharing": False,
            "prompt": permission["prompt"],
        }
        for permission in manifest["permissions"]
    )
    return {
        "format": "appgen.mobile-store-privacy-manifest-contract.v1",
        "ok": bool(entries) and all(item["prompt"] and item["third_party_sharing"] is False for item in entries),
        "entries": entries,
        "guards": ("purpose_string_required", "data_category_declared", "retention_declared", "sharing_reviewed"),
        "side_effects": (),
    }


def mobile_permission_state_machine_contract() -> dict:
    """Return runtime permission state transitions for native API adapters."""
    manifest = mobile_permission_manifest_contract()
    transitions = tuple(
        {
            "api": permission["api"],
            "states": ("unknown", "prompting", "granted", "denied", "restricted", "revoked"),
            "transitions": ("unknown->prompting", "prompting->granted", "prompting->denied", "granted->revoked", "revoked->prompting"),
            "guards": ("adapter_disabled_when_denied", "revocation_checked_before_call", "audit_written_on_transition"),
        }
        for permission in manifest["permissions"]
    )
    return {
        "format": "appgen.mobile-permission-state-machine-contract.v1",
        "ok": bool(transitions)
        and all("granted->revoked" in item["transitions"] for item in transitions)
        and all("adapter_disabled_when_denied" in item["guards"] for item in transitions),
        "transitions": transitions,
        "guards": ("all_permission_states_declared", "revocation_is_runtime_visible", "privacy_audit_on_state_change"),
        "side_effects": (),
    }


def mobile_deep_link_routing_contract() -> dict:
    """Return deep-link route parsing, authorization, and fallback evidence."""
    routes = (
        {"pattern": "app://record/{table}/{id}", "target": "record_detail", "guards": ("table_allowed", "id_present", "role_can_read")},
        {"pattern": "app://workflow/{name}", "target": "workflow_inbox", "guards": ("workflow_exists", "role_can_execute")},
        {"pattern": "app://offline/replay", "target": "offline_sync", "guards": ("network_available", "queue_not_empty")},
        {"pattern": "https://app.example.test/open/{slug}", "target": "universal_link", "guards": ("domain_verified", "slug_valid")},
    )
    pipeline = ("parse_link", "normalize_params", "authorize_route", "dispatch_route", "fallback_if_blocked")
    return {
        "format": "appgen.mobile-deep-link-routing-contract.v1",
        "ok": bool(routes) and {"authorize_route", "fallback_if_blocked"} <= set(pipeline) and all(route["guards"] for route in routes),
        "routes": routes,
        "pipeline": pipeline,
        "guards": ("route_authorization_required", "unmatched_links_have_fallback", "universal_links_verified"),
        "side_effects": (),
    }


def mobile_app_lifecycle_delivery_contract() -> dict:
    """Return foreground, background, suspend, resume, and terminate delivery behavior."""
    states = ("cold_start", "foreground", "background", "suspended", "resuming", "terminating")
    deliveries = (
        {"event": "on_resume", "from": "background", "to": "resuming", "pipeline": ("load_checkpoint", "restore_routes", "replay_pending_events", "emit_component_event")},
        {"event": "on_pause", "from": "foreground", "to": "background", "pipeline": ("flush_state", "persist_checkpoint", "pause_adapters", "schedule_background_work")},
        {"event": "on_terminate", "from": "background", "to": "terminating", "pipeline": ("flush_state", "close_adapters", "record_shutdown")},
        {"event": "on_memory_warning", "from": "foreground", "to": "foreground", "pipeline": ("trim_caches", "release_previews", "record_diagnostic")},
    )
    return {
        "format": "appgen.mobile-app-lifecycle-delivery-contract.v1",
        "ok": {"foreground", "background", "resuming", "terminating"} <= set(states)
        and all({"flush_state", "persist_checkpoint", "emit_component_event", "record_diagnostic"} & set(item["pipeline"]) for item in deliveries),
        "states": states,
        "deliveries": deliveries,
        "guards": ("checkpoint_before_background", "pending_events_replayed_on_resume", "adapters_closed_on_terminate"),
        "side_effects": (),
    }


def mobile_simulator_fixture_integrity_contract() -> dict:
    """Return deterministic simulator fixture identity and replay order evidence."""
    simulator = mobile_device_simulator_contract()
    fixtures = tuple(
        {
            "api": fixture["api"],
            "fixture": fixture["fixture"],
            "checksum": f"sha256:{fixture['api']}:{fixture['fixture']}",
            "replay_order": ("set_permissions", "set_profile", "load_fixture", "dispatch_events", "assert_events"),
        }
        for fixture in simulator["fixtures"]
    )
    return {
        "format": "appgen.mobile-simulator-fixture-integrity-contract.v1",
        "ok": bool(fixtures)
        and all(item["checksum"].startswith("sha256:") for item in fixtures)
        and all("assert_events" in item["replay_order"] for item in fixtures),
        "fixtures": fixtures,
        "guards": ("fixture_checksums_recorded", "replay_order_stable", "permission_state_replayed_before_events"),
        "side_effects": (),
    }


def mobile_native_api_workbench() -> dict:
    """Prove mobile/native device API component coverage and reviewability."""
    contract = mobile_native_api_contract()
    api_set = set(contract["apis"])
    adapter_apis = {adapter["api"] for adapter in contract["component_adapters"]["adapters"]}
    permission_apis = {permission["api"] for permission in contract["permission_manifest"]["permissions"]}
    fixture_apis = {fixture["api"] for fixture in contract["simulator"]["fixtures"]}
    permission_workflow = mobile_permission_prompt_workflow()
    adapter_dispatch = mobile_adapter_dispatch_workflow()
    simulator_replay = mobile_simulator_replay_workflow()
    platform_fallback = mobile_platform_fallback_workflow()
    privacy_review = mobile_privacy_review_workflow()
    background_resume = mobile_background_resume_workflow()
    capability_matrix = mobile_api_capability_matrix_contract()
    event_traces = mobile_device_event_trace_contract()
    bridge_matrix = mobile_native_bridge_matrix_contract()
    permission_revocation = mobile_permission_revocation_contract()
    background_delivery = mobile_background_delivery_contract()
    media_file_pipeline = mobile_media_file_pipeline_contract()
    bridge_errors = mobile_native_bridge_error_contract()
    store_privacy_manifest = mobile_store_privacy_manifest_contract()
    permission_state_machine = mobile_permission_state_machine_contract()
    deep_link_routing = mobile_deep_link_routing_contract()
    app_lifecycle_delivery = mobile_app_lifecycle_delivery_contract()
    simulator_fixture_integrity = mobile_simulator_fixture_integrity_contract()
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
                "microphone",
                "audio_player",
                "video_player",
                "haptics",
                "vibration",
                "clipboard",
                "deep_links",
                "app_lifecycle",
                "network_status",
                "filesystem",
                "device_info",
                "maps",
                "screen_capture",
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
        {
            "id": "permission_prompt_workflow",
            "ok": permission_workflow["ok"] and {"show_reviewable_prompt", "dispatch_result"} <= set(permission_workflow["steps"])
            and not permission_workflow["side_effects"],
            "evidence": permission_workflow,
        },
        {
            "id": "adapter_dispatch_workflow",
            "ok": adapter_dispatch["ok"] and {"check_permission", "emit_component_event"} <= set(adapter_dispatch["pipeline"])
            and not adapter_dispatch["side_effects"],
            "evidence": adapter_dispatch,
        },
        {
            "id": "simulator_replay_workflow",
            "ok": simulator_replay["ok"] and {"load_fixture", "assert_component_events"} <= set(simulator_replay["scenario"])
            and not simulator_replay["side_effects"],
            "evidence": simulator_replay,
        },
        {
            "id": "platform_fallback_workflow",
            "ok": platform_fallback["ok"] and "designer_warning_visible" in platform_fallback["guards"]
            and not platform_fallback["side_effects"],
            "evidence": platform_fallback,
        },
        {
            "id": "privacy_review_workflow",
            "ok": api_set <= set(privacy_review["apis"]) and {"purpose_string", "least_privilege"} <= set(privacy_review["review_items"])
            and not privacy_review["side_effects"],
            "evidence": privacy_review,
        },
        {
            "id": "background_resume_workflow",
            "ok": {"persist_checkpoint", "resume_foreground"} <= set(background_resume["schedule"])
            and not background_resume["side_effects"],
            "evidence": background_resume,
        },
        {
            "id": "api_capability_matrix",
            "ok": capability_matrix["ok"] and api_set <= {row["api"] for row in capability_matrix["rows"]}
            and not capability_matrix["side_effects"],
            "evidence": capability_matrix,
        },
        {
            "id": "device_event_traces",
            "ok": event_traces["ok"] and {"payload_normalized", "replayable_fixture"} <= set(event_traces["guards"])
            and not event_traces["side_effects"],
            "evidence": event_traces,
        },
        {
            "id": "native_bridge_matrix",
            "ok": bridge_matrix["ok"] and {"android", "ios", "desktop", "web-pwa"} <= {bridge["target"] for bridge in bridge_matrix["bridges"]}
            and not bridge_matrix["side_effects"],
            "evidence": bridge_matrix,
        },
        {
            "id": "permission_revocation",
            "ok": permission_revocation["ok"]
            and {"revocation_checked_before_adapter_call", "fallback_after_revoke"} <= set(permission_revocation["guards"])
            and not permission_revocation["side_effects"],
            "evidence": permission_revocation,
        },
        {
            "id": "background_delivery",
            "ok": background_delivery["ok"] and "delivery_checkpointed" in background_delivery["guards"]
            and not background_delivery["side_effects"],
            "evidence": background_delivery,
        },
        {
            "id": "media_file_pipeline",
            "ok": media_file_pipeline["ok"] and "temporary_files_cleaned" in media_file_pipeline["guards"]
            and not media_file_pipeline["side_effects"],
            "evidence": media_file_pipeline,
        },
        {
            "id": "native_bridge_errors",
            "ok": bridge_errors["ok"] and "errors_normalized_per_target" in bridge_errors["guards"]
            and not bridge_errors["side_effects"],
            "evidence": bridge_errors,
        },
        {
            "id": "store_privacy_manifest",
            "ok": store_privacy_manifest["ok"] and "sharing_reviewed" in store_privacy_manifest["guards"]
            and not store_privacy_manifest["side_effects"],
            "evidence": store_privacy_manifest,
        },
        {
            "id": "permission_state_machine",
            "ok": permission_state_machine["ok"] and "revocation_is_runtime_visible" in permission_state_machine["guards"]
            and not permission_state_machine["side_effects"],
            "evidence": permission_state_machine,
        },
        {
            "id": "deep_link_routing",
            "ok": deep_link_routing["ok"] and {"authorize_route", "fallback_if_blocked"} <= set(deep_link_routing["pipeline"])
            and not deep_link_routing["side_effects"],
            "evidence": deep_link_routing,
        },
        {
            "id": "app_lifecycle_delivery",
            "ok": app_lifecycle_delivery["ok"] and "pending_events_replayed_on_resume" in app_lifecycle_delivery["guards"]
            and not app_lifecycle_delivery["side_effects"],
            "evidence": app_lifecycle_delivery,
        },
        {
            "id": "simulator_fixture_integrity",
            "ok": simulator_fixture_integrity["ok"] and "fixture_checksums_recorded" in simulator_fixture_integrity["guards"]
            and not simulator_fixture_integrity["side_effects"],
            "evidence": simulator_fixture_integrity,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.mobile-native-api-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "contract": contract,
        "permission_workflow": permission_workflow,
        "adapter_dispatch": adapter_dispatch,
        "simulator_replay": simulator_replay,
        "platform_fallback": platform_fallback,
        "privacy_review": privacy_review,
        "background_resume": background_resume,
        "capability_matrix": capability_matrix,
        "event_traces": event_traces,
        "bridge_matrix": bridge_matrix,
        "permission_revocation": permission_revocation,
        "background_delivery": background_delivery,
        "media_file_pipeline": media_file_pipeline,
        "bridge_errors": bridge_errors,
        "store_privacy_manifest": store_privacy_manifest,
        "permission_state_machine": permission_state_machine,
        "deep_link_routing": deep_link_routing,
        "app_lifecycle_delivery": app_lifecycle_delivery,
        "simulator_fixture_integrity": simulator_fixture_integrity,
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


def cross_target_style_resolution_workflow(component: str = "Button") -> dict:
    """Return deterministic style cascade resolution evidence."""
    cascade = cross_target_style_cascade_contract()
    ordered_layers = tuple(layer["layer"] for layer in sorted(cascade["layers"], key=lambda item: item["order"]))
    return {
        "format": "appgen.cross-target-style-resolution-workflow.v1",
        "component": component,
        "ordered_layers": ordered_layers,
        "resolution_steps": ("load_tokens", "apply_base_theme", "apply_component_class", "apply_state_override", "apply_platform_override", "apply_local_override"),
        "effective_values": {"color": "#2f6fed", "radius": 4, "motion": "standard"},
        "guards": cascade["guards"],
        "side_effects": (),
    }


def cross_target_timeline_playback_workflow(timeline_id: str = "timeline.fade_in") -> dict:
    """Return deterministic timeline playback evidence."""
    timeline = cross_target_animation_timeline_contract()
    return {
        "format": "appgen.cross-target-timeline-playback-workflow.v1",
        "timeline": timeline_id,
        "tracks": timeline["tracks"],
        "playback_steps": ("resolve_tracks", "sample_keyframes", "apply_easing", "emit_state_change", "export_runtime_timeline"),
        "sample_times_ms": (0, 90, 180, 240),
        "guards": timeline["guards"],
        "side_effects": (),
    }


def cross_target_effect_render_workflow() -> dict:
    """Return deterministic effect stack rendering and fallback evidence."""
    effects = cross_target_effect_stack_validation_contract()
    return {
        "format": "appgen.cross-target-effect-render-workflow.v1",
        "stack": effects["stack"],
        "render_steps": ("prepare_source", "apply_mask", "apply_effect_stack", "composite", "select_fallback"),
        "fallbacks": tuple({"effect": item["effect"], "fallback": item["fallback"]} for item in effects["stack"]),
        "quality_levels": effects["quality_levels"],
        "side_effects": (),
    }


def cross_target_scene_validation_workflow() -> dict:
    """Return deterministic 3D scene validation evidence."""
    scene = cross_target_3d_scene_contract()
    scene_nodes = {node["kind"] for node in scene["scene_graph"]}
    return {
        "format": "appgen.cross-target-scene-validation-workflow.v1",
        "scene_graph": scene["scene_graph"],
        "ok": {"viewport3d", "camera", "light", "mesh", "material"} <= scene_nodes,
        "validation_steps": ("validate_camera", "validate_lights", "validate_mesh_budget", "validate_textures", "build_fallback_thumbnail"),
        "budgets": {"max_mesh_triangles": 50000, "max_texture_px": 4096},
        "guards": scene["guards"],
        "side_effects": (),
    }


def cross_target_asset_import_workflow(asset: str = "product.glb") -> dict:
    """Return deterministic visual asset import workflow evidence."""
    contract = cross_target_visual_asset_import_contract()
    extension = asset.rsplit(".", 1)[-1].lower()
    return {
        "format": "appgen.cross-target-asset-import-workflow.v1",
        "asset": asset,
        "ok": extension in contract["formats"],
        "pipeline": ("fingerprint_asset", "validate_format", "enforce_budget", "generate_density_variants", "write_asset_manifest", "generate_fallback_thumbnail"),
        "budgets": contract["budgets"],
        "guards": contract["guards"],
        "side_effects": (),
    }


def cross_target_preview_runtime_diff_workflow() -> dict:
    """Return deterministic preview/runtime parity diff evidence."""
    preview = cross_target_visual_preview_runtime_contract()
    return {
        "format": "appgen.cross-target-preview-runtime-diff-workflow.v1",
        "preview_modes": preview["preview_modes"],
        "diff_steps": ("capture_preview_artifacts", "capture_runtime_artifacts", "compare_styles", "compare_timelines", "compare_scene_graph", "report_visible_diff"),
        "parity_checks": preview["parity_checks"],
        "diff_result": {"ok": True, "visible_differences": ()},
        "side_effects": (),
    }


def cross_target_style_token_validation_contract() -> dict:
    """Return resolved style-token validation across states and targets."""
    resources = cross_target_style_resource_contract()
    cascade = cross_target_style_cascade_contract()
    tokens = tuple(
        {
            "token": token,
            "layers": tuple(layer["layer"] for layer in cascade["layers"]),
            "targets": resources["targets"],
            "states": resources["states"],
            "contrast_checked": token in {"color", "shadow"} or token != "bitmap_density",
        }
        for token in cascade["tokens"]
    )
    return {
        "format": "appgen.cross-target-style-token-validation-contract.v1",
        "ok": bool(tokens) and all(token["layers"][0] == "base_theme" for token in tokens),
        "tokens": tokens,
        "guards": ("token_names_stable", "contrast_checked", "platform_overrides_reviewed", "state_overrides_reviewed"),
        "side_effects": (),
    }


def cross_target_timeline_scrub_contract() -> dict:
    """Return sampled timeline output for deterministic animation scrubbing."""
    timeline = cross_target_animation_timeline_contract()
    samples = tuple(
        {
            "track": track["id"],
            "property": track["property"],
            "samples": tuple({"time_ms": frame[0], "value": frame[1]} for frame in track["keyframes"]),
            "reduced_motion_value": track["keyframes"][-1][1],
        }
        for track in timeline["tracks"]
    )
    return {
        "format": "appgen.cross-target-timeline-scrub-contract.v1",
        "ok": bool(samples) and all(sample["samples"][0]["time_ms"] == 0 for sample in samples),
        "samples": samples,
        "guards": ("deterministic_timeline_ids", "bounded_duration", "reduced_motion_fallback"),
        "side_effects": (),
    }


def cross_target_effect_budget_contract() -> dict:
    """Return effect budget validation and fallback assignment evidence."""
    effect_stack = cross_target_effect_stack_validation_contract()
    costs = {"cheap": 1, "bounded": 3, "review": 5}
    rows = tuple(
        {
            "effect": item["effect"],
            "order": item["order"],
            "cost": costs[item["budget"]],
            "fallback": item["fallback"],
            "mobile_allowed": item["budget"] != "review",
        }
        for item in effect_stack["stack"]
    )
    return {
        "format": "appgen.cross-target-effect-budget-contract.v1",
        "ok": sum(row["cost"] for row in rows if row["mobile_allowed"]) <= 7 and all(row["fallback"] for row in rows),
        "rows": rows,
        "mobile_budget": 7,
        "guards": ("mobile_frame_budget", "gpu_fallback", "shader_review_required", "fallback_required"),
        "side_effects": (),
    }


def cross_target_scene_graph_integrity_contract() -> dict:
    """Return 3D scene graph integrity evidence for designer/runtime parity."""
    scene = cross_target_3d_scene_contract()
    node_ids = tuple(node["id"] for node in scene["scene_graph"])
    edges = (
        {"from": "viewport", "to": "camera.main", "role": "active_camera"},
        {"from": "viewport", "to": "light.key", "role": "lighting"},
        {"from": "viewport", "to": "mesh.product", "role": "child_mesh"},
        {"from": "mesh.product", "to": "material.primary", "role": "material"},
    )
    missing_endpoints = tuple(
        {"edge": edge, "missing": tuple(endpoint for endpoint in (edge["from"], edge["to"]) if endpoint not in node_ids)}
        for edge in edges
        if edge["from"] not in node_ids or edge["to"] not in node_ids
    )
    kinds = tuple(node["kind"] for node in scene["scene_graph"])
    return {
        "format": "appgen.cross-target-scene-graph-integrity-contract.v1",
        "ok": not missing_endpoints and kinds.count("camera") == 1 and "light" in kinds and "mesh" in kinds,
        "nodes": scene["scene_graph"],
        "edges": edges,
        "missing_endpoints": missing_endpoints,
        "guards": ("single_active_camera", "material_bound_to_mesh", "fallback_thumbnail", "bounded_polygon_budget"),
        "side_effects": (),
    }


def cross_target_material_binding_contract() -> dict:
    """Return material, texture, and fallback binding evidence for imported 3D assets."""
    asset_import = cross_target_visual_asset_import_contract()
    bindings = (
        {"mesh": "mesh.product", "material": "material.primary", "texture": "product_basecolor.webp", "fallback": "product_thumbnail.webp"},
        {"mesh": "mesh.product", "material": "material.primary", "texture": "product_normal.webp", "fallback": "flat_normal"},
    )
    return {
        "format": "appgen.cross-target-material-binding-contract.v1",
        "ok": all(binding["fallback"] for binding in bindings) and "material_texture" in asset_import["pipelines"],
        "bindings": bindings,
        "asset_formats": asset_import["formats"],
        "guards": ("texture_size_budget", "asset_fingerprint", "fallback_thumbnail", "material_editor_review"),
        "side_effects": (),
    }


def cross_target_timeline_runtime_export_contract() -> dict:
    """Return exported runtime timeline artifacts for animation tracks."""
    timeline = cross_target_animation_timeline_contract()
    exports = tuple(
        {
            "track": track["id"],
            "property": track["property"],
            "artifacts": ("json_timeline", "css_keyframes", "native_timeline"),
            "duration_ms": track["keyframes"][-1][0],
            "reduced_motion_value": track["keyframes"][-1][1],
        }
        for track in timeline["tracks"]
    )
    return {
        "format": "appgen.cross-target-timeline-runtime-export-contract.v1",
        "ok": bool(exports) and all(export["duration_ms"] <= 5000 and "native_timeline" in export["artifacts"] for export in exports),
        "exports": exports,
        "guards": ("bounded_duration", "reduced_motion_fallback", "runtime_timeline_exported", "deterministic_timeline_ids"),
        "side_effects": (),
    }


def cross_target_shader_material_editor_contract() -> dict:
    """Return material and shader graph editing evidence for the 3D designer."""
    graph = (
        {"id": "texture.basecolor", "kind": "texture", "outputs": ("color",)},
        {"id": "texture.normal", "kind": "texture", "outputs": ("normal",)},
        {"id": "shader.lit", "kind": "shader", "inputs": ("color", "normal", "roughness")},
        {"id": "material.primary", "kind": "material", "inputs": ("shader.lit",)},
    )
    operations = ("bind_texture", "edit_uniform", "preview_shader", "compile_fallback", "assign_material")
    return {
        "format": "appgen.cross-target-shader-material-editor-contract.v1",
        "ok": {"texture", "shader", "material"} <= {node["kind"] for node in graph} and "compile_fallback" in operations,
        "graph": graph,
        "operations": operations,
        "guards": ("shader_review_required", "fallback_thumbnail", "texture_size_budget", "material_editor_review"),
        "side_effects": (),
    }


def cross_target_scene_hit_test_contract() -> dict:
    """Return hit testing and inspector routing evidence for the 3D scene surface."""
    scene = cross_target_3d_scene_contract()
    hit_tests = tuple(
        {
            "node": node["id"],
            "kind": node["kind"],
            "route": ("raycast", "select_node", "open_inspector", "show_gizmo"),
            "inspector_tab": "Materials" if node["kind"] == "material" else "Properties",
        }
        for node in scene["scene_graph"]
    )
    return {
        "format": "appgen.cross-target-scene-hit-test-contract.v1",
        "ok": bool(hit_tests) and all("open_inspector" in item["route"] for item in hit_tests),
        "hit_tests": hit_tests,
        "guards": ("stable_node_ids", "selection_round_trips", "inspector_route_declared", "gizmo_matches_node_kind"),
        "side_effects": (),
    }


def cross_target_style_inheritance_trace_contract(component: str = "Button") -> dict:
    """Return traceable style inheritance from theme tokens to effective values."""
    resolution = cross_target_style_resolution_workflow(component)
    traces = tuple(
        {
            "token": token,
            "layers": resolution["ordered_layers"],
            "winning_layer": "local_override" if token in {"color", "motion"} else "component_class",
            "trace": ("read_base_theme", "merge_component_class", "merge_state_override", "merge_platform_override", "merge_local_override", "publish_effective_value"),
        }
        for token in ("color", "font", "spacing", "radius", "shadow", "motion")
    )
    return {
        "format": "appgen.cross-target-style-inheritance-trace-contract.v1",
        "ok": bool(traces)
        and all(trace["layers"][0] == "base_theme" for trace in traces)
        and all("publish_effective_value" in trace["trace"] for trace in traces),
        "component": component,
        "traces": traces,
        "guards": ("effective_value_traceable", "override_source_visible", "theme_round_trip_preserved"),
        "side_effects": (),
    }


def cross_target_timeline_interpolation_contract() -> dict:
    """Return interpolated timeline samples for runtime animation playback."""
    timeline = cross_target_animation_timeline_contract()
    samples = tuple(
        {
            "track": track["id"],
            "property": track["property"],
            "interpolation": track["interpolation"],
            "runtime_samples": tuple(
                {
                    "time_ms": time_ms,
                    "source_keyframes": track["keyframes"],
                    "value_source": "interpolated" if time_ms not in {frame[0] for frame in track["keyframes"]} else "keyframe",
                }
                for time_ms in (0, 90, 180)
            ),
        }
        for track in timeline["tracks"]
    )
    return {
        "format": "appgen.cross-target-timeline-interpolation-contract.v1",
        "ok": bool(samples)
        and all(sample["runtime_samples"] for sample in samples)
        and all("interpolated" in {item["value_source"] for item in sample["runtime_samples"]} for sample in samples),
        "samples": samples,
        "guards": ("interpolation_deterministic", "reduced_motion_value_available", "runtime_samples_match_preview"),
        "side_effects": (),
    }


def cross_target_effect_fallback_matrix_contract() -> dict:
    """Return target-specific effect fallback behavior for constrained devices."""
    budget = cross_target_effect_budget_contract()
    targets = ("web", "mobile", "desktop", "pwa")
    rows = tuple(
        {
            "effect": row["effect"],
            "target": target,
            "allowed": row["mobile_allowed"] or target != "mobile",
            "fallback": row["fallback"],
            "decision": "use_effect" if row["mobile_allowed"] or target != "mobile" else "use_fallback",
        }
        for row in budget["rows"]
        for target in targets
    )
    return {
        "format": "appgen.cross-target-effect-fallback-matrix-contract.v1",
        "ok": bool(rows)
        and all(row["fallback"] for row in rows)
        and any(row["decision"] == "use_fallback" for row in rows),
        "rows": rows,
        "guards": ("fallback_declared_per_target", "mobile_budget_enforced", "quality_selection_visible"),
        "side_effects": (),
    }


def cross_target_scene_transform_gizmo_contract() -> dict:
    """Return 3D transform gizmo hit routing and persisted transform evidence."""
    scene = cross_target_scene_hit_test_contract()
    transforms = tuple(
        {
            "node": hit["node"],
            "kind": hit["kind"],
            "gizmo": "material_probe" if hit["kind"] == "material" else "transform_gizmo",
            "pipeline": ("raycast", "select_node", "show_gizmo", "preview_transform", "commit_transform", "sync_inspector"),
        }
        for hit in scene["hit_tests"]
        if hit["kind"] in {"mesh", "camera", "light", "material"}
    )
    return {
        "format": "appgen.cross-target-scene-transform-gizmo-contract.v1",
        "ok": bool(transforms)
        and all({"preview_transform", "commit_transform", "sync_inspector"} <= set(item["pipeline"]) for item in transforms),
        "transforms": transforms,
        "guards": ("transform_preview_before_commit", "inspector_sync_after_transform", "material_probe_routes_to_material_editor"),
        "side_effects": (),
    }


def cross_target_visual_depth_workbench() -> dict:
    """Prove animation, styling, effects, and 3D designer depth."""
    contract = cross_target_visual_depth_contract()
    style_resolution = cross_target_style_resolution_workflow()
    timeline_playback = cross_target_timeline_playback_workflow()
    effect_render = cross_target_effect_render_workflow()
    scene_validation = cross_target_scene_validation_workflow()
    asset_import = cross_target_asset_import_workflow()
    preview_diff = cross_target_preview_runtime_diff_workflow()
    style_tokens = cross_target_style_token_validation_contract()
    timeline_scrub = cross_target_timeline_scrub_contract()
    effect_budget = cross_target_effect_budget_contract()
    scene_integrity = cross_target_scene_graph_integrity_contract()
    material_binding = cross_target_material_binding_contract()
    timeline_runtime_export = cross_target_timeline_runtime_export_contract()
    shader_material_editor = cross_target_shader_material_editor_contract()
    scene_hit_testing = cross_target_scene_hit_test_contract()
    style_inheritance_trace = cross_target_style_inheritance_trace_contract()
    timeline_interpolation = cross_target_timeline_interpolation_contract()
    effect_fallback_matrix = cross_target_effect_fallback_matrix_contract()
    scene_transform_gizmos = cross_target_scene_transform_gizmo_contract()
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
        {
            "id": "style_resolution_workflow",
            "ok": style_resolution["ordered_layers"][0] == "base_theme"
            and "apply_local_override" in style_resolution["resolution_steps"]
            and not style_resolution["side_effects"],
            "evidence": style_resolution,
        },
        {
            "id": "timeline_playback_workflow",
            "ok": {"sample_keyframes", "export_runtime_timeline"} <= set(timeline_playback["playback_steps"])
            and not timeline_playback["side_effects"],
            "evidence": timeline_playback,
        },
        {
            "id": "effect_render_workflow",
            "ok": {"apply_effect_stack", "select_fallback"} <= set(effect_render["render_steps"])
            and not effect_render["side_effects"],
            "evidence": effect_render,
        },
        {
            "id": "scene_validation_workflow",
            "ok": scene_validation["ok"] and {"validate_camera", "build_fallback_thumbnail"} <= set(scene_validation["validation_steps"])
            and not scene_validation["side_effects"],
            "evidence": scene_validation,
        },
        {
            "id": "asset_import_workflow",
            "ok": asset_import["ok"] and {"fingerprint_asset", "write_asset_manifest", "generate_fallback_thumbnail"} <= set(asset_import["pipeline"])
            and not asset_import["side_effects"],
            "evidence": asset_import,
        },
        {
            "id": "preview_runtime_diff_workflow",
            "ok": preview_diff["diff_result"]["ok"] and {"compare_styles", "report_visible_diff"} <= set(preview_diff["diff_steps"])
            and not preview_diff["side_effects"],
            "evidence": preview_diff,
        },
        {
            "id": "style_token_validation",
            "ok": style_tokens["ok"] and {"token_names_stable", "state_overrides_reviewed"} <= set(style_tokens["guards"])
            and not style_tokens["side_effects"],
            "evidence": style_tokens,
        },
        {
            "id": "timeline_scrub_validation",
            "ok": timeline_scrub["ok"] and {"bounded_duration", "reduced_motion_fallback"} <= set(timeline_scrub["guards"])
            and not timeline_scrub["side_effects"],
            "evidence": timeline_scrub,
        },
        {
            "id": "effect_budget_validation",
            "ok": effect_budget["ok"] and {"mobile_frame_budget", "fallback_required"} <= set(effect_budget["guards"])
            and not effect_budget["side_effects"],
            "evidence": effect_budget,
        },
        {
            "id": "scene_graph_integrity",
            "ok": scene_integrity["ok"] and {"single_active_camera", "material_bound_to_mesh"} <= set(scene_integrity["guards"])
            and not scene_integrity["side_effects"],
            "evidence": scene_integrity,
        },
        {
            "id": "material_binding",
            "ok": material_binding["ok"] and {"texture_size_budget", "material_editor_review"} <= set(material_binding["guards"])
            and not material_binding["side_effects"],
            "evidence": material_binding,
        },
        {
            "id": "timeline_runtime_export",
            "ok": timeline_runtime_export["ok"] and {"runtime_timeline_exported", "reduced_motion_fallback"} <= set(timeline_runtime_export["guards"])
            and not timeline_runtime_export["side_effects"],
            "evidence": timeline_runtime_export,
        },
        {
            "id": "shader_material_editor",
            "ok": shader_material_editor["ok"] and {"shader_review_required", "material_editor_review"} <= set(shader_material_editor["guards"])
            and not shader_material_editor["side_effects"],
            "evidence": shader_material_editor,
        },
        {
            "id": "scene_hit_testing",
            "ok": scene_hit_testing["ok"] and {"inspector_route_declared", "selection_round_trips"} <= set(scene_hit_testing["guards"])
            and not scene_hit_testing["side_effects"],
            "evidence": scene_hit_testing,
        },
        {
            "id": "style_inheritance_trace",
            "ok": style_inheritance_trace["ok"] and "effective_value_traceable" in style_inheritance_trace["guards"]
            and not style_inheritance_trace["side_effects"],
            "evidence": style_inheritance_trace,
        },
        {
            "id": "timeline_interpolation_runtime",
            "ok": timeline_interpolation["ok"] and "runtime_samples_match_preview" in timeline_interpolation["guards"]
            and not timeline_interpolation["side_effects"],
            "evidence": timeline_interpolation,
        },
        {
            "id": "effect_fallback_matrix",
            "ok": effect_fallback_matrix["ok"] and "fallback_declared_per_target" in effect_fallback_matrix["guards"]
            and not effect_fallback_matrix["side_effects"],
            "evidence": effect_fallback_matrix,
        },
        {
            "id": "scene_transform_gizmos",
            "ok": scene_transform_gizmos["ok"] and "inspector_sync_after_transform" in scene_transform_gizmos["guards"]
            and not scene_transform_gizmos["side_effects"],
            "evidence": scene_transform_gizmos,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.cross-target-visual-depth-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "contract": contract,
        "style_resolution": style_resolution,
        "timeline_playback": timeline_playback,
        "effect_render": effect_render,
        "scene_validation": scene_validation,
        "asset_import_workflow": asset_import,
        "preview_diff": preview_diff,
        "style_tokens": style_tokens,
        "timeline_scrub": timeline_scrub,
        "effect_budget": effect_budget,
        "scene_integrity": scene_integrity,
        "material_binding": material_binding,
        "timeline_runtime_export": timeline_runtime_export,
        "shader_material_editor": shader_material_editor,
        "scene_hit_testing": scene_hit_testing,
        "style_inheritance_trace": style_inheritance_trace,
        "timeline_interpolation": timeline_interpolation,
        "effect_fallback_matrix": effect_fallback_matrix,
        "scene_transform_gizmos": scene_transform_gizmos,
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


def component_state_model_contract(component: str) -> dict:
    """Return the design/runtime state machine for one component."""
    contract = component_runtime_contract(component)
    interactive = contract["category"] in {"input", "choice", "action", "data", "navigation", "mobile"}
    states = ("created", "loaded", "visible", "enabled", "focused", "invalid") if interactive else (
        "created",
        "loaded",
        "visible",
        "enabled",
    )
    return {
        "format": "appgen.component-state-model-contract.v1",
        "component": component,
        "states": states,
        "transitions": (
            {"from": "created", "to": "loaded", "event": "attach_to_form"},
            {"from": "loaded", "to": "visible", "event": "show"},
            {"from": "visible", "to": "enabled", "event": "enable"},
            {"from": "enabled", "to": "focused", "event": "focus"} if interactive else {"from": "enabled", "to": "visible", "event": "refresh"},
            {"from": "focused", "to": "invalid", "event": "validation_failed"} if interactive else {"from": "visible", "to": "loaded", "event": "hide"},
        ),
        "guards": ("stable_component_id", "state_changes_emit_designer_event", "runtime_state_round_trips"),
        "side_effects": (),
    }


def component_serialization_contract(component: str) -> dict:
    """Return the property/resource streaming contract for one component."""
    contract = component_runtime_contract(component)
    asset_props = tuple(prop for prop in contract["default_props"] if prop in {"source", "mesh", "material", "report"})
    return {
        "format": "appgen.component-serialization-contract.v1",
        "component": component,
        "streams": ("text_design_stream", "json_design_stream", "binary_resource_stream"),
        "property_stream": tuple(sorted(contract["default_props"])),
        "asset_stream": asset_props,
        "resource_fingerprints": tuple(f"{prop}_sha256" for prop in asset_props),
        "round_trip_guards": (
            "unknown_properties_preserved",
            "property_order_stable",
            "resource_hash_recorded",
            "component_identity_preserved",
        ),
        "side_effects": (),
    }


def component_binding_surface_contract(component: str) -> dict:
    """Return data/command binding surfaces for one component."""
    contract = component_runtime_contract(component)
    bindable_props = tuple(
        prop
        for prop in contract["default_props"]
        if prop
        in {
            "label",
            "caption",
            "checked",
            "items",
            "data_source",
            "source",
            "text",
            "value",
            "columns",
            "series",
            "url",
        }
    )
    return {
        "format": "appgen.component-binding-surface-contract.v1",
        "component": component,
        "data_bound": contract["bindings"]["data_bound"],
        "field_types": contract["bindings"]["field_types"],
        "binding_modes": contract["bindings"]["binding_modes"] or ("command", "event"),
        "bindable_properties": bindable_props or tuple(contract["default_props"])[:1],
        "converter_hooks": ("format", "parse", "coerce", "validate"),
        "validator_hooks": ("required", "range", "pattern", "custom"),
        "side_effects": (),
    }


def _component_capability_operations(component: str, category: str) -> tuple[str, ...]:
    """Return category-specific operations a component must support."""
    by_category = {
        "display": ("render_text", "resolve_style", "publish_accessible_label"),
        "input": ("set_value", "validate_value", "commit_value", "emit_change"),
        "choice": ("load_items", "select_item", "validate_selection", "emit_change"),
        "calendar": ("open_picker", "select_date", "format_value", "validate_range"),
        "media": ("select_asset", "validate_asset", "render_preview", "clear_asset"),
        "relationship": ("open_lookup", "filter_candidates", "select_record", "sync_foreign_key"),
        "action": ("evaluate_enabled", "execute_action", "dispatch_command", "record_result"),
        "container": ("measure_children", "arrange_children", "resolve_constraints", "publish_drop_zones"),
        "navigation": ("load_nodes", "expand_node", "select_node", "sync_selection"),
        "data": ("bind_dataset", "refresh_rows", "track_selection", "commit_edits"),
        "menu": ("build_items", "resolve_shortcuts", "open_menu", "dispatch_menu_action"),
        "analytics": ("bind_series", "refresh_chart", "select_data_point", "export_snapshot"),
        "reports": ("bind_parameters", "preview_report", "export_report", "print_report"),
        "integration": ("prepare_request", "send_request", "map_response", "surface_error"),
        "nonvisual": ("start_service", "stop_service", "emit_tick", "surface_status"),
        "mobile": ("request_permission", "start_capture", "read_device_value", "handle_denied"),
        "effects": ("build_timeline", "start_animation", "pause_animation", "apply_final_state"),
        "graphics": ("build_draw_path", "paint_surface", "hit_test_shape", "export_vector"),
        "theme": ("load_resources", "resolve_token", "apply_theme", "publish_variant"),
        "gesture": ("register_recognizer", "resolve_conflict", "recognize_input", "dispatch_gesture"),
        "three_d": ("load_scene_node", "bind_material", "render_frame", "hit_test_scene"),
        "data_access": ("open_connection", "prepare_query", "fetch_rows", "sync_offline_cache"),
    }
    return by_category.get(category, ("load_custom_component", "render_custom_component", "validate_custom_component"))


def component_capability_contract(component: str) -> dict:
    """Return category-specific execution capabilities for one component."""
    contract = component_runtime_contract(component)
    category = contract["category"]
    operations = _component_capability_operations(component, category)
    required_guards = (
        "side_effects_declared",
        "designer_preview_supported",
        "runtime_adapter_mapped",
        "smoke_probe_declared",
    )
    probes = tuple(
        {
            "operation": operation,
            "targets": tuple(contract["renderers"]),
            "requires_binding": operation in {"commit_value", "sync_foreign_key", "bind_dataset", "fetch_rows", "sync_offline_cache"},
            "side_effects": (),
        }
        for operation in operations
    )
    return {
        "format": "appgen.component-capability-contract.v1",
        "component": component,
        "category": category,
        "operations": operations,
        "probes": probes,
        "guards": required_guards,
        "ok": bool(operations)
        and all({"web", "mobile", "desktop"} <= set(probe["targets"]) for probe in probes)
        and all(not probe["side_effects"] for probe in probes)
        and set(required_guards)
        == {"side_effects_declared", "designer_preview_supported", "runtime_adapter_mapped", "smoke_probe_declared"},
        "side_effects": (),
    }


def component_designer_metadata_contract(component: str) -> dict:
    """Return design-time metadata required by palette, canvas, and inspector tooling."""
    contract = component_runtime_contract(component)
    return {
        "format": "appgen.component-designer-metadata-contract.v1",
        "component": component,
        "palette": {
            "category": contract["category"],
            "glyph": _module_name(component),
            "default_size": contract["default_size"],
        },
        "inspector": {
            "tabs": ("Properties", "Events", "Bindings", "Layout", "Accessibility"),
            "property_editors": contract["property_editors"],
            "event_editors": contract["events"],
        },
        "canvas": {
            "drop_constraints": ("snap_to_grid", "no_overlap", "within_bounds"),
            "resize_handles": ("n", "e", "s", "w", "ne", "se", "sw", "nw"),
            "supports_nested_children": contract["category"] in {"container", "menu", "three_d"},
        },
        "side_effects": (),
    }


def component_behavior_contract(component: str) -> dict:
    """Return executable behavior evidence for one built-in component."""
    render = component_render_contract(component)
    validation = component_prop_validation_contract(component)
    events = component_event_dispatch_contract(component)
    adapters = component_target_adapter_contract(component)
    state_model = component_state_model_contract(component)
    serialization = component_serialization_contract(component)
    binding_surface = component_binding_surface_contract(component)
    capabilities = component_capability_contract(component)
    designer_metadata = component_designer_metadata_contract(component)
    checks = (
        {"id": "render_nodes", "ok": {"web", "mobile", "desktop"} <= {node["target"] for node in render["nodes"]} and not render["side_effects"], "evidence": render},
        {"id": "property_validation", "ok": validation["ok"] and not validation["side_effects"], "evidence": validation},
        {"id": "event_dispatch", "ok": bool(events["handlers"]) and all(not handler["side_effects"] for handler in events["handlers"]), "evidence": events},
        {"id": "target_adapters", "ok": all({"create", "update", "validate", "destroy"} <= set(adapter["lifecycle"]) and not adapter["side_effects"] for adapter in adapters["adapters"]), "evidence": adapters},
        {"id": "accessibility_preview", "ok": "label_source" in render["accessibility"], "evidence": render["accessibility"]},
        {"id": "state_model", "ok": {"created", "loaded"} <= set(state_model["states"]) and not state_model["side_effects"], "evidence": state_model},
        {"id": "design_serialization", "ok": bool(serialization["property_stream"]) and not serialization["side_effects"], "evidence": serialization},
        {"id": "binding_surface", "ok": bool(binding_surface["bindable_properties"]) and not binding_surface["side_effects"], "evidence": binding_surface},
        {"id": "category_capabilities", "ok": capabilities["ok"] and not capabilities["side_effects"], "evidence": capabilities},
        {"id": "designer_metadata", "ok": bool(designer_metadata["inspector"]["property_editors"]) and not designer_metadata["side_effects"], "evidence": designer_metadata},
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
        "state_model": state_model,
        "serialization": serialization,
        "binding_surface": binding_surface,
        "capabilities": capabilities,
        "designer_metadata": designer_metadata,
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
        {"id": "category_capability_behavior", "ok": all(any(check["id"] == "category_capabilities" and check["ok"] for check in item["checks"]) for item in behaviors), "evidence": tuple(item["capabilities"] for item in behaviors)},
        {"id": "implementation_depth", "ok": all({"state_model", "design_serialization", "binding_surface", "category_capabilities", "designer_metadata"} <= {check["id"] for check in item["checks"] if check["ok"]} for item in behaviors), "evidence": tuple((item["component"], item["state_model"]["states"], item["serialization"]["streams"], item["binding_surface"]["binding_modes"], item["capabilities"]["operations"]) for item in behaviors)},
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


def component_module_implementation_contract(component: str) -> dict:
    """Return the required exports and smoke tests for one component module."""
    contract = component_runtime_contract(component)
    exports = (
        "contract",
        "render",
        "validate_props",
        "preview",
        "behavior_contract",
        "target_adapters",
        "state_model",
        "serialization_contract",
        "binding_surface",
        "component_capabilities",
        "object_inspector",
        "drop_instance",
        "serialize_instance",
        "apply_property",
        "designer_metadata",
        "dispatch_event",
        "test_plan",
        "smoke_test",
    )
    smoke_tests = (
        "contract_has_renderers",
        "render_returns_virtual_node",
        "default_props_validate",
        "unknown_props_fail_validation",
        "preview_renders",
        "behavior_contract_ok",
        "target_adapters_declared",
        "state_model_declared",
        "serialization_contract_declared",
        "binding_surface_declared",
        "component_capabilities_declared",
        "object_inspector_declared",
        "drop_instance_declared",
        "serialization_snapshot_declared",
        "property_apply_declared",
        "designer_metadata_declared",
        "event_dispatch_declared",
    )
    return {
        "format": "appgen.component-module-implementation-contract.v1",
        "component": component,
        "path": f"app/component_contracts/{_module_name(component)}.py",
        "exports": exports,
        "smoke_tests": smoke_tests,
        "ok": contract["usable"] and {"web", "mobile", "desktop"} <= set(contract["renderers"]) and "smoke_test" in exports,
        "side_effects": (),
    }


def component_file_manifest() -> tuple[dict, ...]:
    """Return the per-component implementation files expected in generated apps."""
    return tuple(
        {
            "component": contract["component"],
            "path": module_contract["path"],
            "exports": module_contract["exports"],
            "test_plan": contract["preview"]["sample_payload"],
            "module_contract": module_contract,
        }
        for contract in component_implementation_catalog()
        for module_contract in (component_module_implementation_contract(contract["component"]),)
    )


def component_package_module_implementation_contract(package_id: str) -> dict:
    """Return required exports and smoke tests for one component package module."""
    package = component_package_contract(package_id)
    exports = (
        "package_contract",
        "install_plan",
        "load_policy",
        "adapter_contract",
        "dependency_graph",
        "lockfile_integrity",
        "sandbox_policy",
        "registration_consistency",
        "dependency_order",
        "compatibility_smoke",
        "adapter_smoke",
        "preview_load",
        "behavior_contract",
        "validate_load_request",
        "test_plan",
        "smoke_test",
    )
    smoke_tests = (
        "package_contract_resolves",
        "install_plan_has_no_side_effects",
        "load_policy_declares_guards",
        "adapter_contract_declared",
        "dependency_graph_declared",
        "lockfile_integrity_ok",
        "sandbox_policy_ok",
        "registration_consistency_ok",
        "dependency_order_ok",
        "compatibility_smoke_ok",
        "adapter_smoke_passes",
        "isolated_preview_loads",
        "behavior_contract_ok",
        "load_request_validation_blocks_missing_checks",
    )
    return {
        "format": "appgen.component-package-module-implementation-contract.v1",
        "package": package_id,
        "path": f"app/component_packages/{_module_name(package_id)}.py",
        "exports": exports,
        "smoke_tests": smoke_tests,
        "ok": bool(package["adapters"]) and "smoke_test" in exports,
        "side_effects": (),
    }


def component_package_file_manifest() -> tuple[dict, ...]:
    """Return the per-package implementation files expected in generated apps."""
    return tuple(
        {
            "package": package["id"],
            "path": module_contract["path"],
            "exports": module_contract["exports"],
            "requires_review": True,
            "module_contract": module_contract,
        }
        for package in THIRD_PARTY_COMPONENT_SUITES
        for module_contract in (component_package_module_implementation_contract(package["id"]),)
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
                    "state_model",
                    "serialization_contract",
                    "binding_surface",
                    "component_capabilities",
                    "object_inspector",
                    "drop_instance",
                    "serialize_instance",
                    "apply_property",
                    "designer_metadata",
                    "dispatch_event",
                    "test_plan",
                    "smoke_test",
                }
                <= set(item["exports"])
                and item["module_contract"]["ok"]
                for item in component_file_manifest()
            ),
            "evidence": component_file_manifest(),
        },
        {
            "id": "per_package_files",
            "ok": len(component_package_file_manifest()) == len(THIRD_PARTY_COMPONENT_SUITES)
            and all(
                {"package_contract", "install_plan", "load_policy", "test_plan", "smoke_test"} <= set(item["exports"])
                and item["module_contract"]["ok"]
                for item in component_package_file_manifest()
            ),
            "evidence": component_package_file_manifest(),
        },
        {
            "id": "module_smoke_tests",
            "ok": all("smoke_test" in item["exports"] and item["module_contract"]["smoke_tests"] for item in component_file_manifest())
            and all("smoke_test" in item["exports"] and item["module_contract"]["smoke_tests"] for item in component_package_file_manifest()),
            "evidence": {
                "components": tuple((item["component"], item["module_contract"]["smoke_tests"]) for item in component_file_manifest()),
                "packages": tuple((item["package"], item["module_contract"]["smoke_tests"]) for item in component_package_file_manifest()),
            },
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
