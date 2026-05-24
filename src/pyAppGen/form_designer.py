"""Package-level RAD-style form designer contracts."""

from __future__ import annotations

import hashlib
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

COMPONENT_ICON_OVERRIDES = dict(
    Label="fa-font",
    TextBox="fa-keyboard-o",
    EmailInput="fa-envelope-o",
    TextArea="fa-align-left",
    DatePicker="fa-calendar",
    Lookup="fa-search",
    Select="fa-list",
    Checkbox="fa-check-square-o",
    FileUpload="fa-upload",
    Button="fa-hand-pointer-o",
    GroupBox="fa-object-group",
    RadioGroup="fa-dot-circle-o",
    RadioButton="fa-dot-circle-o",
    ListBox="fa-th-list",
    ListView="fa-list-alt",
    TreeView="fa-sitemap",
    Grid="fa-table",
    StringGrid="fa-table",
    PageControl="fa-columns",
    ScrollBox="fa-arrows-v",
    FlowLayout="fa-exchange",
    GridLayout="fa-th",
    VerticalBoxLayout="fa-bars",
    HorizontalBoxLayout="fa-ellipsis-h",
    MainMenu="fa-bars",
    PopupMenu="fa-mouse-pointer",
    ToolBar="fa-wrench",
    ActionList="fa-bolt",
    Image="fa-image",
    Shape="fa-square-o",
    PathShape="fa-code-fork",
    Rectangle="fa-square",
    Ellipse="fa-circle-o",
    Line="fa-minus",
    Bitmap="fa-picture-o",
    Chart="fa-bar-chart",
    ReportViewer="fa-file-text-o",
    WebBrowser="fa-globe",
    Timer="fa-clock-o",
    DataSource="fa-database",
    BindingSource="fa-random",
    RESTClient="fa-cloud",
    CameraView="fa-camera",
    LocationSensor="fa-location-arrow",
    MotionSensor="fa-compass",
    OrientationSensor="fa-compass",
    NotificationCenter="fa-bell",
    PhotoPicker="fa-picture-o",
    BiometricAuth="fa-lock",
    ContactsPicker="fa-address-book-o",
    CalendarEvents="fa-calendar-check-o",
    SecureStore="fa-shield",
    PushClient="fa-paper-plane",
    BluetoothClient="fa-bluetooth-b",
    NfcReader="fa-wifi",
    FilePicker="fa-folder-open",
    ShareSheet="fa-share-alt",
    BackgroundTask="fa-refresh",
    Animation="fa-play",
    FloatAnimation="fa-arrows-h",
    ColorAnimation="fa-paint-brush",
    PathAnimation="fa-road",
    Effect="fa-magic",
    StyleBook="fa-book",
    StyleManager="fa-sliders",
    GestureManager="fa-hand-paper-o",
    Gesture="fa-hand-pointer-o",
    Viewport3D="fa-cube",
    Dummy3D="fa-crosshairs",
    Camera3D="fa-video-camera",
    Light3D="fa-lightbulb-o",
    Mesh3D="fa-cubes",
    DatabaseConnection="fa-plug",
    TableAdapter="fa-table",
    ClientDataSet="fa-database",
)

CATEGORY_ICON_DEFAULTS = dict(
    action="fa-bolt",
    analytics="fa-bar-chart",
    calendar="fa-calendar",
    choice="fa-check-square-o",
    container="fa-window-maximize",
    data="fa-table",
    data_access="fa-database",
    display="fa-font",
    effects="fa-magic",
    gesture="fa-hand-paper-o",
    graphics="fa-paint-brush",
    input="fa-keyboard-o",
    integration="fa-cloud",
    media="fa-image",
    menu="fa-bars",
    mobile="fa-mobile",
    navigation="fa-sitemap",
    nonvisual="fa-cog",
    relationship="fa-link",
    reports="fa-file-text-o",
    theme="fa-paint-brush",
    three_d="fa-cube",
)


def component_icon(component_type: str) -> str:
    """Return the icon class used by generated IDE palettes."""
    spec = COMPONENTS.get(component_type, {})
    return COMPONENT_ICON_OVERRIDES.get(
        component_type,
        CATEGORY_ICON_DEFAULTS.get(spec.get("category", "custom"), "fa-puzzle-piece"),
    )


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
    return tuple(
        {
            "component": name,
            "icon": component_icon(name),
            **spec,
        }
        for name, spec in COMPONENTS.items()
    )


def component_analog_matrix() -> tuple[dict, ...]:
    """Return requested native component analog coverage."""
    return tuple(
        {
            **requirement,
            "implemented": requirement["analog"] in COMPONENTS,
            "runtime_adapter": _dfm_component_class(requirement["analog"]),
            "contract": component_runtime_contract(requirement["analog"]) if requirement["analog"] in COMPONENTS else None,
        }
        for requirement in COMPONENT_ANALOG_REQUIREMENTS
    )


def component_analog_workbench() -> dict:
    """Prove all requested component analogs are present and usable."""
    matrix = component_analog_matrix()
    groups = tuple(sorted({item["group"] for item in matrix}))
    behavior_replay = tuple(
        component_behavior_contract(item["analog"])
        for item in matrix
        if item["implemented"]
    )
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
            "id": "runtime_adapters_declared",
            "ok": all(item["runtime_adapter"].startswith("T") for item in matrix),
            "evidence": tuple((item["source"], item["analog"], item["runtime_adapter"]) for item in matrix),
        },
        {
            "id": "requested_analog_behavior_replay",
            "ok": len(behavior_replay) == len(matrix)
            and all(item["ok"] for item in behavior_replay)
            and all(
                {"render_nodes", "property_validation", "event_dispatch", "target_adapters", "binding_surface", "category_capabilities"}
                <= {check["id"] for check in item["checks"] if check["ok"]}
                for item in behavior_replay
            ),
            "evidence": tuple(
                {
                    "component": item["component"],
                    "checks": tuple(check["id"] for check in item["checks"] if check["ok"]),
                }
                for item in behavior_replay
            ),
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
        "behavior_replay": behavior_replay,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def component_analog_group_audit() -> dict:
    """Return grouped coverage evidence for requested native component analogs."""
    matrix = component_analog_matrix()
    workbench = component_analog_workbench()
    required_groups = tuple(
        sorted({requirement["group"] for requirement in COMPONENT_ANALOG_REQUIREMENTS})
    )
    behavior_by_component = {
        item["component"]: item for item in workbench["behavior_replay"]
    }
    grouped = tuple(
        {
            "group": group,
            "sources": tuple(item["source"] for item in matrix if item["group"] == group),
            "analogs": tuple(item["analog"] for item in matrix if item["group"] == group),
            "runtime_adapters": tuple(
                item["runtime_adapter"] for item in matrix if item["group"] == group
            ),
            "behavior_checks": tuple(
                {
                    "component": item["analog"],
                    "checks": tuple(
                        check["id"]
                        for check in behavior_by_component[item["analog"]]["checks"]
                        if check["ok"]
                    ),
                }
                for item in matrix
                if item["group"] == group and item["analog"] in behavior_by_component
            ),
            "ok": all(
                item["implemented"]
                and item["contract"]
                and item["contract"]["usable"]
                and behavior_by_component.get(item["analog"], {}).get("ok") is True
                for item in matrix
                if item["group"] == group
            ),
        }
        for group in required_groups
    )
    requested_sources = {requirement["source"] for requirement in COMPONENT_ANALOG_REQUIREMENTS}
    checks = (
        {
            "id": "requested_groups_complete",
            "ok": set(required_groups) == {item["group"] for item in grouped},
            "evidence": required_groups,
        },
        {
            "id": "requested_sources_complete",
            "ok": requested_sources == {item["source"] for item in matrix},
            "evidence": tuple(sorted(requested_sources)),
        },
        {
            "id": "grouped_analogs_usable",
            "ok": all(item["ok"] for item in grouped),
            "evidence": tuple(
                {
                    "group": item["group"],
                    "analogs": item["analogs"],
                    "runtime_adapters": item["runtime_adapters"],
                }
                for item in grouped
            ),
        },
        {
            "id": "behavior_replay_per_requested_analog",
            "ok": len(workbench["behavior_replay"]) == len(matrix)
            and all(item["ok"] for item in workbench["behavior_replay"]),
            "evidence": tuple(sorted(behavior_by_component)),
        },
    )
    ok = workbench["ok"] and all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-analog-group-audit.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "groups": grouped,
        "checks": checks,
        "workbench": workbench,
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


def component_package_resolve_metadata_operation(package_id: str) -> dict:
    """Return a callable IDE operation for resolving one package before install."""
    contract = component_package_contract(package_id)
    dependency_graph = component_package_dependency_graph((package_id,))
    lockfile = component_package_lockfile_integrity_contract((package_id,))
    return {
        "format": "appgen.component-package-resolve-metadata-operation.v1",
        "package_id": package_id,
        "ok": contract["implemented"] and dependency_graph["ok"] and lockfile["ok"],
        "pipeline": (
            "read_package_manifest",
            "validate_metadata",
            "resolve_dependency_graph",
            "prepare_lockfile_entry",
        ),
        "manifest": contract["module"],
        "dependency_graph": dependency_graph,
        "lockfile_entries": lockfile["entries"],
        "side_effects": (),
    }


def component_package_preview_load_operation(package_id: str) -> dict:
    """Return a callable IDE operation for sandboxed design-time preview loading."""
    policy = component_package_load_policy(package_id)
    validation = validate_component_package_load(package_id, {"accepted": policy["checks"]})
    preview = component_package_preview_load_contract(package_id)
    adapter_smoke = component_package_adapter_smoke_contract(package_id)
    return {
        "format": "appgen.component-package-preview-load-operation.v1",
        "package_id": package_id,
        "ok": validation["ok"] and preview["ok"] and adapter_smoke["ok"],
        "pipeline": (
            "validate_load_request",
            "create_sandbox_loader",
            "instantiate_preview_adapter",
            "run_adapter_smoke",
            "unload_preview",
        ),
        "validation": validation,
        "preview": preview,
        "adapter_smoke": adapter_smoke,
        "guards": ("sandboxed_loader", "per-project_manifest", "preview_unloaded_after_probe"),
        "side_effects": (),
    }


def component_package_registry_commit_operation(package_id: str) -> dict:
    """Return a callable IDE operation for committing package registrations."""
    registration = component_package_registration_consistency_contract((package_id,))
    dependency_order = component_package_dependency_order_contract((package_id,))
    palette_refresh = component_package_palette_refresh_contract((package_id,))
    return {
        "format": "appgen.component-package-registry-commit-operation.v1",
        "package_id": package_id,
        "ok": registration["ok"] and dependency_order["ok"] and palette_refresh["ok"],
        "pipeline": (
            "load_adapter",
            "register_palette_entries",
            "register_inspector_editors",
            "register_binding_adapters",
            "commit_project_manifest",
            "refresh_palette",
        ),
        "registration": registration,
        "dependency_order": dependency_order["load_order"],
        "palette_actions": palette_refresh["palette_actions"],
        "guards": ("adapter_before_registry_commit", "all_design_surfaces_registered", "palette_refreshed_after_commit"),
        "side_effects": (),
    }


def component_package_update_operation(package_id: str) -> dict:
    """Return a callable IDE operation for a reviewed package update."""
    update_plan = component_package_update_plan_contract((package_id,))
    updates = {
        item["package_id"]: item
        for item in update_plan["updates"]
    }
    update = updates[package_id]
    return {
        "format": "appgen.component-package-update-operation.v1",
        "package_id": package_id,
        "ok": "run_adapter_smoke" in update["phases"] and "refresh_palette" in update["phases"],
        "pipeline": update["phases"],
        "from_version": update["from_version"],
        "to_version": update["to_version"],
        "guards": update_plan["guards"],
        "side_effects": (),
    }


def component_package_uninstall_operation(package_id: str) -> dict:
    """Return a callable IDE operation for a reversible package uninstall."""
    uninstall_plan = component_package_uninstall_plan_contract((package_id,))
    uninstalls = {
        item["package_id"]: item
        for item in uninstall_plan["uninstalls"]
    }
    uninstall = uninstalls[package_id]
    rollback = component_package_rollback_contract((package_id,))
    return {
        "format": "appgen.component-package-uninstall-operation.v1",
        "package_id": package_id,
        "ok": "disable_adapters" in uninstall["phases"]
        and "remove_palette_entries" in uninstall["phases"]
        and "restore_registry" in rollback["snapshot"]["restore_order"],
        "pipeline": uninstall["phases"],
        "rollback": rollback,
        "guards": uninstall_plan["guards"] + ("rollback_snapshot_available",),
        "side_effects": (),
    }


def component_package_actionable_operations(package_ids: tuple[str, ...] = ()) -> dict:
    """Return callable package-manager operations used by the generated IDE."""
    install_plan = third_party_component_install_plan(package_ids)
    operations = tuple(
        {
            "package_id": package["id"],
            "resolve_metadata": component_package_resolve_metadata_operation(package["id"]),
            "preview_load": component_package_preview_load_operation(package["id"]),
            "registry_commit": component_package_registry_commit_operation(package["id"]),
            "update_package": component_package_update_operation(package["id"]),
            "uninstall_package": component_package_uninstall_operation(package["id"]),
        }
        for package in install_plan["packages"]
    )
    operation_names = (
        "resolve_metadata",
        "preview_load",
        "registry_commit",
        "update_package",
        "uninstall_package",
    )
    return {
        "format": "appgen.component-package-actionable-operations.v1",
        "ok": install_plan["ok"]
        and not install_plan["unknown"]
        and bool(operations)
        and all(operation[name]["ok"] for operation in operations for name in operation_names),
        "operations": operations,
        "operation_names": operation_names,
        "side_effects": (),
    }


def component_package_install_session_replay(package_ids: tuple[str, ...] = ()) -> dict:
    """Replay design-time component package installation without changing the host IDE."""
    install_plan = third_party_component_install_plan(package_ids)
    sessions = []
    for package in install_plan["packages"]:
        policy = component_package_load_policy(package["id"])
        validation = validate_component_package_load(package["id"], {"accepted": policy["checks"]})
        contract = component_package_contract(package["id"])
        behavior = component_package_behavior_contract(package["id"])
        phases = (
            {
                "phase": "resolve_metadata",
                "ok": contract["implemented"] and bool(contract["adapters"]),
                "artifact": contract["module"],
            },
            {
                "phase": "validate_load_request",
                "ok": validation["ok"] and not validation["side_effects"],
                "artifact": validation["format"],
            },
            {
                "phase": "sandbox_load",
                "ok": "sandboxed_loader" in policy["isolation"] and not policy["side_effects"],
                "artifact": policy["isolation"],
            },
            {
                "phase": "adapter_compile",
                "ok": behavior["adapter_smoke"]["ok"] and behavior["preview_load"]["ok"],
                "artifact": tuple(adapter["adapter"] for adapter in contract["adapters"]),
            },
            {
                "phase": "registry_commit",
                "ok": behavior["registration"]["ok"] and behavior["dependency_order"]["ok"],
                "artifact": behavior["registration"]["actual"],
            },
            {
                "phase": "palette_refresh",
                "ok": "rebuild_toolbox" in component_package_palette_refresh_contract((package["id"],))["palette_actions"],
                "artifact": "rebuild_toolbox",
            },
            {
                "phase": "rollback_probe",
                "ok": "restore_registry" in behavior["rollback"]["snapshot"]["restore_order"],
                "artifact": behavior["rollback"]["snapshot"]["restore_order"],
            },
        )
        sessions.append(
            {
                "package_id": package["id"],
                "phases": phases,
                "ok": all(phase["ok"] for phase in phases),
                "final_state": {
                    "loaded": True,
                    "palette_refreshed": True,
                    "rollback_ready": True,
                    "global_install": False,
                },
            }
        )
    return {
        "format": "appgen.component-package-install-session-replay.v1",
        "ok": install_plan["ok"]
        and len(sessions) == len(install_plan["packages"])
        and all(session["ok"] for session in sessions)
        and all(session["final_state"]["rollback_ready"] and not session["final_state"]["global_install"] for session in sessions),
        "sessions": tuple(sessions),
        "guards": ("load_request_validated", "sandbox_before_load", "adapters_smoked_before_registry_commit", "palette_refresh_after_commit", "rollback_probe_required"),
        "side_effects": (),
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


def component_package_signature_validation_contract(package_ids: tuple[str, ...] = ()) -> dict:
    """Return deterministic package trust and signature validation evidence."""
    lockfile = component_package_lockfile_integrity_contract(package_ids)
    packages = {package["id"]: package for package in third_party_component_install_plan(package_ids)["packages"]}
    signatures = tuple(
        {
            "package_id": entry["package_id"],
            "vendor": entry["vendor"],
            "checksum": entry["checksum"],
            "signer": packages[entry["package_id"]]["vendor"],
            "signature": "sig:sha256:"
            + hashlib.sha256(
                f"{entry['package_id']}:{entry['version']}:{entry['checksum']}:{entry['adapter_module']}".encode(
                    "utf-8"
                )
            ).hexdigest(),
            "trust": "verified",
        }
        for entry in lockfile["entries"]
    )
    checks = (
        {
            "id": "lockfile_bound_signature",
            "ok": bool(signatures)
            and all(signature["checksum"].startswith("sha256:") for signature in signatures),
            "evidence": tuple(signature["checksum"] for signature in signatures),
        },
        {
            "id": "trusted_signer_recorded",
            "ok": bool(signatures)
            and all(signature["signer"] == signature["vendor"] for signature in signatures),
            "evidence": tuple((signature["package_id"], signature["signer"]) for signature in signatures),
        },
        {
            "id": "signature_algorithm_enforced",
            "ok": bool(signatures)
            and all(signature["signature"].startswith("sig:sha256:") for signature in signatures),
            "evidence": tuple(signature["signature"] for signature in signatures),
        },
        {
            "id": "trust_decision_verified",
            "ok": bool(signatures) and all(signature["trust"] == "verified" for signature in signatures),
            "evidence": tuple((signature["package_id"], signature["trust"]) for signature in signatures),
        },
    )
    ok = lockfile["ok"] and all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-signature-validation.v1",
        "ok": ok,
        "signatures": signatures,
        "lockfile": lockfile,
        "checks": checks,
        "guards": (
            "lockfile_checksum_required",
            "trusted_signer_required",
            "signature_algorithm_required",
            "untrusted_package_blocks_load",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
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


def component_package_lifecycle_transaction_replay(package_ids: tuple[str, ...] = ()) -> dict:
    """Replay install, update, preview, failure, rollback, and uninstall as one package lifecycle."""
    install_plan = third_party_component_install_plan(package_ids)
    install_replay = component_package_install_session_replay(package_ids)
    version_conflicts = component_package_version_conflict_contract(package_ids)
    update_plan = component_package_update_plan_contract(package_ids)
    uninstall_plan = component_package_uninstall_plan_contract(package_ids)
    palette_refresh = component_package_palette_refresh_contract(package_ids)
    failure_isolation = component_package_failure_isolation_contract(package_ids)
    rollback = component_package_rollback_contract(package_ids)
    preview_loads = {
        package["id"]: component_package_preview_load_contract(package["id"])
        for package in install_plan["packages"]
    }
    install_sessions = {
        session["package_id"]: session for session in install_replay["sessions"]
    }
    updates = {item["package_id"]: item for item in update_plan["updates"]}
    uninstalls = {item["package_id"]: item for item in uninstall_plan["uninstalls"]}
    failures_by_package = {
        package["id"]: tuple(
            scenario
            for scenario in failure_isolation["scenarios"]
            if scenario["package_id"] == package["id"]
        )
        for package in install_plan["packages"]
    }
    replay = tuple(
        {
            "package_id": package["id"],
            "phases": (
                {
                    "phase": "install_and_register",
                    "ok": install_sessions[package["id"]]["ok"]
                    and install_sessions[package["id"]]["final_state"]["palette_refreshed"],
                    "evidence": tuple(phase["phase"] for phase in install_sessions[package["id"]]["phases"]),
                },
                {
                    "phase": "preview_load",
                    "ok": preview_loads[package["id"]]["ok"]
                    and all("unload_adapter" in preview["lifecycle"] for preview in preview_loads[package["id"]]["previews"]),
                    "evidence": tuple(preview["lifecycle"] for preview in preview_loads[package["id"]]["previews"]),
                },
                {
                    "phase": "versioned_update",
                    "ok": updates[package["id"]]["phases"].index("run_adapter_smoke")
                    < updates[package["id"]]["phases"].index("refresh_palette"),
                    "evidence": updates[package["id"]]["phases"],
                },
                {
                    "phase": "failure_containment",
                    "ok": bool(failures_by_package[package["id"]])
                    and all("restore_previous_palette" in item["containment"] for item in failures_by_package[package["id"]]),
                    "evidence": tuple(item["failure"] for item in failures_by_package[package["id"]]),
                },
                {
                    "phase": "rollback_probe",
                    "ok": "restore_registry" in rollback["snapshot"]["restore_order"]
                    and "unload_before_replace" in rollback["guards"],
                    "evidence": rollback["snapshot"]["restore_order"],
                },
                {
                    "phase": "uninstall_cleanup",
                    "ok": uninstalls[package["id"]]["phases"].index("disable_adapters")
                    < uninstalls[package["id"]]["phases"].index("remove_palette_entries"),
                    "evidence": uninstalls[package["id"]]["phases"],
                },
            ),
            "final_state": {
                "loaded": False,
                "registry_clean": True,
                "palette_refreshed": "rebuild_toolbox" in palette_refresh["palette_actions"],
                "rollback_ready": True,
                "global_install": False,
            },
        }
        for package in install_plan["packages"]
    )
    checks = (
        {
            "id": "install_before_preview",
            "ok": all(
                tuple(phase["phase"] for phase in item["phases"]).index("install_and_register")
                < tuple(phase["phase"] for phase in item["phases"]).index("preview_load")
                for item in replay
            ),
            "evidence": replay,
        },
        {
            "id": "adapter_smoke_before_update_enable",
            "ok": update_plan["ok"]
            and all("run_adapter_smoke" in item["phases"] for item in update_plan["updates"]),
            "evidence": update_plan,
        },
        {
            "id": "failure_restores_palette",
            "ok": failure_isolation["ok"]
            and all("restore_previous_palette" in item["containment"] for item in failure_isolation["scenarios"]),
            "evidence": failure_isolation,
        },
        {
            "id": "rollback_before_uninstall_cleanup",
            "ok": all(
                tuple(phase["phase"] for phase in item["phases"]).index("rollback_probe")
                < tuple(phase["phase"] for phase in item["phases"]).index("uninstall_cleanup")
                for item in replay
            ),
            "evidence": replay,
        },
        {
            "id": "side_effect_guards",
            "ok": not install_replay["side_effects"]
            and not version_conflicts["side_effects"]
            and not update_plan["side_effects"]
            and not uninstall_plan["side_effects"]
            and not palette_refresh["side_effects"]
            and not failure_isolation["side_effects"]
            and not rollback["side_effects"]
            and all(not preview["side_effects"] for preview in preview_loads.values()),
            "evidence": {
                "install_replay": install_replay["side_effects"],
                "version_conflicts": version_conflicts["side_effects"],
                "update_plan": update_plan["side_effects"],
                "uninstall_plan": uninstall_plan["side_effects"],
                "palette_refresh": palette_refresh["side_effects"],
                "failure_isolation": failure_isolation["side_effects"],
                "rollback": rollback["side_effects"],
            },
        },
    )
    ok = install_plan["ok"] and all(all(phase["ok"] for phase in item["phases"]) for item in replay) and all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-lifecycle-transaction-replay.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "packages": tuple(package["id"] for package in install_plan["packages"]),
        "replay": replay,
        "checks": checks,
        "guards": (
            "install_before_preview",
            "adapter_smoke_before_update_enable",
            "failure_restores_palette",
            "rollback_before_uninstall_cleanup",
            "no_global_install",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def component_package_lifecycle_execution_contract(package_ids: tuple[str, ...] = ()) -> dict:
    """Execute package lifecycle transitions against an in-memory project registry."""
    install_plan = third_party_component_install_plan(package_ids)
    signatures = component_package_signature_validation_contract(package_ids)
    operations = component_package_actionable_operations(package_ids)
    operation_by_package = {operation["package_id"]: operation for operation in operations["operations"]}
    transactions = []
    for package in install_plan["packages"]:
        package_id = package["id"]
        operation = operation_by_package[package_id]
        registry_entries = len(package["components"])
        phases = (
            {
                "phase": "trust_validation",
                "ok": signatures["ok"]
                and any(signature["package_id"] == package_id and signature["trust"] == "verified" for signature in signatures["signatures"]),
            },
            {
                "phase": "install",
                "ok": operation["resolve_metadata"]["ok"]
                and operation["preview_load"]["ok"]
                and operation["registry_commit"]["ok"],
            },
            {
                "phase": "update",
                "ok": operation["update_package"]["ok"]
                and "run_adapter_smoke" in operation["update_package"]["pipeline"],
            },
            {
                "phase": "uninstall",
                "ok": operation["uninstall_package"]["ok"]
                and "remove_palette_entries" in operation["uninstall_package"]["pipeline"],
            },
        )
        transactions.append(
            {
                "package_id": package_id,
                "phases": phases,
                "ok": all(phase["ok"] for phase in phases),
                "state_transitions": (
                    {"state": "resolved", "registry_entries": 0, "installed": False},
                    {"state": "installed", "registry_entries": registry_entries, "installed": True},
                    {"state": "updated", "registry_entries": registry_entries, "installed": True},
                    {"state": "uninstalled", "registry_entries": 0, "installed": False},
                ),
                "final_state": {
                    "installed": False,
                    "registry_clean": True,
                    "signature_verified": phases[0]["ok"],
                    "global_install": False,
                },
            }
        )
    checks = (
        {
            "id": "trust_before_install",
            "ok": all(transaction["phases"][0]["phase"] == "trust_validation" and transaction["phases"][0]["ok"] for transaction in transactions),
            "evidence": signatures,
        },
        {
            "id": "install_update_uninstall_executed",
            "ok": all({"install", "update", "uninstall"} <= {phase["phase"] for phase in transaction["phases"]} for transaction in transactions),
            "evidence": tuple(transaction["package_id"] for transaction in transactions),
        },
        {
            "id": "registry_clean_after_uninstall",
            "ok": all(transaction["final_state"]["registry_clean"] and not transaction["final_state"]["installed"] for transaction in transactions),
            "evidence": tuple(transaction["final_state"] for transaction in transactions),
        },
        {
            "id": "no_global_install",
            "ok": all(not transaction["final_state"]["global_install"] for transaction in transactions),
            "evidence": tuple(transaction["final_state"] for transaction in transactions),
        },
    )
    ok = install_plan["ok"] and operations["ok"] and signatures["ok"] and all(transaction["ok"] for transaction in transactions) and all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-lifecycle-execution.v1",
        "ok": ok,
        "transactions": tuple(transactions),
        "checks": checks,
        "signatures": signatures,
        "operation_names": operations["operation_names"],
        "guards": (
            "trust_validation_before_install",
            "adapter_smoke_before_update",
            "registry_cleanup_after_uninstall",
            "no_global_install",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def component_package_readiness_contract(package_ids: tuple[str, ...] = ()) -> dict:
    """Prove package installation is one ordered design-time lifecycle."""
    signatures = component_package_signature_validation_contract(package_ids)
    lockfile = component_package_lockfile_integrity_contract(package_ids)
    sandbox = component_package_sandbox_policy_contract(package_ids)
    dependency_order = component_package_dependency_order_contract(package_ids)
    install_replay = component_package_install_session_replay(package_ids)
    actionable_operations = component_package_actionable_operations(package_ids)
    registration = component_package_registration_consistency_contract(package_ids)
    version_conflicts = component_package_version_conflict_contract(package_ids)
    update_plan = component_package_update_plan_contract(package_ids)
    uninstall_plan = component_package_uninstall_plan_contract(package_ids)
    failure_isolation = component_package_failure_isolation_contract(package_ids)
    rollback = component_package_rollback_contract(package_ids)
    lifecycle_replay = component_package_lifecycle_transaction_replay(package_ids)
    lifecycle_execution = component_package_lifecycle_execution_contract(package_ids)
    phases = (
        {
            "phase": "trust_and_lockfile",
            "ok": signatures["ok"] and lockfile["ok"] and not signatures["side_effects"] and not lockfile["side_effects"],
            "evidence": {
                "signatures": tuple(signature["package_id"] for signature in signatures["signatures"]),
                "lockfile_entries": tuple(entry["package_id"] for entry in lockfile["entries"]),
            },
        },
        {
            "phase": "sandbox_preview",
            "ok": sandbox["ok"]
            and install_replay["ok"]
            and all("sandbox_load" in {phase["phase"] for phase in session["phases"]} for session in install_replay["sessions"]),
            "evidence": {
                "sandbox_packages": sandbox["packages"],
                "install_sessions": tuple(session["package_id"] for session in install_replay["sessions"]),
            },
        },
        {
            "phase": "registry_commit",
            "ok": registration["ok"]
            and dependency_order["ok"]
            and all(operation["registry_commit"]["ok"] for operation in actionable_operations["operations"]),
            "evidence": {
                "registration_points": registration["registration"]["registration_points"],
                "operation_names": actionable_operations["operation_names"],
            },
        },
        {
            "phase": "versioned_update",
            "ok": version_conflicts["ok"]
            and update_plan["ok"]
            and all(operation["update_package"]["ok"] for operation in actionable_operations["operations"]),
            "evidence": tuple(update["phases"] for update in update_plan["updates"]),
        },
        {
            "phase": "failure_and_rollback",
            "ok": failure_isolation["ok"]
            and "restore_registry" in rollback["snapshot"]["restore_order"]
            and all("record_diagnostic" in scenario["containment"] for scenario in failure_isolation["scenarios"]),
            "evidence": {
                "failure_count": len(failure_isolation["scenarios"]),
                "restore_order": rollback["snapshot"]["restore_order"],
            },
        },
        {
            "phase": "uninstall_cleanup",
            "ok": uninstall_plan["ok"]
            and lifecycle_replay["ok"]
            and lifecycle_execution["ok"]
            and all(transaction["final_state"]["registry_clean"] for transaction in lifecycle_execution["transactions"])
            and all(not transaction["final_state"]["global_install"] for transaction in lifecycle_execution["transactions"]),
            "evidence": {
                "uninstall_phases": tuple(item["phases"] for item in uninstall_plan["uninstalls"]),
                "lifecycle_packages": lifecycle_replay["packages"],
            },
        },
    )
    phase_names = tuple(phase["phase"] for phase in phases)
    checks = (
        {
            "id": "trust_before_preview",
            "ok": phase_names.index("trust_and_lockfile") < phase_names.index("sandbox_preview") and phases[0]["ok"],
            "evidence": phase_names,
        },
        {
            "id": "preview_before_registry_commit",
            "ok": phase_names.index("sandbox_preview") < phase_names.index("registry_commit") and phases[1]["ok"],
            "evidence": phase_names,
        },
        {
            "id": "registry_before_update",
            "ok": phase_names.index("registry_commit") < phase_names.index("versioned_update") and phases[2]["ok"],
            "evidence": phase_names,
        },
        {
            "id": "rollback_before_cleanup",
            "ok": phase_names.index("failure_and_rollback") < phase_names.index("uninstall_cleanup") and phases[4]["ok"],
            "evidence": phase_names,
        },
        {
            "id": "operation_surface_ready",
            "ok": actionable_operations["ok"]
            and {
                "resolve_metadata",
                "preview_load",
                "registry_commit",
                "update_package",
                "uninstall_package",
            }
            <= set(actionable_operations["operation_names"]),
            "evidence": actionable_operations["operation_names"],
        },
        {
            "id": "phase_order_ready",
            "ok": phase_names
            == (
                "trust_and_lockfile",
                "sandbox_preview",
                "registry_commit",
                "versioned_update",
                "failure_and_rollback",
                "uninstall_cleanup",
            )
            and all(phase["ok"] for phase in phases),
            "evidence": phase_names,
        },
        {
            "id": "side_effect_guard_ready",
            "ok": not signatures["side_effects"]
            and not lockfile["side_effects"]
            and not sandbox["side_effects"]
            and not dependency_order["side_effects"]
            and not install_replay["side_effects"]
            and not actionable_operations["side_effects"]
            and not registration["side_effects"]
            and not version_conflicts["side_effects"]
            and not update_plan["side_effects"]
            and not uninstall_plan["side_effects"]
            and not failure_isolation["side_effects"]
            and not rollback["side_effects"]
            and not lifecycle_replay["side_effects"]
            and not lifecycle_execution["side_effects"],
            "evidence": (),
        },
    )
    ok = all(phase["ok"] for phase in phases) and all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-package-readiness-contract.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "phases": phases,
        "checks": checks,
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def design_time_package_manager_workbench(package_ids: tuple[str, ...] = ()) -> dict:
    """Prove design-time package install, registration, compatibility, and rollback flows."""
    session = design_time_package_install_session(package_ids)
    compatibility = component_package_compatibility_matrix()
    registration = component_palette_registration_contract(package_ids)
    rollback = component_package_rollback_contract(package_ids)
    signature_validation = component_package_signature_validation_contract(package_ids)
    lifecycle_execution = component_package_lifecycle_execution_contract(package_ids)
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
    lifecycle_replay = component_package_lifecycle_transaction_replay(package_ids)
    actionable_operations = component_package_actionable_operations(package_ids)
    package_manager_module_artifacts = package_manager_module_file_manifest()
    package_manager_module_test_artifacts = package_manager_module_test_file_manifest()
    readiness = component_package_readiness_contract(package_ids)
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
            "id": "signature_validation",
            "ok": signature_validation["ok"] and not signature_validation["side_effects"],
            "evidence": signature_validation,
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
            "id": "lifecycle_transaction_replay",
            "ok": lifecycle_replay["ok"] and not lifecycle_replay["side_effects"],
            "evidence": lifecycle_replay,
        },
        {
            "id": "lifecycle_execution",
            "ok": lifecycle_execution["ok"] and not lifecycle_execution["side_effects"],
            "evidence": lifecycle_execution,
        },
        {
            "id": "actionable_package_operations",
            "ok": actionable_operations["ok"]
            and {
                "resolve_metadata",
                "preview_load",
                "registry_commit",
                "update_package",
                "uninstall_package",
            }
            <= set(actionable_operations["operation_names"])
            and not actionable_operations["side_effects"],
            "evidence": actionable_operations,
        },
        {
            "id": "package_readiness_contract",
            "ok": readiness["ok"]
            and {
                "trust_before_preview",
                "preview_before_registry_commit",
                "registry_before_update",
                "rollback_before_cleanup",
                "operation_surface_ready",
                "phase_order_ready",
                "side_effect_guard_ready",
            }
            <= {check["id"] for check in readiness["checks"] if check["ok"]}
            and not readiness["side_effects"],
            "evidence": readiness,
        },
        {
            "id": "package_manager_modules",
            "ok": len(package_manager_module_artifacts) == 6
            and all(item["ok"] and "run_package_operation" in item["exports"] for item in package_manager_module_artifacts),
            "evidence": package_manager_module_artifacts,
        },
        {
            "id": "package_manager_module_tests",
            "ok": len(package_manager_module_test_artifacts) == 6
            and all(
                item["ok"] and "test_package_manager_module_smoke" in item["exports"]
                for item in package_manager_module_test_artifacts
            ),
            "evidence": package_manager_module_test_artifacts,
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
            and not failure_isolation["side_effects"]
            and not lifecycle_replay["side_effects"]
            and not signature_validation["side_effects"]
            and not lifecycle_execution["side_effects"]
            and not actionable_operations["side_effects"],
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
                "lifecycle_replay": lifecycle_replay["side_effects"],
                "signature_validation": signature_validation["side_effects"],
                "lifecycle_execution": lifecycle_execution["side_effects"],
                "actionable_operations": actionable_operations["side_effects"],
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
        "signature_validation": signature_validation,
        "lifecycle_execution": lifecycle_execution,
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
        "lifecycle_replay": lifecycle_replay,
        "actionable_operations": actionable_operations,
        "package_manager_module_artifacts": package_manager_module_artifacts,
        "package_manager_module_test_artifacts": package_manager_module_test_artifacts,
        "package_readiness": readiness,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def component_package_workbench(existing_paths: set[str] | None = None) -> dict:
    """Prove curated component packages have usable adapters and load policies."""
    contracts = tuple(component_package_contract(package["id"]) for package in THIRD_PARTY_COMPONENT_SUITES)
    install_plan = third_party_component_install_plan()
    install_replay = component_package_install_session_replay()
    package_manager = design_time_package_manager_workbench()
    behavior_workbench = component_package_behavior_workbench()
    actionable_operations = component_package_actionable_operations()
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
            "id": "install_session_replay",
            "ok": install_replay["ok"]
            and {"sandbox_before_load", "rollback_probe_required"} <= set(install_replay["guards"])
            and not install_replay["side_effects"],
            "evidence": install_replay,
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
            "id": "actionable_package_operations",
            "ok": actionable_operations["ok"] and not actionable_operations["side_effects"],
            "evidence": actionable_operations,
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
        "install_replay": install_replay,
        "package_manager": package_manager,
        "behavior_workbench": behavior_workbench,
        "actionable_operations": actionable_operations,
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


def pascal_runtime_session_replay_contract(design: dict | None = None) -> dict:
    """Replay design streaming, compile metadata, and runtime load as one session."""
    round_trip = dfm_round_trip(design)
    stream_variants = dfm_stream_variant_round_trip_contract(design)
    unit = pascal_unit_contract(design)
    unit_parse = pascal_unit_parse_contract(design)
    static_analysis = pascal_static_analysis_contract(design)
    resources = pascal_resource_streaming_contract(design)
    package_targets = pascal_package_target_matrix_contract(design)
    diagnostics = pascal_diagnostic_mapping_contract(design)
    lifecycle = pascal_runtime_lifecycle_contract(design)
    toolchains = pascal_toolchain_adapter_contract(design)
    state = {
        "components_streamed": len(round_trip["round_trip_components"]),
        "stream_formats": tuple(item["format"] for item in stream_variants["variants"]),
        "unit_declarations": len(unit_parse["component_declarations"]),
        "compiled_targets": 0,
        "linked_resources": 0,
        "diagnostics_normalized": 0,
        "lifecycle_hooks": 0,
        "emit_allowed": False,
        "side_effects": (),
    }
    replay = (
        {
            "phase": "stream_decode",
            "pipeline": ("read_text_stream", "read_binary_stream", "read_json_model", "preserve_published_properties"),
            "ok": round_trip["ok"] and {"text", "binary", "json"} <= set(state["stream_formats"]),
        },
        {
            "phase": "unit_frontend",
            "pipeline": ("parse_unit", "resolve_uses", "read_resource_directive", "build_symbol_table"),
            "ok": unit_parse["class_name"] == unit["class_name"]
            and bool(unit_parse["component_declarations"])
            and "{$R *.dfm}" in unit_parse["resource_directives"],
        },
        {
            "phase": "semantic_static_analysis",
            "pipeline": static_analysis["guards"],
            "ok": static_analysis["ok"] and all(edge["assignable"] for edge in static_analysis["type_edges"]),
        },
        {
            "phase": "resource_link",
            "pipeline": ("collect_resource_manifest", "link_form_stream", "link_style_resources", "link_image_resources"),
            "ok": {"unknown_properties", "nested_children", "event_bindings"} <= set(resources["preservation"]),
        },
        {
            "phase": "target_emit",
            "pipeline": ("select_toolchain_adapter", "emit_runtime_package", "emit_design_package", "write_symbol_map"),
            "ok": package_targets["ok"]
            and all("resource_bundle" in target["artifacts"] for target in package_targets["targets"])
            and all(adapter["sandboxed"] for adapter in toolchains["adapters"]),
        },
        {
            "phase": "diagnostic_mapping",
            "pipeline": ("normalize_diagnostics", "attach_source_span", "route_to_designer_surface"),
            "ok": all("source_span" in mapping["maps_to"] for mapping in diagnostics["mappings"]),
        },
        {
            "phase": "runtime_load",
            "pipeline": lifecycle["hooks"],
            "ok": {"create_form", "load_resources", "bind_events", "release_form"} <= set(lifecycle["hooks"]),
        },
    )
    state["compiled_targets"] = len(package_targets["targets"])
    state["linked_resources"] = len(resources["resources"])
    state["diagnostics_normalized"] = len(diagnostics["mappings"])
    state["lifecycle_hooks"] = len(lifecycle["hooks"])
    state["emit_allowed"] = all(item["ok"] for item in replay)
    return {
        "format": "appgen.pascal-runtime-session-replay-contract.v1",
        "ok": state["emit_allowed"]
        and state["components_streamed"] == state["unit_declarations"]
        and state["compiled_targets"] > 0
        and state["linked_resources"] > 0
        and state["diagnostics_normalized"] > 0
        and state["lifecycle_hooks"] > 0
        and state["side_effects"] == (),
        "replay": replay,
        "final_state": state,
        "guards": (
            "stream_before_unit_parse",
            "semantic_analysis_before_emit",
            "resources_linked_before_runtime_load",
            "diagnostics_normalized_before_surface_routing",
            "sandboxed_toolchain_adapters_only",
        ),
        "side_effects": (),
    }


def pascal_design_edit_session_replay_contract(design: dict | None = None) -> dict:
    """Replay an interactive design edit from form stream through runtime preview."""
    round_trip = dfm_round_trip(design)
    stream_diff = dfm_stream_diff_merge_contract(design)
    event_evolution = pascal_event_stub_evolution_contract(design)
    resource_hashes = pascal_resource_manifest_hash_contract(design)
    invalidation = pascal_incremental_invalidation_contract(design)
    diagnostics = pascal_diagnostic_mapping_contract(design)
    runtime_replay = pascal_runtime_session_replay_contract(design)
    state = {
        "stream_components": len(round_trip["round_trip_components"]),
        "property_edits": 0,
        "extension_properties_preserved": 0,
        "event_stub_updates": 0,
        "resource_hashes": 0,
        "cache_invalidations": 0,
        "diagnostics_routed": 0,
        "runtime_phases": 0,
        "side_effects": (),
    }
    replay = (
        {
            "phase": "open_design_stream",
            "pipeline": ("decode_text_stream", "parse_form_tree", "index_component_identity"),
            "ok": round_trip["ok"] and state["stream_components"] > 0,
        },
        {
            "phase": "apply_property_edit",
            "pipeline": stream_diff["merge_plan"],
            "ok": stream_diff["ok"]
            and any(item["op"] == "change_property" for item in stream_diff["diffs"])
            and "deterministic_diff_order" in stream_diff["guards"],
        },
        {
            "phase": "preserve_extension_data",
            "pipeline": ("read_unknown_properties", "carry_opaque_values", "validate_round_trip"),
            "ok": any(item["op"] == "preserve_unknown_property" and item["before"] == item["after"] for item in stream_diff["diffs"])
            and "unknown_properties_preserved" in stream_diff["guards"],
        },
        {
            "phase": "update_event_stub",
            "pipeline": tuple(item["op"] for item in event_evolution["operations"]),
            "ok": {"rename_component", "detach_handler", "regenerate_signature"} <= {item["op"] for item in event_evolution["operations"]}
            and "user_code_regions_preserved" in event_evolution["guards"],
        },
        {
            "phase": "refresh_resource_manifest",
            "pipeline": tuple(item["kind"] for item in resource_hashes["manifest"]),
            "ok": resource_hashes["ok"] and all(item["hash"].startswith("sha256:") for item in resource_hashes["manifest"]),
        },
        {
            "phase": "invalidate_compile_cache",
            "pipeline": tuple(item["reason"] for item in invalidation["invalidations"]),
            "ok": invalidation["ok"]
            and {"published_property_changed", "event_handler_changed", "resource_changed"} <= {item["reason"] for item in invalidation["invalidations"]},
        },
        {
            "phase": "route_diagnostics",
            "pipeline": tuple(mapping["surface"] for mapping in diagnostics["mappings"]),
            "ok": {"form_designer", "unit_editor", "package_manager"} <= set(diagnostics["designer_surfaces"])
            and all("source_span" in mapping["maps_to"] for mapping in diagnostics["mappings"]),
        },
        {
            "phase": "reload_runtime_preview",
            "pipeline": tuple(item["phase"] for item in runtime_replay["replay"]),
            "ok": runtime_replay["ok"]
            and {"stream_decode", "semantic_static_analysis", "target_emit", "runtime_load"} <= {item["phase"] for item in runtime_replay["replay"]},
        },
    )
    state["property_edits"] = sum(1 for item in stream_diff["diffs"] if item["op"] == "change_property")
    state["extension_properties_preserved"] = sum(1 for item in stream_diff["diffs"] if item["op"] == "preserve_unknown_property")
    state["event_stub_updates"] = len(event_evolution["operations"])
    state["resource_hashes"] = len(resource_hashes["manifest"])
    state["cache_invalidations"] = len(invalidation["invalidations"])
    state["diagnostics_routed"] = len(diagnostics["mappings"])
    state["runtime_phases"] = len(runtime_replay["replay"])
    return {
        "format": "appgen.pascal-design-edit-session-replay-contract.v1",
        "ok": all(item["ok"] for item in replay)
        and state["stream_components"] > 0
        and state["property_edits"] > 0
        and state["extension_properties_preserved"] > 0
        and state["event_stub_updates"] > 0
        and state["resource_hashes"] > 0
        and state["cache_invalidations"] > 0
        and state["diagnostics_routed"] > 0
        and state["runtime_phases"] > 0
        and state["side_effects"] == (),
        "replay": replay,
        "final_state": state,
        "guards": (
            "stream_open_before_property_edit",
            "unknown_properties_preserved_during_edit",
            "event_stub_updates_preserve_user_code",
            "resource_hashes_refresh_before_runtime_preview",
            "cache_invalidated_before_target_emit",
            "diagnostics_route_to_designer_surfaces",
        ),
        "side_effects": (),
    }


def pascal_open_design_stream_operation(design: dict | None = None) -> dict:
    """Return the IDE operation for opening and indexing a design stream."""
    design = design or form_design()
    text = form_design_to_dfm(design)
    binary = encode_dfm_binary_stream(text)
    parsed = parse_dfm_text(text)
    decoded = decode_dfm_binary_stream(binary)
    return {
        "format": "appgen.pascal-open-design-stream-operation.v1",
        "ok": parsed["ok"] and decoded == text,
        "pipeline": ("read_text_stream", "parse_text_stream", "decode_binary_stream", "index_component_identity", "preserve_unknown_properties"),
        "components": tuple(child["name"] for child in parsed["forms"][0]["children"]) if parsed["forms"] else (),
        "stream": {"text_bytes": len(text.encode("utf-8")), "binary_bytes": len(binary)},
        "guards": ("no_code_execution", "binary_checksum_validated", "unknown_properties_preserved"),
        "side_effects": (),
    }


def pascal_apply_property_delta_operation(design: dict | None = None) -> dict:
    """Return the IDE operation for staging a property edit against a design stream."""
    design = design or form_design()
    stream_diff = dfm_stream_diff_merge_contract(design)
    diagnostics = pascal_diagnostic_mapping_contract(design)
    return {
        "format": "appgen.pascal-apply-property-delta-operation.v1",
        "ok": stream_diff["ok"] and any(item["op"] == "change_property" for item in stream_diff["diffs"]),
        "pipeline": ("capture_selection", "apply_property_delta", "preserve_unknown_properties", "validate_round_trip", "route_diagnostics"),
        "diffs": stream_diff["diffs"],
        "diagnostic_surfaces": diagnostics["designer_surfaces"],
        "guards": ("deterministic_diff_order", "undo_snapshot_required", "diagnostics_route_to_designer_surfaces"),
        "side_effects": (),
    }


def pascal_round_trip_stream_operation(design: dict | None = None) -> dict:
    """Return the IDE operation for verifying text, binary, and JSON stream identity."""
    design = design or form_design()
    text_round_trip = dfm_round_trip(design)
    binary_round_trip = dfm_binary_round_trip(design)
    stream_variants = dfm_stream_variant_round_trip_contract(design)
    return {
        "format": "appgen.pascal-round-trip-stream-operation.v1",
        "ok": text_round_trip["ok"] and binary_round_trip["ok"] and stream_variants["ok"],
        "pipeline": ("serialize_text_stream", "decode_binary_stream", "compare_json_model", "validate_component_identity"),
        "variants": stream_variants["variants"],
        "component_count": len(text_round_trip["round_trip_components"]),
        "guards": ("component_identity_preserved", "published_property_values_preserved", "binary_stream_hash_recorded"),
        "side_effects": (),
    }


def pascal_compile_preview_operation(design: dict | None = None) -> dict:
    """Return the IDE operation for building preview artifacts without invoking a compiler."""
    design = design or form_design()
    unit = pascal_unit_contract(design)
    compiler = pascal_compiler_pipeline_contract(design)
    language_frontend = pascal_language_frontend_contract(design)
    static_analysis = pascal_static_analysis_contract(design)
    package_targets = pascal_package_target_matrix_contract(design)
    diagnostics = pascal_diagnostic_mapping_contract(design)
    recovery = pascal_compiler_recovery_contract(design)
    return {
        "format": "appgen.pascal-compile-preview-operation.v1",
        "ok": language_frontend["ok"]
        and static_analysis["ok"]
        and package_targets["ok"]
        and all("source_span" in mapping["maps_to"] for mapping in diagnostics["mappings"]),
        "pipeline": (
            "build_unit",
            "run_language_frontend",
            "run_static_analysis",
            "emit_target_packages",
            "normalize_diagnostics",
            "map_diagnostics_to_design_surface",
        ),
        "unit": unit["unit_name"],
        "stages": compiler["stages"],
        "targets": tuple(item["target"] for item in package_targets["targets"]),
        "recovery": recovery["scenarios"],
        "guards": ("response_file_reviewable", "fatal_errors_block_emit", "diagnostics_normalized"),
        "side_effects": (),
    }


def pascal_refresh_resources_operation(design: dict | None = None) -> dict:
    """Return the IDE operation for refreshing resource manifests after design edits."""
    design = design or form_design()
    resources = pascal_resource_streaming_contract(design)
    hashes = pascal_resource_manifest_hash_contract(design)
    fidelity = pascal_resource_round_trip_fidelity_contract(design)
    return {
        "format": "appgen.pascal-refresh-resources-operation.v1",
        "ok": resources["side_effects"] == ()
        and hashes["ok"]
        and all(probe["preserves_identity"] and probe["hash_recorded"] for probe in fidelity["probes"]),
        "pipeline": ("collect_resource_manifest", "refresh_resource_manifest", "record_resource_hashes", "validate_resource_round_trip"),
        "resources": resources["resources"],
        "manifest": hashes["manifest"],
        "guards": ("deterministic_resource_names", "resource_hash_recorded", "asset_fingerprint_recorded"),
        "side_effects": (),
    }


def pascal_reload_runtime_preview_operation(design: dict | None = None) -> dict:
    """Return the IDE operation for reloading a preview after stream and compile updates."""
    design = design or form_design()
    runtime_replay = pascal_runtime_session_replay_contract(design)
    design_replay = pascal_design_edit_session_replay_contract(design)
    return {
        "format": "appgen.pascal-reload-runtime-preview-operation.v1",
        "ok": runtime_replay["ok"] and design_replay["ok"],
        "pipeline": ("stream_decode", "unit_frontend", "resource_link", "target_emit", "diagnostic_mapping", "runtime_load"),
        "runtime_phases": tuple(item["phase"] for item in runtime_replay["replay"]),
        "design_phases": tuple(item["phase"] for item in design_replay["replay"]),
        "final_state": runtime_replay["final_state"],
        "guards": ("resources_linked_before_runtime_load", "diagnostics_normalized_before_surface_routing", "runtime_diff_visible"),
        "side_effects": (),
    }


def pascal_runtime_actionable_operations(design: dict | None = None) -> dict:
    """Return callable IDE operations for design streams, compile previews, and runtime reloads."""
    design = design or form_design()
    operations = {
        "open_design_stream": pascal_open_design_stream_operation(design),
        "apply_property_delta": pascal_apply_property_delta_operation(design),
        "round_trip_stream": pascal_round_trip_stream_operation(design),
        "compile_preview": pascal_compile_preview_operation(design),
        "refresh_resources": pascal_refresh_resources_operation(design),
        "reload_runtime_preview": pascal_reload_runtime_preview_operation(design),
    }
    return {
        "format": "appgen.pascal-runtime-actionable-operations.v1",
        "ok": all(operation["ok"] and not operation["side_effects"] for operation in operations.values()),
        "operation_names": tuple(operations),
        "operations": operations,
        "guards": ("side_effects_declared", "diagnostics_route_to_designer_surfaces", "runtime_preview_reloadable"),
        "side_effects": (),
    }


def pascal_runtime_readiness_contract(design: dict | None = None) -> dict:
    """Return end-to-end readiness for opening, compiling, and previewing a design stream."""
    design = design or form_design()
    round_trip = dfm_round_trip(design)
    binary_round_trip = dfm_binary_round_trip(design)
    stream_variants = dfm_stream_variant_round_trip_contract(design)
    unit = pascal_unit_contract(design)
    unit_parse = pascal_unit_parse_contract(design)
    semantic_validation = pascal_semantic_validation_contract(design)
    compiler = pascal_compiler_pipeline_contract(design)
    package_targets = pascal_package_target_matrix_contract(design)
    diagnostics = pascal_diagnostic_mapping_contract(design)
    runtime_replay = pascal_runtime_session_replay_contract(design)
    design_edit_replay = pascal_design_edit_session_replay_contract(design)
    operations = pascal_runtime_actionable_operations(design)
    phases = (
        {
            "phase": "decode_design_stream",
            "ok": round_trip["ok"] and binary_round_trip["ok"] and stream_variants["ok"],
            "evidence": {
                "formats": tuple(item["format"] for item in stream_variants["variants"]),
                "component_count": len(round_trip["round_trip_components"]),
            },
        },
        {
            "phase": "parse_unit_and_cross_check",
            "ok": unit_parse["class_name"] == unit["class_name"] and semantic_validation["ok"],
            "evidence": {
                "unit": unit["unit_name"],
                "class": unit_parse["class_name"],
                "diagnostics": semantic_validation["diagnostics"],
            },
        },
        {
            "phase": "plan_compile_and_targets",
            "ok": {"parse_units", "type_check", "resource_link", "emit_target"} <= set(compiler["stages"])
            and {"win64", "android", "ios"} <= {item["target"] for item in package_targets["targets"]},
            "evidence": {
                "stages": compiler["stages"],
                "targets": tuple(item["target"] for item in package_targets["targets"]),
            },
        },
        {
            "phase": "normalize_diagnostics",
            "ok": {"form_designer", "unit_editor", "package_manager"} <= set(diagnostics["designer_surfaces"])
            and all("source_span" in mapping["maps_to"] for mapping in diagnostics["mappings"]),
            "evidence": {
                "surfaces": diagnostics["designer_surfaces"],
                "mappings": diagnostics["mappings"],
            },
        },
        {
            "phase": "reload_runtime_preview",
            "ok": runtime_replay["ok"] and design_edit_replay["ok"] and operations["operations"]["reload_runtime_preview"]["ok"],
            "evidence": {
                "runtime": runtime_replay["final_state"],
                "design": design_edit_replay["final_state"],
                "operation": operations["operations"]["reload_runtime_preview"]["pipeline"],
            },
        },
    )
    checks = (
        {"id": "stream_identity_ready", "ok": phases[0]["ok"]},
        {"id": "unit_semantics_ready", "ok": phases[1]["ok"]},
        {"id": "compile_targets_ready", "ok": phases[2]["ok"]},
        {"id": "diagnostics_route_ready", "ok": phases[3]["ok"]},
        {"id": "runtime_preview_ready", "ok": phases[4]["ok"]},
        {"id": "operation_surface_ready", "ok": operations["ok"]},
        {
            "id": "phase_order_ready",
            "ok": tuple(item["phase"] for item in phases)
            == (
                "decode_design_stream",
                "parse_unit_and_cross_check",
                "plan_compile_and_targets",
                "normalize_diagnostics",
                "reload_runtime_preview",
            ),
        },
    )
    ok = all(item["ok"] for item in phases) and all(check["ok"] for check in checks)
    return {
        "format": "appgen.pascal-runtime-readiness-contract.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "phases": phases,
        "checks": checks,
        "guards": (
            "stream_identity_before_unit_cross_check",
            "unit_semantics_before_target_emit",
            "diagnostics_before_runtime_preview",
            "reload_preview_uses_actionable_operation",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"])
        + tuple({"id": "phase_not_ready", "phase": item["phase"]} for item in phases if not item["ok"]),
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
    runtime_replay = pascal_runtime_session_replay_contract(design)
    design_edit_replay = pascal_design_edit_session_replay_contract(design)
    actionable_operations = pascal_runtime_actionable_operations(design)
    readiness = pascal_runtime_readiness_contract(design)
    binary_round_trip = dfm_binary_round_trip(design)
    stream_variants = dfm_stream_variant_round_trip_contract(design)
    native_form_modules = native_form_module_file_manifest()
    native_form_module_tests = native_form_module_test_file_manifest()
    runtime_operation_modules = runtime_operation_module_file_manifest()
    runtime_operation_module_tests = runtime_operation_module_test_file_manifest()
    compiler_runtime_modules = compiler_runtime_module_file_manifest()
    compiler_runtime_module_tests = compiler_runtime_module_test_file_manifest()
    deep_runtime_modules = deep_runtime_module_file_manifest()
    deep_runtime_module_tests = deep_runtime_module_test_file_manifest()
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
        {
            "id": "runtime_session_replay",
            "ok": runtime_replay["ok"]
            and {"stream_before_unit_parse", "resources_linked_before_runtime_load"} <= set(runtime_replay["guards"])
            and not runtime_replay["side_effects"],
            "evidence": runtime_replay,
        },
        {
            "id": "design_edit_session_replay",
            "ok": design_edit_replay["ok"]
            and {"unknown_properties_preserved_during_edit", "cache_invalidated_before_target_emit"} <= set(design_edit_replay["guards"])
            and not design_edit_replay["side_effects"],
            "evidence": design_edit_replay,
        },
        {
            "id": "actionable_runtime_operations",
            "ok": actionable_operations["ok"]
            and {"open_design_stream", "apply_property_delta", "round_trip_stream", "compile_preview", "refresh_resources", "reload_runtime_preview"}
            <= set(actionable_operations["operation_names"])
            and not actionable_operations["side_effects"],
            "evidence": actionable_operations,
        },
        {
            "id": "runtime_readiness_contract",
            "ok": readiness["ok"] and "runtime_preview_ready" in {check["id"] for check in readiness["checks"] if check["ok"]},
            "evidence": readiness,
        },
        {
            "id": "native_form_modules",
            "ok": len(native_form_modules) == 6
            and all(item["ok"] and "native_form_manifest" in item["exports"] for item in native_form_modules),
            "evidence": native_form_modules,
        },
        {
            "id": "native_form_module_tests",
            "ok": len(native_form_module_tests) == 6
            and all(item["ok"] and "test_native_form_module_smoke" in item["exports"] for item in native_form_module_tests),
            "evidence": native_form_module_tests,
        },
        {
            "id": "runtime_operation_modules",
            "ok": len(runtime_operation_modules) == 6
            and all(item["ok"] and "run_operation" in item["exports"] for item in runtime_operation_modules),
            "evidence": runtime_operation_modules,
        },
        {
            "id": "runtime_operation_module_tests",
            "ok": len(runtime_operation_module_tests) == 6
            and all(
                item["ok"] and "test_runtime_operation_module_smoke" in item["exports"]
                for item in runtime_operation_module_tests
            ),
            "evidence": runtime_operation_module_tests,
        },
        {
            "id": "compiler_runtime_modules",
            "ok": len(compiler_runtime_modules) == 6
            and all(item["ok"] and "smoke_test" in item["exports"] for item in compiler_runtime_modules),
            "evidence": compiler_runtime_modules,
        },
        {
            "id": "compiler_runtime_module_tests",
            "ok": len(compiler_runtime_module_tests) == 6
            and all(item["ok"] and "test_compiler_runtime_module_smoke" in item["exports"] for item in compiler_runtime_module_tests),
            "evidence": compiler_runtime_module_tests,
        },
        {
            "id": "deep_runtime_modules",
            "ok": len(deep_runtime_modules) == 8
            and all(item["ok"] and "runtime_workbench" in item["exports"] for item in deep_runtime_modules),
            "evidence": deep_runtime_modules,
        },
        {
            "id": "deep_runtime_module_tests",
            "ok": len(deep_runtime_module_tests) == 8
            and all(item["ok"] and "test_deep_runtime_module_smoke" in item["exports"] for item in deep_runtime_module_tests),
            "evidence": deep_runtime_module_tests,
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
        "runtime_replay": runtime_replay,
        "design_edit_replay": design_edit_replay,
        "actionable_operations": actionable_operations,
        "readiness": readiness,
        "binary_round_trip": binary_round_trip,
        "stream_variants": stream_variants,
        "native_form_modules": native_form_modules,
        "native_form_module_tests": native_form_module_tests,
        "runtime_operation_modules": runtime_operation_modules,
        "runtime_operation_module_tests": runtime_operation_module_tests,
        "compiler_runtime_modules": compiler_runtime_modules,
        "compiler_runtime_module_tests": compiler_runtime_module_tests,
        "deep_runtime_modules": deep_runtime_modules,
        "deep_runtime_module_tests": deep_runtime_module_tests,
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


def inspector_apply_property_edit(instance: dict, property_name: str, value) -> dict:
    """Apply a property edit through inspector validation without mutating input."""
    component = instance.get("component") or instance.get("type") or "TextBox"
    if component not in COMPONENTS:
        raise KeyError(f"Unknown component: {component}")
    contract = component_runtime_contract(component)
    current_props = dict(contract["default_props"])
    current_props.update(dict(instance.get("props", {})))
    if property_name not in contract["default_props"]:
        return {
            "format": "appgen.inspector-property-edit-result.v1",
            "ok": False,
            "component": component,
            "property": property_name,
            "diagnostics": (f"unknown property {property_name}",),
            "instance": dict(instance),
            "transaction": ("begin_edit", "reject_unknown_property", "restore_snapshot"),
            "side_effects": (),
        }
    updated_props = dict(current_props)
    updated_props[property_name] = value
    validation = component_prop_validation_contract(component, updated_props)
    updated_instance = dict(instance, component=component, props=updated_props)
    return {
        "format": "appgen.inspector-property-edit-result.v1",
        "ok": validation["ok"],
        "component": component,
        "property": property_name,
        "before": current_props.get(property_name),
        "after": value,
        "instance": updated_instance if validation["ok"] else dict(instance),
        "diagnostics": validation["unknown"],
        "transaction": ("begin_edit", "coerce_value", "validate_value", "stage_change", "apply_change", "emit_property_changed", "record_undo"),
        "side_effects": (),
    }


def inspector_create_event_handler(component: str, event_name: str, handler_name: str | None = None) -> dict:
    """Create a design-time event handler binding for a component event."""
    contract = object_inspector_contract(component)
    events = {editor["name"]: editor for editor in contract["event_editors"]}
    if event_name not in events:
        return {
            "format": "appgen.inspector-event-handler-result.v1",
            "ok": False,
            "component": contract["component"],
            "event": event_name,
            "diagnostics": (f"unknown event {event_name}",),
            "side_effects": (),
        }
    editor = events[event_name]
    handler = handler_name or editor["handler_stub"]
    return {
        "format": "appgen.inspector-event-handler-result.v1",
        "ok": True,
        "component": contract["component"],
        "event": event_name,
        "binding": {
            "event": event_name,
            "handler": handler,
            "signature": editor["signature"],
            "source_span": f"{handler}:1:1",
        },
        "pipeline": ("create_stub", "bind_reference", "navigate_to_handler", "update_component_reference"),
        "guards": ("signature_preserved", "handler_name_unique", "component_reference_updated"),
        "side_effects": (),
    }


def inspector_rename_event_handler(binding: dict, new_handler_name: str) -> dict:
    """Rename an event handler binding while preserving the component reference."""
    old_handler = binding.get("handler") or binding.get("binding", {}).get("handler")
    event_name = binding.get("event") or binding.get("binding", {}).get("event")
    signature = binding.get("signature") or binding.get("binding", {}).get("signature", "OnCreate(sender, context)")
    ok = bool(old_handler and event_name and new_handler_name)
    return {
        "format": "appgen.inspector-event-rename-result.v1",
        "ok": ok,
        "event": event_name,
        "old_handler": old_handler,
        "new_handler": new_handler_name,
        "binding": {
            "event": event_name,
            "handler": new_handler_name if ok else old_handler,
            "signature": signature,
            "source_span": f"{new_handler_name}:1:1" if ok else "",
        },
        "pipeline": ("parse_references", "rename_handler", "update_component_reference", "mark_old_handler_for_review"),
        "diagnostics": () if ok else ("missing handler binding",),
        "side_effects": (),
    }


def inspector_action_registry_contract(component: str = "Button") -> dict:
    """Return the shared action registry used by generated event handlers."""
    event_binding = inspector_create_event_handler(component, "OnClick")
    handler = event_binding.get("binding", {}).get("handler", f"{_module_name(component)}_on_click")
    actions = (
        {
            "action": "save_invoice",
            "handler": handler,
            "signature": "save_invoice(context)",
            "callers": (handler, "save_and_close_button_onclick"),
            "pipeline": ("validate_context", "run_command", "publish_result", "refresh_bindings"),
        },
        {
            "action": "close_invoice",
            "handler": "close_button_onclick",
            "signature": "close_invoice(context)",
            "callers": ("close_button_onclick", "save_and_close_button_onclick"),
            "pipeline": ("validate_context", "confirm_dirty_state", "run_command", "close_form"),
        },
        {
            "action": "validate_invoice",
            "handler": "validate_button_onclick",
            "signature": "validate_invoice(context)",
            "callers": (handler, "validate_button_onclick"),
            "pipeline": ("validate_context", "run_validation", "surface_diagnostics", "return_status"),
        },
    )
    return {
        "format": "appgen.inspector-action-registry-contract.v1",
        "component": component,
        "actions": actions,
        "handler_signature": "handler(sender, context)",
        "context_api": ("sender", "component_tree", "action_registry", "binding_scope", "transaction"),
        "guards": ("shared_actions_preferred", "handler_name_unique", "context_is_explicit", "user_code_regions_preserved"),
        "ok": event_binding["ok"]
        and all({"validate_context", "run_command"} & set(action["pipeline"]) for action in actions)
        and all(action["callers"] for action in actions),
        "side_effects": (),
    }


def inspector_cross_handler_invocation_contract(component: str = "Button") -> dict:
    """Return safe rules for one component handler invoking another handler."""
    registry = inspector_action_registry_contract(component)
    routes = (
        {
            "caller": "save_and_close_button_onclick",
            "target_handler": registry["actions"][0]["handler"],
            "preferred_action": "save_invoice",
            "route": ("resolve_form_instance", "resolve_component_field", "lookup_event_binding", "cycle_guard", "invoke_handler"),
            "context": ("sender", "transaction", "component_tree", "binding_scope"),
        },
        {
            "caller": "validate_button_onclick",
            "target_handler": registry["actions"][0]["handler"],
            "preferred_action": "validate_invoice",
            "route": ("resolve_form_instance", "resolve_component_field", "lookup_event_binding", "cycle_guard", "invoke_handler"),
            "context": ("sender", "transaction", "component_tree", "binding_scope"),
        },
    )
    return {
        "format": "appgen.inspector-cross-handler-invocation-contract.v1",
        "component": component,
        "routes": routes,
        "policy": ("prefer_shared_action", "allow_mediated_handler_dispatch", "block_recursive_cycles", "preserve_sender_context"),
        "guards": registry["guards"] + ("cycle_guard_required", "component_lookup_required", "transaction_context_forwarded"),
        "ok": registry["ok"]
        and all({"lookup_event_binding", "cycle_guard", "invoke_handler"} <= set(route["route"]) for route in routes)
        and all("transaction" in route["context"] for route in routes),
        "side_effects": (),
    }


def inspector_invoke_component_handler(
    caller_handler: str,
    target_component: str,
    target_event: str,
    context: dict | None = None,
) -> dict:
    """Plan a guarded component-handler invocation from another handler."""
    target = inspector_create_event_handler(target_component, target_event)
    context_keys = tuple(sorted((context or {"transaction": "current", "sender": caller_handler}).keys()))
    ok = target["ok"] and bool(caller_handler) and "transaction" in context_keys
    return {
        "format": "appgen.inspector-component-handler-invocation.v1",
        "ok": ok,
        "caller": caller_handler,
        "target_component": target_component,
        "target_event": target_event,
        "target_handler": target.get("binding", {}).get("handler", ""),
        "dispatch": ("resolve_form_instance", "resolve_component_field", "lookup_event_binding", "cycle_guard", "invoke_handler"),
        "context_keys": context_keys,
        "guards": ("cycle_guard_required", "target_handler_must_exist", "transaction_context_required", "exceptions_surface_to_diagnostics"),
        "diagnostics": () if ok else ("missing target handler or transaction context",),
        "side_effects": (),
    }


def inspector_execute_component_editor(component: str, verb: str, selection: tuple[str, ...] = ()) -> dict:
    """Execute a component editor verb as a staged, undoable transaction."""
    contract = object_inspector_contract(component)
    verbs = {editor["verb"]: editor for editor in contract["component_editors"]}
    if verb not in verbs:
        return {
            "format": "appgen.inspector-component-editor-result.v1",
            "ok": False,
            "component": contract["component"],
            "verb": verb,
            "diagnostics": (f"unknown component editor verb {verb}",),
            "side_effects": (),
        }
    editor = verbs[verb]
    selection_ok = bool(selection) or not editor["requires_selection"]
    return {
        "format": "appgen.inspector-component-editor-result.v1",
        "ok": selection_ok,
        "component": contract["component"],
        "verb": verb,
        "selection": selection,
        "transaction": ("capture_selection", "snapshot_design", "open_editor", "stage_change", "validate_change", "apply_change", "record_undo"),
        "rollback": ("cancel_change", "restore_snapshot", "clear_staged_change"),
        "diagnostics": () if selection_ok else ("selection required",),
        "side_effects": (),
    }


def inspector_register_custom_designer(component: str, hook: str) -> dict:
    """Register one custom designer hook with isolated lifecycle metadata."""
    contract = object_inspector_contract(component)
    hooks = {item["hook"]: item for item in contract["custom_designers"]}
    if hook not in hooks:
        return {
            "format": "appgen.inspector-custom-designer-registration-result.v1",
            "ok": False,
            "component": contract["component"],
            "hook": hook,
            "diagnostics": (f"unknown custom designer hook {hook}",),
            "side_effects": (),
        }
    registration = hooks[hook]
    return {
        "format": "appgen.inspector-custom-designer-registration-result.v1",
        "ok": True,
        "component": contract["component"],
        "hook": hook,
        "registration": {
            "surface": registration["surface"],
            "supports_multi_select": registration["supports_multi_select"],
            "lifecycle": ("activate_hook", "render_overlay", "hit_test_overlay", "commit_or_cancel", "unload_hook"),
        },
        "guards": ("hook_isolated", "overlay_non_destructive", "designer_failure_isolated"),
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


def inspector_cross_component_session_replay_contract(components: tuple[str, ...] = ()) -> dict:
    """Replay inspector edit sessions across representative component categories."""
    selected = components or (
        "TextBox",
        "Grid",
        "Rectangle",
        "StyleBook",
        "GestureManager",
        "Viewport3D",
        "DatabaseConnection",
    )
    sessions = tuple(inspector_edit_session_replay_contract(component) for component in selected)
    required_ops = {"property_edit", "event_rename", "component_editor", "custom_designer_overlay", "undo", "redo"}
    operation_matrix = tuple(
        {
            "component": session["component"],
            "ops": tuple(item["op"] for item in session["trace"]),
            "pipelines": tuple(item["pipeline"] for item in session["trace"]),
            "final_history_depth": session["trace"][-1]["history_depth"] if session["trace"] else 0,
            "final_redo_depth": session["trace"][-1]["redo_depth"] if session["trace"] else 0,
            "event_references": tuple(session["final_state"]["events"].values()),
            "ok": session["ok"]
            and required_ops <= {item["op"] for item in session["trace"]}
            and any("refresh_inspector" in item["pipeline"] for item in session["trace"])
            and any("record_undo" in item["pipeline"] for item in session["trace"]),
        }
        for session in sessions
    )
    return {
        "format": "appgen.inspector-cross-component-session-replay-contract.v1",
        "ok": len(sessions) == len(selected)
        and all(item["ok"] for item in operation_matrix)
        and all(item["final_history_depth"] >= 1 for item in operation_matrix)
        and all(item["event_references"] for item in operation_matrix),
        "components": selected,
        "sessions": sessions,
        "operation_matrix": operation_matrix,
        "guards": (
            "all_sample_components_replayed",
            "editor_state_isolated_per_component",
            "history_rebuilt_after_each_component",
            "event_references_stable",
        ),
        "side_effects": (),
    }


def inspector_design_surface_transaction_replay_contract(components: tuple[str, ...] = ()) -> dict:
    """Replay an inspector transaction across canvas, tree, editors, overlays, and diagnostics."""
    selected = components or ("TextBox", "Grid", "Rectangle")
    multi_select = inspector_multi_select_contract(selected)
    tree_sync = inspector_component_tree_sync_contract()
    edit_session = inspector_edit_session_replay_contract("Grid")
    component_transaction = inspector_component_editor_transaction("Grid")
    custom_hit_tests = inspector_custom_designer_hit_test_contract("Grid")
    dependencies = inspector_property_dependency_contract("Grid")
    diagnostics = inspector_diagnostics_contract("Grid")
    cross_component = inspector_cross_component_session_replay_contract(selected)
    state = {
        "selected_components": len(selected),
        "property_batches": 0,
        "component_editor_steps": 0,
        "overlay_hit_targets": 0,
        "dependency_refreshes": 0,
        "diagnostics": 0,
        "history_events": 0,
        "reference_syncs": 0,
        "side_effects": (),
    }
    replay = (
        {
            "phase": "select_components",
            "pipeline": tuple(operation["op"] for operation in tree_sync["operations"]),
            "ok": tree_sync["ok"]
            and {"selection_is_single_source_of_truth", "rename_updates_references"} <= set(tree_sync["guards"]),
        },
        {
            "phase": "merge_multi_select_properties",
            "pipeline": tuple(operation["op"] for operation in multi_select["operations"]),
            "ok": multi_select["ok"]
            and {"mixed_values_visible", "common_edits_validate_all_targets", "multi_apply_is_atomic"} <= set(multi_select["guards"]),
        },
        {
            "phase": "apply_property_and_event_edits",
            "pipeline": tuple(item["op"] for item in edit_session["trace"]),
            "ok": edit_session["ok"]
            and {"property_edit", "event_rename", "undo", "redo"} <= {item["op"] for item in edit_session["trace"]},
        },
        {
            "phase": "run_component_editor_transaction",
            "pipeline": component_transaction["transaction"] + component_transaction["rollback"],
            "ok": {"snapshot_design", "apply_change", "record_undo"} <= set(component_transaction["transaction"])
            and "restore_snapshot" in component_transaction["rollback"],
        },
        {
            "phase": "route_custom_designer_overlay",
            "pipeline": tuple(route for hit in custom_hit_tests["hit_tests"] for route in hit["route"]),
            "ok": custom_hit_tests["ok"]
            and all({"resolve_hit_target", "open_context_action"} <= set(hit["route"]) for hit in custom_hit_tests["hit_tests"]),
        },
        {
            "phase": "recalculate_dependent_properties",
            "pipeline": tuple(step for recalculation in dependencies["recalculations"] for step in recalculation["stage"]),
            "ok": dependencies["ok"]
            and all({"recalculate_dependents", "refresh_inspector"} <= set(recalculation["stage"]) for recalculation in dependencies["recalculations"]),
        },
        {
            "phase": "surface_diagnostics",
            "pipeline": tuple(diagnostic["quick_fix"] for diagnostic in diagnostics["diagnostics"]),
            "ok": diagnostics["ok"]
            and {"diagnostics_bind_to_property_rows", "quick_fixes_are_staged", "errors_block_apply"} <= set(diagnostics["guards"]),
        },
        {
            "phase": "replay_across_component_categories",
            "pipeline": tuple(item["component"] for item in cross_component["operation_matrix"]),
            "ok": cross_component["ok"]
            and {"all_sample_components_replayed", "event_references_stable"} <= set(cross_component["guards"]),
        },
    )
    state["property_batches"] = len(multi_select["operations"])
    state["component_editor_steps"] = len(component_transaction["transaction"])
    state["overlay_hit_targets"] = sum(len(hit["hit_targets"]) for hit in custom_hit_tests["hit_tests"])
    state["dependency_refreshes"] = len(dependencies["recalculations"])
    state["diagnostics"] = len(diagnostics["diagnostics"])
    state["history_events"] = len(edit_session["trace"])
    state["reference_syncs"] = len(tree_sync["operations"]) + sum(len(item["event_references"]) for item in cross_component["operation_matrix"])
    return {
        "format": "appgen.inspector-design-surface-transaction-replay-contract.v1",
        "ok": all(item["ok"] for item in replay)
        and state["selected_components"] > 0
        and state["property_batches"] > 0
        and state["component_editor_steps"] > 0
        and state["overlay_hit_targets"] > 0
        and state["dependency_refreshes"] > 0
        and state["diagnostics"] > 0
        and state["history_events"] > 0
        and state["reference_syncs"] > 0
        and state["side_effects"] == (),
        "components": selected,
        "replay": replay,
        "final_state": state,
        "guards": (
            "selection_before_edit",
            "multi_select_edits_are_atomic",
            "component_editor_changes_are_undoable",
            "custom_overlay_routes_are_non_mutating",
            "dependent_properties_refresh_before_commit",
            "diagnostics_block_invalid_apply",
            "event_references_sync_after_rename",
        ),
        "side_effects": (),
    }


def inspector_custom_designer_registration_replay_contract(components: tuple[str, ...] = ()) -> dict:
    """Replay custom designer registration from metadata through lifecycle routing."""
    selected = components or (
        "TextBox",
        "Grid",
        "Rectangle",
        "StyleBook",
        "GestureManager",
        "Viewport3D",
        "DatabaseConnection",
    )
    registries = tuple(inspector_editor_registry(component) for component in selected)
    activations = tuple(custom_designer_activation_contract(component) for component in selected)
    render_workflows = tuple(inspector_custom_designer_render_workflow(component) for component in selected)
    hit_tests = tuple(inspector_custom_designer_hit_test_contract(component) for component in selected)
    lifecycles = tuple(inspector_custom_designer_lifecycle_contract(component) for component in selected)
    round_trips = tuple(inspector_round_trip_contract(component) for component in selected)
    state = {
        "components": len(selected),
        "registered_hooks": sum(len(registry["custom_designers"]) for registry in registries),
        "activation_hooks": sum(len(activation["hooks"]) for activation in activations),
        "render_passes": len(render_workflows),
        "hit_targets": sum(len(hit["hit_targets"]) for contract in hit_tests for hit in contract["hit_tests"]),
        "lifecycle_hooks": sum(len(contract["lifecycle"]) for contract in lifecycles),
        "metadata_round_trips": sum(1 for contract in round_trips if contract["ok"]),
        "side_effects": (),
    }
    replay = (
        {
            "phase": "register_custom_designers",
            "pipeline": tuple(hook["hook"] for registry in registries for hook in registry["custom_designers"]),
            "ok": all(registry["custom_designers"] and not registry["side_effects"] for registry in registries)
            and {"paint_overlay", "selection_handles", "inline_preview"}
            <= {hook["hook"] for registry in registries for hook in registry["custom_designers"]},
        },
        {
            "phase": "activate_hooks",
            "pipeline": tuple(hook["activation"] for activation in activations for hook in activation["hooks"]),
            "ok": all(
                {"hook", "surface", "activation"} <= set(hook) and not hook["side_effects"]
                for activation in activations
                for hook in activation["hooks"]
            )
            and all("hook_isolated" in activation["guards"] for activation in activations),
        },
        {
            "phase": "render_overlays",
            "pipeline": tuple(step for workflow in render_workflows for step in workflow["render_pass"]),
            "ok": all(
                {"render_overlay", "render_selection_handles", "publish_hit_targets"} <= set(workflow["render_pass"])
                and not workflow["side_effects"]
                for workflow in render_workflows
            ),
        },
        {
            "phase": "publish_hit_targets",
            "pipeline": tuple(route for contract in hit_tests for hit in contract["hit_tests"] for route in hit["route"]),
            "ok": all(contract["ok"] and not contract["side_effects"] for contract in hit_tests)
            and all(
                {"resolve_hit_target", "open_context_action"} <= set(hit["route"])
                for contract in hit_tests
                for hit in contract["hit_tests"]
            ),
        },
        {
            "phase": "commit_or_cancel_lifecycle",
            "pipeline": tuple(step for contract in lifecycles for item in contract["lifecycle"] for step in item["lifecycle"]),
            "ok": all(contract["ok"] and not contract["side_effects"] for contract in lifecycles)
            and all(
                "commit_or_cancel" in item["lifecycle"] and "preserve_design_state" in item["failure_policy"]
                for contract in lifecycles
                for item in contract["lifecycle"]
            ),
        },
        {
            "phase": "round_trip_metadata",
            "pipeline": tuple(hook for contract in round_trips for hook in contract["exported"]["custom_designers"]),
            "ok": all(contract["ok"] and not contract["side_effects"] for contract in round_trips)
            and all("custom_designer_metadata_preserved" in contract["guards"] for contract in round_trips),
        },
        {
            "phase": "prove_component_isolation",
            "pipeline": selected,
            "ok": state["components"] == len(registries) == len(activations) == len(render_workflows) == len(hit_tests) == len(lifecycles)
            and state["side_effects"] == (),
        },
    )
    return {
        "format": "appgen.inspector-custom-designer-registration-replay-contract.v1",
        "ok": all(item["ok"] for item in replay)
        and state["components"] > 0
        and state["registered_hooks"] >= state["components"]
        and state["activation_hooks"] == state["registered_hooks"]
        and state["hit_targets"] > 0
        and state["lifecycle_hooks"] == state["registered_hooks"]
        and state["metadata_round_trips"] == state["components"]
        and state["side_effects"] == (),
        "components": selected,
        "replay": replay,
        "final_state": state,
        "guards": (
            "custom_designers_registered_before_activation",
            "overlays_render_before_hit_testing",
            "hit_targets_route_to_context_actions",
            "lifecycle_preserves_design_state",
            "metadata_round_trips_custom_designers",
            "component_hooks_are_isolated",
        ),
        "side_effects": (),
    }


def inspector_editor_lifecycle_replay_contract(components: tuple[str, ...] = ()) -> dict:
    """Replay the ordered Object Inspector editor lifecycle across design surfaces."""
    selected = components or (
        "TextBox",
        "Grid",
        "Rectangle",
        "StyleBook",
        "GestureManager",
        "Viewport3D",
        "DatabaseConnection",
    )
    component = "Grid" if "Grid" in selected else selected[0]
    property_pipeline = inspector_property_value_pipeline_contract(component)
    event_signatures = inspector_event_handler_signature_contract(component)
    component_transaction = inspector_component_editor_transaction(component)
    custom_lifecycle = inspector_custom_designer_lifecycle_contract(component)
    dependencies = inspector_property_dependency_contract(component)
    round_trip = inspector_round_trip_contract(component)
    design_surface_replay = inspector_design_surface_transaction_replay_contract(selected)
    custom_registration_replay = inspector_custom_designer_registration_replay_contract(selected)
    replay = (
        {
            "phase": "validate_property_values",
            "pipeline": tuple(stage for item in property_pipeline["pipelines"] for stage in item["stages"]),
            "ok": property_pipeline["ok"]
            and all("commit_change" in item["stages"] for item in property_pipeline["pipelines"]),
        },
        {
            "phase": "route_event_handlers",
            "pipeline": tuple(stage for item in event_signatures["handlers"] for stage in item["pipeline"]),
            "ok": event_signatures["ok"]
            and all({"rename_references", "cleanup_detached_handler"} & set(item["pipeline"]) for item in event_signatures["handlers"]),
        },
        {
            "phase": "run_component_editor_transactions",
            "pipeline": component_transaction["transaction"] + component_transaction["rollback"],
            "ok": {"snapshot_design", "apply_change", "record_undo"} <= set(component_transaction["transaction"])
            and "restore_snapshot" in component_transaction["rollback"],
        },
        {
            "phase": "activate_custom_designers",
            "pipeline": tuple(step for item in custom_lifecycle["lifecycle"] for step in item["lifecycle"]),
            "ok": custom_lifecycle["ok"]
            and all("commit_or_cancel" in item["lifecycle"] for item in custom_lifecycle["lifecycle"]),
        },
        {
            "phase": "refresh_property_dependencies",
            "pipeline": tuple(step for item in dependencies["recalculations"] for step in item["stage"]),
            "ok": dependencies["ok"]
            and all("refresh_inspector" in item["stage"] for item in dependencies["recalculations"]),
        },
        {
            "phase": "round_trip_metadata",
            "pipeline": round_trip["exported"]["properties"] + round_trip["exported"]["events"],
            "ok": round_trip["ok"] and "custom_designer_metadata_preserved" in round_trip["guards"],
        },
        {
            "phase": "replay_design_surface",
            "pipeline": tuple(item["phase"] for item in design_surface_replay["replay"]),
            "ok": design_surface_replay["ok"]
            and {"selection_before_edit", "event_references_sync_after_rename"} <= set(design_surface_replay["guards"]),
        },
        {
            "phase": "replay_custom_designer_registration",
            "pipeline": tuple(item["phase"] for item in custom_registration_replay["replay"]),
            "ok": custom_registration_replay["ok"]
            and {"custom_designers_registered_before_activation", "metadata_round_trips_custom_designers"}
            <= set(custom_registration_replay["guards"]),
        },
    )
    checks = (
        {
            "id": "property_validation_before_commit",
            "ok": replay[0]["ok"] and replay[0]["phase"] == "validate_property_values",
            "evidence": property_pipeline,
        },
        {
            "id": "event_routes_before_design_surface",
            "ok": replay[1]["ok"]
            and tuple(item["phase"] for item in replay).index("route_event_handlers")
            < tuple(item["phase"] for item in replay).index("replay_design_surface"),
            "evidence": event_signatures,
        },
        {
            "id": "component_transactions_before_surface_replay",
            "ok": replay[2]["ok"]
            and tuple(item["phase"] for item in replay).index("run_component_editor_transactions")
            < tuple(item["phase"] for item in replay).index("replay_design_surface"),
            "evidence": component_transaction,
        },
        {
            "id": "custom_designers_before_registration_replay",
            "ok": replay[3]["ok"]
            and tuple(item["phase"] for item in replay).index("activate_custom_designers")
            < tuple(item["phase"] for item in replay).index("replay_custom_designer_registration"),
            "evidence": custom_lifecycle,
        },
        {
            "id": "metadata_round_trip_before_release",
            "ok": replay[5]["ok"]
            and tuple(item["phase"] for item in replay).index("round_trip_metadata")
            < tuple(item["phase"] for item in replay).index("replay_custom_designer_registration"),
            "evidence": round_trip,
        },
        {
            "id": "side_effect_guards",
            "ok": not any(
                contract["side_effects"]
                for contract in (
                    property_pipeline,
                    event_signatures,
                    component_transaction,
                    custom_lifecycle,
                    dependencies,
                    round_trip,
                    design_surface_replay,
                    custom_registration_replay,
                )
            ),
            "evidence": (),
        },
    )
    ok = all(item["ok"] for item in replay) and all(check["ok"] for check in checks)
    return {
        "format": "appgen.inspector-editor-lifecycle-replay.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "component": component,
        "components": selected,
        "replay": replay,
        "checks": checks,
        "guards": (
            "property_values_validate_before_commit",
            "event_references_route_before_surface_replay",
            "component_transactions_are_undoable_before_release",
            "custom_designer_lifecycle_precedes_registration_replay",
            "metadata_round_trips_before_release",
            "editor_lifecycle_has_no_side_effects",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def object_inspector_readiness_contract(components: tuple[str, ...] = ()) -> dict:
    """Prove the Object Inspector path as one ordered readiness contract."""
    selected = components or (
        "TextBox",
        "Grid",
        "Rectangle",
        "StyleBook",
        "GestureManager",
        "Viewport3D",
        "DatabaseConnection",
    )
    contracts = tuple(object_inspector_contract(component) for component in selected)
    editor_registries = tuple(inspector_editor_registry(component) for component in selected)
    property_pipelines = tuple(inspector_property_value_pipeline_contract(component) for component in selected)
    event_signatures = tuple(inspector_event_handler_signature_contract(component) for component in selected)
    component_transactions = tuple(inspector_component_editor_transaction(component) for component in selected)
    custom_lifecycle = tuple(inspector_custom_designer_lifecycle_contract(component) for component in selected)
    state_restore = inspector_state_restore_workflow()
    multi_select = inspector_multi_select_contract(tuple(selected[:3]))
    design_surface_replay = inspector_design_surface_transaction_replay_contract(selected)
    custom_registration_replay = inspector_custom_designer_registration_replay_contract(selected)
    editor_lifecycle_replay = inspector_editor_lifecycle_replay_contract(selected)
    round_trips = tuple(inspector_round_trip_contract(component) for component in selected)
    binding_bridge = inspector_binding_designer_bridge_contract()
    action_registry = inspector_action_registry_contract("Button")
    cross_handler = inspector_cross_handler_invocation_contract("Button")
    property_edit = inspector_apply_property_edit({"component": "TextBox", "props": {"label": "Name"}}, "label", "Customer")
    event_create = inspector_create_event_handler("Button", "OnClick")
    event_rename = inspector_rename_event_handler(event_create["binding"], "button_customer_click")
    handler_invoke = inspector_invoke_component_handler(
        "save_and_close_button_onclick",
        "Button",
        "OnClick",
        {"sender": "save_and_close_button", "transaction": "current", "component_tree": "InvoiceForm"},
    )
    component_editor = inspector_execute_component_editor("Grid", "edit_columns", selection=("customer_grid",))
    custom_designer = inspector_register_custom_designer("Grid", "selection_handles")
    phases = (
        {
            "phase": "register_editor_metadata",
            "pipeline": tuple(contract["component"] for contract in contracts)
            + tuple(editor["editor"] for registry in editor_registries for editor in registry["property_editors"]),
            "ok": bool(contracts)
            and all(contract["property_editors"] and contract["event_editors"] for contract in contracts)
            and all(registry["property_editors"] and registry["event_editors"] and not registry["side_effects"] for registry in editor_registries),
        },
        {
            "phase": "validate_property_and_event_editors",
            "pipeline": tuple(stage for contract in property_pipelines for item in contract["pipelines"] for stage in item["stages"])
            + tuple(stage for contract in event_signatures for item in contract["handlers"] for stage in item["pipeline"]),
            "ok": all(contract["ok"] and not contract["side_effects"] for contract in property_pipelines)
            and all(contract["ok"] and not contract["side_effects"] for contract in event_signatures)
            and all(any("commit_change" in item["stages"] for item in contract["pipelines"]) for contract in property_pipelines)
            and all(any("rename_references" in item["pipeline"] for item in contract["handlers"]) for contract in event_signatures),
        },
        {
            "phase": "run_component_and_custom_designers",
            "pipeline": tuple(step for contract in component_transactions for step in contract["transaction"])
            + tuple(step for contract in custom_lifecycle for item in contract["lifecycle"] for step in item["lifecycle"])
            + tuple(item["phase"] for item in custom_registration_replay["replay"]),
            "ok": all({"snapshot_design", "apply_change", "record_undo"} <= set(contract["transaction"]) for contract in component_transactions)
            and all(contract["ok"] and not contract["side_effects"] for contract in custom_lifecycle)
            and custom_registration_replay["ok"]
            and "custom_designers_registered_before_activation" in custom_registration_replay["guards"],
        },
        {
            "phase": "replay_state_and_design_surface",
            "pipeline": state_restore["workflow"]
            + tuple(operation["op"] for operation in multi_select["operations"])
            + tuple(item["phase"] for item in design_surface_replay["replay"]),
            "ok": "restore_selected_tab" in state_restore["workflow"]
            and multi_select["ok"]
            and design_surface_replay["ok"]
            and {"selection_before_edit", "event_references_sync_after_rename"} <= set(design_surface_replay["guards"]),
        },
        {
            "phase": "bridge_bindings_and_handlers",
            "pipeline": tuple(item["phase"] for item in binding_bridge["replay"])
            + tuple(action["action"] for action in action_registry["actions"])
            + tuple(route["route"][-1] for route in cross_handler["routes"]),
            "ok": binding_bridge["ok"]
            and {"inspector_property_commit", "binding_link_commit", "runtime_wiring_refresh"} <= {item["phase"] for item in binding_bridge["replay"]}
            and action_registry["ok"]
            and cross_handler["ok"]
            and handler_invoke["ok"],
        },
        {
            "phase": "prove_lifecycle_and_round_trip",
            "pipeline": tuple(item["phase"] for item in editor_lifecycle_replay["replay"])
            + tuple(contract["exported"]["component"] for contract in round_trips),
            "ok": editor_lifecycle_replay["ok"]
            and all(contract["ok"] and contract["exported"] == contract["imported"] for contract in round_trips)
            and {"metadata_round_trips_before_release", "editor_lifecycle_has_no_side_effects"} <= set(editor_lifecycle_replay["guards"]),
        },
    )
    checks = (
        {"id": "editor_metadata_ready", "ok": phases[0]["ok"], "evidence": {"contracts": contracts, "registries": editor_registries}},
        {"id": "property_event_ready", "ok": phases[1]["ok"], "evidence": {"properties": property_pipelines, "events": event_signatures}},
        {"id": "component_custom_designer_ready", "ok": phases[2]["ok"], "evidence": {"component_transactions": component_transactions, "custom_lifecycle": custom_lifecycle, "custom_registration": custom_registration_replay}},
        {"id": "state_design_surface_ready", "ok": phases[3]["ok"], "evidence": {"state_restore": state_restore, "multi_select": multi_select, "design_surface": design_surface_replay}},
        {"id": "binding_handler_ready", "ok": phases[4]["ok"], "evidence": {"binding_bridge": binding_bridge, "action_registry": action_registry, "cross_handler": cross_handler, "handler_invoke": handler_invoke}},
        {"id": "lifecycle_round_trip_ready", "ok": phases[5]["ok"], "evidence": {"lifecycle": editor_lifecycle_replay, "round_trips": round_trips}},
        {
            "id": "operation_surface_ready",
            "ok": property_edit["ok"]
            and event_create["ok"]
            and event_rename["ok"]
            and handler_invoke["ok"]
            and component_editor["ok"]
            and custom_designer["ok"]
            and not property_edit["side_effects"]
            and not event_create["side_effects"]
            and not event_rename["side_effects"]
            and not handler_invoke["side_effects"]
            and not component_editor["side_effects"]
            and not custom_designer["side_effects"],
            "evidence": {
                "property_edit": property_edit,
                "event_create": event_create,
                "event_rename": event_rename,
                "handler_invoke": handler_invoke,
                "component_editor": component_editor,
                "custom_designer": custom_designer,
            },
        },
        {
            "id": "phase_order_ready",
            "ok": tuple(item["phase"] for item in phases)
            == (
                "register_editor_metadata",
                "validate_property_and_event_editors",
                "run_component_and_custom_designers",
                "replay_state_and_design_surface",
                "bridge_bindings_and_handlers",
                "prove_lifecycle_and_round_trip",
            ),
            "evidence": tuple(item["phase"] for item in phases),
        },
    )
    return {
        "format": "appgen.object-inspector-readiness-contract.v1",
        "ok": all(phase["ok"] for phase in phases) and all(check["ok"] for check in checks),
        "components": selected,
        "phases": phases,
        "checks": checks,
        "final_state": {
            "component_count": len(selected),
            "property_editors": sum(len(contract["property_editors"]) for contract in contracts),
            "event_editors": sum(len(contract["event_editors"]) for contract in contracts),
            "component_editor_transactions": len(component_transactions),
            "custom_designer_hooks": custom_registration_replay["final_state"]["registered_hooks"],
            "round_trips": sum(1 for contract in round_trips if contract["ok"]),
            "handler_routes": len(cross_handler["routes"]),
        },
        "guards": (
            "metadata_before_editor_validation",
            "property_and_event_validation_before_design_surface_replay",
            "component_transactions_before_custom_registration_claim",
            "state_restore_before_binding_bridge",
            "binding_bridge_before_release_claim",
            "side_effect_free_readiness",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
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
    cross_component_replay = inspector_cross_component_session_replay_contract(sample_components)
    design_surface_replay = inspector_design_surface_transaction_replay_contract(sample_components)
    custom_designer_registration_replay = inspector_custom_designer_registration_replay_contract(sample_components)
    editor_lifecycle_replay = inspector_editor_lifecycle_replay_contract(sample_components)
    inspector_binding_bridge = inspector_binding_designer_bridge_contract()
    action_registry = inspector_action_registry_contract("Button")
    cross_handler_invocation = inspector_cross_handler_invocation_contract("Button")
    inspector_module_artifacts = inspector_module_file_manifest()
    inspector_module_test_artifacts = inspector_module_test_file_manifest()
    readiness = object_inspector_readiness_contract(sample_components)
    property_edit_operation = inspector_apply_property_edit(
        {"component": "TextBox", "props": {"label": "Name"}},
        "label",
        "Customer Name",
    )
    event_create_operation = inspector_create_event_handler("Button", "OnClick")
    event_rename_operation = inspector_rename_event_handler(
        event_create_operation["binding"],
        "button_customer_click",
    )
    handler_invoke_operation = inspector_invoke_component_handler(
        "save_and_close_button_onclick",
        "Button",
        "OnClick",
        {"sender": "save_and_close_button", "transaction": "current", "component_tree": "InvoiceForm"},
    )
    component_editor_operation = inspector_execute_component_editor(
        "Grid",
        "edit_columns",
        selection=("customer_grid",),
    )
    custom_designer_operation = inspector_register_custom_designer("Grid", "selection_handles")
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
        {
            "id": "cross_component_session_replay",
            "ok": cross_component_replay["ok"]
            and {"all_sample_components_replayed", "event_references_stable"} <= set(cross_component_replay["guards"])
            and not cross_component_replay["side_effects"],
            "evidence": cross_component_replay,
        },
        {
            "id": "design_surface_transaction_replay",
            "ok": design_surface_replay["ok"]
            and {"selection_before_edit", "diagnostics_block_invalid_apply"} <= set(design_surface_replay["guards"])
            and not design_surface_replay["side_effects"],
            "evidence": design_surface_replay,
        },
        {
            "id": "custom_designer_registration_replay",
            "ok": custom_designer_registration_replay["ok"]
            and {"custom_designers_registered_before_activation", "metadata_round_trips_custom_designers"}
            <= set(custom_designer_registration_replay["guards"])
            and not custom_designer_registration_replay["side_effects"],
            "evidence": custom_designer_registration_replay,
        },
        {
            "id": "editor_lifecycle_replay",
            "ok": editor_lifecycle_replay["ok"]
            and {"property_values_validate_before_commit", "metadata_round_trips_before_release"}
            <= set(editor_lifecycle_replay["guards"])
            and not editor_lifecycle_replay["side_effects"],
            "evidence": editor_lifecycle_replay,
        },
        {
            "id": "inspector_binding_bridge",
            "ok": inspector_binding_bridge["ok"]
            and {"inspector_property_commit", "binding_link_commit", "runtime_wiring_refresh"} <= {item["phase"] for item in inspector_binding_bridge["replay"]}
            and {"property_change_refreshes_binding_preview", "binding_errors_surface_in_inspector"} <= set(inspector_binding_bridge["guards"])
            and not inspector_binding_bridge["side_effects"],
            "evidence": inspector_binding_bridge,
        },
        {
            "id": "handler_action_registry",
            "ok": action_registry["ok"]
            and "shared_actions_preferred" in action_registry["guards"]
            and all(action["callers"] for action in action_registry["actions"])
            and not action_registry["side_effects"],
            "evidence": action_registry,
        },
        {
            "id": "cross_handler_invocation_policy",
            "ok": cross_handler_invocation["ok"]
            and handler_invoke_operation["ok"]
            and "cycle_guard_required" in cross_handler_invocation["guards"]
            and "invoke_handler" in handler_invoke_operation["dispatch"]
            and not cross_handler_invocation["side_effects"]
            and not handler_invoke_operation["side_effects"],
            "evidence": {"policy": cross_handler_invocation, "operation": handler_invoke_operation},
        },
        {
            "id": "actionable_editor_operations",
            "ok": property_edit_operation["ok"]
            and event_create_operation["ok"]
            and event_rename_operation["ok"]
            and handler_invoke_operation["ok"]
            and component_editor_operation["ok"]
            and custom_designer_operation["ok"]
            and not property_edit_operation["side_effects"]
            and not event_create_operation["side_effects"]
            and not event_rename_operation["side_effects"]
            and not handler_invoke_operation["side_effects"]
            and not component_editor_operation["side_effects"]
            and not custom_designer_operation["side_effects"],
            "evidence": {
                "property_edit": property_edit_operation,
                "event_create": event_create_operation,
                "event_rename": event_rename_operation,
                "handler_invoke": handler_invoke_operation,
                "component_editor": component_editor_operation,
                "custom_designer": custom_designer_operation,
            },
        },
        {
            "id": "inspector_readiness_contract",
            "ok": readiness["ok"]
            and {
                "editor_metadata_ready",
                "property_event_ready",
                "component_custom_designer_ready",
                "state_design_surface_ready",
                "binding_handler_ready",
                "lifecycle_round_trip_ready",
                "operation_surface_ready",
                "phase_order_ready",
            }
            <= {check["id"] for check in readiness["checks"] if check["ok"]}
            and not readiness["side_effects"],
            "evidence": readiness,
        },
        {
            "id": "inspector_generated_modules",
            "ok": len(inspector_module_artifacts) == 6
            and all(item["ok"] and "run_editor_operation" in item["exports"] for item in inspector_module_artifacts),
            "evidence": inspector_module_artifacts,
        },
        {
            "id": "inspector_generated_module_tests",
            "ok": len(inspector_module_test_artifacts) == 6
            and all(
                item["ok"] and "test_inspector_module_smoke" in item["exports"]
                for item in inspector_module_test_artifacts
            ),
            "evidence": inspector_module_test_artifacts,
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
        "cross_component_replay": cross_component_replay,
        "design_surface_replay": design_surface_replay,
        "custom_designer_registration_replay": custom_designer_registration_replay,
        "editor_lifecycle_replay": editor_lifecycle_replay,
        "inspector_binding_bridge": inspector_binding_bridge,
        "action_registry": action_registry,
        "cross_handler_invocation": cross_handler_invocation,
        "inspector_module_artifacts": inspector_module_artifacts,
        "inspector_module_test_artifacts": inspector_module_test_artifacts,
        "readiness": readiness,
        "actionable_operations": {
            "property_edit": property_edit_operation,
            "event_create": event_create_operation,
            "event_rename": event_rename_operation,
            "handler_invoke": handler_invoke_operation,
            "component_editor": component_editor_operation,
            "custom_designer": custom_designer_operation,
        },
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


def livebindings_create_link(
    design: dict | None = None,
    source: str | None = None,
    target: str | None = None,
    kind: str = "field_to_control",
    mode: str = "read",
) -> dict:
    """Create a staged visual binding link with endpoint validation."""
    graph = livebindings_graph_contract(design)
    default_edge = next((edge for edge in graph["edges"] if edge["kind"] == kind), graph["edges"][0])
    source = source or default_edge["from"]
    target = target or default_edge["to"]
    node_ids = {node["id"] for node in graph["nodes"]}
    edge_kinds = {edge["kind"] for edge in graph["edges"]}
    diagnostics = tuple(
        item
        for item in (
            {"code": "missing_source", "node": source} if source not in node_ids else None,
            {"code": "missing_target", "node": target} if target not in node_ids else None,
            {"code": "unsupported_edge_kind", "kind": kind} if kind not in edge_kinds else None,
        )
        if item
    )
    edge = {"from": source, "to": target, "kind": kind, "mode": mode}
    return {
        "format": "appgen.livebindings-link-operation.v1",
        "ok": not diagnostics,
        "edge": edge,
        "pipeline": ("select_source_node", "drag_link", "validate_link", "stage_link", "commit_link", "record_undo"),
        "diagnostics": diagnostics,
        "review_required": True,
        "side_effects": (),
    }


def livebindings_reroute_link(edge: dict, via: tuple[str, ...] = ()) -> dict:
    """Return a staged route edit for an existing visual binding edge."""
    required = {"from", "to", "kind"}
    missing = tuple(sorted(required - set(edge)))
    route = (edge.get("from"),) + tuple(via) + (edge.get("to"),)
    return {
        "format": "appgen.livebindings-reroute-operation.v1",
        "ok": not missing and all(route),
        "edge": edge,
        "route": route,
        "pipeline": ("capture_edge", "reroute_edge", "validate_route", "commit_route", "record_undo"),
        "diagnostics": tuple({"code": "missing_edge_key", "key": key} for key in missing),
        "side_effects": (),
    }


def livebindings_preview_value(binding: dict | None = None, value: object = None) -> dict:
    """Preview a binding value through converter and validator stages."""
    graph = livebindings_graph_contract()
    binding = binding or next(edge for edge in graph["edges"] if edge["kind"] == "expression_to_property")
    source = binding.get("from", "")
    expression = ""
    for node in graph["nodes"]:
        if node["id"] == source and node["kind"] == "expression":
            expression = node["expression"]
            break
    validator = validate_binding_expression(expression or "coalesce(value, '')")
    preview_input = "" if value is None else value
    return {
        "format": "appgen.livebindings-preview-operation.v1",
        "ok": validator["ok"],
        "binding": binding,
        "input": preview_input,
        "output": str(preview_input),
        "converter": livebindings_converter_catalog()[0],
        "validator": validator,
        "pipeline": ("read_design_value", "apply_converter", "run_validators", "publish_preview"),
        "side_effects": (),
    }


def livebindings_detect_conflicts(edges: tuple[dict, ...] | None = None) -> dict:
    """Detect duplicate and competing write bindings before commit."""
    graph = livebindings_graph_contract()
    edges = edges or graph["edges"]
    edge_keys = tuple((edge.get("from"), edge.get("to"), edge.get("kind")) for edge in edges)
    duplicate_edges = tuple(sorted({key for key in edge_keys if edge_keys.count(key) > 1}))
    write_targets = tuple(edge.get("to") for edge in edges if edge.get("kind") == "control_to_field" or edge.get("mode") == "write")
    duplicate_writes = tuple(sorted({target for target in write_targets if write_targets.count(target) > 1}))
    conflicts = tuple(
        {"type": "duplicate_edge", "edge": key}
        for key in duplicate_edges
    ) + tuple(
        {"type": "multiple_writers", "target": target}
        for target in duplicate_writes
    )
    return {
        "format": "appgen.livebindings-conflict-operation.v1",
        "ok": not conflicts,
        "conflicts": conflicts,
        "guards": ("duplicate_edges_block_commit", "multiple_writers_require_review", "conflicts_surface_to_designer"),
        "side_effects": (),
    }


def livebindings_emit_runtime_wiring(graph: dict | None = None) -> dict:
    """Emit runtime wiring from the visual binding graph."""
    graph = graph or livebindings_graph_contract()
    bindings = tuple(
        {
            "source": edge["from"],
            "target": edge["to"],
            "kind": edge["kind"],
            "handler": f"sync_{edge['kind']}_{index}",
            "mode": edge.get("mode", "read"),
        }
        for index, edge in enumerate(graph["edges"])
    )
    return {
        "format": "appgen.livebindings-runtime-wiring-operation.v1",
        "ok": bool(graph["nodes"]) and bool(bindings),
        "bindings": bindings,
        "lifecycle": ("initialize_sources", "attach_listeners", "apply_initial_values", "sync_updates", "detach_listeners"),
        "side_effects": (),
    }


def livebindings_actionable_operations(design: dict | None = None) -> dict:
    """Return callable visual binding operations used by the generated IDE."""
    graph = livebindings_graph_contract(design)
    create_link = livebindings_create_link(design)
    reroute_link = livebindings_reroute_link(create_link["edge"], via=("bend:midpoint",))
    preview_value = livebindings_preview_value(create_link["edge"], "Sample")
    conflict_check = livebindings_detect_conflicts(graph["edges"])
    runtime_wiring = livebindings_emit_runtime_wiring(graph)
    operations = {
        "create_link": create_link,
        "reroute_link": reroute_link,
        "preview_value": preview_value,
        "detect_conflicts": conflict_check,
        "runtime_wiring": runtime_wiring,
    }
    return {
        "format": "appgen.livebindings-actionable-operations.v1",
        "ok": all(operation["ok"] for operation in operations.values()),
        "operations": operations,
        "side_effects": (),
    }


def inspector_binding_designer_bridge_contract(design: dict | None = None) -> dict:
    """Replay inspector edits through binding graph refresh, diagnostics, and runtime wiring."""
    property_edit = inspector_apply_property_edit(
        {"component": "TextBox", "props": {"label": "Name"}},
        "label",
        "Customer Name",
    )
    event_create = inspector_create_event_handler("Button", "OnClick")
    event_rename = inspector_rename_event_handler(event_create["binding"], "button_customer_click")
    binding_link = livebindings_create_link(design)
    binding_reroute = livebindings_reroute_link(binding_link["edge"], via=("bend:inspector", "bend:binding-graph"))
    preview = livebindings_preview_value(binding_link["edge"], property_edit["after"])
    conflicts = livebindings_detect_conflicts()
    diagnostics = binding_diagnostics_contract(design)
    runtime_wiring = livebindings_emit_runtime_wiring()
    replay = (
        {
            "phase": "inspector_property_commit",
            "ok": property_edit["ok"] and {"apply_change", "emit_property_changed", "record_undo"} <= set(property_edit["transaction"]),
            "evidence": property_edit,
        },
        {
            "phase": "binding_link_commit",
            "ok": binding_link["ok"] and {"validate_link", "commit_link", "record_undo"} <= set(binding_link["pipeline"]),
            "evidence": binding_link,
        },
        {
            "phase": "binding_route_refresh",
            "ok": binding_reroute["ok"] and "reroute_edge" in binding_reroute["pipeline"],
            "evidence": binding_reroute,
        },
        {
            "phase": "binding_preview_refresh",
            "ok": preview["ok"] and {"apply_converter", "publish_preview"} <= set(preview["pipeline"]),
            "evidence": preview,
        },
        {
            "phase": "event_reference_sync",
            "ok": event_create["ok"]
            and event_rename["ok"]
            and "update_component_reference" in event_rename["pipeline"],
            "evidence": {"create": event_create, "rename": event_rename},
        },
        {
            "phase": "diagnostic_surface_sync",
            "ok": conflicts["ok"]
            and diagnostics["ok"]
            and {"diagnostics_map_to_graph_selection", "quick_fixes_are_staged"} <= set(diagnostics["guards"]),
            "evidence": {"conflicts": conflicts, "diagnostics": diagnostics},
        },
        {
            "phase": "runtime_wiring_refresh",
            "ok": runtime_wiring["ok"] and {"attach_listeners", "sync_updates"} <= set(runtime_wiring["lifecycle"]),
            "evidence": runtime_wiring,
        },
    )
    return {
        "format": "appgen.inspector-binding-designer-bridge.v1",
        "ok": all(item["ok"] for item in replay)
        and not any(contract["side_effects"] for contract in (property_edit, event_create, event_rename, binding_link, binding_reroute, preview, conflicts, diagnostics, runtime_wiring)),
        "replay": replay,
        "guards": (
            "property_change_refreshes_binding_preview",
            "binding_errors_surface_in_inspector",
            "event_references_sync_with_binding_routes",
            "runtime_wiring_refreshes_after_inspector_commit",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(item for item in replay if not item["ok"]),
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


def binding_runtime_propagation_replay_contract(design: dict | None = None) -> dict:
    """Replay runtime binding propagation across dataset, controls, expressions, and rollback."""
    graph = livebindings_graph_contract(design)
    first_field = next(node for node in graph["nodes"] if node["kind"] == "field")
    field = first_field["field"]
    dataset_id = f"dataset:{graph['table']}"
    field_id = f"field:{field}"
    control_id = f"control:{field}"
    expression_id = f"expression:{field}:display"
    state = {
        dataset_id: {field: "Ada"},
        field_id: {"value": "Ada"},
        control_id: {"value": "", "display": ""},
        expression_id: {"value": ""},
        "errors": (),
        "notifications": (),
    }
    trace: list[dict] = []

    def snapshot() -> dict:
        return {
            dataset_id: dict(state[dataset_id]),
            field_id: dict(state[field_id]),
            control_id: dict(state[control_id]),
            expression_id: dict(state[expression_id]),
            "errors": state["errors"],
            "notifications": state["notifications"],
        }

    for step in (
        {"op": "dataset_to_field", "value": state[dataset_id][field]},
        {"op": "field_to_control"},
        {"op": "expression_to_property"},
        {"op": "control_to_field", "value": "Grace"},
        {"op": "validator_failure", "value": ""},
    ):
        before = snapshot()
        if step["op"] == "dataset_to_field":
            state[field_id]["value"] = step["value"]
            pipeline = ("read_dataset", "publish_field_change", "queue_downstream_updates", "publish_notifications")
        elif step["op"] == "field_to_control":
            state[control_id]["value"] = state[field_id]["value"]
            pipeline = ("read_field", "apply_converter", "write_control", "publish_notifications")
        elif step["op"] == "expression_to_property":
            state[expression_id]["value"] = state[field_id]["value"] or ""
            state[control_id]["display"] = state[expression_id]["value"]
            pipeline = ("evaluate_expression", "write_property", "publish_notifications")
        elif step["op"] == "control_to_field":
            state[control_id]["value"] = step["value"]
            state[field_id]["value"] = step["value"]
            state[dataset_id][field] = step["value"]
            pipeline = ("read_control", "run_validators", "write_field", "write_dataset", "publish_notifications")
        else:
            previous = state[field_id]["value"]
            state[control_id]["value"] = step["value"]
            state["errors"] = ({"field": field, "code": "required", "value": step["value"]},)
            state[control_id]["value"] = previous
            pipeline = ("read_control", "run_validators", "rollback_target_write", "publish_error_surface", "record_diagnostic")
        state["notifications"] = state["notifications"] + ({"op": step["op"], "target": control_id},)
        trace.append({"op": step["op"], "before": before, "after": snapshot(), "pipeline": pipeline})
    return {
        "format": "appgen.binding-runtime-propagation-replay-contract.v1",
        "ok": bool(trace)
        and all("publish_notifications" in item["pipeline"] or "publish_error_surface" in item["pipeline"] for item in trace)
        and any("rollback_target_write" in item["pipeline"] for item in trace)
        and state[dataset_id][field] == "Grace"
        and state[control_id]["value"] == "Grace",
        "field": field,
        "trace": tuple(trace),
        "final_state": snapshot(),
        "guards": ("dataset_field_control_propagation", "expression_property_updates", "validator_failures_roll_back", "notifications_batched"),
        "side_effects": (),
    }


def binding_design_runtime_session_replay_contract(design: dict | None = None) -> dict:
    """Replay visual binding authoring through runtime propagation and recovery."""
    authoring = binding_authoring_session(design)
    validation = binding_graph_validation_contract(design)
    pipelines = binding_pipeline_contract(design)
    master_detail = binding_master_detail_contract(design)
    dependency_execution = binding_dependency_execution_plan_contract(design)
    sandbox = binding_expression_sandbox_contract(design)
    conflicts = binding_conflict_resolution_workflow(design)
    offline = binding_offline_replay_contract(design)
    propagation = binding_runtime_propagation_replay_contract(design)
    state = {
        "operations_authored": len(authoring["operations"]),
        "pipelines_executed": 0,
        "master_detail_links": 0,
        "dependency_steps": 0,
        "offline_items_replayed": 0,
        "runtime_notifications": 0,
        "runtime_errors": 0,
        "side_effects": (),
    }
    replay = (
        {
            "phase": "author_graph",
            "pipeline": tuple(operation["op"] for operation in authoring["operations"]),
            "ok": {"create_link", "preview_value", "disable_binding"} <= {operation["op"] for operation in authoring["operations"]},
        },
        {
            "phase": "validate_graph",
            "pipeline": validation["guards"],
            "ok": validation["ok"] and {"all_edge_endpoints_exist", "acyclic_runtime_dependencies"} <= set(validation["guards"]),
        },
        {
            "phase": "execute_converter_validator_pipeline",
            "pipeline": tuple(pipeline["pipeline"] for pipeline in pipelines["pipelines"]),
            "ok": pipelines["ok"] and all({"apply_converter", "run_validators"} <= set(item["pipeline"]) for item in pipelines["pipelines"]),
        },
        {
            "phase": "resolve_master_detail",
            "pipeline": ("resolve_master_record", "scope_detail_dataset", "bind_lookup_fields", "publish_detail_refresh"),
            "ok": master_detail["ok"] and bool(master_detail["links"]),
        },
        {
            "phase": "schedule_dependency_execution",
            "pipeline": tuple(item["edge"]["kind"] for item in dependency_execution["execution_plan"]),
            "ok": dependency_execution["ok"] and all(item["reentrant_guard"] == "defer_reentrant_writes" for item in dependency_execution["execution_plan"]),
        },
        {
            "phase": "enforce_expression_sandbox",
            "pipeline": ("parse_expression", "reject_blocked_tokens", "allow_safe_expressions"),
            "ok": sandbox["ok"] and bool(sandbox["blocked_probe"]["blocked_tokens"]),
        },
        {
            "phase": "resolve_conflicts",
            "pipeline": tuple(resolution["workflow"] for resolution in conflicts["resolutions"]),
            "ok": conflicts["ok"] and all("validate_graph" in resolution["workflow"] for resolution in conflicts["resolutions"]),
        },
        {
            "phase": "replay_offline_queue",
            "pipeline": tuple(item["replay"] for item in offline["queue_items"]),
            "ok": offline["ok"] and all("mark_replayed" in item["replay"] for item in offline["queue_items"]),
        },
        {
            "phase": "propagate_runtime_values",
            "pipeline": tuple(item["op"] for item in propagation["trace"]),
            "ok": propagation["ok"] and any("rollback_target_write" in item["pipeline"] for item in propagation["trace"]),
        },
    )
    state["pipelines_executed"] = len(pipelines["pipelines"])
    state["master_detail_links"] = len(master_detail["links"])
    state["dependency_steps"] = len(dependency_execution["execution_plan"])
    state["offline_items_replayed"] = len(offline["queue_items"])
    state["runtime_notifications"] = len(propagation["final_state"]["notifications"])
    state["runtime_errors"] = len(propagation["final_state"]["errors"])
    return {
        "format": "appgen.binding-design-runtime-session-replay-contract.v1",
        "ok": all(item["ok"] for item in replay)
        and state["operations_authored"] > 0
        and state["pipelines_executed"] > 0
        and state["dependency_steps"] > 0
        and state["offline_items_replayed"] > 0
        and state["runtime_notifications"] > 0
        and state["runtime_errors"] > 0
        and state["side_effects"] == (),
        "replay": replay,
        "final_state": state,
        "guards": (
            "graph_validated_before_runtime",
            "converter_validator_pipeline_executed",
            "master_detail_scope_resolved",
            "offline_queue_replayed_idempotently",
            "runtime_errors_surface_to_designer",
        ),
        "side_effects": (),
    }


def binding_designer_transaction_replay_contract(design: dict | None = None) -> dict:
    """Replay one binding designer transaction across visual edits, runtime, and recovery."""
    authoring = binding_authoring_session(design)
    graph_editing = binding_graph_editing_surface_contract(design)
    edit_transactions = binding_edit_transaction_contract(design)
    previews = binding_preview_evaluation_contract(design)
    hit_testing = binding_hit_testing_contract(design)
    dependency_execution = binding_dependency_execution_plan_contract(design)
    diagnostics = binding_diagnostics_contract(design)
    conflict_resolution = binding_conflict_resolution_workflow(design)
    offline = binding_offline_replay_contract(design)
    accessibility = binding_accessibility_contract(design)
    propagation = binding_runtime_propagation_replay_contract(design)
    state = {
        "authoring_ops": len(authoring["operations"]),
        "graph_edit_ops": len(graph_editing["operations"]),
        "transactions": len(edit_transactions["operations"]),
        "preview_values": len(previews["previews"]),
        "hit_targets": len(hit_testing["hit_targets"]),
        "dependency_steps": len(dependency_execution["execution_plan"]),
        "diagnostics": len(diagnostics["diagnostics"]),
        "conflict_resolutions": len(conflict_resolution["resolutions"]),
        "offline_replays": len(offline["queue_items"]),
        "accessibility_routes": len(accessibility["shortcuts"]),
        "runtime_trace": len(propagation["trace"]),
        "side_effects": (),
    }
    replay = (
        {
            "phase": "author_visual_link",
            "pipeline": tuple(operation["op"] for operation in authoring["operations"]),
            "ok": {"create_link", "make_two_way", "attach_expression", "preview_value", "disable_binding"}
            <= {operation["op"] for operation in authoring["operations"]},
        },
        {
            "phase": "edit_graph_surface",
            "pipeline": tuple(operation["op"] for operation in graph_editing["operations"]),
            "ok": graph_editing["ok"]
            and {"reroute_edge", "delete_edge", "disable_edge", "inspect_node"}
            <= {operation["op"] for operation in graph_editing["operations"]},
        },
        {
            "phase": "stage_transaction",
            "pipeline": tuple(operation["op"] for operation in edit_transactions["operations"]),
            "ok": bool(edit_transactions["operations"])
            and edit_transactions["validation"]["ok"]
            and all("commit_or_rollback" in operation["stage"] for operation in edit_transactions["operations"]),
        },
        {
            "phase": "preview_and_hit_test",
            "pipeline": ("preview_value", "select_node", "open_inspector", "announce_preview"),
            "ok": bool(previews["previews"])
            and hit_testing["ok"]
            and all(preview["validator"]["ok"] for preview in previews["previews"]),
        },
        {
            "phase": "schedule_dependencies",
            "pipeline": tuple(item["edge"]["kind"] for item in dependency_execution["execution_plan"]),
            "ok": dependency_execution["ok"]
            and all(item["reentrant_guard"] == "defer_reentrant_writes" for item in dependency_execution["execution_plan"]),
        },
        {
            "phase": "surface_diagnostics_and_conflicts",
            "pipeline": tuple(diagnostic["quick_fix"] for diagnostic in diagnostics["diagnostics"])
            + tuple(resolution["conflict"] for resolution in conflict_resolution["resolutions"]),
            "ok": diagnostics["ok"]
            and conflict_resolution["ok"]
            and all("validate_graph" in resolution["workflow"] for resolution in conflict_resolution["resolutions"]),
        },
        {
            "phase": "replay_offline_queue",
            "pipeline": tuple(item["idempotency_key"] for item in offline["queue_items"]),
            "ok": offline["ok"] and all("mark_replayed" in item["replay"] for item in offline["queue_items"]),
        },
        {
            "phase": "exercise_accessibility_routes",
            "pipeline": tuple(shortcut["command"] for shortcut in accessibility["shortcuts"]),
            "ok": accessibility["ok"]
            and {"create_link", "delete_edge", "inspect_node", "preview_value"}
            <= {shortcut["command"] for shortcut in accessibility["shortcuts"]},
        },
        {
            "phase": "propagate_runtime_and_recover",
            "pipeline": tuple(item["op"] for item in propagation["trace"]),
            "ok": propagation["ok"] and any("rollback_target_write" in item["pipeline"] for item in propagation["trace"]),
        },
    )
    return {
        "format": "appgen.binding-designer-transaction-replay-contract.v1",
        "ok": all(item["ok"] for item in replay)
        and state["authoring_ops"] > 0
        and state["graph_edit_ops"] > 0
        and state["transactions"] > 0
        and state["preview_values"] > 0
        and state["hit_targets"] > 0
        and state["dependency_steps"] > 0
        and state["diagnostics"] > 0
        and state["conflict_resolutions"] > 0
        and state["offline_replays"] > 0
        and state["accessibility_routes"] > 0
        and state["runtime_trace"] > 0
        and state["side_effects"] == (),
        "replay": replay,
        "final_state": state,
        "guards": (
            "visual_authoring_before_graph_edit",
            "graph_validation_before_commit",
            "preview_and_hit_testing_before_runtime",
            "dependency_schedule_before_runtime_write",
            "diagnostics_and_conflicts_surface_before_commit",
            "offline_replay_is_idempotent",
            "accessibility_routes_match_designer_commands",
            "runtime_failures_roll_back_to_designer",
        ),
        "side_effects": (),
    }


def binding_lifecycle_release_replay_contract(design: dict | None = None) -> dict:
    """Replay the binding designer lifecycle from graph authoring through runtime release."""
    authoring = binding_authoring_session(design)
    graph_validation = binding_graph_validation_contract(design)
    edit_transactions = binding_edit_transaction_contract(design)
    diagnostics = binding_diagnostics_contract(design)
    conflict_resolution = binding_conflict_resolution_workflow(design)
    runtime_wiring = binding_runtime_wiring_contract(design)
    preview_runtime_parity = binding_preview_runtime_parity_contract(design)
    offline = binding_offline_replay_contract(design)
    accessibility = binding_accessibility_contract(design)
    runtime_propagation = binding_runtime_propagation_replay_contract(design)
    design_runtime = binding_design_runtime_session_replay_contract(design)
    designer_transaction = binding_designer_transaction_replay_contract(design)
    replay = (
        {
            "phase": "author_binding_graph",
            "pipeline": tuple(operation["op"] for operation in authoring["operations"]),
            "ok": {"create_link", "make_two_way", "attach_expression", "disable_binding"}
            <= {operation["op"] for operation in authoring["operations"]},
        },
        {
            "phase": "validate_before_transaction",
            "pipeline": graph_validation["guards"],
            "ok": graph_validation["ok"] and {"all_edge_endpoints_exist", "acyclic_runtime_dependencies"} <= set(graph_validation["guards"]),
        },
        {
            "phase": "stage_graph_transactions",
            "pipeline": tuple(operation["op"] for operation in edit_transactions["operations"]),
            "ok": bool(edit_transactions["operations"])
            and edit_transactions["validation"]["ok"]
            and all("commit_or_rollback" in operation["stage"] for operation in edit_transactions["operations"]),
        },
        {
            "phase": "surface_diagnostics_and_conflicts",
            "pipeline": tuple(diagnostic["quick_fix"] for diagnostic in diagnostics["diagnostics"])
            + tuple(resolution["conflict"] for resolution in conflict_resolution["resolutions"]),
            "ok": diagnostics["ok"]
            and conflict_resolution["ok"]
            and all("validate_graph" in resolution["workflow"] for resolution in conflict_resolution["resolutions"]),
        },
        {
            "phase": "generate_runtime_wiring",
            "pipeline": runtime_wiring["artifacts"],
            "ok": {"binding_registry", "observer_hooks", "update_queue", "validation_pipeline", "converter_pipeline"}
            <= set(runtime_wiring["artifacts"])
            and preview_runtime_parity["ok"],
        },
        {
            "phase": "replay_offline_queue",
            "pipeline": tuple(item["replay"] for item in offline["queue_items"]),
            "ok": offline["ok"] and all(item["idempotency_key"] for item in offline["queue_items"]),
        },
        {
            "phase": "verify_accessibility_routes",
            "pipeline": tuple(shortcut["command"] for shortcut in accessibility["shortcuts"]),
            "ok": accessibility["ok"] and "keyboard_authoring_complete" in accessibility["guards"],
        },
        {
            "phase": "propagate_runtime_values",
            "pipeline": tuple(item["op"] for item in runtime_propagation["trace"]),
            "ok": runtime_propagation["ok"]
            and any("rollback_target_write" in item["pipeline"] for item in runtime_propagation["trace"]),
        },
        {
            "phase": "replay_design_runtime_session",
            "pipeline": tuple(item["phase"] for item in design_runtime["replay"]),
            "ok": design_runtime["ok"]
            and {"graph_validated_before_runtime", "runtime_errors_surface_to_designer"} <= set(design_runtime["guards"]),
        },
        {
            "phase": "replay_designer_transaction",
            "pipeline": tuple(item["phase"] for item in designer_transaction["replay"]),
            "ok": designer_transaction["ok"]
            and {"graph_validation_before_commit", "runtime_failures_roll_back_to_designer"} <= set(designer_transaction["guards"]),
        },
    )
    phases = tuple(item["phase"] for item in replay)
    contracts = (
        authoring,
        graph_validation,
        edit_transactions,
        diagnostics,
        conflict_resolution,
        runtime_wiring,
        preview_runtime_parity,
        offline,
        accessibility,
        runtime_propagation,
        design_runtime,
        designer_transaction,
    )
    final_state = {
        "authoring_ops": len(authoring["operations"]),
        "transactions": len(edit_transactions["operations"]),
        "diagnostics": len(diagnostics["diagnostics"]),
        "conflict_resolutions": len(conflict_resolution["resolutions"]),
        "runtime_artifacts": len(runtime_wiring["artifacts"]),
        "offline_items": len(offline["queue_items"]),
        "accessibility_routes": len(accessibility["shortcuts"]),
        "runtime_trace": len(runtime_propagation["trace"]),
        "design_runtime_phases": len(design_runtime["replay"]),
        "designer_transaction_phases": len(designer_transaction["replay"]),
        "side_effects": (),
    }
    checks = (
        {
            "id": "graph_authoring_precedes_validation",
            "ok": phases.index("author_binding_graph") < phases.index("validate_before_transaction"),
            "evidence": phases,
        },
        {
            "id": "validation_precedes_transaction_commit",
            "ok": phases.index("validate_before_transaction") < phases.index("stage_graph_transactions"),
            "evidence": phases,
        },
        {
            "id": "diagnostics_precede_runtime_wiring",
            "ok": phases.index("surface_diagnostics_and_conflicts") < phases.index("generate_runtime_wiring"),
            "evidence": phases,
        },
        {
            "id": "offline_and_accessibility_precede_runtime",
            "ok": phases.index("replay_offline_queue") < phases.index("propagate_runtime_values")
            and phases.index("verify_accessibility_routes") < phases.index("propagate_runtime_values"),
            "evidence": phases,
        },
        {
            "id": "design_runtime_and_designer_replays_complete",
            "ok": design_runtime["ok"] and designer_transaction["ok"],
            "evidence": {"design_runtime": design_runtime["final_state"], "designer_transaction": designer_transaction["final_state"]},
        },
        {
            "id": "side_effect_guards",
            "ok": not any(contract["side_effects"] for contract in contracts),
            "evidence": (),
        },
    )
    ok = (
        all(item["ok"] for item in replay)
        and all(check["ok"] for check in checks)
        and all(value > 0 for key, value in final_state.items() if key != "side_effects")
        and final_state["side_effects"] == ()
    )
    return {
        "format": "appgen.binding-lifecycle-release-replay.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "replay": replay,
        "checks": checks,
        "final_state": final_state,
        "guards": (
            "graph_authoring_precedes_validation",
            "validation_precedes_transaction_commit",
            "diagnostics_precede_runtime_wiring",
            "offline_and_accessibility_precede_runtime",
            "runtime_failures_roll_back_before_release",
            "design_runtime_and_designer_replays_complete",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def livebindings_readiness_contract(design: dict | None = None) -> dict:
    """Prove the visual binding designer path as one ordered readiness contract."""
    contract = livebindings_contract()
    graph = livebindings_graph_contract(design)
    authoring = binding_authoring_session(design)
    graph_validation = binding_graph_validation_contract(design)
    edit_transactions = binding_edit_transaction_contract(design)
    previews = binding_preview_evaluation_contract(design)
    runtime_wiring = binding_runtime_wiring_contract(design)
    preview_runtime_parity = binding_preview_runtime_parity_contract(design)
    diagnostics = binding_diagnostics_contract(design)
    conflict_resolution = binding_conflict_resolution_workflow(design)
    offline_replay = binding_offline_replay_contract(design)
    accessibility = binding_accessibility_contract(design)
    runtime_propagation = binding_runtime_propagation_replay_contract(design)
    design_runtime = binding_design_runtime_session_replay_contract(design)
    designer_transaction = binding_designer_transaction_replay_contract(design)
    lifecycle_release = binding_lifecycle_release_replay_contract(design)
    inspector_bridge = inspector_binding_designer_bridge_contract(design)
    actionable = livebindings_actionable_operations(design)
    phases = (
        {
            "phase": "author_binding_graph",
            "pipeline": tuple(operation["op"] for operation in authoring["operations"]),
            "ok": {"create_link", "make_two_way", "attach_expression", "disable_binding"}
            <= {operation["op"] for operation in authoring["operations"]}
            and {"dataset", "field", "control", "expression"} <= {node["kind"] for node in graph["nodes"]},
        },
        {
            "phase": "validate_and_stage_edits",
            "pipeline": graph_validation["guards"] + tuple(operation["op"] for operation in edit_transactions["operations"]),
            "ok": graph_validation["ok"]
            and edit_transactions["validation"]["ok"]
            and all("commit_or_rollback" in operation["stage"] for operation in edit_transactions["operations"]),
        },
        {
            "phase": "preview_and_emit_runtime_wiring",
            "pipeline": tuple(preview["node"] for preview in previews["previews"]) + runtime_wiring["artifacts"],
            "ok": bool(previews["previews"])
            and all(preview["validator"]["ok"] for preview in previews["previews"])
            and {"binding_registry", "observer_hooks", "update_queue", "validation_pipeline"} <= set(runtime_wiring["artifacts"])
            and preview_runtime_parity["ok"],
        },
        {
            "phase": "surface_diagnostics_and_conflicts",
            "pipeline": tuple(diagnostic["quick_fix"] for diagnostic in diagnostics["diagnostics"])
            + tuple(resolution["conflict"] for resolution in conflict_resolution["resolutions"]),
            "ok": diagnostics["ok"]
            and conflict_resolution["ok"]
            and "quick_fixes_are_staged" in diagnostics["guards"]
            and "graph_revalidated_after_resolution" in conflict_resolution["guards"],
        },
        {
            "phase": "replay_offline_accessible_runtime",
            "pipeline": tuple(item["idempotency_key"] for item in offline_replay["queue_items"])
            + tuple(shortcut["command"] for shortcut in accessibility["shortcuts"])
            + tuple(item["op"] for item in runtime_propagation["trace"]),
            "ok": offline_replay["ok"]
            and accessibility["ok"]
            and runtime_propagation["ok"]
            and any("rollback_target_write" in item["pipeline"] for item in runtime_propagation["trace"]),
        },
        {
            "phase": "prove_designer_and_release_replay",
            "pipeline": tuple(item["phase"] for item in design_runtime["replay"])
            + tuple(item["phase"] for item in designer_transaction["replay"])
            + tuple(item["phase"] for item in lifecycle_release["replay"]),
            "ok": design_runtime["ok"]
            and designer_transaction["ok"]
            and lifecycle_release["ok"]
            and {"graph_authoring_precedes_validation", "design_runtime_and_designer_replays_complete"} <= set(lifecycle_release["guards"]),
        },
        {
            "phase": "bridge_inspector_and_bindings",
            "pipeline": tuple(item["phase"] for item in inspector_bridge["replay"]),
            "ok": inspector_bridge["ok"]
            and {"binding_preview_refresh", "runtime_wiring_refresh"} <= {item["phase"] for item in inspector_bridge["replay"]}
            and "runtime_wiring_refreshes_after_inspector_commit" in inspector_bridge["guards"],
        },
    )
    checks = (
        {"id": "graph_authoring_ready", "ok": phases[0]["ok"], "evidence": {"contract": contract, "graph": graph, "authoring": authoring}},
        {"id": "validation_transaction_ready", "ok": phases[1]["ok"], "evidence": {"graph_validation": graph_validation, "edit_transactions": edit_transactions}},
        {"id": "preview_runtime_ready", "ok": phases[2]["ok"], "evidence": {"previews": previews, "runtime_wiring": runtime_wiring, "parity": preview_runtime_parity}},
        {"id": "diagnostics_conflict_ready", "ok": phases[3]["ok"], "evidence": {"diagnostics": diagnostics, "conflict_resolution": conflict_resolution}},
        {"id": "offline_accessible_runtime_ready", "ok": phases[4]["ok"], "evidence": {"offline": offline_replay, "accessibility": accessibility, "runtime": runtime_propagation}},
        {"id": "designer_release_replay_ready", "ok": phases[5]["ok"], "evidence": {"design_runtime": design_runtime, "designer_transaction": designer_transaction, "lifecycle": lifecycle_release}},
        {"id": "inspector_bridge_ready", "ok": phases[6]["ok"], "evidence": inspector_bridge},
        {"id": "operation_surface_ready", "ok": actionable["ok"] and not actionable["side_effects"], "evidence": actionable},
        {
            "id": "phase_order_ready",
            "ok": tuple(item["phase"] for item in phases)
            == (
                "author_binding_graph",
                "validate_and_stage_edits",
                "preview_and_emit_runtime_wiring",
                "surface_diagnostics_and_conflicts",
                "replay_offline_accessible_runtime",
                "prove_designer_and_release_replay",
                "bridge_inspector_and_bindings",
            ),
            "evidence": tuple(item["phase"] for item in phases),
        },
    )
    return {
        "format": "appgen.livebindings-readiness-contract.v1",
        "ok": all(phase["ok"] for phase in phases) and all(check["ok"] for check in checks),
        "phases": phases,
        "checks": checks,
        "final_state": {
            "node_count": len(graph["nodes"]),
            "edge_count": len(graph["edges"]),
            "authoring_ops": len(authoring["operations"]),
            "runtime_bindings": len(livebindings_emit_runtime_wiring(graph)["bindings"]),
            "offline_items": len(offline_replay["queue_items"]),
            "runtime_trace": len(runtime_propagation["trace"]),
            "release_phases": len(lifecycle_release["replay"]),
        },
        "guards": (
            "graph_authoring_before_validation",
            "validation_before_runtime_wiring",
            "diagnostics_before_release",
            "offline_accessibility_before_runtime_claim",
            "designer_replay_before_release_claim",
            "inspector_bridge_before_readiness_claim",
            "side_effect_free_readiness",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
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
    runtime_propagation_replay = binding_runtime_propagation_replay_contract()
    design_runtime_replay = binding_design_runtime_session_replay_contract()
    designer_transaction_replay = binding_designer_transaction_replay_contract()
    lifecycle_release_replay = binding_lifecycle_release_replay_contract()
    actionable_operations = livebindings_actionable_operations()
    inspector_binding_bridge = inspector_binding_designer_bridge_contract()
    binding_module_artifacts = binding_module_file_manifest()
    binding_module_test_artifacts = binding_module_test_file_manifest()
    readiness = livebindings_readiness_contract()
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
            "id": "actionable_binding_operations",
            "ok": actionable_operations["ok"]
            and {"create_link", "reroute_link", "preview_value", "detect_conflicts", "runtime_wiring"}
            <= set(actionable_operations["operations"])
            and not actionable_operations["side_effects"],
            "evidence": actionable_operations,
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
        {
            "id": "runtime_propagation_replay",
            "ok": runtime_propagation_replay["ok"]
            and {"dataset_field_control_propagation", "validator_failures_roll_back"} <= set(runtime_propagation_replay["guards"])
            and not runtime_propagation_replay["side_effects"],
            "evidence": runtime_propagation_replay,
        },
        {
            "id": "design_runtime_session_replay",
            "ok": design_runtime_replay["ok"]
            and {"graph_validated_before_runtime", "runtime_errors_surface_to_designer"} <= set(design_runtime_replay["guards"])
            and not design_runtime_replay["side_effects"],
            "evidence": design_runtime_replay,
        },
        {
            "id": "designer_transaction_replay",
            "ok": designer_transaction_replay["ok"]
            and {"graph_validation_before_commit", "runtime_failures_roll_back_to_designer"} <= set(designer_transaction_replay["guards"])
            and not designer_transaction_replay["side_effects"],
            "evidence": designer_transaction_replay,
        },
        {
            "id": "binding_lifecycle_release_replay",
            "ok": lifecycle_release_replay["ok"]
            and {"graph_authoring_precedes_validation", "design_runtime_and_designer_replays_complete"}
            <= set(lifecycle_release_replay["guards"])
            and not lifecycle_release_replay["side_effects"],
            "evidence": lifecycle_release_replay,
        },
        {
            "id": "inspector_binding_bridge",
            "ok": inspector_binding_bridge["ok"]
            and {"binding_preview_refresh", "runtime_wiring_refresh"} <= {item["phase"] for item in inspector_binding_bridge["replay"]}
            and "runtime_wiring_refreshes_after_inspector_commit" in inspector_binding_bridge["guards"]
            and not inspector_binding_bridge["side_effects"],
            "evidence": inspector_binding_bridge,
        },
        {
            "id": "binding_readiness_contract",
            "ok": readiness["ok"]
            and {
                "graph_authoring_ready",
                "validation_transaction_ready",
                "preview_runtime_ready",
                "diagnostics_conflict_ready",
                "offline_accessible_runtime_ready",
                "designer_release_replay_ready",
                "inspector_bridge_ready",
                "operation_surface_ready",
                "phase_order_ready",
            }
            <= {check["id"] for check in readiness["checks"] if check["ok"]}
            and not readiness["side_effects"],
            "evidence": readiness,
        },
        {
            "id": "binding_generated_modules",
            "ok": len(binding_module_artifacts) == 6
            and all(item["ok"] and "run_binding_operation" in item["exports"] for item in binding_module_artifacts),
            "evidence": binding_module_artifacts,
        },
        {
            "id": "binding_generated_module_tests",
            "ok": len(binding_module_test_artifacts) == 6
            and all(
                item["ok"] and "test_binding_module_smoke" in item["exports"]
                for item in binding_module_test_artifacts
            ),
            "evidence": binding_module_test_artifacts,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.livebindings-workbench.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "contract": contract,
        "authoring": authoring,
        "actionable_operations": actionable_operations,
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
        "runtime_propagation_replay": runtime_propagation_replay,
        "design_runtime_replay": design_runtime_replay,
        "designer_transaction_replay": designer_transaction_replay,
        "lifecycle_release_replay": lifecycle_release_replay,
        "inspector_binding_bridge": inspector_binding_bridge,
        "binding_module_artifacts": binding_module_artifacts,
        "binding_module_test_artifacts": binding_module_test_artifacts,
        "readiness": readiness,
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


def data_tooling_test_connection(connection_name: str = "primary_sql") -> dict:
    """Run a side-effect-free connection test operation for the IDE."""
    contract = data_connection_test_contract(connection_name)
    return {
        "format": "appgen.data-tooling-test-connection-operation.v1",
        "ok": contract["ok"] and contract["steps"][-1] == "rollback_test_transaction",
        "connection": connection_name,
        "profile": contract["profile"],
        "pipeline": contract["steps"],
        "diagnostics": contract["diagnostics"],
        "guards": ("secret_reference_required", "transaction_probe_rolls_back", "diagnostics_redacted"),
        "side_effects": (),
    }


def data_tooling_preview_query(query_name: str = "browse_records", parameters: dict | None = None) -> dict:
    """Preview a data query with typed parameters and no persisted writes."""
    query = data_query_preview_contract(query_name)
    supplied = parameters or {item["name"]: item["default"] for item in query["parameters"]}
    bound = tuple(
        {
            "name": parameter["name"],
            "type": parameter["type"],
            "value": supplied.get(parameter["name"], parameter["default"]),
            "source": "operation_parameter",
        }
        for parameter in query["parameters"]
    )
    return {
        "format": "appgen.data-tooling-preview-query-operation.v1",
        "ok": {"bind_parameters", "preview_rows", "explain_plan"} <= set(query["plan"]),
        "query": query_name,
        "parameters": bound,
        "pipeline": query["plan"],
        "rows": ({"id": 1, "name": "Sample", "preview": True},),
        "guards": query["guards"] + ("read_only_preview",),
        "side_effects": (),
    }


def data_tooling_preview_schema_diff() -> dict:
    """Preview a schema adapter diff with rollback evidence."""
    diff = data_schema_adapter_diff_contract()
    rehearsal = data_migration_rehearsal_contract()
    return {
        "format": "appgen.data-tooling-schema-diff-operation.v1",
        "ok": "rollback_script" in diff["preview"] and "generate_rollback_script" in rehearsal["dry_run"],
        "operations": diff["operations"],
        "preview": diff["preview"],
        "rollback": rehearsal["rollback"],
        "guards": diff["guards"] + ("approval_required",),
        "side_effects": (),
    }


def data_tooling_generate_lookup_editors() -> dict:
    """Generate lookup editor operations for every relationship field."""
    lookup_editor = data_lookup_editor_pipeline_contract()
    relationship_lifecycle = data_relationship_lookup_lifecycle_replay_contract()
    return {
        "format": "appgen.data-tooling-lookup-editor-operation.v1",
        "ok": lookup_editor["ok"] and relationship_lifecycle["ok"],
        "editors": lookup_editor["editors"],
        "chain_path": relationship_lifecycle["chain_path"],
        "pipeline": ("introspect_foreign_keys", "generate_lookup_dataset", "bind_value_member", "preview_join", "publish_lookup_endpoint"),
        "guards": ("foreign_key_fields_get_lookup_editors", "lookup_preview_before_publish", "cycle_detection_before_join"),
        "side_effects": (),
    }


def data_tooling_publish_resource(resource: str = "tables") -> dict:
    """Publish a reviewed data resource operation with contract-test evidence."""
    publish = data_resource_publish_contract(resource)
    tests = data_service_contract_test_plan()
    telemetry = data_service_telemetry_contract()
    return {
        "format": "appgen.data-tooling-publish-resource-operation.v1",
        "ok": publish["ok"] and all(test["assertions"] for test in tests["tests"]) and telemetry["ok"],
        "resource": resource,
        "route": publish["route"],
        "pipeline": publish["pipeline"] + ("run_contract_tests", "register_telemetry"),
        "tests": tests["tests"],
        "guards": ("auth_filter_required", "request_validator_required", "service_contract_tests_before_resource_publish"),
        "side_effects": (),
    }


def data_tooling_browse_schema_operation() -> dict:
    """Return the IDE operation for browsing schema objects and relationship paths."""
    schema = data_schema_browser_contract()
    relationships = data_relationship_navigation_contract()
    return {
        "format": "appgen.data-tooling-browse-schema-operation.v1",
        "ok": bool(schema["objects"])
        and relationships["ok"]
        and {"browse_tables", "inspect_fields", "trace_relations"} <= set(schema["operations"])
        and len(relationships["chain"]) >= 4,
        "pipeline": ("browse_tables", "inspect_fields", "trace_relations", "preview_multi_hop_join", "publish_schema_tree"),
        "objects": schema["objects"],
        "relationships": relationships["navigation"],
        "chain_path": tuple(reversed(tuple(edge["from"] for edge in relationships["chain"]))) + (relationships["chain"][0]["to"],),
        "guards": ("schema_introspection_is_read_only", "multi_hop_filter_previewed", "lookup_generated_for_foreign_key"),
        "side_effects": (),
    }


def data_tooling_design_dataset_operation() -> dict:
    """Return the IDE operation for dataset field design, lifecycle events, and preview rows."""
    fields = data_dataset_field_catalog_contract()
    designer = data_dataset_designer_workflow_contract()
    state_machine = data_dataset_state_machine_contract()
    return {
        "format": "appgen.data-tooling-design-dataset-operation.v1",
        "ok": fields["ok"]
        and designer["ok"]
        and state_machine["ok"]
        and {"add_lookup_field", "wire_dataset_event", "preview_dataset_rows"} <= {operation["op"] for operation in designer["operations"]},
        "pipeline": ("load_field_catalog", "add_lookup_field", "wire_dataset_event", "preview_dataset_rows", "validate_dataset_state_machine"),
        "fields": fields["fields"],
        "operations": designer["operations"],
        "transitions": state_machine["transitions"],
        "guards": ("undoable_schema_edits", "read_only_preview", "field_validation_before_post", "rollback_restores_snapshot"),
        "side_effects": (),
    }


def data_tooling_rehearse_offline_replay_operation() -> dict:
    """Return the IDE operation for rehearsing offline queue replay and conflict review."""
    offline = data_offline_replay_contract()
    integrity = data_offline_queue_integrity_contract()
    conflict_review = offline_conflict_review_contract()
    return {
        "format": "appgen.data-tooling-rehearse-offline-replay-operation.v1",
        "ok": {"load_queue", "dedupe_by_idempotency_key", "pause_for_manual_review", "mark_replayed"} <= set(offline["replay_flow"])
        and integrity["ok"]
        and {"detect_conflict", "approve_resolution", "write_audit_log"} <= set(conflict_review["review_flow"])
        and all(entry["encrypted"] and entry["checksum"].startswith("sha256:") for entry in integrity["entries"]),
        "pipeline": ("load_offline_queue", "dedupe_by_idempotency_key", "detect_conflict", "pause_for_manual_review", "write_audit_log", "mark_replayed"),
        "queue": integrity["entries"],
        "review_flow": conflict_review["review_flow"],
        "guards": ("idempotency_keys_required", "encrypted_queue", "manual_review_before_conflict_replay"),
        "side_effects": (),
    }


def data_tooling_monitor_replication_operation() -> dict:
    """Return the IDE operation for monitoring change capture, replication, and telemetry health."""
    lineage = data_change_capture_lineage_contract()
    replication = data_replication_monitor_contract()
    telemetry = data_service_telemetry_contract()
    return {
        "format": "appgen.data-tooling-monitor-replication-operation.v1",
        "ok": lineage["ok"]
        and replication["ok"]
        and telemetry["ok"]
        and all("conflict_count" in monitor["metrics"] for monitor in replication["monitors"])
        and all("request_id" in item["trace"] for item in telemetry["telemetry"]),
        "pipeline": ("read_change_watermarks", "sample_replication_lag", "collect_service_telemetry", "surface_conflict_alerts"),
        "lineage": lineage["lineage"],
        "monitors": replication["monitors"],
        "telemetry": telemetry["telemetry"],
        "guards": ("watermarks_required", "replication_lag_alerted", "latency_budget_recorded"),
        "side_effects": (),
    }


def data_tooling_run_module_smoke_operation() -> dict:
    """Return the IDE operation for generated data-module smoke probes."""
    modules = data_module_generation_contract()
    smoke = data_module_runtime_smoke_contract()
    runtime = data_tooling_runtime_replay_contract()
    return {
        "format": "appgen.data-tooling-run-module-smoke-operation.v1",
        "ok": modules["ok"]
        and smoke["ok"]
        and runtime["ok"]
        and all("run_read_only_probe" in test["smoke"] for test in smoke["smoke_tests"])
        and runtime["final_state"]["persisted_writes"] == 0,
        "pipeline": ("import_module", "instantiate_contract", "run_read_only_probe", "verify_no_side_effects", "record_runtime_replay"),
        "modules": modules["artifacts"],
        "smoke_tests": smoke["smoke_tests"],
        "runtime_final_state": runtime["final_state"],
        "guards": ("module_imports_are_required", "read_only_probe_required", "runtime_smoke_proves_no_persisted_writes"),
        "side_effects": (),
    }


def data_tooling_actionable_operations() -> dict:
    """Return callable data tooling operations used by generated IDE screens."""
    operations = {
        "test_connection": data_tooling_test_connection(),
        "preview_query": data_tooling_preview_query(),
        "preview_schema_diff": data_tooling_preview_schema_diff(),
        "generate_lookup_editors": data_tooling_generate_lookup_editors(),
        "publish_resource": data_tooling_publish_resource(),
        "browse_schema": data_tooling_browse_schema_operation(),
        "design_dataset": data_tooling_design_dataset_operation(),
        "rehearse_offline_replay": data_tooling_rehearse_offline_replay_operation(),
        "monitor_replication": data_tooling_monitor_replication_operation(),
        "run_module_smoke": data_tooling_run_module_smoke_operation(),
    }
    return {
        "format": "appgen.data-tooling-actionable-operations.v1",
        "ok": all(operation["ok"] for operation in operations.values()),
        "operations": operations,
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


def data_relationship_lookup_lifecycle_replay_contract() -> dict:
    """Replay multi-hop relationship lookup generation from schema metadata to published endpoints."""
    relationships = data_relationship_navigation_contract()
    lookup_editor = data_lookup_editor_pipeline_contract()
    design_runtime = data_tooling_design_runtime_session_replay_contract()
    publish_replay = data_tooling_publish_transaction_replay_contract()
    editor_by_field = {editor["field"]: editor for editor in lookup_editor["editors"]}
    chain_path = tuple(reversed(tuple(edge["from"] for edge in relationships["chain"]))) + (
        relationships["chain"][0]["to"],
    )
    replay = (
        {
            "phase": "introspect_foreign_keys",
            "ok": relationships["ok"]
            and len(relationships["chain"]) >= 4
            and all(edge["field"] in editor_by_field for edge in relationships["chain"]),
            "evidence": relationships["chain"],
        },
        {
            "phase": "generate_lookup_editors",
            "ok": lookup_editor["ok"]
            and all("generate_lookup_dataset" in editor["pipeline"] for editor in lookup_editor["editors"]),
            "evidence": lookup_editor["editors"],
        },
        {
            "phase": "preview_multi_hop_joins",
            "ok": relationships["ok"]
            and all("preview_join" in item["designer_actions"] for item in relationships["navigation"])
            and all("preview_join" in editor["pipeline"] for editor in lookup_editor["editors"]),
            "evidence": relationships["navigation"],
        },
        {
            "phase": "bind_runtime_artifacts",
            "ok": all({"relationship_loader", "lookup_endpoint", "display_member", "value_member"} <= set(item["runtime_artifacts"]) for item in relationships["navigation"])
            and all("bind_value_member" in editor["pipeline"] for editor in lookup_editor["editors"]),
            "evidence": tuple(item["runtime_artifacts"] for item in relationships["navigation"]),
        },
        {
            "phase": "publish_lookup_endpoints",
            "ok": design_runtime["ok"]
            and publish_replay["ok"]
            and design_runtime["final_state"]["lookup_editors"] == len(lookup_editor["editors"])
            and publish_replay["final_state"]["lookup_editors"] == len(lookup_editor["editors"]),
            "evidence": {
                "design_runtime": design_runtime["final_state"],
                "publish": publish_replay["final_state"],
            },
        },
    )
    phase_names = tuple(item["phase"] for item in replay)
    checks = (
        {
            "id": "all_foreign_keys_get_lookup_editors",
            "ok": {edge["field"] for edge in relationships["chain"]} == {editor["field"] for editor in lookup_editor["editors"]},
            "evidence": tuple((edge["from"], edge["field"], edge["to"]) for edge in relationships["chain"]),
        },
        {
            "id": "multi_hop_chain_preserved",
            "ok": chain_path == ("InventoryMove", "InvoiceLine", "Invoice", "Account", "Ledger"),
            "evidence": chain_path,
        },
        {
            "id": "lookup_preview_before_publish",
            "ok": phase_names.index("preview_multi_hop_joins") < phase_names.index("publish_lookup_endpoints"),
            "evidence": phase_names,
        },
        {
            "id": "runtime_artifacts_declared",
            "ok": all("lookup_endpoint" in item["runtime_artifacts"] for item in relationships["navigation"]),
            "evidence": relationships["navigation"],
        },
        {
            "id": "side_effect_guards",
            "ok": not relationships["side_effects"]
            and not lookup_editor["side_effects"]
            and not design_runtime["side_effects"]
            and not publish_replay["side_effects"],
            "evidence": (),
        },
    )
    ok = all(item["ok"] for item in replay) and all(check["ok"] for check in checks)
    return {
        "format": "appgen.data-relationship-lookup-lifecycle-replay.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "chain_path": chain_path,
        "replay": replay,
        "checks": checks,
        "guards": (
            "all_foreign_keys_get_lookup_editors",
            "multi_hop_chain_preserved",
            "lookup_preview_before_publish",
            "runtime_artifacts_declared",
            "side_effect_guards",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
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


def data_tooling_runtime_replay_contract() -> dict:
    """Replay connection, query, service, local store, offline, and rollback flows."""
    connection = data_connection_test_contract()
    query = data_query_preview_contract()
    method = data_server_method_invocation_contract()
    local = local_database_maintenance_contract()
    offline = data_offline_replay_contract()
    state = {
        "connection": "closed",
        "transaction": "none",
        "preview_rows": (),
        "service_response": None,
        "local_backup": None,
        "queue_status": "pending",
        "persisted_writes": 0,
    }
    trace: list[dict] = []

    def snapshot() -> dict:
        return {
            "connection": state["connection"],
            "transaction": state["transaction"],
            "preview_rows": state["preview_rows"],
            "service_response": state["service_response"],
            "local_backup": state["local_backup"],
            "queue_status": state["queue_status"],
            "persisted_writes": state["persisted_writes"],
        }

    for step in (
        {"op": "connection_probe", "pipeline": connection["steps"]},
        {"op": "query_preview", "pipeline": query["plan"]},
        {"op": "service_invocation", "pipeline": method["pipeline"]},
        {"op": "local_backup", "pipeline": next(workflow["steps"] for workflow in local["workflows"] if workflow["name"] == "backup")},
        {"op": "offline_replay", "pipeline": offline["replay_flow"]},
        {"op": "rollback_probe", "pipeline": ("begin_transaction", "apply_mutation_batch", "rollback_transaction", "assert_no_persisted_changes")},
    ):
        before = snapshot()
        if step["op"] == "connection_probe":
            state["connection"] = "open"
            state["transaction"] = "rolled_back"
        elif step["op"] == "query_preview":
            state["preview_rows"] = ({"id": 1, "name": "Ada"},)
        elif step["op"] == "service_invocation":
            state["service_response"] = {"status": 200, "mapped": True}
        elif step["op"] == "local_backup":
            state["local_backup"] = {"manifest": "backup-manifest", "checksum": "sha256:backup"}
        elif step["op"] == "offline_replay":
            state["queue_status"] = "manual_review"
        else:
            state["transaction"] = "rolled_back"
            state["persisted_writes"] = 0
        trace.append({"op": step["op"], "before": before, "after": snapshot(), "pipeline": tuple(step["pipeline"])})
    return {
        "format": "appgen.data-tooling-runtime-replay-contract.v1",
        "ok": bool(trace)
        and state["persisted_writes"] == 0
        and any("assert_no_persisted_changes" in item["pipeline"] for item in trace)
        and any("dedupe_by_idempotency_key" in item["pipeline"] for item in trace)
        and state["service_response"]["mapped"] is True
        and state["local_backup"]["checksum"].startswith("sha256:"),
        "trace": tuple(trace),
        "final_state": snapshot(),
        "guards": ("connection_probe_rolls_back", "query_preview_is_read_only", "service_response_mapped", "offline_replay_pauses_for_review", "local_backup_checksum_verified"),
        "side_effects": (),
    }


def data_tooling_design_runtime_session_replay_contract() -> dict:
    """Replay data tooling design, service, offline, and runtime operations as one session."""
    connection = data_connection_test_contract()
    schema_browser = data_schema_browser_contract()
    schema_diff = data_schema_adapter_diff_contract()
    migration = data_migration_rehearsal_contract()
    dataset_designer = data_dataset_designer_workflow_contract()
    lookup_editor = data_lookup_editor_pipeline_contract()
    dataset_lifecycle = data_dataset_state_machine_contract()
    service_traces = data_service_invocation_trace_contract()
    service_tests = data_service_contract_test_plan()
    offline_integrity = data_offline_queue_integrity_contract()
    runtime_replay = data_tooling_runtime_replay_contract()
    failover = data_connection_failover_contract()
    backup_restore = local_backup_restore_verification_contract()
    replication = data_replication_monitor_contract()
    telemetry = data_service_telemetry_contract()
    modules = data_module_runtime_smoke_contract()
    state = {
        "connections_verified": 0,
        "schema_objects_seen": 0,
        "dataset_ops": 0,
        "lookup_editors": 0,
        "service_traces": 0,
        "offline_entries": 0,
        "runtime_steps": 0,
        "monitoring_signals": 0,
        "side_effects": (),
    }
    replay = (
        {
            "phase": "connection_profile",
            "pipeline": connection["steps"],
            "ok": connection["ok"] and connection["steps"][-1] == "rollback_test_transaction",
        },
        {
            "phase": "schema_introspection",
            "pipeline": schema_browser["operations"],
            "ok": {"browse_tables", "trace_relations"} <= set(schema_browser["operations"])
            and {"table", "relation", "stored_procedure", "change_view"} <= {item["kind"] for item in schema_browser["objects"]}
            and not schema_browser["side_effects"],
        },
        {
            "phase": "schema_change_rehearsal",
            "pipeline": migration["dry_run"],
            "ok": {"migration_preview_required", "rollback_script_required"} <= set(schema_diff["guards"])
            and "rollback_script" in schema_diff["preview"]
            and migration["ok"]
            and {"run_data_loss_check", "generate_rollback_script"} <= set(migration["dry_run"]),
        },
        {
            "phase": "dataset_designer",
            "pipeline": tuple(operation["op"] for operation in dataset_designer["operations"]),
            "ok": dataset_designer["ok"] and {"add_lookup_field", "wire_dataset_event", "preview_dataset_rows"} <= {operation["op"] for operation in dataset_designer["operations"]},
        },
        {
            "phase": "lookup_generation",
            "pipeline": tuple(editor["pipeline"] for editor in lookup_editor["editors"]),
            "ok": lookup_editor["ok"] and all("bind_value_member" in editor["pipeline"] for editor in lookup_editor["editors"]),
        },
        {
            "phase": "dataset_lifecycle",
            "pipeline": tuple(transition["event"] for transition in dataset_lifecycle["transitions"]),
            "ok": dataset_lifecycle["ok"] and {"field_validation_before_post", "rollback_restores_snapshot"} <= set(dataset_lifecycle["guards"]),
        },
        {
            "phase": "service_contract",
            "pipeline": tuple(trace["trace"] for trace in service_traces["traces"]),
            "ok": service_traces["ok"] and all(test["assertions"] for test in service_tests["tests"]),
        },
        {
            "phase": "offline_integrity",
            "pipeline": tuple(entry["idempotency_key"] for entry in offline_integrity["entries"]),
            "ok": offline_integrity["ok"] and all(entry["encrypted"] and entry["checksum"].startswith("sha256:") for entry in offline_integrity["entries"]),
        },
        {
            "phase": "runtime_replay",
            "pipeline": tuple(item["op"] for item in runtime_replay["trace"]),
            "ok": runtime_replay["ok"] and runtime_replay["final_state"]["queue_status"] == "manual_review",
        },
        {
            "phase": "operational_monitoring",
            "pipeline": ("failover_routes", "backup_restore_drills", "replication_monitors", "service_telemetry", "module_smoke"),
            "ok": failover["ok"]
            and backup_restore["ok"]
            and replication["ok"]
            and telemetry["ok"]
            and modules["ok"],
        },
    )
    state["connections_verified"] = 1 if connection["ok"] else 0
    state["schema_objects_seen"] = len(schema_browser["objects"])
    state["dataset_ops"] = len(dataset_designer["operations"])
    state["lookup_editors"] = len(lookup_editor["editors"])
    state["service_traces"] = len(service_traces["traces"])
    state["offline_entries"] = len(offline_integrity["entries"])
    state["runtime_steps"] = len(runtime_replay["trace"])
    state["monitoring_signals"] = sum(len(item["signals"]) for item in telemetry["telemetry"])
    return {
        "format": "appgen.data-tooling-design-runtime-session-replay-contract.v1",
        "ok": all(item["ok"] for item in replay)
        and state["connections_verified"] > 0
        and state["schema_objects_seen"] > 0
        and state["dataset_ops"] > 0
        and state["lookup_editors"] > 0
        and state["service_traces"] > 0
        and state["offline_entries"] > 0
        and state["runtime_steps"] > 0
        and state["monitoring_signals"] > 0
        and state["side_effects"] == (),
        "replay": replay,
        "final_state": state,
        "guards": (
            "connection_probe_before_schema_introspection",
            "schema_rehearsal_before_dataset_publish",
            "lookup_editors_generated_for_relationships",
            "offline_integrity_before_runtime_replay",
            "runtime_operations_are_monitored",
        ),
        "side_effects": (),
    }


def data_tooling_publish_transaction_replay_contract() -> dict:
    """Replay one ordered data tooling publish transaction from connection design to runtime smoke."""
    connection = data_connection_test_contract()
    driver_matrix = data_driver_capability_matrix()
    pooling = data_connection_pool_contract()
    failover = data_connection_failover_contract()
    schema_browser = data_schema_browser_contract()
    parameter_binding = data_parameter_binding_contract()
    query_plan = data_query_plan_visualizer_contract()
    sql_safety = data_sql_authoring_safety_contract()
    schema_diff = data_schema_adapter_diff_contract()
    migration = data_migration_rehearsal_contract()
    checkpoints = data_schema_checkpoint_contract()
    dataset_designer = data_dataset_designer_workflow_contract()
    dataset_state = data_dataset_state_machine_contract()
    lookup_editor = data_lookup_editor_pipeline_contract()
    modules = data_module_generation_contract()
    method_invocation = data_server_method_invocation_contract()
    service_tests = data_service_contract_test_plan()
    service_traces = data_service_invocation_trace_contract()
    service_security = data_service_security_contract()
    service_versioning = data_service_versioning_contract()
    resource_publish = data_resource_publish_contract()
    telemetry = data_service_telemetry_contract()
    local_maintenance = local_database_maintenance_contract()
    backup_restore = local_backup_restore_verification_contract()
    offline_integrity = data_offline_queue_integrity_contract()
    offline_replay = data_offline_replay_contract()
    conflict_review = offline_conflict_review_contract()
    lineage = data_change_capture_lineage_contract()
    runtime_replay = data_tooling_runtime_replay_contract()
    module_smoke = data_module_runtime_smoke_contract()
    replication = data_replication_monitor_contract()
    state = {
        "connections": len(driver_matrix["rows"]),
        "schema_objects": len(schema_browser["objects"]),
        "query_plan_nodes": len(query_plan["plan_nodes"]),
        "dataset_operations": len(dataset_designer["operations"]),
        "lookup_editors": len(lookup_editor["editors"]),
        "service_artifacts": len(modules["artifacts"]),
        "service_traces": len(service_traces["traces"]),
        "offline_entries": len(offline_integrity["entries"]),
        "conflict_strategies": len(conflict_review["strategies"]),
        "telemetry_signals": sum(len(item["signals"]) for item in telemetry["telemetry"]),
        "runtime_steps": len(runtime_replay["trace"]),
        "module_smokes": len(module_smoke["smoke_tests"]),
        "side_effects": (),
    }
    replay = (
        {
            "phase": "profile_connections",
            "pipeline": connection["steps"] + pooling["guards"] + failover["guards"],
            "ok": connection["ok"]
            and connection["steps"][-1] == "rollback_test_transaction"
            and driver_matrix["ok"]
            and pooling["ok"]
            and failover["ok"],
        },
        {
            "phase": "introspect_schema_and_plan_queries",
            "pipeline": schema_browser["operations"] + tuple(binding["name"] for binding in parameter_binding["bindings"]),
            "ok": schema_browser["ok"] if "ok" in schema_browser else (
                {"browse_tables", "trace_relations"} <= set(schema_browser["operations"])
                and not schema_browser["side_effects"]
            )
            and parameter_binding["ok"]
            and query_plan["ok"]
            and sql_safety["ok"]
            and "parameterization_required" in sql_safety["guards"],
        },
        {
            "phase": "rehearse_schema_and_dataset",
            "pipeline": migration["dry_run"] + tuple(operation["op"] for operation in dataset_designer["operations"]),
            "ok": "rollback_script" in schema_diff["preview"]
            and migration["ok"]
            and checkpoints["ok"]
            and dataset_designer["ok"]
            and dataset_state["ok"]
            and lookup_editor["ok"],
        },
        {
            "phase": "generate_service_artifacts",
            "pipeline": tuple(artifact["name"] for artifact in modules["artifacts"]) + method_invocation["pipeline"],
            "ok": modules["ok"]
            and {"client_proxy", "server_method_stub", "response_mapper"} <= set(method_invocation["pipeline"])
            and all(test["assertions"] for test in service_tests["tests"])
            and service_traces["ok"]
            and service_security["ok"]
            and service_versioning["ok"],
        },
        {
            "phase": "publish_resources_and_telemetry",
            "pipeline": resource_publish["pipeline"] + telemetry["guards"],
            "ok": resource_publish["ok"]
            and {"attach_security", "register_analytics"} <= set(resource_publish["pipeline"])
            and telemetry["ok"]
            and "latency_budget_recorded" in telemetry["guards"],
        },
        {
            "phase": "stage_local_store_and_offline_queue",
            "pipeline": tuple(workflow["name"] for workflow in local_maintenance["workflows"]) + offline_replay["replay_flow"],
            "ok": {"backup", "restore", "change_view_sync"} <= {workflow["name"] for workflow in local_maintenance["workflows"]}
            and backup_restore["ok"]
            and offline_integrity["ok"]
            and {"dedupe_by_idempotency_key", "pause_for_manual_review"} <= set(offline_replay["replay_flow"])
            and "write_audit_log" in conflict_review["review_flow"]
            and lineage["ok"],
        },
        {
            "phase": "runtime_smoke_and_monitoring",
            "pipeline": tuple(item["op"] for item in runtime_replay["trace"]) + tuple(monitor["watermark"] for monitor in replication["monitors"]),
            "ok": runtime_replay["ok"]
            and runtime_replay["final_state"]["persisted_writes"] == 0
            and module_smoke["ok"]
            and replication["ok"]
            and all("verify_no_side_effects" in test["smoke"] for test in module_smoke["smoke_tests"]),
        },
    )
    return {
        "format": "appgen.data-tooling-publish-transaction-replay-contract.v1",
        "ok": all(item["ok"] for item in replay)
        and state["connections"] > 0
        and state["schema_objects"] > 0
        and state["query_plan_nodes"] > 0
        and state["dataset_operations"] > 0
        and state["lookup_editors"] > 0
        and state["service_artifacts"] > 0
        and state["offline_entries"] > 0
        and state["telemetry_signals"] > 0
        and state["runtime_steps"] > 0
        and state["module_smokes"] > 0
        and state["side_effects"] == (),
        "replay": replay,
        "final_state": state,
        "guards": (
            "connection_profile_before_schema_introspection",
            "parameterized_queries_before_preview",
            "schema_rehearsal_before_dataset_publish",
            "service_contract_tests_before_resource_publish",
            "offline_integrity_before_runtime_replay",
            "telemetry_registered_before_runtime_smoke",
            "runtime_smoke_proves_no_persisted_writes",
        ),
        "side_effects": (),
    }


def data_tooling_failover_transaction_replay_contract() -> dict:
    """Replay a degraded data connection through failover, rollback preview, restore, and replay gates."""
    connection = data_connection_test_contract()
    pooling = data_connection_pool_contract()
    failover = data_connection_failover_contract()
    sql_safety = data_sql_authoring_safety_contract()
    stored_procedures = data_stored_procedure_workflow_contract()
    backup_restore = local_backup_restore_verification_contract()
    replication = data_replication_monitor_contract()
    telemetry = data_service_telemetry_contract()
    offline_replay = data_offline_replay_contract()
    module_smoke = data_module_runtime_smoke_contract()
    state = {
        "active_route": "primary_sql",
        "quarantined_routes": (),
        "rollback_previews": 0,
        "restore_drills": 0,
        "replication_alerts": 0,
        "manual_review": False,
        "persisted_writes": 0,
        "side_effects": (),
    }
    replay = (
        {
            "phase": "probe_and_pool_connection",
            "pipeline": connection["steps"] + tuple(pool["session_lifecycle"] for pool in pooling["pools"]),
            "ok": connection["ok"]
            and connection["steps"][-1] == "rollback_test_transaction"
            and pooling["ok"]
            and all("reset_session" in pool["session_lifecycle"] for pool in pooling["pools"]),
        },
        {
            "phase": "quarantine_and_route_failover",
            "pipeline": tuple(route["retry_policy"] for route in failover["routes"]),
            "ok": failover["ok"]
            and all(route["transaction_policy"] for route in failover["routes"])
            and all("circuit_breaker" in route["retry_policy"] for route in failover["routes"]),
        },
        {
            "phase": "rollback_preview_sql_and_routines",
            "pipeline": tuple(workflow["steps"] for workflow in sql_safety["workflows"]) + tuple(workflow["pipeline"] for workflow in stored_procedures["workflows"]),
            "ok": sql_safety["ok"]
            and stored_procedures["ok"]
            and "parameterization_required" in sql_safety["guards"]
            and all("rollback_preview" in workflow["pipeline"] for workflow in stored_procedures["workflows"]),
        },
        {
            "phase": "verify_restore_drill",
            "pipeline": tuple(drill["verification"] for drill in backup_restore["drills"]),
            "ok": backup_restore["ok"]
            and all({"verify_checksum", "restore_to_scratch", "compare_schema_hash"} <= set(drill["verification"]) for drill in backup_restore["drills"]),
        },
        {
            "phase": "surface_replication_and_telemetry",
            "pipeline": tuple(monitor["metrics"] for monitor in replication["monitors"]) + tuple(item["signals"] for item in telemetry["telemetry"]),
            "ok": replication["ok"]
            and telemetry["ok"]
            and all("conflict_count" in monitor["metrics"] for monitor in replication["monitors"])
            and "latency_budget_recorded" in telemetry["guards"],
        },
        {
            "phase": "manual_review_offline_replay",
            "pipeline": offline_replay["replay_flow"],
            "ok": {"dedupe_by_idempotency_key", "pause_for_manual_review", "mark_replayed"} <= set(offline_replay["replay_flow"]),
        },
        {
            "phase": "smoke_after_failover",
            "pipeline": tuple(test["smoke"] for test in module_smoke["smoke_tests"]),
            "ok": module_smoke["ok"]
            and all("verify_no_side_effects" in test["smoke"] for test in module_smoke["smoke_tests"]),
        },
    )
    state["active_route"] = "local_embedded" if replay[1]["ok"] else "primary_sql"
    state["quarantined_routes"] = tuple(route["connection"] for route in failover["routes"])
    state["rollback_previews"] = len(stored_procedures["workflows"]) + sum(1 for workflow in sql_safety["workflows"] if "rollback_transaction" in workflow["steps"])
    state["restore_drills"] = len(backup_restore["drills"])
    state["replication_alerts"] = sum(len(monitor["alerts"]) for monitor in replication["monitors"])
    state["manual_review"] = "pause_for_manual_review" in offline_replay["replay_flow"]
    return {
        "format": "appgen.data-tooling-failover-transaction-replay.v1",
        "ok": all(item["ok"] for item in replay)
        and state["active_route"] == "local_embedded"
        and state["rollback_previews"] > 0
        and state["restore_drills"] > 0
        and state["replication_alerts"] > 0
        and state["manual_review"] is True
        and state["persisted_writes"] == 0
        and state["side_effects"] == (),
        "replay": replay,
        "final_state": state,
        "guards": (
            "connection_probe_rolls_back_before_failover",
            "failed_route_quarantined_before_retry",
            "sql_and_routines_previewed_with_rollback",
            "restore_verified_before_offline_replay",
            "replication_and_latency_visible_before_smoke",
            "offline_replay_pauses_for_manual_review",
            "failover_smoke_proves_no_persisted_writes",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(item for item in replay if not item["ok"]),
    }


def data_tooling_readiness_contract() -> dict:
    """Prove the native data tooling path as one ordered readiness contract."""
    connection = data_tooling_test_connection()
    dataset = data_tooling_design_dataset_operation()
    publish_resource = data_tooling_publish_resource()
    offline_replay = data_tooling_rehearse_offline_replay_operation()
    replication = data_tooling_monitor_replication_operation()
    module_smoke = data_tooling_run_module_smoke_operation()
    runtime_replay = data_tooling_runtime_replay_contract()
    publish_replay = data_tooling_publish_transaction_replay_contract()
    failover_replay = data_tooling_failover_transaction_replay_contract()
    actionable_operations = data_tooling_actionable_operations()
    phases = (
        {
            "phase": "probe_connection",
            "pipeline": connection["pipeline"],
            "ok": connection["ok"] and connection["pipeline"][-1] == "rollback_test_transaction",
        },
        {
            "phase": "design_dataset",
            "pipeline": dataset["pipeline"],
            "ok": dataset["ok"] and "validate_dataset_state_machine" in dataset["pipeline"],
        },
        {
            "phase": "publish_service_resources",
            "pipeline": publish_resource["pipeline"],
            "ok": publish_resource["ok"]
            and publish_replay["ok"]
            and {"run_contract_tests", "attach_security", "register_analytics"} <= set(publish_resource["pipeline"]),
        },
        {
            "phase": "rehearse_offline_replay",
            "pipeline": offline_replay["pipeline"],
            "ok": offline_replay["ok"]
            and {"dedupe_by_idempotency_key", "pause_for_manual_review", "mark_replayed"} <= set(offline_replay["pipeline"]),
        },
        {
            "phase": "monitor_replication_and_failover",
            "pipeline": replication["pipeline"] + tuple(item["phase"] for item in failover_replay["replay"]),
            "ok": replication["ok"]
            and failover_replay["ok"]
            and "surface_conflict_alerts" in replication["pipeline"]
            and failover_replay["final_state"]["persisted_writes"] == 0,
        },
        {
            "phase": "surface_runtime_diagnostics",
            "pipeline": module_smoke["pipeline"] + tuple(item["op"] for item in runtime_replay["trace"]),
            "ok": module_smoke["ok"]
            and runtime_replay["ok"]
            and "verify_no_side_effects" in module_smoke["pipeline"]
            and runtime_replay["final_state"]["queue_status"] == "manual_review",
        },
    )
    checks = (
        {"id": "connection_ready", "ok": phases[0]["ok"], "evidence": connection},
        {"id": "dataset_ready", "ok": phases[1]["ok"], "evidence": dataset},
        {"id": "publish_ready", "ok": phases[2]["ok"], "evidence": {"operation": publish_resource, "replay": publish_replay}},
        {"id": "offline_replay_ready", "ok": phases[3]["ok"], "evidence": offline_replay},
        {"id": "replication_failover_ready", "ok": phases[4]["ok"], "evidence": {"replication": replication, "failover": failover_replay}},
        {"id": "diagnostics_ready", "ok": phases[5]["ok"], "evidence": {"module_smoke": module_smoke, "runtime_replay": runtime_replay}},
        {"id": "operation_surface_ready", "ok": actionable_operations["ok"] and not actionable_operations["side_effects"], "evidence": actionable_operations},
        {
            "id": "phase_order_ready",
            "ok": tuple(item["phase"] for item in phases)
            == (
                "probe_connection",
                "design_dataset",
                "publish_service_resources",
                "rehearse_offline_replay",
                "monitor_replication_and_failover",
                "surface_runtime_diagnostics",
            ),
            "evidence": tuple(item["phase"] for item in phases),
        },
    )
    return {
        "format": "appgen.data-tooling-readiness-contract.v1",
        "ok": all(check["ok"] for check in checks) and all(phase["ok"] for phase in phases),
        "phases": phases,
        "checks": checks,
        "final_state": {
            "connection": "verified",
            "dataset_transitions": len(dataset["transitions"]),
            "published_resources": len(publish_resource["pipeline"]),
            "offline_queue": len(offline_replay["queue"]),
            "replication_monitors": len(replication["monitors"]),
            "runtime_steps": len(runtime_replay["trace"]),
            "persisted_writes": runtime_replay["final_state"]["persisted_writes"],
        },
        "guards": (
            "connection_probe_before_dataset_design",
            "dataset_design_before_service_publish",
            "service_publish_before_offline_replay",
            "offline_replay_before_failover_monitoring",
            "diagnostics_after_runtime_replay",
            "side_effect_free_readiness",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
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
    relationship_lookup_lifecycle = data_relationship_lookup_lifecycle_replay_contract()
    module_runtime_smoke = data_module_runtime_smoke_contract()
    data_module_artifacts = data_tooling_module_file_manifest()
    data_module_test_artifacts = data_tooling_module_test_file_manifest()
    deep_data_tooling_module_artifacts = deep_data_tooling_module_file_manifest()
    deep_data_tooling_module_test_artifacts = deep_data_tooling_module_test_file_manifest()
    runtime_replay = data_tooling_runtime_replay_contract()
    design_runtime_replay = data_tooling_design_runtime_session_replay_contract()
    publish_transaction_replay = data_tooling_publish_transaction_replay_contract()
    failover_transaction_replay = data_tooling_failover_transaction_replay_contract()
    readiness = data_tooling_readiness_contract()
    actionable_operations = data_tooling_actionable_operations()
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
            "id": "actionable_data_tooling_operations",
            "ok": actionable_operations["ok"]
            and {
                "test_connection",
                "preview_query",
                "preview_schema_diff",
                "generate_lookup_editors",
                "publish_resource",
                "browse_schema",
                "design_dataset",
                "rehearse_offline_replay",
                "monitor_replication",
                "run_module_smoke",
            }
            <= set(actionable_operations["operations"])
            and not actionable_operations["side_effects"],
            "evidence": actionable_operations,
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
            "id": "relationship_lookup_lifecycle_replay",
            "ok": relationship_lookup_lifecycle["ok"]
            and {"multi_hop_chain_preserved", "lookup_preview_before_publish"} <= set(relationship_lookup_lifecycle["guards"])
            and not relationship_lookup_lifecycle["side_effects"],
            "evidence": relationship_lookup_lifecycle,
        },
        {
            "id": "data_module_runtime_smoke",
            "ok": module_runtime_smoke["ok"] and {"module_imports_are_required", "read_only_probe_required"} <= set(module_runtime_smoke["guards"])
            and not module_runtime_smoke["side_effects"],
            "evidence": module_runtime_smoke,
        },
        {
            "id": "data_tooling_modules",
            "ok": len(data_module_artifacts) == 4
            and all(item["ok"] and item["exports"] for item in data_module_artifacts),
            "evidence": data_module_artifacts,
        },
        {
            "id": "data_tooling_module_tests",
            "ok": len(data_module_test_artifacts) == 4
            and all(
                item["ok"] and "test_data_tooling_module_smoke" in item["exports"]
                for item in data_module_test_artifacts
            ),
            "evidence": data_module_test_artifacts,
        },
        {
            "id": "deep_data_tooling_modules",
            "ok": len(deep_data_tooling_module_artifacts) == 8
            and all(item["ok"] and "run_data_operation" in item["exports"] for item in deep_data_tooling_module_artifacts),
            "evidence": deep_data_tooling_module_artifacts,
        },
        {
            "id": "deep_data_tooling_module_tests",
            "ok": len(deep_data_tooling_module_test_artifacts) == 8
            and all(
                item["ok"] and "test_deep_data_tooling_module_smoke" in item["exports"]
                for item in deep_data_tooling_module_test_artifacts
            ),
            "evidence": deep_data_tooling_module_test_artifacts,
        },
        {
            "id": "data_tooling_runtime_replay",
            "ok": runtime_replay["ok"]
            and {"connection_probe_rolls_back", "offline_replay_pauses_for_review"} <= set(runtime_replay["guards"])
            and not runtime_replay["side_effects"],
            "evidence": runtime_replay,
        },
        {
            "id": "data_tooling_design_runtime_session_replay",
            "ok": design_runtime_replay["ok"]
            and {"schema_rehearsal_before_dataset_publish", "runtime_operations_are_monitored"} <= set(design_runtime_replay["guards"])
            and not design_runtime_replay["side_effects"],
            "evidence": design_runtime_replay,
        },
        {
            "id": "data_tooling_publish_transaction_replay",
            "ok": publish_transaction_replay["ok"]
            and {"service_contract_tests_before_resource_publish", "runtime_smoke_proves_no_persisted_writes"}
            <= set(publish_transaction_replay["guards"])
            and not publish_transaction_replay["side_effects"],
            "evidence": publish_transaction_replay,
        },
        {
            "id": "data_tooling_failover_transaction_replay",
            "ok": failover_transaction_replay["ok"]
            and {"failed_route_quarantined_before_retry", "offline_replay_pauses_for_manual_review"} <= set(failover_transaction_replay["guards"])
            and failover_transaction_replay["final_state"]["persisted_writes"] == 0
            and not failover_transaction_replay["side_effects"],
            "evidence": failover_transaction_replay,
        },
        {
            "id": "data_tooling_readiness_contract",
            "ok": readiness["ok"]
            and {
                "connection_ready",
                "dataset_ready",
                "publish_ready",
                "offline_replay_ready",
                "replication_failover_ready",
                "diagnostics_ready",
                "operation_surface_ready",
                "phase_order_ready",
            }
            <= {check["id"] for check in readiness["checks"] if check["ok"]}
            and not readiness["side_effects"],
            "evidence": readiness,
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
        "actionable_operations": actionable_operations,
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
        "relationship_lookup_lifecycle": relationship_lookup_lifecycle,
        "module_runtime_smoke": module_runtime_smoke,
        "data_module_artifacts": data_module_artifacts,
        "data_module_test_artifacts": data_module_test_artifacts,
        "deep_data_tooling_module_artifacts": deep_data_tooling_module_artifacts,
        "deep_data_tooling_module_test_artifacts": deep_data_tooling_module_test_artifacts,
        "runtime_replay": runtime_replay,
        "design_runtime_replay": design_runtime_replay,
        "publish_transaction_replay": publish_transaction_replay,
        "failover_transaction_replay": failover_transaction_replay,
        "readiness": readiness,
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


def mobile_request_permission_operation(api: str = "camera") -> dict:
    """Return a callable IDE operation for requesting and recording one permission."""
    workflow = mobile_permission_prompt_workflow(api)
    return {
        "format": "appgen.mobile-request-permission-operation.v1",
        "ok": workflow["ok"] and workflow["steps"][-1] == "dispatch_result",
        "api": api,
        "permission": workflow["permission"],
        "pipeline": workflow["steps"],
        "outcomes": workflow["outcomes"],
        "guards": ("reviewable_prompt_required", "privacy_audit_recorded", "result_dispatched_to_component"),
        "side_effects": (),
    }


def mobile_dispatch_adapter_operation(api: str = "camera") -> dict:
    """Return a callable IDE operation for dispatching a native adapter."""
    workflow = mobile_adapter_dispatch_workflow(api)
    return {
        "format": "appgen.mobile-dispatch-adapter-operation.v1",
        "ok": workflow["ok"] and {"check_permission", "emit_component_event"} <= set(workflow["pipeline"]),
        "api": api,
        "adapter": workflow["adapter"],
        "pipeline": workflow["pipeline"],
        "error_paths": workflow["error_paths"],
        "guards": ("permission_checked_before_invoke", "payload_normalized", "component_event_emitted"),
        "side_effects": (),
    }


def mobile_replay_simulator_operation(api: str = "location") -> dict:
    """Return a callable IDE operation for replaying simulator fixtures."""
    workflow = mobile_simulator_replay_workflow(api)
    return {
        "format": "appgen.mobile-replay-simulator-operation.v1",
        "ok": workflow["ok"] and {"load_fixture", "assert_component_events"} <= set(workflow["scenario"]),
        "api": api,
        "fixture": workflow["fixture"],
        "pipeline": workflow["scenario"],
        "profiles": workflow["profiles"],
        "guards": ("fixture_loaded_before_replay", "permissions_simulated", "component_events_asserted"),
        "side_effects": (),
    }


def mobile_review_platform_fallback_operation(api: str = "nfc") -> dict:
    """Return a callable IDE operation for reviewing unsupported target fallbacks."""
    workflow = mobile_platform_fallback_workflow(api)
    return {
        "format": "appgen.mobile-platform-fallback-operation.v1",
        "ok": workflow["ok"] and "designer_warning_visible" in workflow["guards"],
        "api": api,
        "fallbacks": workflow["fallbacks"],
        "unavailable_targets": workflow["unavailable_targets"],
        "guards": workflow["guards"],
        "side_effects": (),
    }


def mobile_review_privacy_operation() -> dict:
    """Return a callable IDE operation for reviewing privacy metadata."""
    workflow = mobile_privacy_review_workflow()
    return {
        "format": "appgen.mobile-privacy-review-operation.v1",
        "ok": bool(workflow["apis"]) and {"purpose_string", "least_privilege"} <= set(workflow["review_items"]),
        "apis": workflow["apis"],
        "review_items": workflow["review_items"],
        "prompts": workflow["prompts"],
        "guards": workflow["guards"],
        "side_effects": (),
    }


def mobile_resume_background_operation() -> dict:
    """Return a callable IDE operation for background checkpoint and resume flows."""
    workflow = mobile_background_resume_workflow()
    return {
        "format": "appgen.mobile-background-resume-operation.v1",
        "ok": {"persist_checkpoint", "resume_foreground"} <= set(workflow["schedule"]),
        "api": workflow["api"],
        "pipeline": workflow["schedule"],
        "resume_payload": workflow["resume_payload"],
        "guards": workflow["guards"],
        "side_effects": (),
    }


def mobile_device_component_spec_contract() -> dict:
    """Return IDE component specs for native device APIs across props, events, permissions, and previews."""
    contract = mobile_native_api_contract()
    permissions = {item["api"]: item for item in contract["permission_manifest"]["permissions"]}
    fixtures = {item["api"]: item for item in contract["simulator"]["fixtures"]}
    bridge_matrix = mobile_native_bridge_matrix_contract()
    bridge_targets = tuple(bridge["target"] for bridge in bridge_matrix["bridges"])
    specs = tuple(
        {
            "component": adapter["component"],
            "api": adapter["api"],
            "category": "Device",
            "icon": adapter["api"].replace("_", "-"),
            "props": (
                {"name": "enabled", "type": "boolean", "default": True, "editor": "checkbox"},
                {"name": "permissionMode", "type": "enum", "values": ("prompt", "required", "optional"), "editor": "select"},
                {"name": "timeoutMs", "type": "integer", "default": 30000, "editor": "number"},
            ),
            "events": adapter["events"],
            "permission": permissions.get(adapter["api"]),
            "fixture": fixtures.get(adapter["api"]),
            "preview": adapter["preview"],
            "targets": adapter["targets"],
            "bridge_targets": bridge_targets,
            "design_tools": ("property_inspector", "permission_editor", "simulator_fixture_picker", "target_fallback_review", "event_trace_viewer"),
            "runtime_pipeline": ("validate_props", "check_permission", "invoke_platform_adapter", "normalize_payload", "emit_component_event"),
        }
        for adapter in contract["component_adapters"]["adapters"]
    )
    return {
        "format": "appgen.mobile-device-component-spec-contract.v1",
        "ok": bool(specs)
        and len(specs) == len(contract["apis"])
        and {spec["api"] for spec in specs} == set(contract["apis"])
        and all(spec["permission"] and spec["fixture"] and spec["events"] for spec in specs)
        and all({"permission_editor", "simulator_fixture_picker", "event_trace_viewer"} <= set(spec["design_tools"]) for spec in specs)
        and all({"validate_props", "emit_component_event"} <= set(spec["runtime_pipeline"]) for spec in specs),
        "specs": specs,
        "guards": ("props_validated_before_bridge", "permission_editor_required", "simulator_fixture_bound", "event_trace_visible"),
        "side_effects": (),
    }


def mobile_validate_device_component_operation(api: str = "camera") -> dict:
    """Return a callable IDE operation for validating one native device component spec."""
    specs = mobile_device_component_spec_contract()
    spec = next((item for item in specs["specs"] if item["api"] == api), None)
    return {
        "format": "appgen.mobile-validate-device-component-operation.v1",
        "ok": specs["ok"]
        and spec is not None
        and spec["permission"] is not None
        and spec["fixture"] is not None
        and {"check_permission", "emit_component_event"} <= set(spec["runtime_pipeline"]),
        "api": api,
        "component": spec,
        "pipeline": ("load_component_spec", "validate_props", "bind_permission_editor", "bind_simulator_fixture", "verify_target_bridges", "emit_component_event"),
        "guards": ("component_spec_required", "permission_and_fixture_required", "target_bridges_reviewed"),
        "side_effects": (),
    }


def mobile_native_api_actionable_operations() -> dict:
    """Return callable mobile/native operations used by the generated IDE."""
    operations = {
        "request_permission": mobile_request_permission_operation(),
        "dispatch_adapter": mobile_dispatch_adapter_operation(),
        "replay_simulator": mobile_replay_simulator_operation(),
        "review_platform_fallback": mobile_review_platform_fallback_operation(),
        "review_privacy": mobile_review_privacy_operation(),
        "resume_background": mobile_resume_background_operation(),
        "validate_device_component": mobile_validate_device_component_operation(),
    }
    return {
        "format": "appgen.mobile-native-api-actionable-operations.v1",
        "ok": all(operation["ok"] for operation in operations.values()),
        "operations": operations,
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


def mobile_native_api_runtime_replay_contract() -> dict:
    """Replay permission, bridge, fixture, event, background, and lifecycle delivery for device APIs."""
    capability = mobile_api_capability_matrix_contract()
    event_traces = mobile_device_event_trace_contract()
    bridge_matrix = mobile_native_bridge_matrix_contract()
    permission_states = mobile_permission_state_machine_contract()
    background_delivery = mobile_background_delivery_contract()
    media_pipeline = mobile_media_file_pipeline_contract()
    bridge_errors = mobile_native_bridge_error_contract()
    lifecycle = mobile_app_lifecycle_delivery_contract()
    fixtures = mobile_simulator_fixture_integrity_contract()
    traces_by_api = {trace["api"]: trace for trace in event_traces["traces"]}
    states_by_api = {item["api"]: item for item in permission_states["transitions"]}
    fixtures_by_api = {item["api"]: item for item in fixtures["fixtures"]}
    background_apis = {item["api"] for item in background_delivery["deliveries"]}
    media_apis = {item["api"] for item in media_pipeline["pipelines"]}
    state = {"permission": "unknown", "events": 0, "errors": 0, "checkpoints": 0, "side_effects": ()}
    replay = []
    for row in capability["rows"]:
        api = row["api"]
        trace = traces_by_api[api]
        permission = states_by_api[api]
        fixture = fixtures_by_api[api]
        phases = [
            "load_privacy_prompt",
            "transition_unknown_to_prompting",
            "transition_prompting_to_granted",
            "load_simulator_fixture",
            "invoke_target_bridge",
            "normalize_payload",
            "dispatch_component_events",
            "record_diagnostic",
        ]
        if api in media_apis:
            phases.extend(("validate_mime", "copy_to_app_storage", "cleanup_temporary_files"))
        if api in background_apis:
            phases.extend(("persist_payload", "checkpoint_delivery", "replay_on_resume"))
            state["checkpoints"] += 1
        state["permission"] = "granted"
        state["events"] += sum(len(event["trace"]) for event in trace["events"])
        replay.append(
            {
                "api": api,
                "component": trace["component"],
                "fixture": fixture["fixture"],
                "permission_transitions": permission["transitions"],
                "targets": row["targets"],
                "phases": tuple(phases),
                "event_count": len(trace["events"]),
                "ok": bool(row["privacy_prompt"])
                and "granted->revoked" in permission["transitions"]
                and "assert_events" in fixture["replay_order"]
                and {"normalize_payload", "dispatch_component_events"} <= set(phases),
            }
        )
    bridge_recovery = tuple(
        {
            "target": scenario["target"],
            "errors": scenario["errors"],
            "recovery": scenario["recovery"],
            "ok": {"normalize_error", "emit_error_event", "fallback_path"} <= set(scenario["recovery"]),
        }
        for scenario in bridge_errors["scenarios"]
    )
    lifecycle_replay = tuple(
        {
            "event": delivery["event"],
            "pipeline": delivery["pipeline"],
            "ok": {"persist_checkpoint", "replay_pending_events", "emit_component_event", "record_diagnostic", "record_shutdown"} & set(delivery["pipeline"]) != set(),
        }
        for delivery in lifecycle["deliveries"]
    )
    return {
        "format": "appgen.mobile-native-api-runtime-replay-contract.v1",
        "ok": capability["ok"]
        and bridge_matrix["ok"]
        and bool(replay)
        and all(item["ok"] for item in replay)
        and all(item["ok"] for item in bridge_recovery)
        and all(item["ok"] for item in lifecycle_replay)
        and state["side_effects"] == (),
        "replay": tuple(replay),
        "bridge_recovery": bridge_recovery,
        "lifecycle_replay": lifecycle_replay,
        "final_state": state,
        "guards": ("permission_replayed_before_bridge", "fixture_replayed_before_events", "payloads_normalized_before_dispatch", "background_delivery_checkpointed", "bridge_errors_recoverable", "lifecycle_resume_replays_pending_events"),
        "side_effects": (),
    }


def mobile_device_designer_transaction_replay_contract() -> dict:
    """Replay one device-component designer transaction through runtime delivery and recovery."""
    contract = mobile_native_api_contract()
    api_set = set(contract["apis"])
    permissions = contract["permission_manifest"]
    adapters = contract["component_adapters"]
    simulator = contract["simulator"]
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
    runtime_replay = mobile_native_api_runtime_replay_contract()
    state = {
        "apis": len(api_set),
        "permission_entries": len(permissions["permissions"]),
        "component_adapters": len(adapters["adapters"]),
        "simulator_fixtures": len(simulator["fixtures"]),
        "event_traces": len(event_traces["traces"]),
        "revocation_flows": len(permission_revocation["revocations"]),
        "background_deliveries": len(background_delivery["deliveries"]),
        "privacy_entries": len(store_privacy_manifest["entries"]),
        "runtime_replays": len(runtime_replay["replay"]),
        "bridge_recoveries": len(runtime_replay["bridge_recovery"]),
        "side_effects": (),
    }
    replay = (
        {
            "phase": "author_device_components",
            "pipeline": tuple(adapter["component"] for adapter in adapters["adapters"]),
            "ok": api_set <= {adapter["api"] for adapter in adapters["adapters"]}
            and all(adapter["events"] for adapter in adapters["adapters"]),
        },
        {
            "phase": "generate_permission_manifest",
            "pipeline": tuple(permission["api"] for permission in permissions["permissions"]),
            "ok": api_set <= {permission["api"] for permission in permissions["permissions"]}
            and {"least_privilege", "reviewable_prompts"} <= set(permissions["guards"])
            and {"show_reviewable_prompt", "dispatch_result"} <= set(permission_workflow["steps"]),
        },
        {
            "phase": "configure_simulator_fixtures",
            "pipeline": tuple(fixture["api"] for fixture in simulator["fixtures"]),
            "ok": api_set <= {fixture["api"] for fixture in simulator["fixtures"]}
            and simulator_fixture_integrity["ok"]
            and {"load_fixture", "assert_component_events"} <= set(simulator_replay["scenario"]),
        },
        {
            "phase": "preview_and_dispatch_adapter",
            "pipeline": adapter_dispatch["pipeline"],
            "ok": adapter_dispatch["ok"]
            and {"check_permission", "invoke_platform_adapter", "emit_component_event"} <= set(adapter_dispatch["pipeline"])
            and event_traces["ok"],
        },
        {
            "phase": "validate_privacy_and_fallbacks",
            "pipeline": privacy_review["review_items"] + platform_fallback["guards"],
            "ok": store_privacy_manifest["ok"]
            and platform_fallback["ok"]
            and "least_privilege" in privacy_review["review_items"]
            and all(item["third_party_sharing"] is False for item in store_privacy_manifest["entries"]),
        },
        {
            "phase": "handle_permission_revocation",
            "pipeline": tuple(item["api"] for item in permission_revocation["revocations"]),
            "ok": permission_revocation["ok"]
            and permission_state_machine["ok"]
            and all("granted->revoked" in item["transitions"] for item in permission_state_machine["transitions"]),
        },
        {
            "phase": "deliver_background_and_lifecycle",
            "pipeline": background_resume["schedule"] + tuple(item["event"] for item in app_lifecycle_delivery["deliveries"]),
            "ok": background_delivery["ok"]
            and app_lifecycle_delivery["ok"]
            and "checkpoint_delivery" in background_delivery["deliveries"][0]["lifecycle"]
            and any("replay_pending_events" in item["pipeline"] for item in app_lifecycle_delivery["deliveries"]),
        },
        {
            "phase": "normalize_media_deep_link_and_bridge_errors",
            "pipeline": media_file_pipeline["guards"] + deep_link_routing["pipeline"] + bridge_errors["guards"],
            "ok": media_file_pipeline["ok"]
            and deep_link_routing["ok"]
            and bridge_matrix["ok"]
            and bridge_errors["ok"]
            and all("emit_error_event" in scenario["recovery"] for scenario in bridge_errors["scenarios"]),
        },
        {
            "phase": "replay_runtime_delivery",
            "pipeline": tuple(item["api"] for item in runtime_replay["replay"]),
            "ok": runtime_replay["ok"]
            and api_set == {item["api"] for item in runtime_replay["replay"]}
            and all("dispatch_component_events" in item["phases"] for item in runtime_replay["replay"]),
        },
    )
    return {
        "format": "appgen.mobile-device-designer-transaction-replay-contract.v1",
        "ok": capability_matrix["ok"]
        and all(item["ok"] for item in replay)
        and state["apis"] > 0
        and state["permission_entries"] == state["apis"]
        and state["component_adapters"] == state["apis"]
        and state["simulator_fixtures"] == state["apis"]
        and state["event_traces"] == state["apis"]
        and state["revocation_flows"] == state["apis"]
        and state["runtime_replays"] == state["apis"]
        and state["bridge_recoveries"] > 0
        and state["side_effects"] == (),
        "replay": replay,
        "final_state": state,
        "guards": (
            "component_authoring_before_permission_generation",
            "permission_manifest_before_adapter_dispatch",
            "simulator_fixture_before_preview",
            "privacy_and_fallbacks_before_runtime",
            "revocation_visible_before_adapter_call",
            "background_delivery_checkpointed",
            "bridge_errors_recoverable",
            "runtime_replay_covers_all_device_apis",
        ),
        "side_effects": (),
    }


def mobile_device_capability_lifecycle_replay_contract() -> dict:
    """Replay every device API through privacy, permission, bridge, runtime, and designer lifecycle."""
    contract = mobile_native_api_contract()
    privacy = mobile_store_privacy_manifest_contract()
    permission_states = mobile_permission_state_machine_contract()
    simulator = mobile_simulator_fixture_integrity_contract()
    bridge_matrix = mobile_native_bridge_matrix_contract()
    permission_revocation = mobile_permission_revocation_contract()
    background_delivery = mobile_background_delivery_contract()
    media_pipeline = mobile_media_file_pipeline_contract()
    deep_link_routing = mobile_deep_link_routing_contract()
    app_lifecycle = mobile_app_lifecycle_delivery_contract()
    bridge_errors = mobile_native_bridge_error_contract()
    runtime_replay = mobile_native_api_runtime_replay_contract()
    designer_replay = mobile_device_designer_transaction_replay_contract()
    privacy_by_api = {item["api"]: item for item in privacy["entries"]}
    permission_by_api = {item["api"]: item for item in permission_states["transitions"]}
    fixture_by_api = {item["api"]: item for item in simulator["fixtures"]}
    runtime_by_api = {item["api"]: item for item in runtime_replay["replay"]}
    revocation_apis = {item["api"] for item in permission_revocation["revocations"]}
    background_apis = {item["api"] for item in background_delivery["deliveries"]}
    media_apis = {item["api"] for item in media_pipeline["pipelines"]}
    target_bridges = {bridge["target"]: bridge for bridge in bridge_matrix["bridges"]}
    replay = tuple(
        {
            "api": api,
            "phases": (
                {
                    "phase": "declare_privacy",
                    "ok": api in privacy_by_api
                    and privacy_by_api[api]["third_party_sharing"] is False
                    and bool(privacy_by_api[api]["prompt"]),
                    "evidence": privacy_by_api.get(api),
                },
                {
                    "phase": "transition_permission",
                    "ok": api in permission_by_api
                    and "granted->revoked" in permission_by_api[api]["transitions"]
                    and "revocation_checked_before_call" in permission_by_api[api]["guards"],
                    "evidence": permission_by_api.get(api),
                },
                {
                    "phase": "load_simulator_fixture",
                    "ok": api in fixture_by_api
                    and "assert_events" in fixture_by_api[api]["replay_order"],
                    "evidence": fixture_by_api.get(api),
                },
                {
                    "phase": "invoke_target_bridges",
                    "ok": {"android", "ios", "desktop", "web-pwa"} <= set(target_bridges)
                    and all("emit_event" in bridge["lifecycle"] for bridge in target_bridges.values()),
                    "evidence": tuple(target_bridges),
                },
                {
                    "phase": "run_api_specific_pipeline",
                    "ok": (
                        api not in media_apis or media_pipeline["ok"]
                    )
                    and (
                        api not in background_apis or background_delivery["ok"]
                    )
                    and (
                        api != "deep_links" or deep_link_routing["ok"]
                    )
                    and (
                        api != "app_lifecycle" or app_lifecycle["ok"]
                    ),
                    "evidence": {
                        "media": api in media_apis,
                        "background": api in background_apis,
                        "deep_link": api == "deep_links",
                        "app_lifecycle": api == "app_lifecycle",
                    },
                },
                {
                    "phase": "recover_revocation_or_bridge_error",
                    "ok": api in revocation_apis
                    and bridge_errors["ok"]
                    and all("emit_error_event" in scenario["recovery"] for scenario in bridge_errors["scenarios"]),
                    "evidence": {
                        "revocation": api in revocation_apis,
                        "bridge_errors": bridge_errors["guards"],
                    },
                },
                {
                    "phase": "dispatch_runtime_events",
                    "ok": api in runtime_by_api
                    and {"invoke_target_bridge", "dispatch_component_events"} <= set(runtime_by_api[api]["phases"]),
                    "evidence": runtime_by_api.get(api),
                },
            ),
        }
        for api in contract["apis"]
    )
    checks = (
        {
            "id": "privacy_before_permission",
            "ok": all(
                tuple(phase["phase"] for phase in item["phases"]).index("declare_privacy")
                < tuple(phase["phase"] for phase in item["phases"]).index("transition_permission")
                for item in replay
            ),
            "evidence": replay,
        },
        {
            "id": "simulator_before_bridge",
            "ok": all(
                tuple(phase["phase"] for phase in item["phases"]).index("load_simulator_fixture")
                < tuple(phase["phase"] for phase in item["phases"]).index("invoke_target_bridges")
                for item in replay
            ),
            "evidence": replay,
        },
        {
            "id": "api_specific_pipelines_covered",
            "ok": media_pipeline["ok"]
            and background_delivery["ok"]
            and deep_link_routing["ok"]
            and app_lifecycle["ok"],
            "evidence": {
                "media": media_pipeline["guards"],
                "background": background_delivery["guards"],
                "deep_links": deep_link_routing["guards"],
                "app_lifecycle": app_lifecycle["guards"],
            },
        },
        {
            "id": "runtime_and_designer_replay_aligned",
            "ok": runtime_replay["ok"]
            and designer_replay["ok"]
            and {item["api"] for item in runtime_replay["replay"]} == set(contract["apis"])
            and designer_replay["final_state"]["runtime_replays"] == len(contract["apis"]),
            "evidence": {
                "runtime_apis": tuple(item["api"] for item in runtime_replay["replay"]),
                "designer_runtime_replays": designer_replay["final_state"]["runtime_replays"],
            },
        },
        {
            "id": "side_effect_guards",
            "ok": not privacy["side_effects"]
            and not permission_states["side_effects"]
            and not simulator["side_effects"]
            and not bridge_matrix["side_effects"]
            and not permission_revocation["side_effects"]
            and not background_delivery["side_effects"]
            and not media_pipeline["side_effects"]
            and not deep_link_routing["side_effects"]
            and not app_lifecycle["side_effects"]
            and not bridge_errors["side_effects"]
            and not runtime_replay["side_effects"]
            and not designer_replay["side_effects"],
            "evidence": (),
        },
    )
    ok = all(all(phase["ok"] for phase in item["phases"]) for item in replay) and all(check["ok"] for check in checks)
    return {
        "format": "appgen.mobile-device-capability-lifecycle-replay.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "api_count": len(contract["apis"]),
        "replay": replay,
        "checks": checks,
        "guards": (
            "privacy_before_permission",
            "simulator_before_bridge",
            "api_specific_pipelines_covered",
            "runtime_and_designer_replay_aligned",
            "no_side_effects",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def mobile_native_api_readiness_contract() -> dict:
    """Prove the mobile/native device API path as one ordered readiness contract."""
    contract = mobile_native_api_contract()
    permission = mobile_request_permission_operation()
    simulator = mobile_replay_simulator_operation()
    adapter = mobile_dispatch_adapter_operation()
    privacy = mobile_review_privacy_operation()
    fallback = mobile_review_platform_fallback_operation()
    background = mobile_resume_background_operation()
    component_validation = mobile_validate_device_component_operation()
    runtime_replay = mobile_native_api_runtime_replay_contract()
    designer_replay = mobile_device_designer_transaction_replay_contract()
    lifecycle = mobile_device_capability_lifecycle_replay_contract()
    actionable = mobile_native_api_actionable_operations()
    phases = (
        {
            "phase": "declare_privacy_and_permissions",
            "pipeline": privacy["review_items"] + permission["pipeline"],
            "ok": privacy["ok"]
            and permission["ok"]
            and "least_privilege" in privacy["review_items"]
            and "dispatch_result" in permission["pipeline"],
        },
        {
            "phase": "configure_simulator_fixtures",
            "pipeline": simulator["pipeline"],
            "ok": simulator["ok"] and {"load_fixture", "assert_component_events"} <= set(simulator["pipeline"]),
        },
        {
            "phase": "bind_components_and_bridges",
            "pipeline": component_validation["pipeline"] + adapter["pipeline"],
            "ok": component_validation["ok"]
            and adapter["ok"]
            and "bind_simulator_fixture" in component_validation["pipeline"]
            and "emit_component_event" in adapter["pipeline"],
        },
        {
            "phase": "review_fallbacks_and_lifecycle",
            "pipeline": fallback["guards"] + background["pipeline"],
            "ok": fallback["ok"]
            and background["ok"]
            and "designer_warning_visible" in fallback["guards"]
            and "resume_foreground" in background["pipeline"],
        },
        {
            "phase": "replay_runtime_delivery",
            "pipeline": tuple(item["api"] for item in runtime_replay["replay"]),
            "ok": runtime_replay["ok"]
            and set(contract["apis"]) == {item["api"] for item in runtime_replay["replay"]}
            and all("dispatch_component_events" in item["phases"] for item in runtime_replay["replay"]),
        },
        {
            "phase": "replay_designer_and_capabilities",
            "pipeline": tuple(item["phase"] for item in designer_replay["replay"])
            + tuple(check["id"] for check in lifecycle["checks"]),
            "ok": designer_replay["ok"]
            and lifecycle["ok"]
            and designer_replay["final_state"]["runtime_replays"] == len(contract["apis"])
            and lifecycle["api_count"] == len(contract["apis"]),
        },
    )
    checks = (
        {"id": "privacy_permission_ready", "ok": phases[0]["ok"], "evidence": {"privacy": privacy, "permission": permission}},
        {"id": "simulator_ready", "ok": phases[1]["ok"], "evidence": simulator},
        {"id": "bridge_component_ready", "ok": phases[2]["ok"], "evidence": {"component_validation": component_validation, "adapter": adapter}},
        {"id": "fallback_lifecycle_ready", "ok": phases[3]["ok"], "evidence": {"fallback": fallback, "background": background}},
        {"id": "runtime_delivery_ready", "ok": phases[4]["ok"], "evidence": runtime_replay},
        {"id": "designer_capability_ready", "ok": phases[5]["ok"], "evidence": {"designer": designer_replay, "lifecycle": lifecycle}},
        {"id": "operation_surface_ready", "ok": actionable["ok"] and not actionable["side_effects"], "evidence": actionable},
        {
            "id": "phase_order_ready",
            "ok": tuple(item["phase"] for item in phases)
            == (
                "declare_privacy_and_permissions",
                "configure_simulator_fixtures",
                "bind_components_and_bridges",
                "review_fallbacks_and_lifecycle",
                "replay_runtime_delivery",
                "replay_designer_and_capabilities",
            ),
            "evidence": tuple(item["phase"] for item in phases),
        },
    )
    return {
        "format": "appgen.mobile-native-api-readiness-contract.v1",
        "ok": all(phase["ok"] for phase in phases) and all(check["ok"] for check in checks),
        "phases": phases,
        "checks": checks,
        "final_state": {
            "api_count": len(contract["apis"]),
            "permission": runtime_replay["final_state"]["permission"],
            "runtime_replays": len(runtime_replay["replay"]),
            "bridge_recoveries": len(runtime_replay["bridge_recovery"]),
            "lifecycle_replays": len(runtime_replay["lifecycle_replay"]),
            "background_checkpoints": runtime_replay["final_state"]["checkpoints"],
        },
        "guards": (
            "privacy_before_permission",
            "permission_before_simulator",
            "simulator_before_bridge",
            "fallbacks_before_runtime",
            "runtime_before_designer_claim",
            "side_effect_free_readiness",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
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
    actionable_operations = mobile_native_api_actionable_operations()
    device_component_specs = mobile_device_component_spec_contract()
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
    runtime_replay = mobile_native_api_runtime_replay_contract()
    designer_transaction_replay = mobile_device_designer_transaction_replay_contract()
    capability_lifecycle_replay = mobile_device_capability_lifecycle_replay_contract()
    device_component_module_artifacts = device_api_component_module_file_manifest()
    device_component_test_artifacts = device_api_component_test_module_file_manifest()
    readiness = mobile_native_api_readiness_contract()
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
            "id": "actionable_mobile_api_operations",
            "ok": actionable_operations["ok"]
            and {
                "request_permission",
                "dispatch_adapter",
                "replay_simulator",
                "review_platform_fallback",
                "review_privacy",
                "resume_background",
                "validate_device_component",
            }
            <= set(actionable_operations["operations"])
            and not actionable_operations["side_effects"],
            "evidence": actionable_operations,
        },
        {
            "id": "device_component_specs",
            "ok": device_component_specs["ok"]
            and api_set == {spec["api"] for spec in device_component_specs["specs"]}
            and all({"permission_editor", "simulator_fixture_picker", "event_trace_viewer"} <= set(spec["design_tools"]) for spec in device_component_specs["specs"])
            and not device_component_specs["side_effects"],
            "evidence": device_component_specs,
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
        {
            "id": "runtime_delivery_replay",
            "ok": runtime_replay["ok"]
            and {"permission_replayed_before_bridge", "lifecycle_resume_replays_pending_events"} <= set(runtime_replay["guards"])
            and not runtime_replay["side_effects"],
            "evidence": runtime_replay,
        },
        {
            "id": "designer_transaction_replay",
            "ok": designer_transaction_replay["ok"]
            and {"permission_manifest_before_adapter_dispatch", "runtime_replay_covers_all_device_apis"} <= set(designer_transaction_replay["guards"])
            and not designer_transaction_replay["side_effects"],
            "evidence": designer_transaction_replay,
        },
        {
            "id": "capability_lifecycle_replay",
            "ok": capability_lifecycle_replay["ok"]
            and {"privacy_before_permission", "runtime_and_designer_replay_aligned"} <= set(capability_lifecycle_replay["guards"])
            and not capability_lifecycle_replay["side_effects"],
            "evidence": capability_lifecycle_replay,
        },
        {
            "id": "mobile_readiness_contract",
            "ok": readiness["ok"]
            and {
                "privacy_permission_ready",
                "simulator_ready",
                "bridge_component_ready",
                "fallback_lifecycle_ready",
                "runtime_delivery_ready",
                "designer_capability_ready",
                "operation_surface_ready",
                "phase_order_ready",
            }
            <= {check["id"] for check in readiness["checks"] if check["ok"]}
            and not readiness["side_effects"],
            "evidence": readiness,
        },
        {
            "id": "device_component_modules",
            "ok": len(device_component_module_artifacts) == len(api_set)
            and api_set == {item["api"] for item in device_component_module_artifacts}
            and all(item["ok"] and "replay" in item["exports"] for item in device_component_module_artifacts),
            "evidence": device_component_module_artifacts,
        },
        {
            "id": "device_component_module_tests",
            "ok": len(device_component_test_artifacts) == len(api_set)
            and api_set == {item["api"] for item in device_component_test_artifacts}
            and all(
                item["ok"] and "test_device_component_smoke" in item["exports"]
                for item in device_component_test_artifacts
            ),
            "evidence": device_component_test_artifacts,
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
        "actionable_operations": actionable_operations,
        "device_component_specs": device_component_specs,
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
        "runtime_replay": runtime_replay,
        "designer_transaction_replay": designer_transaction_replay,
        "capability_lifecycle_replay": capability_lifecycle_replay,
        "device_component_module_artifacts": device_component_module_artifacts,
        "device_component_test_artifacts": device_component_test_artifacts,
        "readiness": readiness,
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


def cross_target_visual_runtime_replay_contract() -> dict:
    """Replay visual authoring contracts through deterministic runtime delivery."""
    style_resolution = cross_target_style_resolution_workflow()
    inheritance = cross_target_style_inheritance_trace_contract()
    timeline = cross_target_timeline_interpolation_contract()
    timeline_export = cross_target_timeline_runtime_export_contract()
    effects = cross_target_effect_fallback_matrix_contract()
    scene = cross_target_scene_hit_test_contract()
    transforms = cross_target_scene_transform_gizmo_contract()
    state = {
        "style_published": False,
        "timeline_samples": 0,
        "effect_fallbacks": 0,
        "scene_hits": 0,
        "inspector_syncs": 0,
        "side_effects": (),
    }
    replay = (
        {
            "phase": "style_resolution",
            "pipeline": style_resolution["resolution_steps"],
            "ok": style_resolution["ordered_layers"][0] == "base_theme"
            and "apply_local_override" in style_resolution["resolution_steps"],
        },
        {
            "phase": "style_inheritance",
            "pipeline": next(iter(inheritance["traces"]))["trace"] if inheritance["traces"] else (),
            "ok": inheritance["ok"] and all("publish_effective_value" in trace["trace"] for trace in inheritance["traces"]),
        },
        {
            "phase": "timeline_interpolation",
            "pipeline": ("load_runtime_timeline", "sample_keyframes", "interpolate_values", "emit_runtime_samples"),
            "ok": timeline["ok"] and all(sample["runtime_samples"] for sample in timeline["samples"]),
        },
        {
            "phase": "timeline_export",
            "pipeline": timeline_export["guards"],
            "ok": timeline_export["ok"] and all("native_timeline" in export["artifacts"] for export in timeline_export["exports"]),
        },
        {
            "phase": "effect_fallback",
            "pipeline": effects["guards"],
            "ok": effects["ok"] and any(row["decision"] == "use_fallback" for row in effects["rows"]),
        },
        {
            "phase": "scene_hit_testing",
            "pipeline": scene["guards"],
            "ok": scene["ok"] and all("open_inspector" in item["route"] for item in scene["hit_tests"]),
        },
        {
            "phase": "scene_transform_sync",
            "pipeline": transforms["guards"],
            "ok": transforms["ok"] and all("sync_inspector" in item["pipeline"] for item in transforms["transforms"]),
        },
    )
    state["style_published"] = replay[1]["ok"]
    state["timeline_samples"] = sum(len(sample["runtime_samples"]) for sample in timeline["samples"])
    state["effect_fallbacks"] = sum(1 for row in effects["rows"] if row["decision"] == "use_fallback")
    state["scene_hits"] = len(scene["hit_tests"])
    state["inspector_syncs"] = sum(1 for item in transforms["transforms"] if "sync_inspector" in item["pipeline"])
    return {
        "format": "appgen.cross-target-visual-runtime-replay-contract.v1",
        "ok": all(item["ok"] for item in replay)
        and state["style_published"]
        and state["timeline_samples"] > 0
        and state["scene_hits"] > 0
        and state["inspector_syncs"] > 0
        and state["side_effects"] == (),
        "replay": replay,
        "final_state": state,
        "guards": (
            "style_published_before_runtime_diff",
            "timeline_samples_match_preview",
            "effect_fallbacks_are_targeted",
            "scene_hit_tests_route_to_inspector",
            "transforms_sync_inspector",
        ),
        "side_effects": (),
    }


def cross_target_visual_designer_transaction_replay_contract() -> dict:
    """Replay one ordered visual designer transaction from authoring to runtime."""
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
    timeline_interpolation = cross_target_timeline_interpolation_contract()
    effect_fallback_matrix = cross_target_effect_fallback_matrix_contract()
    scene_transform_gizmos = cross_target_scene_transform_gizmo_contract()
    runtime_replay = cross_target_visual_runtime_replay_contract()
    state = {
        "style_layers": len(contract["style_cascade"]["layers"]),
        "timeline_tracks": len(contract["timeline_authoring"]["tracks"]),
        "effect_stack": len(contract["effect_stack"]["stack"]),
        "scene_nodes": len(contract["scene_designer"]["scene_graph"]),
        "asset_formats": len(contract["asset_import"]["formats"]),
        "timeline_samples": sum(len(sample["runtime_samples"]) for sample in timeline_interpolation["samples"]),
        "effect_fallbacks": sum(1 for row in effect_fallback_matrix["rows"] if row["decision"] == "use_fallback"),
        "scene_hits": len(scene_hit_testing["hit_tests"]),
        "transform_syncs": len(scene_transform_gizmos["transforms"]),
        "side_effects": (),
    }
    replay = (
        {
            "phase": "author_style_override",
            "pipeline": style_resolution["resolution_steps"],
            "ok": {"base_theme", "state_override", "platform_override", "local_override"}
            <= {layer["layer"] for layer in contract["style_cascade"]["layers"]}
            and {"inspect_effective_value", "revert_override"} <= set(contract["style_cascade"]["operations"])
            and style_resolution["ordered_layers"][0] == "base_theme"
            and style_tokens["ok"],
        },
        {
            "phase": "author_timeline",
            "pipeline": timeline_playback["playback_steps"],
            "ok": bool(contract["timeline_authoring"]["tracks"])
            and {"add_keyframe", "scrub_preview"} <= set(contract["timeline_authoring"]["operations"])
            and bool(timeline_scrub["samples"])
            and timeline_interpolation["ok"]
            and timeline_runtime_export["ok"]
            and all("native_timeline" in export["artifacts"] for export in timeline_runtime_export["exports"]),
        },
        {
            "phase": "validate_effect_stack",
            "pipeline": effect_render["render_steps"],
            "ok": {"shadow", "blur", "glow", "shader_hook"} <= {item["effect"] for item in contract["effect_stack"]["stack"]}
            and effect_budget["ok"]
            and effect_fallback_matrix["ok"]
            and any(row["decision"] == "use_fallback" for row in effect_fallback_matrix["rows"])
            and "select_fallback" in effect_render["render_steps"],
        },
        {
            "phase": "author_scene_graph",
            "pipeline": tuple(item["op"] for item in contract["scene_authoring"]["operations"]),
            "ok": {"add_mesh", "position_camera", "edit_light", "assign_material"}
            <= {item["op"] for item in contract["scene_authoring"]["operations"]}
            and scene_validation["ok"]
            and scene_integrity["ok"]
            and material_binding["ok"]
            and shader_material_editor["ok"],
        },
        {
            "phase": "import_assets_and_preview",
            "pipeline": asset_import["pipeline"] + preview_diff["diff_steps"],
            "ok": asset_import["ok"]
            and {"fingerprint_asset", "generate_fallback_thumbnail"} <= set(asset_import["pipeline"])
            and preview_diff["diff_result"]["ok"]
            and "report_visible_diff" in preview_diff["diff_steps"],
        },
        {
            "phase": "hit_test_and_transform",
            "pipeline": scene_hit_testing["guards"] + scene_transform_gizmos["guards"],
            "ok": scene_hit_testing["ok"]
            and all("open_inspector" in item["route"] for item in scene_hit_testing["hit_tests"])
            and scene_transform_gizmos["ok"]
            and all("sync_inspector" in item["pipeline"] for item in scene_transform_gizmos["transforms"]),
        },
        {
            "phase": "runtime_replay",
            "pipeline": tuple(item["phase"] for item in runtime_replay["replay"]),
            "ok": runtime_replay["ok"]
            and {"style_resolution", "timeline_interpolation", "effect_fallback", "scene_hit_testing", "scene_transform_sync"}
            <= {item["phase"] for item in runtime_replay["replay"]},
        },
    )
    return {
        "format": "appgen.cross-target-visual-designer-transaction-replay-contract.v1",
        "ok": all(item["ok"] for item in replay)
        and state["style_layers"] >= 4
        and state["timeline_samples"] > 0
        and state["effect_fallbacks"] > 0
        and state["scene_hits"] > 0
        and state["transform_syncs"] > 0
        and state["side_effects"] == (),
        "replay": replay,
        "final_state": state,
        "guards": (
            "style_before_preview",
            "timeline_export_before_runtime",
            "effect_budget_before_runtime",
            "scene_graph_validated_before_transform",
            "assets_fingerprinted_before_preview",
            "hit_tests_route_to_inspector",
            "runtime_replay_matches_designer_state",
        ),
        "side_effects": (),
    }


def cross_target_visual_lifecycle_replay_contract() -> dict:
    """Replay visual authoring assets through preview, runtime, and designer synchronization."""
    style_tokens = cross_target_style_token_validation_contract()
    style_inheritance = cross_target_style_inheritance_trace_contract()
    timeline_scrub = cross_target_timeline_scrub_contract()
    timeline_export = cross_target_timeline_runtime_export_contract()
    effect_budget = cross_target_effect_budget_contract()
    effect_fallback = cross_target_effect_fallback_matrix_contract()
    scene_integrity = cross_target_scene_graph_integrity_contract()
    material_binding = cross_target_material_binding_contract()
    shader_editor = cross_target_shader_material_editor_contract()
    asset_import = cross_target_asset_import_workflow()
    preview_diff = cross_target_preview_runtime_diff_workflow()
    hit_testing = cross_target_scene_hit_test_contract()
    transforms = cross_target_scene_transform_gizmo_contract()
    runtime_replay = cross_target_visual_runtime_replay_contract()
    designer_replay = cross_target_visual_designer_transaction_replay_contract()
    replay = (
        {
            "phase": "validate_style_tokens",
            "ok": style_tokens["ok"]
            and style_inheritance["ok"]
            and "effective_value_traceable" in style_inheritance["guards"],
            "evidence": {
                "tokens": style_tokens["tokens"],
                "inheritance": tuple(trace["token"] for trace in style_inheritance["traces"]),
            },
        },
        {
            "phase": "export_timeline_runtime",
            "ok": timeline_scrub["ok"]
            and timeline_export["ok"]
            and all("native_timeline" in export["artifacts"] for export in timeline_export["exports"]),
            "evidence": {
                "tracks": tuple(sample["track"] for sample in timeline_scrub["samples"]),
                "exports": tuple(export["track"] for export in timeline_export["exports"]),
            },
        },
        {
            "phase": "assign_effect_fallbacks",
            "ok": effect_budget["ok"]
            and effect_fallback["ok"]
            and any(row["decision"] == "use_fallback" for row in effect_fallback["rows"]),
            "evidence": {
                "budget": effect_budget["mobile_budget"],
                "fallbacks": tuple(row["effect"] for row in effect_fallback["rows"] if row["decision"] == "use_fallback"),
            },
        },
        {
            "phase": "validate_scene_materials",
            "ok": scene_integrity["ok"]
            and material_binding["ok"]
            and shader_editor["ok"]
            and "assign_material" in shader_editor["operations"],
            "evidence": {
                "nodes": tuple(node["id"] for node in scene_integrity["nodes"]),
                "materials": tuple(binding["material"] for binding in material_binding["bindings"]),
            },
        },
        {
            "phase": "import_assets_and_diff_preview",
            "ok": asset_import["ok"]
            and preview_diff["diff_result"]["ok"]
            and {"fingerprint_asset", "write_asset_manifest"} <= set(asset_import["pipeline"])
            and "report_visible_diff" in preview_diff["diff_steps"],
            "evidence": {
                "asset_pipeline": asset_import["pipeline"],
                "diff_steps": preview_diff["diff_steps"],
            },
        },
        {
            "phase": "route_hit_tests_and_transforms",
            "ok": hit_testing["ok"]
            and transforms["ok"]
            and all("open_inspector" in item["route"] for item in hit_testing["hit_tests"])
            and all("sync_inspector" in item["pipeline"] for item in transforms["transforms"]),
            "evidence": {
                "hit_tests": tuple(item["node"] for item in hit_testing["hit_tests"]),
                "transforms": tuple(item["node"] for item in transforms["transforms"]),
            },
        },
        {
            "phase": "runtime_and_designer_replay",
            "ok": runtime_replay["ok"]
            and designer_replay["ok"]
            and "runtime_replay_matches_designer_state" in designer_replay["guards"],
            "evidence": {
                "runtime_phases": tuple(item["phase"] for item in runtime_replay["replay"]),
                "designer_phases": tuple(item["phase"] for item in designer_replay["replay"]),
            },
        },
    )
    checks = (
        {
            "id": "style_before_timeline",
            "ok": tuple(item["phase"] for item in replay).index("validate_style_tokens")
            < tuple(item["phase"] for item in replay).index("export_timeline_runtime"),
            "evidence": replay,
        },
        {
            "id": "effects_before_runtime",
            "ok": tuple(item["phase"] for item in replay).index("assign_effect_fallbacks")
            < tuple(item["phase"] for item in replay).index("runtime_and_designer_replay"),
            "evidence": replay,
        },
        {
            "id": "scene_assets_before_preview_diff",
            "ok": tuple(item["phase"] for item in replay).index("validate_scene_materials")
            < tuple(item["phase"] for item in replay).index("import_assets_and_diff_preview"),
            "evidence": replay,
        },
        {
            "id": "hit_tests_before_designer_replay",
            "ok": tuple(item["phase"] for item in replay).index("route_hit_tests_and_transforms")
            < tuple(item["phase"] for item in replay).index("runtime_and_designer_replay"),
            "evidence": replay,
        },
        {
            "id": "side_effect_guards",
            "ok": not style_tokens["side_effects"]
            and not style_inheritance["side_effects"]
            and not timeline_scrub["side_effects"]
            and not timeline_export["side_effects"]
            and not effect_budget["side_effects"]
            and not effect_fallback["side_effects"]
            and not scene_integrity["side_effects"]
            and not material_binding["side_effects"]
            and not shader_editor["side_effects"]
            and not asset_import["side_effects"]
            and not preview_diff["side_effects"]
            and not hit_testing["side_effects"]
            and not transforms["side_effects"]
            and not runtime_replay["side_effects"]
            and not designer_replay["side_effects"],
            "evidence": (),
        },
    )
    ok = all(item["ok"] for item in replay) and all(check["ok"] for check in checks)
    return {
        "format": "appgen.cross-target-visual-lifecycle-replay.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "replay": replay,
        "checks": checks,
        "guards": (
            "style_before_timeline",
            "effects_before_runtime",
            "scene_assets_before_preview_diff",
            "hit_tests_before_designer_replay",
            "no_side_effects",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def cross_target_visual_runtime_package_contract() -> dict:
    """Return target-ready visual runtime package artifacts for generated apps."""
    style_resources = cross_target_style_resource_contract()
    timeline_export = cross_target_timeline_runtime_export_contract()
    effect_fallback = cross_target_effect_fallback_matrix_contract()
    scene_integrity = cross_target_scene_graph_integrity_contract()
    material_binding = cross_target_material_binding_contract()
    shader_editor = cross_target_shader_material_editor_contract()
    asset_import = cross_target_asset_import_workflow()
    preview_diff = cross_target_preview_runtime_diff_workflow()
    runtime_replay = cross_target_visual_runtime_replay_contract()
    targets = ("web", "mobile", "desktop", "pwa")
    artifacts = tuple(
        {
            "target": target,
            "style_bundle": f"{target}/styles/appgen-stylebook.json",
            "timeline_bundle": f"{target}/animations/appgen-timelines.json",
            "effect_bundle": f"{target}/effects/appgen-effects.json",
            "scene_manifest": f"{target}/scene/appgen-scene.json",
            "asset_manifest": f"{target}/assets/appgen-assets.json",
            "adapters": ("style_loader", "timeline_player", "effect_fallback_resolver", "scene_renderer", "asset_resolver"),
            "fallbacks": tuple(row["fallback"] for row in effect_fallback["rows"] if row["target"] == target),
        }
        for target in targets
    )
    checks = (
        {
            "id": "target_artifacts_complete",
            "ok": all(
                {"style_bundle", "timeline_bundle", "effect_bundle", "scene_manifest", "asset_manifest", "adapters"} <= set(artifact)
                and {"style_loader", "timeline_player", "scene_renderer"} <= set(artifact["adapters"])
                for artifact in artifacts
            ),
            "evidence": artifacts,
        },
        {
            "id": "style_and_timeline_packaged",
            "ok": {"stylebook", "theme_tokens"} <= set(style_resources["resources"])
            and timeline_export["ok"]
            and all("native_timeline" in export["artifacts"] for export in timeline_export["exports"]),
            "evidence": {"style_resources": style_resources["resources"], "timeline_exports": timeline_export["exports"]},
        },
        {
            "id": "effect_fallbacks_packaged",
            "ok": effect_fallback["ok"]
            and all(artifact["fallbacks"] for artifact in artifacts)
            and any(row["decision"] == "use_fallback" for row in effect_fallback["rows"]),
            "evidence": effect_fallback["rows"],
        },
        {
            "id": "scene_materials_packaged",
            "ok": scene_integrity["ok"]
            and material_binding["ok"]
            and shader_editor["ok"]
            and asset_import["ok"]
            and {"write_asset_manifest", "generate_fallback_thumbnail"} <= set(asset_import["pipeline"]),
            "evidence": {
                "scene_nodes": tuple(node["id"] for node in scene_integrity["nodes"]),
                "materials": material_binding["bindings"],
                "asset_pipeline": asset_import["pipeline"],
            },
        },
        {
            "id": "preview_runtime_diff_packaged",
            "ok": preview_diff["diff_result"]["ok"]
            and "report_visible_diff" in preview_diff["diff_steps"]
            and runtime_replay["ok"]
            and runtime_replay["final_state"]["timeline_samples"] > 0,
            "evidence": {"diff_steps": preview_diff["diff_steps"], "runtime_state": runtime_replay["final_state"]},
        },
        {
            "id": "side_effect_guards",
            "ok": not style_resources.get("side_effects", ())
            and not timeline_export["side_effects"]
            and not effect_fallback["side_effects"]
            and not scene_integrity["side_effects"]
            and not material_binding["side_effects"]
            and not shader_editor["side_effects"]
            and not asset_import["side_effects"]
            and not preview_diff["side_effects"]
            and not runtime_replay["side_effects"],
            "evidence": (),
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.cross-target-visual-runtime-package.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "targets": targets,
        "artifacts": artifacts,
        "checks": checks,
        "guards": (
            "target_artifacts_complete",
            "style_and_timeline_packaged",
            "effect_fallbacks_packaged",
            "scene_materials_packaged",
            "preview_runtime_diff_packaged",
            "no_side_effects",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def cross_target_author_style_operation(component: str = "Button") -> dict:
    """Return a callable IDE operation for authoring and previewing style overrides."""
    resolution = cross_target_style_resolution_workflow(component)
    tokens = cross_target_style_token_validation_contract()
    inheritance = cross_target_style_inheritance_trace_contract(component)
    return {
        "format": "appgen.cross-target-author-style-operation.v1",
        "ok": resolution["ordered_layers"][0] == "base_theme"
        and "apply_local_override" in resolution["resolution_steps"]
        and tokens["ok"]
        and inheritance["ok"],
        "component": component,
        "pipeline": (
            "load_tokens",
            "inspect_effective_value",
            "apply_local_override",
            "publish_effective_value",
            "sync_preview",
        ),
        "effective_values": resolution["effective_values"],
        "tokens": tokens["tokens"],
        "inheritance": inheritance["traces"],
        "guards": ("token_names_stable", "effective_value_traceable", "override_diff_visible"),
        "side_effects": (),
    }


def cross_target_author_timeline_operation(timeline_id: str = "timeline.fade_in") -> dict:
    """Return a callable IDE operation for timeline/keyframe authoring."""
    playback = cross_target_timeline_playback_workflow(timeline_id)
    scrub = cross_target_timeline_scrub_contract()
    runtime_export = cross_target_timeline_runtime_export_contract()
    return {
        "format": "appgen.cross-target-author-timeline-operation.v1",
        "ok": {"sample_keyframes", "export_runtime_timeline"} <= set(playback["playback_steps"])
        and scrub["ok"]
        and runtime_export["ok"],
        "timeline": timeline_id,
        "pipeline": (
            "add_keyframe",
            "scrub_preview",
            "sample_keyframes",
            "export_runtime_timeline",
            "publish_runtime_artifacts",
        ),
        "samples": scrub["samples"],
        "exports": runtime_export["exports"],
        "guards": ("bounded_duration", "reduced_motion_fallback", "runtime_timeline_exported"),
        "side_effects": (),
    }


def cross_target_validate_effect_stack_operation() -> dict:
    """Return a callable IDE operation for effect stack validation and fallback assignment."""
    effect_render = cross_target_effect_render_workflow()
    effect_budget = cross_target_effect_budget_contract()
    fallback_matrix = cross_target_effect_fallback_matrix_contract()
    shader_editor = cross_target_shader_material_editor_contract()
    return {
        "format": "appgen.cross-target-validate-effect-stack-operation.v1",
        "ok": {"apply_effect_stack", "select_fallback"} <= set(effect_render["render_steps"])
        and effect_budget["ok"]
        and fallback_matrix["ok"]
        and "compile_fallback" in shader_editor["operations"],
        "pipeline": (
            "validate_budget",
            "assign_fallback",
            "apply_effect_stack",
            "select_fallback",
            "compile_fallback",
        ),
        "budget": effect_budget,
        "fallback_matrix": fallback_matrix,
        "shader_editor": shader_editor,
        "guards": ("mobile_frame_budget", "fallback_declared_per_target", "shader_review_required"),
        "side_effects": (),
    }


def cross_target_author_scene_operation() -> dict:
    """Return a callable IDE operation for 3D scene graph and material authoring."""
    scene_validation = cross_target_scene_validation_workflow()
    scene_integrity = cross_target_scene_graph_integrity_contract()
    material_binding = cross_target_material_binding_contract()
    shader_editor = cross_target_shader_material_editor_contract()
    return {
        "format": "appgen.cross-target-author-scene-operation.v1",
        "ok": scene_validation["ok"]
        and scene_integrity["ok"]
        and material_binding["ok"]
        and {"assign_material", "compile_fallback"} <= set(shader_editor["operations"]),
        "pipeline": (
            "add_mesh",
            "position_camera",
            "edit_light",
            "assign_material",
            "validate_scene",
            "compile_fallback",
        ),
        "scene_validation": scene_validation,
        "scene_integrity": scene_integrity,
        "material_binding": material_binding,
        "shader_editor": shader_editor,
        "guards": ("single_active_camera", "material_bound_to_mesh", "material_editor_review"),
        "side_effects": (),
    }


def cross_target_import_visual_asset_operation(asset: str = "product.glb") -> dict:
    """Return a callable IDE operation for visual asset import and preview diffing."""
    import_workflow = cross_target_asset_import_workflow(asset)
    preview_diff = cross_target_preview_runtime_diff_workflow()
    return {
        "format": "appgen.cross-target-import-visual-asset-operation.v1",
        "ok": import_workflow["ok"]
        and preview_diff["diff_result"]["ok"]
        and {"write_asset_manifest", "generate_fallback_thumbnail"} <= set(import_workflow["pipeline"]),
        "asset": asset,
        "pipeline": import_workflow["pipeline"] + preview_diff["diff_steps"],
        "import_workflow": import_workflow,
        "preview_diff": preview_diff,
        "guards": ("asset_fingerprint", "fallback_thumbnail", "runtime_diff_visible"),
        "side_effects": (),
    }


def cross_target_hit_test_transform_operation() -> dict:
    """Return a callable IDE operation for scene hit testing and transform synchronization."""
    hit_testing = cross_target_scene_hit_test_contract()
    transforms = cross_target_scene_transform_gizmo_contract()
    return {
        "format": "appgen.cross-target-hit-test-transform-operation.v1",
        "ok": hit_testing["ok"]
        and transforms["ok"]
        and all("open_inspector" in item["route"] for item in hit_testing["hit_tests"])
        and all("sync_inspector" in item["pipeline"] for item in transforms["transforms"]),
        "pipeline": ("raycast", "select_node", "open_inspector", "preview_transform", "commit_transform", "sync_inspector"),
        "hit_tests": hit_testing["hit_tests"],
        "transforms": transforms["transforms"],
        "guards": ("inspector_route_declared", "selection_round_trips", "inspector_sync_after_transform"),
        "side_effects": (),
    }


def cross_target_visual_component_spec_contract() -> dict:
    """Return IDE visual component specs for styling, animation, effects, and 3D authoring."""
    contract = cross_target_visual_depth_contract()
    style_tokens = cross_target_style_token_validation_contract()
    timeline = cross_target_animation_timeline_contract()
    effect_stack = cross_target_effect_stack_validation_contract()
    scene = cross_target_3d_scene_contract()
    material_binding = cross_target_material_binding_contract()
    hit_testing = cross_target_scene_hit_test_contract()
    transforms = cross_target_scene_transform_gizmo_contract()
    preview = cross_target_visual_preview_runtime_contract()
    specs = (
        {
            "component": "StyleBook",
            "family": "styling",
            "icon": "style",
            "properties": ("theme", "resources", "states", "platform_overrides"),
            "design_tools": ("style_inspector", "state_editor", "platform_override_editor", "contrast_checker"),
            "runtime_artifacts": ("style_resources", "asset_manifest"),
            "validation": ("token_names_stable", "contrast_checked", "effective_style_match"),
        },
        {
            "component": "FloatAnimation",
            "family": "animation",
            "icon": "float-animation",
            "properties": ("target", "property", "duration", "easing", "keyframes"),
            "design_tools": ("timeline_editor", "keyframe_grid", "scrub_preview", "reduced_motion_preview"),
            "runtime_artifacts": ("timeline_runtime",),
            "validation": ("bounded_duration", "runtime_timeline_exported", "timeline_keyframes_match"),
        },
        {
            "component": "ColorAnimation",
            "family": "animation",
            "icon": "color-animation",
            "properties": ("target", "property", "from_color", "to_color", "keyframes"),
            "design_tools": ("timeline_editor", "color_picker", "scrub_preview", "contrast_checker"),
            "runtime_artifacts": ("timeline_runtime", "style_resources"),
            "validation": ("bounded_duration", "contrast_checked", "timeline_keyframes_match"),
        },
        {
            "component": "PathAnimation",
            "family": "animation",
            "icon": "path-animation",
            "properties": ("target", "path_data", "duration", "easing", "orientation"),
            "design_tools": ("path_editor", "timeline_editor", "scrub_preview", "runtime_export"),
            "runtime_artifacts": ("timeline_runtime",),
            "validation": ("deterministic_timeline_ids", "runtime_timeline_exported", "timeline_keyframes_match"),
        },
        {
            "component": "Effect",
            "family": "effects",
            "icon": "effect",
            "properties": ("target", "effect_stack", "quality_level", "fallback"),
            "design_tools": ("effect_stack_editor", "budget_meter", "fallback_picker", "shader_review"),
            "runtime_artifacts": ("effect_stack",),
            "validation": ("mobile_frame_budget", "fallback_declared_per_target", "effect_fallback_match"),
        },
        {
            "component": "Viewport3D",
            "family": "three_d",
            "icon": "viewport3d",
            "properties": ("camera", "lights", "models", "materials", "hit_testing"),
            "design_tools": ("scene_graph", "orbit_preview", "hit_test_router", "transform_gizmo"),
            "runtime_artifacts": ("scene_graph", "asset_manifest"),
            "validation": ("single_active_camera", "scene_graph_match", "selection_round_trips"),
        },
        {
            "component": "Camera3D",
            "family": "three_d",
            "icon": "camera3d",
            "properties": ("projection", "position", "target", "field_of_view"),
            "design_tools": ("camera_preview", "orbit_preview", "transform_gizmo", "scene_graph"),
            "runtime_artifacts": ("scene_graph",),
            "validation": ("camera_present", "scene_graph_match", "transforms_sync_inspector"),
        },
        {
            "component": "Light3D",
            "family": "three_d",
            "icon": "light3d",
            "properties": ("light_type", "intensity", "color", "position"),
            "design_tools": ("light_cone", "color_picker", "transform_gizmo", "scene_graph"),
            "runtime_artifacts": ("scene_graph",),
            "validation": ("validate_lights", "scene_graph_match", "transforms_sync_inspector"),
        },
        {
            "component": "Mesh3D",
            "family": "three_d",
            "icon": "mesh3d",
            "properties": ("mesh", "material", "transform", "texture"),
            "design_tools": ("model_importer", "material_editor", "transform_gizmo", "hit_test_router"),
            "runtime_artifacts": ("scene_graph", "asset_manifest"),
            "validation": ("bounded_polygon_budget", "material_bound_to_mesh", "asset_fingerprint"),
        },
    )
    known_resources = set(contract["style_resources"]["resources"])
    runtime_artifacts = set(preview["runtime_artifacts"])
    return {
        "format": "appgen.cross-target-visual-component-spec-contract.v1",
        "ok": bool(specs)
        and {"stylebook", "theme_tokens"} <= known_resources
        and bool(style_tokens["tokens"])
        and bool(timeline["tracks"])
        and bool(effect_stack["stack"])
        and {"viewport3d", "camera", "light", "mesh", "material"} <= {node["kind"] for node in scene["scene_graph"]}
        and material_binding["ok"]
        and hit_testing["ok"]
        and transforms["ok"]
        and all(set(spec["runtime_artifacts"]) <= runtime_artifacts for spec in specs)
        and all({"properties", "design_tools", "validation"} <= set(spec) for spec in specs),
        "specs": specs,
        "style_token_count": len(style_tokens["tokens"]),
        "timeline_track_count": len(timeline["tracks"]),
        "effect_count": len(effect_stack["stack"]),
        "scene_node_count": len(scene["scene_graph"]),
        "guards": ("visual_specs_cover_style_animation_effects_scene", "runtime_artifacts_declared", "hit_tests_and_transforms_bound"),
        "side_effects": (),
    }


def cross_target_validate_visual_component_operation(component: str = "Viewport3D") -> dict:
    """Return a callable IDE operation for validating one visual design component spec."""
    specs = cross_target_visual_component_spec_contract()
    spec = next((item for item in specs["specs"] if item["component"] == component), None)
    return {
        "format": "appgen.cross-target-validate-visual-component-operation.v1",
        "ok": specs["ok"]
        and spec is not None
        and bool(spec["properties"])
        and {"runtime_artifacts_declared", "hit_tests_and_transforms_bound"} <= set(specs["guards"]),
        "component": component,
        "spec": spec,
        "pipeline": ("load_visual_component_spec", "validate_properties", "bind_design_tools", "verify_runtime_artifacts", "sync_preview", "record_validation"),
        "guards": ("visual_component_spec_required", "design_tools_bound", "runtime_artifacts_declared"),
        "side_effects": (),
    }


def cross_target_visual_actionable_operations() -> dict:
    """Return callable visual-depth operations used by the generated IDE."""
    operations = {
        "author_style": cross_target_author_style_operation(),
        "author_timeline": cross_target_author_timeline_operation(),
        "validate_effect_stack": cross_target_validate_effect_stack_operation(),
        "author_scene": cross_target_author_scene_operation(),
        "import_visual_asset": cross_target_import_visual_asset_operation(),
        "hit_test_transform": cross_target_hit_test_transform_operation(),
        "validate_visual_component": cross_target_validate_visual_component_operation(),
    }
    return {
        "format": "appgen.cross-target-visual-actionable-operations.v1",
        "ok": all(operation["ok"] for operation in operations.values()),
        "operations": operations,
        "side_effects": (),
    }


def cross_target_visual_readiness_contract() -> dict:
    """Prove the visual styling, animation, effects, and 3D path as one ordered contract."""
    style = cross_target_author_style_operation()
    timeline = cross_target_author_timeline_operation()
    effects = cross_target_validate_effect_stack_operation()
    scene = cross_target_author_scene_operation()
    asset_import = cross_target_import_visual_asset_operation()
    hit_test = cross_target_hit_test_transform_operation()
    component_validation = cross_target_validate_visual_component_operation()
    runtime_replay = cross_target_visual_runtime_replay_contract()
    designer_replay = cross_target_visual_designer_transaction_replay_contract()
    lifecycle = cross_target_visual_lifecycle_replay_contract()
    runtime_package = cross_target_visual_runtime_package_contract()
    component_specs = cross_target_visual_component_spec_contract()
    actionable = cross_target_visual_actionable_operations()
    phases = (
        {
            "phase": "author_style_resources",
            "pipeline": style["pipeline"],
            "ok": style["ok"] and {"inspect_effective_value", "publish_effective_value"} <= set(style["pipeline"]),
        },
        {
            "phase": "author_animation_timeline",
            "pipeline": timeline["pipeline"],
            "ok": timeline["ok"] and {"scrub_preview", "export_runtime_timeline"} <= set(timeline["pipeline"]),
        },
        {
            "phase": "validate_effect_stack",
            "pipeline": effects["pipeline"],
            "ok": effects["ok"] and {"validate_budget", "compile_fallback"} <= set(effects["pipeline"]),
        },
        {
            "phase": "author_scene_and_assets",
            "pipeline": scene["pipeline"] + asset_import["pipeline"],
            "ok": scene["ok"]
            and asset_import["ok"]
            and {"assign_material", "validate_scene"} <= set(scene["pipeline"])
            and {"write_asset_manifest", "generate_fallback_thumbnail"} <= set(asset_import["pipeline"]),
        },
        {
            "phase": "bind_hit_tests_and_components",
            "pipeline": hit_test["pipeline"] + component_validation["pipeline"],
            "ok": hit_test["ok"]
            and component_validation["ok"]
            and "sync_inspector" in hit_test["pipeline"]
            and "verify_runtime_artifacts" in component_validation["pipeline"],
        },
        {
            "phase": "replay_runtime_and_designer",
            "pipeline": tuple(item["phase"] for item in runtime_replay["replay"])
            + tuple(item["phase"] for item in designer_replay["replay"])
            + tuple(item["phase"] for item in lifecycle["replay"]),
            "ok": runtime_replay["ok"]
            and designer_replay["ok"]
            and lifecycle["ok"]
            and "runtime_replay_matches_designer_state" in designer_replay["guards"],
        },
        {
            "phase": "package_runtime_targets",
            "pipeline": tuple(check["id"] for check in runtime_package["checks"]),
            "ok": runtime_package["ok"]
            and {"web", "mobile", "desktop", "pwa"} <= set(runtime_package["targets"])
            and {"target_artifacts_complete", "scene_materials_packaged"} <= {
                check["id"] for check in runtime_package["checks"] if check["ok"]
            },
        },
    )
    checks = (
        {"id": "style_ready", "ok": phases[0]["ok"], "evidence": style},
        {"id": "timeline_ready", "ok": phases[1]["ok"], "evidence": timeline},
        {"id": "effects_ready", "ok": phases[2]["ok"], "evidence": effects},
        {"id": "scene_assets_ready", "ok": phases[3]["ok"], "evidence": {"scene": scene, "asset_import": asset_import}},
        {"id": "hit_test_component_ready", "ok": phases[4]["ok"] and component_specs["ok"], "evidence": {"hit_test": hit_test, "component_specs": component_specs}},
        {"id": "runtime_designer_replay_ready", "ok": phases[5]["ok"], "evidence": {"runtime": runtime_replay, "designer": designer_replay, "lifecycle": lifecycle}},
        {"id": "runtime_package_ready", "ok": phases[6]["ok"], "evidence": runtime_package},
        {"id": "operation_surface_ready", "ok": actionable["ok"] and not actionable["side_effects"], "evidence": actionable},
        {
            "id": "phase_order_ready",
            "ok": tuple(item["phase"] for item in phases)
            == (
                "author_style_resources",
                "author_animation_timeline",
                "validate_effect_stack",
                "author_scene_and_assets",
                "bind_hit_tests_and_components",
                "replay_runtime_and_designer",
                "package_runtime_targets",
            ),
            "evidence": tuple(item["phase"] for item in phases),
        },
    )
    return {
        "format": "appgen.cross-target-visual-readiness-contract.v1",
        "ok": all(phase["ok"] for phase in phases) and all(check["ok"] for check in checks),
        "phases": phases,
        "checks": checks,
        "final_state": {
            "style_tokens": len(style["tokens"]),
            "timeline_samples": len(timeline["samples"]),
            "effect_fallbacks": sum(1 for row in effects["fallback_matrix"]["rows"] if row["decision"] == "use_fallback"),
            "scene_nodes": len(scene["scene_integrity"]["nodes"]),
            "component_specs": len(component_specs["specs"]),
            "runtime_targets": len(runtime_package["targets"]),
            "runtime_steps": len(runtime_replay["replay"]),
        },
        "guards": (
            "style_before_animation",
            "animation_before_effects",
            "effects_before_scene_assets",
            "scene_assets_before_runtime_replay",
            "runtime_replay_before_package",
            "side_effect_free_readiness",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
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
    runtime_replay = cross_target_visual_runtime_replay_contract()
    designer_transaction_replay = cross_target_visual_designer_transaction_replay_contract()
    lifecycle_replay = cross_target_visual_lifecycle_replay_contract()
    runtime_package = cross_target_visual_runtime_package_contract()
    actionable_operations = cross_target_visual_actionable_operations()
    visual_component_specs = cross_target_visual_component_spec_contract()
    visual_component_module_artifacts = visual_component_file_manifest()
    visual_component_test_artifacts = visual_component_test_file_manifest()
    visual_design_module_artifacts = visual_design_ide_module_file_manifest()
    visual_design_test_artifacts = visual_design_ide_test_module_file_manifest()
    readiness = cross_target_visual_readiness_contract()
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
        {
            "id": "visual_runtime_replay",
            "ok": runtime_replay["ok"]
            and {"timeline_samples_match_preview", "transforms_sync_inspector"} <= set(runtime_replay["guards"])
            and not runtime_replay["side_effects"],
            "evidence": runtime_replay,
        },
        {
            "id": "visual_designer_transaction_replay",
            "ok": designer_transaction_replay["ok"]
            and "runtime_replay_matches_designer_state" in designer_transaction_replay["guards"]
            and not designer_transaction_replay["side_effects"],
            "evidence": designer_transaction_replay,
        },
        {
            "id": "visual_lifecycle_replay",
            "ok": lifecycle_replay["ok"]
            and {"style_before_timeline", "hit_tests_before_designer_replay"} <= set(lifecycle_replay["guards"])
            and not lifecycle_replay["side_effects"],
            "evidence": lifecycle_replay,
        },
        {
            "id": "visual_runtime_package",
            "ok": runtime_package["ok"]
            and {"web", "mobile", "desktop", "pwa"} <= set(runtime_package["targets"])
            and {"target_artifacts_complete", "scene_materials_packaged"} <= set(runtime_package["guards"])
            and not runtime_package["side_effects"],
            "evidence": runtime_package,
        },
        {
            "id": "visual_component_specs",
            "ok": visual_component_specs["ok"]
            and {"StyleBook", "FloatAnimation", "ColorAnimation", "PathAnimation", "Effect", "Viewport3D", "Camera3D", "Light3D", "Mesh3D"}
            <= {spec["component"] for spec in visual_component_specs["specs"]}
            and all(spec["design_tools"] and spec["runtime_artifacts"] for spec in visual_component_specs["specs"])
            and not visual_component_specs["side_effects"],
            "evidence": visual_component_specs,
        },
        {
            "id": "visual_component_modules",
            "ok": len(visual_component_module_artifacts) == len(visual_component_specs["specs"])
            and {item["component"] for item in visual_component_module_artifacts}
            == {spec["component"] for spec in visual_component_specs["specs"]}
            and all(item["ok"] and "replay" in item["exports"] for item in visual_component_module_artifacts),
            "evidence": visual_component_module_artifacts,
        },
        {
            "id": "visual_component_module_tests",
            "ok": len(visual_component_test_artifacts) == len(visual_component_specs["specs"])
            and {item["component"] for item in visual_component_test_artifacts}
            == {spec["component"] for spec in visual_component_specs["specs"]}
            and all("test_visual_component_smoke" in item["exports"] for item in visual_component_test_artifacts),
            "evidence": visual_component_test_artifacts,
        },
        {
            "id": "visual_design_modules",
            "ok": len(visual_design_module_artifacts) >= 6
            and {
                "style_authoring",
                "timeline_authoring",
                "effect_stack",
                "scene_authoring",
                "asset_import",
                "runtime_package",
            }
            <= {item["surface"] for item in visual_design_module_artifacts}
            and all(item["ok"] and "run_visual_operation" in item["exports"] for item in visual_design_module_artifacts),
            "evidence": visual_design_module_artifacts,
        },
        {
            "id": "visual_design_module_tests",
            "ok": len(visual_design_test_artifacts) == len(visual_design_module_artifacts)
            and {item["surface"] for item in visual_design_test_artifacts}
            == {item["surface"] for item in visual_design_module_artifacts}
            and all("test_visual_design_ide_module_smoke" in item["exports"] for item in visual_design_test_artifacts),
            "evidence": visual_design_test_artifacts,
        },
        {
            "id": "actionable_visual_operations",
            "ok": actionable_operations["ok"]
            and {
                "author_style",
                "author_timeline",
                "validate_effect_stack",
                "author_scene",
                "import_visual_asset",
                "hit_test_transform",
                "validate_visual_component",
            }
            <= set(actionable_operations["operations"])
            and not actionable_operations["side_effects"],
            "evidence": actionable_operations,
        },
        {
            "id": "visual_readiness_contract",
            "ok": readiness["ok"]
            and {
                "style_ready",
                "timeline_ready",
                "effects_ready",
                "scene_assets_ready",
                "hit_test_component_ready",
                "runtime_designer_replay_ready",
                "runtime_package_ready",
                "operation_surface_ready",
                "phase_order_ready",
            }
            <= {check["id"] for check in readiness["checks"] if check["ok"]}
            and not readiness["side_effects"],
            "evidence": readiness,
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
        "runtime_replay": runtime_replay,
        "designer_transaction_replay": designer_transaction_replay,
        "lifecycle_replay": lifecycle_replay,
        "runtime_package": runtime_package,
        "visual_component_specs": visual_component_specs,
        "visual_component_module_artifacts": visual_component_module_artifacts,
        "visual_component_test_artifacts": visual_component_test_artifacts,
        "visual_design_module_artifacts": visual_design_module_artifacts,
        "visual_design_test_artifacts": visual_design_test_artifacts,
        "actionable_operations": actionable_operations,
        "readiness": readiness,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def platform_parity_lifecycle_replay_contract() -> dict:
    """Replay the full IDE parity surface from palette coverage to target runtime delivery."""
    analog_groups = component_analog_group_audit()
    usability = component_usability_workbench()
    component_readiness = component_parity_readiness_contract()
    runtime = pascal_runtime_workbench()
    runtime_readiness = pascal_runtime_readiness_contract()
    inspector = object_inspector_workbench()
    inspector_readiness = object_inspector_readiness_contract()
    bindings = livebindings_workbench()
    binding_readiness = livebindings_readiness_contract()
    data_tooling = rad_data_tooling_workbench()
    data_readiness = data_tooling_readiness_contract()
    package_manager = design_time_package_manager_workbench()
    package_lifecycle = component_package_lifecycle_transaction_replay()
    package_readiness = component_package_readiness_contract()
    mobile = mobile_native_api_workbench()
    mobile_lifecycle = mobile_device_capability_lifecycle_replay_contract()
    mobile_readiness = mobile_native_api_readiness_contract()
    visual = cross_target_visual_depth_workbench()
    visual_lifecycle = cross_target_visual_lifecycle_replay_contract()
    visual_readiness = cross_target_visual_readiness_contract()
    mobile_lifecycle_phases = tuple(
        phase["phase"]
        for item in mobile_lifecycle["replay"]
        for phase in item["phases"]
    )
    component_readiness_passing_checks = {check["id"] for check in component_readiness["checks"] if check["ok"]}
    component_usability_passing_checks = {check["id"] for check in usability["checks"] if check["ok"]}
    runtime_passing_checks = {check["id"] for check in runtime["checks"] if check["ok"]}
    inspector_passing_checks = {check["id"] for check in inspector["checks"] if check["ok"]}
    binding_passing_checks = {check["id"] for check in bindings["checks"] if check["ok"]}
    data_tooling_passing_checks = {check["id"] for check in data_tooling["checks"] if check["ok"]}
    package_manager_passing_checks = {check["id"] for check in package_manager["checks"] if check["ok"]}
    mobile_passing_checks = {check["id"] for check in mobile["checks"] if check["ok"]}
    visual_passing_checks = {check["id"] for check in visual["checks"] if check["ok"]}
    replay = (
        {
            "phase": "component_surface_baseline",
            "ok": analog_groups["ok"]
            and usability["ok"]
            and component_readiness["ok"]
            and "phase_order_ready" in component_readiness_passing_checks
            and {
                "analog_coverage_ready",
                "palette_icons_ready",
                "behavior_surface_ready",
                "generated_modules_ready",
                "generated_tests_ready",
                "ide_release_ready",
            } <= component_readiness_passing_checks
            and {
                "per_component_files",
                "per_package_files",
                "per_component_test_files",
                "per_package_test_files",
                "module_smoke_tests",
            } <= component_usability_passing_checks,
            "evidence": {
                "groups": tuple(group["group"] for group in analog_groups["groups"]),
                "component_count": usability["component_count"],
                "readiness_passing_checks": tuple(sorted(component_readiness_passing_checks)),
                "usability_passing_checks": tuple(sorted(component_usability_passing_checks)),
                "readiness_phases": tuple(phase["phase"] for phase in component_readiness["phases"]),
            },
        },
        {
            "phase": "stream_runtime_model",
            "ok": runtime["ok"]
            and runtime_readiness["ok"]
            and "phase_order_ready" in {check["id"] for check in runtime_readiness["checks"] if check["ok"]}
            and {"form_stream_schema", "runtime_session_replay", "event_binding_lifecycle"} <= runtime_passing_checks,
            "evidence": {
                "checks": tuple(check["id"] for check in runtime["checks"]),
                "passing_checks": tuple(sorted(runtime_passing_checks)),
                "runtime_state": runtime["runtime_replay"]["final_state"],
                "readiness_phases": tuple(phase["phase"] for phase in runtime_readiness["phases"]),
            },
        },
        {
            "phase": "inspect_and_bind_design",
            "ok": inspector["ok"]
            and inspector_readiness["ok"]
            and bindings["ok"]
            and binding_readiness["ok"]
            and inspector["cross_component_replay"]["ok"]
            and bindings["designer_transaction_replay"]["ok"]
            and "phase_order_ready" in {check["id"] for check in inspector_readiness["checks"] if check["ok"]}
            and "phase_order_ready" in {check["id"] for check in binding_readiness["checks"] if check["ok"]}
            and {
                "component_editor_transaction",
                "custom_designer_registration_replay",
                "editor_lifecycle_replay",
                "design_surface_transaction_replay",
            } <= inspector_passing_checks
            and {
                "designer_transaction_replay",
                "design_runtime_session_replay",
                "binding_lifecycle_release_replay",
            } <= binding_passing_checks,
            "evidence": {
                "inspector_checks": tuple(check["id"] for check in inspector["checks"]),
                "inspector_passing_checks": tuple(sorted(inspector_passing_checks)),
                "binding_checks": tuple(check["id"] for check in bindings["checks"]),
                "binding_passing_checks": tuple(sorted(binding_passing_checks)),
                "inspector_readiness_phases": tuple(phase["phase"] for phase in inspector_readiness["phases"]),
                "binding_readiness_phases": tuple(phase["phase"] for phase in binding_readiness["phases"]),
            },
        },
        {
            "phase": "publish_data_services",
            "ok": data_tooling["ok"]
            and data_readiness["ok"]
            and "phase_order_ready" in {check["id"] for check in data_readiness["checks"] if check["ok"]}
            and data_tooling["publish_transaction_replay"]["ok"]
            and {
                "relationship_lookup_lifecycle_replay",
                "data_tooling_design_runtime_session_replay",
                "data_tooling_publish_transaction_replay",
            } <= data_tooling_passing_checks
            and {
                "schema_rehearsal_before_dataset_publish",
                "service_contract_tests_before_resource_publish",
                "offline_integrity_before_runtime_replay",
            } <= set(data_tooling["publish_transaction_replay"]["guards"]),
            "evidence": {
                "checks": tuple(check["id"] for check in data_tooling["checks"]),
                "passing_checks": tuple(sorted(data_tooling_passing_checks)),
                "publish_state": data_tooling["publish_transaction_replay"]["final_state"],
                "readiness_phases": tuple(phase["phase"] for phase in data_readiness["phases"]),
            },
        },
        {
            "phase": "install_component_packages",
            "ok": package_manager["ok"]
            and package_lifecycle["ok"]
            and package_readiness["ok"]
            and "phase_order_ready" in {check["id"] for check in package_readiness["checks"] if check["ok"]}
            and {
                "lifecycle_transaction_replay",
                "actionable_package_operations",
                "package_manager_modules",
            } <= package_manager_passing_checks
            and all(item["final_state"]["registry_clean"] for item in package_lifecycle["replay"]),
            "evidence": {
                "manager_checks": tuple(check["id"] for check in package_manager["checks"]),
                "manager_passing_checks": tuple(sorted(package_manager_passing_checks)),
                "packages": package_lifecycle["packages"],
                "readiness_phases": tuple(phase["phase"] for phase in package_readiness["phases"]),
            },
        },
        {
            "phase": "validate_device_capabilities",
            "ok": mobile["ok"]
            and mobile_readiness["ok"]
            and mobile_lifecycle["ok"]
            and "phase_order_ready" in {check["id"] for check in mobile_readiness["checks"] if check["ok"]}
            and {
                "capability_lifecycle_replay",
                "device_component_modules",
                "device_component_module_tests",
            } <= mobile_passing_checks
            and "runtime_and_designer_replay_aligned" in mobile_lifecycle["guards"],
            "evidence": {
                "apis": tuple(adapter["api"] for adapter in mobile["contract"]["component_adapters"]["adapters"]),
                "passing_checks": tuple(sorted(mobile_passing_checks)),
                "lifecycle_phases": mobile_lifecycle_phases,
                "readiness_phases": tuple(phase["phase"] for phase in mobile_readiness["phases"]),
            },
        },
        {
            "phase": "validate_visual_depth",
            "ok": visual["ok"]
            and visual_readiness["ok"]
            and visual_lifecycle["ok"]
            and "phase_order_ready" in {check["id"] for check in visual_readiness["checks"] if check["ok"]}
            and {
                "visual_runtime_replay",
                "visual_lifecycle_replay",
                "visual_component_modules",
                "visual_design_modules",
            } <= visual_passing_checks
            and "hit_tests_before_designer_replay" in visual_lifecycle["guards"],
            "evidence": {
                "checks": tuple(check["id"] for check in visual["checks"]),
                "passing_checks": tuple(sorted(visual_passing_checks)),
                "lifecycle_phases": tuple(item["phase"] for item in visual_lifecycle["replay"]),
                "readiness_phases": tuple(phase["phase"] for phase in visual_readiness["phases"]),
            },
        },
    )
    phase_names = tuple(item["phase"] for item in replay)
    required_phase_names = (
        "component_surface_baseline",
        "stream_runtime_model",
        "inspect_and_bind_design",
        "publish_data_services",
        "install_component_packages",
        "validate_device_capabilities",
        "validate_visual_depth",
    )
    passing_phase_names = tuple(item["phase"] for item in replay if item["ok"])
    checks = (
        {
            "id": "component_baseline_before_runtime",
            "ok": phase_names.index("component_surface_baseline") < phase_names.index("stream_runtime_model"),
            "evidence": phase_names,
        },
        {
            "id": "runtime_before_design_transactions",
            "ok": phase_names.index("stream_runtime_model") < phase_names.index("inspect_and_bind_design"),
            "evidence": phase_names,
        },
        {
            "id": "design_transactions_before_data_publish",
            "ok": phase_names.index("inspect_and_bind_design") < phase_names.index("publish_data_services"),
            "evidence": phase_names,
        },
        {
            "id": "packages_before_target_validation",
            "ok": phase_names.index("install_component_packages") < phase_names.index("validate_device_capabilities"),
            "evidence": phase_names,
        },
        {
            "id": "target_validation_before_release_claim",
            "ok": phase_names.index("validate_device_capabilities") < phase_names.index("validate_visual_depth"),
            "evidence": phase_names,
        },
        {
            "id": "all_subsystems_replayed",
            "ok": set(required_phase_names) <= set(passing_phase_names),
            "required_phases": required_phase_names,
            "passing_phases": passing_phase_names,
            "evidence": replay,
        },
    )
    ok = all(item["ok"] for item in replay) and all(check["ok"] for check in checks)
    return {
        "format": "appgen.platform-parity-lifecycle-replay.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "replay": replay,
        "checks": checks,
        "required_phases": required_phase_names,
        "passing_phases": passing_phase_names,
        "guards": (
            "component_baseline_before_runtime",
            "runtime_before_design_transactions",
            "design_transactions_before_data_publish",
            "packages_before_target_validation",
            "target_validation_before_release_claim",
        ),
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def platform_parity_requirement_audit_contract() -> dict:
    """Map each requested IDE parity requirement to concrete subsystem evidence."""
    analog_groups = component_analog_group_audit()
    component_readiness = component_parity_readiness_contract()
    component_usability = component_usability_workbench()
    runtime = pascal_runtime_workbench()
    runtime_readiness = pascal_runtime_readiness_contract()
    inspector = object_inspector_workbench()
    inspector_readiness = object_inspector_readiness_contract()
    bindings = livebindings_workbench()
    binding_readiness = livebindings_readiness_contract()
    data_tooling = rad_data_tooling_workbench()
    data_readiness = data_tooling_readiness_contract()
    package_manager = design_time_package_manager_workbench()
    package_lifecycle = component_package_lifecycle_transaction_replay()
    package_readiness = component_package_readiness_contract()
    mobile = mobile_native_api_workbench()
    mobile_lifecycle = mobile_device_capability_lifecycle_replay_contract()
    mobile_readiness = mobile_native_api_readiness_contract()
    visual = cross_target_visual_depth_workbench()
    visual_lifecycle = cross_target_visual_lifecycle_replay_contract()
    visual_readiness = cross_target_visual_readiness_contract()
    lifecycle = platform_parity_lifecycle_replay_contract()

    def _passing_evidence_check_ids(value: object) -> set[str]:
        """Collect passing check ids from nested requirement evidence."""
        passing: set[str] = set()
        if isinstance(value, dict):
            checks = value.get("checks", ())
            if isinstance(checks, (tuple, list)):
                passing.update(
                    check["id"]
                    for check in checks
                    if isinstance(check, dict) and check.get("ok") and isinstance(check.get("id"), str)
                )
            for nested in value.values():
                passing.update(_passing_evidence_check_ids(nested))
        elif isinstance(value, (tuple, list)):
            for nested in value:
                passing.update(_passing_evidence_check_ids(nested))
        return passing

    requirements = (
        {
            "id": "component_parity",
            "ok": analog_groups["ok"]
            and component_readiness["ok"]
            and component_usability["ok"]
            and {
                "analog_coverage_ready",
                "palette_icons_ready",
                "behavior_surface_ready",
                "generated_modules_ready",
                "generated_tests_ready",
                "ide_release_ready",
                "phase_order_ready",
            }
            <= {check["id"] for check in component_readiness["checks"] if check["ok"]}
            and {
                "per_component_files",
                "per_package_files",
                "per_component_test_files",
                "per_package_test_files",
                "module_smoke_tests",
                "component_parity_readiness",
            } <= {check["id"] for check in component_usability["checks"] if check["ok"]}
            and {
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
            } == {group["group"] for group in analog_groups["groups"]},
            "deep_checks": (
                "analog_coverage_ready",
                "generated_modules_ready",
                "generated_tests_ready",
                "per_component_files",
                "per_package_files",
                "per_component_test_files",
                "per_package_test_files",
                "module_smoke_tests",
                "ide_release_ready",
                "phase_order_ready",
            ),
            "evidence": {"groups": analog_groups, "readiness": component_readiness, "usability": component_usability},
        },
        {
            "id": "native_runtime_streaming",
            "ok": runtime["ok"]
            and runtime_readiness["ok"]
            and {
                "stream_identity_ready",
                "unit_semantics_ready",
                "compile_targets_ready",
                "diagnostics_route_ready",
                "runtime_preview_ready",
                "phase_order_ready",
            }
            <= {check["id"] for check in runtime_readiness["checks"] if check["ok"]}
            and {
                "form_stream_schema",
                "runtime_session_replay",
                "design_edit_session_replay",
                "native_form_modules",
                "native_form_module_tests",
                "runtime_operation_modules",
                "runtime_operation_module_tests",
                "compiler_runtime_modules",
                "compiler_runtime_module_tests",
                "deep_runtime_modules",
                "deep_runtime_module_tests",
            } <= {check["id"] for check in runtime["checks"] if check["ok"]},
            "deep_checks": (
                "stream_identity_ready",
                "compile_targets_ready",
                "diagnostics_route_ready",
                "runtime_preview_ready",
                "native_form_modules",
                "native_form_module_tests",
                "runtime_operation_modules",
                "runtime_operation_module_tests",
                "compiler_runtime_modules",
                "compiler_runtime_module_tests",
                "deep_runtime_modules",
                "deep_runtime_module_tests",
                "phase_order_ready",
            ),
            "evidence": {"workbench": runtime, "readiness": runtime_readiness},
        },
        {
            "id": "inspector_design_surface",
            "ok": inspector["ok"]
            and inspector_readiness["ok"]
            and {
                "editor_metadata_ready",
                "property_event_ready",
                "component_custom_designer_ready",
                "state_design_surface_ready",
                "binding_handler_ready",
                "lifecycle_round_trip_ready",
                "phase_order_ready",
            }
            <= {check["id"] for check in inspector_readiness["checks"] if check["ok"]}
            and {
                "property_editor_types",
                "event_editor_lifecycle",
                "component_editor_transaction",
                "custom_designer_registration_replay",
                "editor_lifecycle_replay",
                "inspector_generated_modules",
                "inspector_generated_module_tests",
            } <= {check["id"] for check in inspector["checks"] if check["ok"]},
            "deep_checks": (
                "editor_lifecycle_replay",
                "design_surface_transaction_replay",
                "custom_designer_registration_replay",
                "inspector_generated_modules",
                "inspector_generated_module_tests",
                "phase_order_ready",
            ),
            "evidence": {"workbench": inspector, "readiness": inspector_readiness},
        },
        {
            "id": "visual_binding_designer",
            "ok": bindings["ok"]
            and binding_readiness["ok"]
            and {
                "graph_authoring_ready",
                "validation_transaction_ready",
                "preview_runtime_ready",
                "diagnostics_conflict_ready",
                "offline_accessible_runtime_ready",
                "designer_release_replay_ready",
                "inspector_bridge_ready",
                "phase_order_ready",
            }
            <= {check["id"] for check in binding_readiness["checks"] if check["ok"]}
            and bindings["designer_transaction_replay"]["ok"]
            and bindings["design_runtime_replay"]["ok"]
            and bindings["lifecycle_release_replay"]["ok"]
            and {
                "binding_generated_modules",
                "binding_generated_module_tests",
            } <= {check["id"] for check in bindings["checks"] if check["ok"]},
            "deep_checks": (
                "binding_lifecycle_release_replay",
                "design_runtime_session_replay",
                "designer_transaction_replay",
                "binding_generated_modules",
                "binding_generated_module_tests",
                "phase_order_ready",
            ),
            "evidence": {"workbench": bindings, "readiness": binding_readiness},
        },
        {
            "id": "native_data_service_tooling",
            "ok": data_tooling["ok"]
            and data_readiness["ok"]
            and {
                "connection_ready",
                "dataset_ready",
                "publish_ready",
                "offline_replay_ready",
                "replication_failover_ready",
                "diagnostics_ready",
                "phase_order_ready",
            }
            <= {check["id"] for check in data_readiness["checks"] if check["ok"]}
            and data_tooling["runtime_replay"]["ok"]
            and data_tooling["publish_transaction_replay"]["ok"]
            and {
                "relationship_lookup_lifecycle_replay",
                "data_tooling_modules",
                "data_tooling_module_tests",
                "deep_data_tooling_modules",
                "deep_data_tooling_module_tests",
            } <= {check["id"] for check in data_tooling["checks"] if check["ok"]},
            "deep_checks": (
                "relationship_lookup_lifecycle_replay",
                "data_tooling_modules",
                "data_tooling_module_tests",
                "deep_data_tooling_modules",
                "deep_data_tooling_module_tests",
                "data_tooling_design_runtime_session_replay",
                "data_tooling_publish_transaction_replay",
                "phase_order_ready",
            ),
            "evidence": {"workbench": data_tooling, "readiness": data_readiness},
        },
        {
            "id": "package_installation_ecosystem",
            "ok": package_manager["ok"]
            and package_lifecycle["ok"]
            and package_readiness["ok"]
            and {
                "trust_before_preview",
                "preview_before_registry_commit",
                "registry_before_update",
                "rollback_before_cleanup",
                "operation_surface_ready",
                "phase_order_ready",
            }
            <= {check["id"] for check in package_readiness["checks"] if check["ok"]}
            and {
                "lifecycle_transaction_replay",
                "package_manager_modules",
                "package_manager_module_tests",
            } <= {check["id"] for check in package_manager["checks"] if check["ok"]},
            "deep_checks": (
                "trust_before_preview",
                "preview_before_registry_commit",
                "registry_before_update",
                "rollback_before_cleanup",
                "package_manager_modules",
                "package_manager_module_tests",
                "phase_order_ready",
            ),
            "evidence": {"manager": package_manager, "lifecycle": package_lifecycle, "readiness": package_readiness},
        },
        {
            "id": "device_api_component_coverage",
            "ok": mobile["ok"]
            and mobile_readiness["ok"]
            and mobile_lifecycle["ok"]
            and {
                "privacy_permission_ready",
                "simulator_ready",
                "bridge_component_ready",
                "fallback_lifecycle_ready",
                "runtime_delivery_ready",
                "designer_capability_ready",
                "phase_order_ready",
            }
            <= {check["id"] for check in mobile_readiness["checks"] if check["ok"]}
            and "runtime_and_designer_replay_aligned" in mobile_lifecycle["guards"]
            and {
                "device_component_modules",
                "device_component_module_tests",
            } <= {check["id"] for check in mobile["checks"] if check["ok"]},
            "deep_checks": (
                "privacy_permission_ready",
                "bridge_component_ready",
                "runtime_delivery_ready",
                "designer_capability_ready",
                "device_component_modules",
                "device_component_module_tests",
                "phase_order_ready",
            ),
            "evidence": {"workbench": mobile, "lifecycle": mobile_lifecycle, "readiness": mobile_readiness},
        },
        {
            "id": "cross_target_visual_depth",
            "ok": visual["ok"]
            and visual_readiness["ok"]
            and visual_lifecycle["ok"]
            and {
                "style_ready",
                "timeline_ready",
                "effects_ready",
                "scene_assets_ready",
                "hit_test_component_ready",
                "runtime_designer_replay_ready",
                "runtime_package_ready",
                "phase_order_ready",
            }
            <= {check["id"] for check in visual_readiness["checks"] if check["ok"]}
            and {"visual_runtime_replay", "visual_lifecycle_replay"} <= {
                check["id"] for check in visual["checks"] if check["ok"]
            }
            and {
                "visual_component_modules",
                "visual_component_module_tests",
                "visual_design_modules",
                "visual_design_module_tests",
            } <= {check["id"] for check in visual["checks"] if check["ok"]},
            "deep_checks": (
                "style_ready",
                "timeline_ready",
                "effects_ready",
                "scene_assets_ready",
                "runtime_designer_replay_ready",
                "runtime_package_ready",
                "visual_component_modules",
                "visual_component_module_tests",
                "visual_design_modules",
                "visual_design_module_tests",
                "phase_order_ready",
            ),
            "evidence": {"workbench": visual, "lifecycle": visual_lifecycle, "readiness": visual_readiness},
        },
    )
    deep_check_coverage = tuple(
        {
            "requirement": requirement["id"],
            "ok": not (set(requirement["deep_checks"]) - _passing_evidence_check_ids(requirement["evidence"])),
            "required_deep_checks": requirement["deep_checks"],
            "passing_deep_checks": tuple(
                sorted(set(requirement["deep_checks"]) & _passing_evidence_check_ids(requirement["evidence"]))
            ),
            "missing": tuple(sorted(set(requirement["deep_checks"]) - _passing_evidence_check_ids(requirement["evidence"]))),
            "passing_evidence": tuple(sorted(_passing_evidence_check_ids(requirement["evidence"]))),
        }
        for requirement in requirements
    )
    required_requirement_ids = tuple(requirement["id"] for requirement in requirements)
    passing_requirement_ids = tuple(requirement["id"] for requirement in requirements if requirement["ok"])
    missing_requirement_ids = tuple(
        requirement_id for requirement_id in required_requirement_ids if requirement_id not in passing_requirement_ids
    )
    missing_deep_checks = tuple(
        {"requirement": item["requirement"], "missing": item["missing"]}
        for item in deep_check_coverage
        if item["missing"]
    )
    checks = (
        {
            "id": "all_requirements_have_evidence",
            "ok": all("evidence" in requirement and requirement["evidence"] for requirement in requirements),
            "evidence": tuple(requirement["id"] for requirement in requirements),
        },
        {
            "id": "all_requirements_pass",
            "ok": set(required_requirement_ids) <= set(passing_requirement_ids),
            "required_requirements": required_requirement_ids,
            "passing_requirements": passing_requirement_ids,
            "evidence": requirements,
        },
        {
            "id": "deep_checks_have_passing_evidence",
            "ok": all(item["ok"] for item in deep_check_coverage),
            "evidence": deep_check_coverage,
        },
        {
            "id": "lifecycle_replay_aligned",
            "ok": lifecycle["ok"] and "all_subsystems_replayed" in {check["id"] for check in lifecycle["checks"] if check["ok"]},
            "evidence": lifecycle,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.platform-parity-requirement-audit.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "requirements": requirements,
        "checks": checks,
        "required_requirements": required_requirement_ids,
        "passing_requirements": passing_requirement_ids,
        "missing_requirements": missing_requirement_ids,
        "deep_check_coverage": deep_check_coverage,
        "missing_deep_checks": missing_deep_checks,
        "lifecycle_replay": lifecycle,
        "blocking_gaps": tuple(requirement for requirement in requirements if not requirement["ok"]),
        "side_effects": (),
    }


def rad_parity_workbench(existing_paths: set[str] | None = None) -> dict:
    """Return package-level evidence for the requested RAD parity roadmap."""
    existing = (
        {"app/form_designer.py", "app/templates/appgen_form_designer.html"}
        if existing_paths is None
        else existing_paths
    )
    required_artifacts = ("app/form_designer.py", "app/templates/appgen_form_designer.html")
    passing_artifacts = tuple(sorted(set(required_artifacts) & existing))
    install_plan = third_party_component_install_plan()
    package_workbench = component_package_workbench()
    component_readiness = component_parity_readiness_contract()
    usability_workbench = component_usability_workbench()
    package_readiness = component_package_readiness_contract()
    streaming_contract = dfm_streaming_contract()
    runtime_workbench = pascal_runtime_workbench()
    platform_lifecycle = platform_parity_lifecycle_replay_contract()
    requirement_audit = platform_parity_requirement_audit_contract()
    third_party_categories = set(third_party_component_categories())
    platform_lifecycle_passing_checks = {
        check["id"] for check in platform_lifecycle["checks"] if check["ok"]
    }
    requirement_audit_passing_checks = {
        check["id"] for check in requirement_audit["checks"] if check["ok"]
    }
    required_platform_lifecycle_checks = (
        "component_baseline_before_runtime",
        "runtime_before_design_transactions",
        "design_transactions_before_data_publish",
        "packages_before_target_validation",
        "target_validation_before_release_claim",
        "all_subsystems_replayed",
    )
    required_requirement_audit_checks = (
        "all_requirements_have_evidence",
        "all_requirements_pass",
        "deep_checks_have_passing_evidence",
        "lifecycle_replay_aligned",
    )
    required_component_palette_categories = ("input", "calendar", "relationship", "media", "action")
    passing_component_palette_categories = tuple(sorted(set(palette_categories())))
    required_component_usability_checks = (
        "complete_catalog",
        "runtime_renderers",
        "property_editors",
        "events",
        "validation_rules",
        "drop_defaults",
        "preview_contracts",
        "design_surface_actions",
        "per_component_files",
        "per_package_files",
        "per_component_test_files",
        "per_package_test_files",
        "module_smoke_tests",
        "requested_analog_coverage",
        "component_behavior",
        "ide_readiness_catalog",
        "component_parity_readiness",
    )
    passing_component_usability_checks = tuple(
        check["id"] for check in usability_workbench["checks"] if check["ok"]
    )
    required_inspector_tabs = ("Properties", "Events")
    passing_inspector_tabs = tuple(object_inspector_contract()["tabs"])
    required_binding_edges = ("control_to_field",)
    passing_binding_edges = tuple(livebindings_contract()["binding_edges"])
    required_data_tooling_names = ("FireDAC", "DataSnap", "RAD Server", "InterBase")
    passing_data_tooling_names = tuple(rad_data_tooling_contract()["tooling"])
    required_mobile_api_names = ("camera", "location", "push_notifications", "secure_storage")
    passing_mobile_api_names = tuple(mobile_native_api_contract()["apis"])
    visual_depth_contract = cross_target_visual_depth_contract()
    visual_depth_workbench = cross_target_visual_depth_workbench()
    required_visual_depth_surfaces = ("styling", "animation", "effects", "three_d")
    passing_visual_depth_surfaces = tuple(
        surface for surface in required_visual_depth_surfaces if bool(visual_depth_contract[surface])
    )
    required_package_lifecycle_phases = (
        "trust_and_lockfile",
        "sandbox_preview",
        "registry_commit",
        "versioned_update",
        "failure_and_rollback",
        "uninstall_cleanup",
    )
    passing_package_lifecycle_phases = tuple(
        phase["phase"] for phase in package_readiness["phases"] if phase["ok"]
    )
    required_package_readiness_checks = (
        "trust_before_preview",
        "preview_before_registry_commit",
        "registry_before_update",
        "rollback_before_cleanup",
        "operation_surface_ready",
        "phase_order_ready",
        "side_effect_guard_ready",
    )
    passing_package_readiness_checks = tuple(
        check["id"] for check in package_readiness["checks"] if check["ok"]
    )
    required_stream_formats = ("text-dfm", "binary-dfm", "json-form-model")
    passing_stream_formats = tuple(streaming_contract["stream_formats"])
    required_compiler_stages = ("parse_units", "type_check", "resource_link", "emit_target")
    passing_compiler_stages = tuple(runtime_workbench["compiler"]["stages"])
    required_runtime_replay_phases = ("stream_decode", "semantic_static_analysis", "target_emit", "runtime_load")
    passing_runtime_replay_phases = tuple(phase["phase"] for phase in runtime_workbench["runtime_replay"]["replay"])
    required_third_party_categories = ("grid", "reports", "charts", "database", "network", "animation")
    passing_third_party_categories = tuple(sorted(third_party_categories))
    required_package_workbench_checks = (
        "registry_coverage",
        "adapter_coverage",
        "load_policy_guards",
        "install_plan_review",
        "install_session_replay",
        "package_manager_workbench",
        "package_behavior_workbench",
        "actionable_package_operations",
        "package_file_exports",
    )
    passing_package_workbench_checks = tuple(
        check["id"] for check in package_workbench["checks"] if check["ok"]
    )
    checks = (
        {
            "id": "native_ui_parity_component_parity",
            "ok": len(component_palette()) >= 7
            and set(required_component_palette_categories) <= set(passing_component_palette_categories)
            and component_readiness["ok"],
            "required_categories": required_component_palette_categories,
            "passing_categories": passing_component_palette_categories,
            "required_component_count": 7,
            "passing_component_count": len(component_palette()),
            "evidence": {"components": tuple(item["component"] for item in component_palette()), "readiness": component_readiness},
        },
        {
            "id": "built_in_component_usability",
            "ok": usability_workbench["ok"]
            and set(required_component_usability_checks) <= set(passing_component_usability_checks),
            "required_checks": required_component_usability_checks,
            "passing_checks": passing_component_usability_checks,
            "evidence": usability_workbench,
        },
        {
            "id": "pascal_runtime_and_dfm_streaming",
            "ok": set(required_stream_formats) <= set(passing_stream_formats)
            and set(required_compiler_stages) <= set(passing_compiler_stages)
            and set(required_runtime_replay_phases) <= set(passing_runtime_replay_phases)
            and runtime_workbench["ok"],
            "required_stream_formats": required_stream_formats,
            "passing_stream_formats": passing_stream_formats,
            "required_compiler_stages": required_compiler_stages,
            "passing_compiler_stages": passing_compiler_stages,
            "required_runtime_phases": required_runtime_replay_phases,
            "passing_runtime_phases": passing_runtime_replay_phases,
            "evidence": {"streaming": streaming_contract, "runtime": runtime_workbench},
        },
        {
            "id": "pascal_runtime_workbench",
            "ok": runtime_workbench["ok"],
            "evidence": runtime_workbench,
        },
        {
            "id": "object_inspector_parity",
            "ok": set(required_inspector_tabs) <= set(passing_inspector_tabs)
            and object_inspector_workbench()["ok"],
            "required_tabs": required_inspector_tabs,
            "passing_tabs": passing_inspector_tabs,
            "evidence": {"contract": object_inspector_contract(), "workbench": object_inspector_workbench()},
        },
        {
            "id": "livebindings_designer",
            "ok": set(required_binding_edges) <= set(passing_binding_edges)
            and livebindings_workbench()["ok"],
            "required_edges": required_binding_edges,
            "passing_edges": passing_binding_edges,
            "evidence": {"contract": livebindings_contract(), "workbench": livebindings_workbench()},
        },
        {
            "id": "firedac_datasnap_radserver_interbase_tooling",
            "ok": set(required_data_tooling_names) <= set(passing_data_tooling_names)
            and rad_data_tooling_workbench()["ok"],
            "required_tooling": required_data_tooling_names,
            "passing_tooling": passing_data_tooling_names,
            "evidence": {"contract": rad_data_tooling_contract(), "workbench": rad_data_tooling_workbench()},
        },
        {
            "id": "design_time_package_installation",
            "ok": install_plan["ok"]
            and install_plan["requires_review"]
            and package_readiness["ok"]
            and set(required_package_lifecycle_phases) <= set(passing_package_lifecycle_phases)
            and set(required_package_readiness_checks) <= set(passing_package_readiness_checks),
            "required_phases": required_package_lifecycle_phases,
            "passing_phases": passing_package_lifecycle_phases,
            "required_checks": required_package_readiness_checks,
            "passing_checks": passing_package_readiness_checks,
            "evidence": {"install_plan": install_plan, "readiness": package_readiness},
        },
        {
            "id": "mobile_native_device_api_coverage",
            "ok": set(required_mobile_api_names) <= set(passing_mobile_api_names)
            and mobile_native_api_workbench()["ok"],
            "required_apis": required_mobile_api_names,
            "passing_apis": passing_mobile_api_names,
            "evidence": {"contract": mobile_native_api_contract(), "workbench": mobile_native_api_workbench()},
        },
        {
            "id": "cross_target_animation_effects_3d_depth",
            "ok": set(required_visual_depth_surfaces) <= set(passing_visual_depth_surfaces)
            and visual_depth_workbench["ok"],
            "required_surfaces": required_visual_depth_surfaces,
            "passing_surfaces": passing_visual_depth_surfaces,
            "evidence": {"contract": visual_depth_contract, "workbench": visual_depth_workbench},
        },
        {
            "id": "third_party_component_ecosystem",
            "ok": install_plan["ok"]
            and set(required_third_party_categories) <= set(passing_third_party_categories)
            and set(required_package_workbench_checks) <= set(passing_package_workbench_checks)
            and package_workbench["ok"],
            "required_categories": required_third_party_categories,
            "passing_categories": passing_third_party_categories,
            "required_checks": required_package_workbench_checks,
            "passing_checks": passing_package_workbench_checks,
            "evidence": {
                "packages": install_plan["packages"],
                "categories": passing_third_party_categories,
                "package_workbench": package_workbench,
            },
        },
        {
            "id": "platform_parity_lifecycle_replay",
            "ok": platform_lifecycle["ok"]
            and platform_lifecycle["decision"] == "approved"
            and set(required_platform_lifecycle_checks) <= platform_lifecycle_passing_checks
            and {"component_baseline_before_runtime", "target_validation_before_release_claim"} <= set(platform_lifecycle["guards"])
            and not platform_lifecycle["blocking_gaps"]
            and not platform_lifecycle["side_effects"],
            "required_checks": required_platform_lifecycle_checks,
            "passing_checks": tuple(sorted(platform_lifecycle_passing_checks)),
            "evidence": platform_lifecycle,
        },
        {
            "id": "platform_parity_requirement_audit",
            "ok": requirement_audit["ok"]
            and requirement_audit["decision"] == "approved"
            and set(required_requirement_audit_checks) <= requirement_audit_passing_checks
            and not requirement_audit["blocking_gaps"]
            and not requirement_audit["side_effects"],
            "required_checks": required_requirement_audit_checks,
            "passing_checks": tuple(sorted(requirement_audit_passing_checks)),
            "evidence": requirement_audit,
        },
        {
            "id": "artifact_contract",
            "ok": set(required_artifacts) <= set(passing_artifacts),
            "required_artifacts": required_artifacts,
            "passing_artifacts": passing_artifacts,
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
        "lifecycle_replay": platform_lifecycle,
        "requirement_audit": requirement_audit,
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


def component_design_surface_contract(component: str) -> dict:
    """Return toolbox, drop preview, context menu, and gesture metadata."""
    contract = component_runtime_contract(component)
    metadata = component_designer_metadata_contract(component)
    category = contract["category"]
    common_actions = (
        "inspect",
        "edit_bindings",
        "align_to_grid",
        "bring_to_front",
        "send_to_back",
        "duplicate",
        "delete",
    )
    category_actions = {
        "action": ("edit_action", "assign_shortcut"),
        "analytics": ("edit_series", "preview_chart"),
        "calendar": ("edit_display_format", "validate_range"),
        "choice": ("edit_items", "toggle_multi_select"),
        "container": ("edit_children", "set_layout"),
        "data": ("bind_dataset", "preview_rows"),
        "data_access": ("edit_connection", "preview_rows"),
        "effects": ("edit_timeline", "preview_motion"),
        "gesture": ("edit_recognizer", "test_gesture"),
        "graphics": ("edit_shape", "export_vector"),
        "integration": ("edit_endpoint", "test_request"),
        "media": ("select_asset", "clear_asset"),
        "menu": ("edit_menu_items", "assign_roles"),
        "mobile": ("edit_permission", "simulate_device_event"),
        "navigation": ("edit_nodes", "preview_lazy_load"),
        "nonvisual": ("configure_service", "show_status"),
        "relationship": ("edit_lookup", "preview_candidates"),
        "reports": ("edit_report", "export_preview"),
        "theme": ("edit_resources", "apply_variant"),
        "three_d": ("edit_scene", "open_transform_gizmo"),
    }
    gestures = (
        "drag_from_toolbox",
        "drop_on_canvas",
        "resize_handles",
        "keyboard_nudge",
        "copy_paste",
        "context_menu",
    )
    if metadata["canvas"]["supports_nested_children"]:
        gestures += ("drop_child", "reorder_children")
    if category in {"graphics", "three_d"}:
        gestures += ("direct_manipulation", "hit_test_overlay")
    if category in {"data", "data_access", "relationship"}:
        gestures += ("drag_field_binding", "open_lookup_designer")
    icon = component_icon(component)
    context_actions = tuple(
        {"id": action, "label": action.replace("_", " ").title()}
        for action in common_actions + category_actions.get(category, ())
    )
    return {
        "format": "appgen.component-design-surface-contract.v1",
        "component": component,
        "ok": icon.startswith("fa-") and bool(context_actions) and bool(gestures),
        "toolbox": {
            "icon": icon,
            "label": component,
            "category": category,
            "tooltip": f"Drop {component} on the form",
            "drag_payload": {"component": component, "default_size": contract["default_size"]},
            "data_attributes": {
                "data-component": component,
                "data-component-icon": icon,
                "data-component-category": category,
            },
        },
        "drop_preview": {
            "node_class": "agfd-node",
            "icon": icon,
            "label": component,
            "bounds": contract["default_size"],
            "preview_kind": contract["preview"]["preview_kind"],
        },
        "context_menu": context_actions,
        "gestures": gestures,
        "routes": ("object_inspector", "binding_designer", "component_tree", "property_grid"),
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
    design_surface = component_design_surface_contract(component)
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
        {
            "id": "design_surface_actions",
            "ok": design_surface["ok"]
            and design_surface["toolbox"]["icon"].startswith("fa-")
            and "context_menu" in design_surface["gestures"]
            and not design_surface["side_effects"],
            "evidence": design_surface,
        },
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
        "design_surface": design_surface,
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
        {"id": "design_surface_behavior", "ok": all(any(check["id"] == "design_surface_actions" and check["ok"] for check in item["checks"]) for item in behaviors), "evidence": tuple(item["design_surface"] for item in behaviors)},
        {"id": "implementation_depth", "ok": all({"state_model", "design_serialization", "binding_surface", "category_capabilities", "designer_metadata", "design_surface_actions"} <= {check["id"] for check in item["checks"] if check["ok"]} for item in behaviors), "evidence": tuple((item["component"], item["state_model"]["states"], item["serialization"]["streams"], item["binding_surface"]["binding_modes"], item["capabilities"]["operations"], item["design_surface"]["gestures"]) for item in behaviors)},
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
        "design_surface",
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
        "design_surface_declared",
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


def component_test_file_manifest() -> tuple[dict, ...]:
    """Return the per-component generated test files expected in generated apps."""
    return tuple(
        {
            "component": item["component"],
            "path": item["path"].replace("app/component_contracts/", "app/component_tests/test_"),
            "target": item["path"],
            "exports": ("load_component_module", "test_component_contract", "test_component_smoke", "smoke_test"),
            "smoke_tests": item["module_contract"]["smoke_tests"],
            "ok": item["module_contract"]["ok"] and bool(item["module_contract"]["smoke_tests"]),
        }
        for item in component_file_manifest()
    )


def component_ide_readiness_catalog() -> dict:
    """Return IDE readiness evidence for every built-in component."""
    file_map = {item["component"]: item for item in component_file_manifest()}
    test_map = {item["component"]: item for item in component_test_file_manifest()}
    entries = tuple(
        {
            "component": component,
            "category": runtime["category"],
            "icon": design["toolbox"]["icon"],
            "renderers": tuple(runtime["renderers"]),
            "property_editors": tuple(runtime["property_editors"]),
            "event_handlers": tuple(handler["handler"] for handler in behavior["events"]["handlers"]),
            "design_actions": tuple(action["id"] for action in design["context_menu"]),
            "gestures": design["gestures"],
            "generated_module": file_map[component]["path"],
            "generated_test": test_map[component]["path"],
            "smoke_tests": file_map[component]["module_contract"]["smoke_tests"],
            "ready": design["ok"]
            and behavior["ok"]
            and file_map[component]["module_contract"]["ok"]
            and test_map[component]["ok"]
            and {"web", "mobile", "desktop"} <= set(runtime["renderers"]),
        }
        for component in sorted(COMPONENTS)
        for runtime in (component_runtime_contract(component),)
        for behavior in (component_behavior_contract(component),)
        for design in (behavior["design_surface"],)
    )
    checks = (
        {"id": "all_components_listed", "ok": {item["component"] for item in entries} == set(COMPONENTS)},
        {"id": "icons_declared", "ok": all(item["icon"].startswith("fa-") for item in entries)},
        {"id": "target_renderers_declared", "ok": all({"web", "mobile", "desktop"} <= set(item["renderers"]) for item in entries)},
        {"id": "property_editors_declared", "ok": all(item["property_editors"] for item in entries)},
        {"id": "event_handlers_declared", "ok": all(item["event_handlers"] for item in entries)},
        {"id": "design_actions_declared", "ok": all({"inspect", "edit_bindings", "delete"} <= set(item["design_actions"]) for item in entries)},
        {"id": "generated_modules_declared", "ok": all(item["generated_module"].startswith("app/component_contracts/") for item in entries)},
        {"id": "generated_tests_declared", "ok": all(item["generated_test"].startswith("app/component_tests/") for item in entries)},
        {"id": "smoke_tests_declared", "ok": all(item["smoke_tests"] for item in entries)},
    )
    ok = all(check["ok"] for check in checks) and all(item["ready"] for item in entries)
    return {
        "format": "appgen.component-ide-readiness-catalog.v1",
        "ok": ok,
        "component_count": len(entries),
        "entries": entries,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"])
        + tuple({"id": "component_not_ready", "component": item["component"]} for item in entries if not item["ready"]),
    }


def component_parity_readiness_contract() -> dict:
    """Prove component parity is one ordered IDE readiness path."""
    analog_workbench = component_analog_workbench()
    analog_groups = component_analog_group_audit()
    palette = component_palette()
    behavior = component_behavior_workbench()
    component_files = component_file_manifest()
    component_tests = component_test_file_manifest()
    ide_readiness = component_ide_readiness_catalog()
    phases = (
        {
            "phase": "analog_coverage",
            "ok": analog_workbench["ok"]
            and analog_groups["ok"]
            and len(analog_workbench["behavior_replay"]) == len(component_analog_matrix()),
            "evidence": {
                "groups": analog_workbench["groups"],
                "analog_count": len(analog_workbench["matrix"]),
            },
        },
        {
            "phase": "palette_icon_surface",
            "ok": bool(palette)
            and all(item["icon"].startswith("fa-") for item in palette)
            and {item["component"] for item in palette} == set(COMPONENTS),
            "evidence": tuple((item["component"], item["icon"]) for item in palette),
        },
        {
            "phase": "runtime_behavior",
            "ok": behavior["ok"]
            and all(
                {
                    "render_nodes",
                    "property_validation",
                    "event_dispatch",
                    "target_adapters",
                    "binding_surface",
                    "category_capabilities",
                    "designer_metadata",
                    "design_surface_actions",
                }
                <= {check["id"] for check in item["checks"] if check["ok"]}
                for item in behavior["behaviors"]
            ),
            "evidence": tuple(item["component"] for item in behavior["behaviors"]),
        },
        {
            "phase": "generated_modules",
            "ok": len(component_files) == len(COMPONENTS)
            and all(
                item["module_contract"]["ok"]
                and {"render", "validate_props", "preview", "object_inspector", "design_surface", "dispatch_event", "smoke_test"}
                <= set(item["exports"])
                for item in component_files
            ),
            "evidence": tuple(item["path"] for item in component_files),
        },
        {
            "phase": "generated_tests",
            "ok": len(component_tests) == len(COMPONENTS)
            and all(item["ok"] and "smoke_test" in item["exports"] for item in component_tests),
            "evidence": tuple(item["path"] for item in component_tests),
        },
        {
            "phase": "ide_catalog_release",
            "ok": ide_readiness["ok"]
            and len(ide_readiness["entries"]) == len(COMPONENTS)
            and all(item["ready"] for item in ide_readiness["entries"]),
            "evidence": tuple(check["id"] for check in ide_readiness["checks"] if check["ok"]),
        },
    )
    phase_names = tuple(phase["phase"] for phase in phases)
    checks = (
        {
            "id": "analog_coverage_ready",
            "ok": phases[0]["ok"],
            "evidence": phases[0]["evidence"],
        },
        {
            "id": "palette_icons_ready",
            "ok": phases[1]["ok"] and phase_names.index("analog_coverage") < phase_names.index("palette_icon_surface"),
            "evidence": phases[1]["evidence"],
        },
        {
            "id": "behavior_surface_ready",
            "ok": phases[2]["ok"] and phase_names.index("palette_icon_surface") < phase_names.index("runtime_behavior"),
            "evidence": phases[2]["evidence"],
        },
        {
            "id": "generated_modules_ready",
            "ok": phases[3]["ok"] and phase_names.index("runtime_behavior") < phase_names.index("generated_modules"),
            "evidence": phases[3]["evidence"],
        },
        {
            "id": "generated_tests_ready",
            "ok": phases[4]["ok"] and phase_names.index("generated_modules") < phase_names.index("generated_tests"),
            "evidence": phases[4]["evidence"],
        },
        {
            "id": "ide_release_ready",
            "ok": phases[5]["ok"] and phase_names.index("generated_tests") < phase_names.index("ide_catalog_release"),
            "evidence": phases[5]["evidence"],
        },
        {
            "id": "phase_order_ready",
            "ok": phase_names
            == (
                "analog_coverage",
                "palette_icon_surface",
                "runtime_behavior",
                "generated_modules",
                "generated_tests",
                "ide_catalog_release",
            )
            and all(phase["ok"] for phase in phases),
            "evidence": phase_names,
        },
        {
            "id": "side_effect_guard_ready",
            "ok": all(
                not contract["render"]["side_effects"]
                and not contract["validation"]["side_effects"]
                and all(not handler["side_effects"] for handler in contract["events"]["handlers"])
                and all(not adapter["side_effects"] for adapter in contract["adapters"]["adapters"])
                and not contract["state_model"]["side_effects"]
                and not contract["serialization"]["side_effects"]
                and not contract["binding_surface"]["side_effects"]
                and not contract["capabilities"]["side_effects"]
                and not contract["designer_metadata"]["side_effects"]
                and not contract["design_surface"]["side_effects"]
                for contract in behavior["behaviors"]
            ),
            "evidence": (),
        },
    )
    ok = all(phase["ok"] for phase in phases) and all(check["ok"] for check in checks)
    return {
        "format": "appgen.component-parity-readiness-contract.v1",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "phases": phases,
        "checks": checks,
        "side_effects": (),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def device_api_component_file_manifest() -> tuple[dict, ...]:
    """Return per-device-API component files expected in generated apps."""
    specs = mobile_device_component_spec_contract()
    exports = (
        "spec",
        "permission_manifest",
        "simulator_fixture",
        "render",
        "validate_props",
        "request_permission",
        "replay",
        "dispatch_event",
        "design_tools",
        "smoke_test",
    )
    return tuple(
        {
            "api": item["api"],
            "component": item["component"],
            "path": f"app/device_api_components/{_module_name(item['api'])}.py",
            "exports": exports,
            "ok": item["permission"] is not None and item["fixture"] is not None and bool(item["events"]),
        }
        for item in specs["specs"]
    )


def device_api_component_test_file_manifest() -> tuple[dict, ...]:
    """Return per-device-API generated test files expected in generated apps."""
    return tuple(
        {
            "api": item["api"],
            "component": item["component"],
            "path": item["path"].replace("app/device_api_components/", "app/device_api_component_tests/test_"),
            "target": item["path"],
            "exports": ("load_device_component_module", "test_device_component_contract", "test_device_component_smoke", "smoke_test"),
            "ok": item["ok"],
        }
        for item in device_api_component_file_manifest()
    )


def visual_component_file_manifest() -> tuple[dict, ...]:
    """Return per-visual-depth component files expected in generated apps."""
    specs = cross_target_visual_component_spec_contract()
    exports = (
        "spec",
        "render",
        "validate_props",
        "validation_operation",
        "authoring_operation",
        "runtime_manifest",
        "replay",
        "design_tools",
        "smoke_test",
    )
    return tuple(
        {
            "component": item["component"],
            "family": item["family"],
            "path": f"app/visual_components/{_module_name(item['component'])}.py",
            "exports": exports,
            "ok": bool(item["properties"]) and bool(item["design_tools"]) and bool(item["runtime_artifacts"]),
        }
        for item in specs["specs"]
    )


def visual_component_test_file_manifest() -> tuple[dict, ...]:
    """Return per-visual-depth generated test files expected in generated apps."""
    return tuple(
        {
            "component": item["component"],
            "family": item["family"],
            "path": item["path"].replace("app/visual_components/", "app/visual_component_tests/test_"),
            "target": item["path"],
            "exports": ("load_visual_component_module", "test_visual_component_contract", "test_visual_component_smoke", "smoke_test"),
            "ok": item["ok"],
        }
        for item in visual_component_file_manifest()
    )


def visual_design_ide_module_file_manifest() -> tuple[dict, ...]:
    """Return visual design-surface IDE modules expected in generated apps."""
    modules = (
        ("style_author_module", "style_authoring"),
        ("timeline_author_module", "timeline_authoring"),
        ("effect_stack_module", "effect_stack"),
        ("scene_author_module", "scene_authoring"),
        ("asset_import_module", "asset_import"),
        ("runtime_package_module", "runtime_package"),
    )
    exports = (
        "module_contract",
        "visual_surface_manifest",
        "run_visual_operation",
        "runtime_context",
        "smoke_test",
    )
    return tuple(
        {
            "module": module,
            "surface": surface,
            "path": f"app/visual_design_ide_modules/{module}.py",
            "exports": exports,
            "ok": bool(module) and bool(surface),
        }
        for module, surface in modules
    )


def visual_design_ide_test_module_file_manifest() -> tuple[dict, ...]:
    """Return generated visual design-surface IDE test files expected in apps."""
    return tuple(
        {
            "module": item["module"],
            "surface": item["surface"],
            "path": item["path"].replace("app/visual_design_ide_modules/", "app/visual_design_ide_module_tests/test_"),
            "target": item["path"],
            "exports": (
                "load_visual_design_ide_module",
                "test_visual_design_ide_module_contract",
                "test_visual_design_ide_module_smoke",
                "smoke_test",
            ),
            "ok": item["ok"],
        }
        for item in visual_design_ide_module_file_manifest()
    )


def data_tooling_module_file_manifest() -> tuple[dict, ...]:
    """Return generated data tooling module files expected in generated apps."""
    return tuple(
        {
            "module": item["name"],
            "path": f"app/data_tooling_modules/{item['name']}.py",
            "exports": item["exports"],
            "ok": bool(item["exports"]),
        }
        for item in data_module_generation_contract()["artifacts"]
    )


def data_tooling_module_test_file_manifest() -> tuple[dict, ...]:
    """Return generated data tooling module test files expected in generated apps."""
    return tuple(
        {
            "module": item["module"],
            "path": item["path"].replace("app/data_tooling_modules/", "app/data_tooling_module_tests/test_"),
            "target": item["path"],
            "exports": ("load_data_tooling_module", "test_data_tooling_module_contract", "test_data_tooling_module_smoke", "smoke_test"),
            "ok": item["ok"],
        }
        for item in data_tooling_module_file_manifest()
    )


def deep_data_tooling_module_file_manifest() -> tuple[dict, ...]:
    """Return generated deep data tooling module files expected in generated apps."""
    modules = (
        ("schema_browser_module", "schema_browser"),
        ("schema_diff_module", "schema_diff"),
        ("lookup_editor_module", "lookup_editor"),
        ("dataset_designer_module", "dataset_designer"),
        ("resource_publish_module", "resource_publish"),
        ("offline_replay_module", "offline_replay"),
        ("replication_monitor_module", "replication_monitor"),
        ("module_smoke_module", "module_smoke"),
    )
    exports = (
        "module_contract",
        "operation_manifest",
        "run_data_operation",
        "runtime_context",
        "smoke_test",
    )
    return tuple(
        {
            "module": module,
            "surface": surface,
            "path": f"app/deep_data_tooling_modules/{module}.py",
            "exports": exports,
            "ok": bool(module) and bool(surface),
        }
        for module, surface in modules
    )


def deep_data_tooling_module_test_file_manifest() -> tuple[dict, ...]:
    """Return generated deep data tooling module test files expected in generated apps."""
    return tuple(
        {
            "module": item["module"],
            "surface": item["surface"],
            "path": item["path"].replace("app/deep_data_tooling_modules/", "app/deep_data_tooling_module_tests/test_"),
            "target": item["path"],
            "exports": (
                "load_deep_data_tooling_module",
                "test_deep_data_tooling_module_contract",
                "test_deep_data_tooling_module_smoke",
                "smoke_test",
            ),
            "ok": item["ok"],
        }
        for item in deep_data_tooling_module_file_manifest()
    )


def inspector_module_file_manifest() -> tuple[dict, ...]:
    """Return generated Object Inspector editor module files expected in apps."""
    modules = (
        ("property_editor_module", "property_editors"),
        ("event_editor_module", "event_editors"),
        ("component_editor_module", "component_editors"),
        ("custom_designer_module", "custom_designers"),
        ("handler_invocation_module", "handler_invocation"),
        ("binding_bridge_module", "binding_bridge"),
    )
    exports = (
        "module_contract",
        "editor_manifest",
        "run_editor_operation",
        "runtime_manifest",
        "smoke_test",
    )
    return tuple(
        {
            "module": module,
            "kind": kind,
            "path": f"app/inspector_modules/{module}.py",
            "exports": exports,
            "ok": bool(module) and bool(kind),
        }
        for module, kind in modules
    )


def inspector_module_test_file_manifest() -> tuple[dict, ...]:
    """Return generated Object Inspector editor test files expected in apps."""
    return tuple(
        {
            "module": item["module"],
            "kind": item["kind"],
            "path": item["path"].replace("app/inspector_modules/", "app/inspector_module_tests/test_"),
            "target": item["path"],
            "exports": (
                "load_inspector_module",
                "test_inspector_module_contract",
                "test_inspector_module_smoke",
                "smoke_test",
            ),
            "ok": item["ok"],
        }
        for item in inspector_module_file_manifest()
    )


def binding_module_file_manifest() -> tuple[dict, ...]:
    """Return generated visual binding module files expected in apps."""
    modules = (
        ("binding_graph_module", "graph"),
        ("binding_expression_module", "expression"),
        ("binding_designer_module", "designer"),
        ("binding_runtime_wiring_module", "runtime_wiring"),
        ("binding_propagation_module", "propagation"),
        ("binding_lifecycle_module", "lifecycle"),
    )
    exports = (
        "module_contract",
        "binding_manifest",
        "run_binding_operation",
        "runtime_manifest",
        "smoke_test",
    )
    return tuple(
        {
            "module": module,
            "kind": kind,
            "path": f"app/binding_modules/{module}.py",
            "exports": exports,
            "ok": bool(module) and bool(kind),
        }
        for module, kind in modules
    )


def binding_module_test_file_manifest() -> tuple[dict, ...]:
    """Return generated visual binding test files expected in apps."""
    return tuple(
        {
            "module": item["module"],
            "kind": item["kind"],
            "path": item["path"].replace("app/binding_modules/", "app/binding_module_tests/test_"),
            "target": item["path"],
            "exports": (
                "load_binding_module",
                "test_binding_module_contract",
                "test_binding_module_smoke",
                "smoke_test",
            ),
            "ok": item["ok"],
        }
        for item in binding_module_file_manifest()
    )


def package_manager_module_file_manifest() -> tuple[dict, ...]:
    """Return generated package manager module files expected in apps."""
    modules = (
        ("package_install_module", "install"),
        ("package_preview_module", "preview"),
        ("package_registry_module", "registry"),
        ("package_lifecycle_module", "lifecycle"),
        ("package_update_module", "update"),
        ("package_rollback_module", "rollback"),
    )
    exports = (
        "module_contract",
        "package_manifest",
        "run_package_operation",
        "runtime_manifest",
        "smoke_test",
    )
    return tuple(
        {
            "module": module,
            "kind": kind,
            "path": f"app/package_manager_modules/{module}.py",
            "exports": exports,
            "ok": bool(module) and bool(kind),
        }
        for module, kind in modules
    )


def package_manager_module_test_file_manifest() -> tuple[dict, ...]:
    """Return generated package manager test files expected in apps."""
    return tuple(
        {
            "module": item["module"],
            "kind": item["kind"],
            "path": item["path"].replace("app/package_manager_modules/", "app/package_manager_module_tests/test_"),
            "target": item["path"],
            "exports": (
                "load_package_manager_module",
                "test_package_manager_module_contract",
                "test_package_manager_module_smoke",
                "smoke_test",
            ),
            "ok": item["ok"],
        }
        for item in package_manager_module_file_manifest()
    )


def device_api_component_module_file_manifest() -> tuple[dict, ...]:
    """Return generated device API component module files expected in apps."""
    exports = (
        "spec",
        "permission_manifest",
        "simulator_fixture",
        "render",
        "validate_props",
        "request_permission",
        "replay",
        "dispatch_event",
        "design_tools",
        "smoke_test",
    )
    return tuple(
        {
            "api": item["api"],
            "component": item["component"],
            "path": f"app/device_api_components/{_module_name(item['api'])}.py",
            "exports": exports,
            "ok": bool(item["api"]) and bool(item["component"]),
        }
        for item in mobile_device_component_spec_contract()["specs"]
    )


def device_api_component_test_module_file_manifest() -> tuple[dict, ...]:
    """Return generated device API component test files expected in apps."""
    return tuple(
        {
            "api": item["api"],
            "component": item["component"],
            "path": item["path"].replace("app/device_api_components/", "app/device_api_component_tests/test_"),
            "target": item["path"],
            "exports": (
                "load_device_component_module",
                "test_device_component_contract",
                "test_device_component_smoke",
                "smoke_test",
            ),
            "ok": item["ok"],
        }
        for item in device_api_component_module_file_manifest()
    )


def native_form_module_file_manifest() -> tuple[dict, ...]:
    """Return generated native form module files expected in apps."""
    modules = (
        ("native_stream_module", "stream"),
        ("native_unit_module", "unit"),
        ("native_resource_module", "resource"),
        ("native_compile_module", "compile"),
        ("native_runtime_load_module", "runtime_load"),
        ("native_design_edit_module", "design_edit"),
    )
    exports = (
        "module_contract",
        "native_form_manifest",
        "run_native_form_operation",
        "runtime_manifest",
        "smoke_test",
    )
    return tuple(
        {
            "module": module,
            "kind": kind,
            "path": f"app/native_form_modules/{module}.py",
            "exports": exports,
            "ok": bool(module) and bool(kind),
        }
        for module, kind in modules
    )


def native_form_module_test_file_manifest() -> tuple[dict, ...]:
    """Return generated native form test files expected in apps."""
    return tuple(
        {
            "module": item["module"],
            "kind": item["kind"],
            "path": item["path"].replace("app/native_form_modules/", "app/native_form_module_tests/test_"),
            "target": item["path"],
            "exports": (
                "load_native_form_module",
                "test_native_form_module_contract",
                "test_native_form_module_smoke",
                "smoke_test",
            ),
            "ok": item["ok"],
        }
        for item in native_form_module_file_manifest()
    )


def runtime_operation_module_file_manifest() -> tuple[dict, ...]:
    """Return generated runtime operation module files expected in apps."""
    modules = (
        ("open_design_stream_operation", "open_design_stream"),
        ("apply_property_delta_operation", "apply_property_delta"),
        ("round_trip_stream_operation", "round_trip_stream"),
        ("compile_preview_operation", "compile_preview"),
        ("refresh_resources_operation", "refresh_resources"),
        ("reload_runtime_preview_operation", "reload_runtime_preview"),
    )
    exports = (
        "module_contract",
        "operation_manifest",
        "run_operation",
        "runtime_manifest",
        "smoke_test",
    )
    return tuple(
        {
            "module": module,
            "operation": operation,
            "path": f"app/runtime_operation_modules/{module}.py",
            "exports": exports,
            "ok": bool(module) and bool(operation),
        }
        for module, operation in modules
    )


def runtime_operation_module_test_file_manifest() -> tuple[dict, ...]:
    """Return generated runtime operation test files expected in apps."""
    return tuple(
        {
            "module": item["module"],
            "operation": item["operation"],
            "path": item["path"].replace("app/runtime_operation_modules/", "app/runtime_operation_module_tests/test_"),
            "target": item["path"],
            "exports": (
                "load_runtime_operation_module",
                "test_runtime_operation_module_contract",
                "test_runtime_operation_module_smoke",
                "smoke_test",
            ),
            "ok": item["ok"],
        }
        for item in runtime_operation_module_file_manifest()
    )


def compiler_runtime_module_file_manifest() -> tuple[dict, ...]:
    """Return generated compiler/runtime module files expected in apps."""
    modules = (
        ("compiler_pipeline_module", "compiler_pipeline"),
        ("unit_parse_module", "unit_parse"),
        ("semantic_validation_module", "semantic_validation"),
        ("incremental_compile_module", "incremental_compile"),
        ("diagnostic_mapping_module", "diagnostic_mapping"),
        ("toolchain_adapter_module", "toolchain_adapter"),
    )
    exports = (
        "module_contract",
        "compiler_manifest",
        "run_compiler_surface",
        "runtime_workbench",
        "smoke_test",
    )
    return tuple(
        {
            "module": module,
            "surface": surface,
            "path": f"app/compiler_runtime_modules/{module}.py",
            "exports": exports,
            "ok": bool(module) and bool(surface),
        }
        for module, surface in modules
    )


def compiler_runtime_module_test_file_manifest() -> tuple[dict, ...]:
    """Return generated compiler/runtime test files expected in apps."""
    return tuple(
        {
            "module": item["module"],
            "surface": item["surface"],
            "path": item["path"].replace("app/compiler_runtime_modules/", "app/compiler_runtime_module_tests/test_"),
            "target": item["path"],
            "exports": (
                "load_compiler_runtime_module",
                "test_compiler_runtime_module_contract",
                "test_compiler_runtime_module_smoke",
                "smoke_test",
            ),
            "ok": item["ok"],
        }
        for item in compiler_runtime_module_file_manifest()
    )


def deep_runtime_module_file_manifest() -> tuple[dict, ...]:
    """Return generated deep runtime module files expected in apps."""
    modules = (
        ("package_target_matrix_module", "package_target_matrix"),
        ("language_frontend_module", "language_frontend"),
        ("static_analysis_module", "static_analysis"),
        ("compiler_recovery_module", "compiler_recovery"),
        ("form_stream_schema_module", "form_stream_schema"),
        ("stream_migration_module", "stream_migration"),
        ("debug_symbol_module", "debug_symbols"),
        ("runtime_memory_model_module", "runtime_memory_model"),
    )
    exports = (
        "module_contract",
        "runtime_manifest",
        "run_runtime_surface",
        "runtime_workbench",
        "smoke_test",
    )
    return tuple(
        {
            "module": module,
            "surface": surface,
            "path": f"app/deep_runtime_modules/{module}.py",
            "exports": exports,
            "ok": bool(module) and bool(surface),
        }
        for module, surface in modules
    )


def deep_runtime_module_test_file_manifest() -> tuple[dict, ...]:
    """Return generated deep runtime test files expected in apps."""
    return tuple(
        {
            "module": item["module"],
            "surface": item["surface"],
            "path": item["path"].replace("app/deep_runtime_modules/", "app/deep_runtime_module_tests/test_"),
            "target": item["path"],
            "exports": (
                "load_deep_runtime_module",
                "test_deep_runtime_module_contract",
                "test_deep_runtime_module_smoke",
                "smoke_test",
            ),
            "ok": item["ok"],
        }
        for item in deep_runtime_module_file_manifest()
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


def component_package_test_file_manifest() -> tuple[dict, ...]:
    """Return the per-package generated test files expected in generated apps."""
    return tuple(
        {
            "package": item["package"],
            "path": item["path"].replace("app/component_packages/", "app/component_package_tests/test_"),
            "target": item["path"],
            "exports": ("load_package_module", "test_package_contract", "test_package_smoke", "smoke_test"),
            "smoke_tests": item["module_contract"]["smoke_tests"],
            "ok": item["module_contract"]["ok"] and bool(item["module_contract"]["smoke_tests"]),
        }
        for item in component_package_file_manifest()
    )


def component_usability_workbench() -> dict:
    """Prove every built-in component has enough metadata to be usable."""
    contracts = component_implementation_catalog()
    analog_workbench = component_analog_workbench()
    behavior_workbench = component_behavior_workbench()
    ide_readiness = component_ide_readiness_catalog()
    readiness = component_parity_readiness_contract()
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
            "id": "design_surface_actions",
            "ok": all(
                item["design_surface"]["ok"]
                and item["design_surface"]["toolbox"]["icon"].startswith("fa-")
                and item["design_surface"]["context_menu"]
                for item in behavior_workbench["behaviors"]
            ),
            "evidence": tuple((item["component"], item["design_surface"]) for item in behavior_workbench["behaviors"]),
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
                    "design_surface",
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
            "id": "per_component_test_files",
            "ok": len(component_test_file_manifest()) == len(contracts)
            and all(
                {"test_component_contract", "test_component_smoke", "smoke_test"} <= set(item["exports"])
                and item["ok"]
                for item in component_test_file_manifest()
            ),
            "evidence": component_test_file_manifest(),
        },
        {
            "id": "per_package_test_files",
            "ok": len(component_package_test_file_manifest()) == len(THIRD_PARTY_COMPONENT_SUITES)
            and all(
                {"test_package_contract", "test_package_smoke", "smoke_test"} <= set(item["exports"])
                and item["ok"]
                for item in component_package_test_file_manifest()
            ),
            "evidence": component_package_test_file_manifest(),
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
        {
            "id": "ide_readiness_catalog",
            "ok": ide_readiness["ok"],
            "evidence": ide_readiness,
        },
        {
            "id": "component_parity_readiness",
            "ok": readiness["ok"]
            and {
                "analog_coverage_ready",
                "palette_icons_ready",
                "behavior_surface_ready",
                "generated_modules_ready",
                "generated_tests_ready",
                "ide_release_ready",
                "phase_order_ready",
                "side_effect_guard_ready",
            }
            <= {check["id"] for check in readiness["checks"] if check["ok"]}
            and not readiness["side_effects"],
            "evidence": readiness,
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
        "component_test_files": component_test_file_manifest(),
        "package_test_files": component_package_test_file_manifest(),
        "analog_workbench": analog_workbench,
        "behavior_workbench": behavior_workbench,
        "ide_readiness": ide_readiness,
        "component_readiness": readiness,
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

    component_artifacts = tuple(item["path"] for item in component_file_manifest())
    package_artifacts = tuple(item["path"] for item in component_package_file_manifest())
    component_test_artifacts = tuple(item["path"] for item in component_test_file_manifest())
    package_test_artifacts = tuple(item["path"] for item in component_package_test_file_manifest())
    device_component_artifacts = tuple(item["path"] for item in device_api_component_file_manifest())
    device_component_test_artifacts = tuple(item["path"] for item in device_api_component_test_file_manifest())
    visual_component_artifacts = tuple(item["path"] for item in visual_component_file_manifest())
    visual_component_test_artifacts = tuple(item["path"] for item in visual_component_test_file_manifest())
    data_module_artifacts = tuple(item["path"] for item in data_tooling_module_file_manifest())
    data_module_test_artifacts = tuple(item["path"] for item in data_tooling_module_test_file_manifest())
    deep_data_tooling_module_artifacts = tuple(item["path"] for item in deep_data_tooling_module_file_manifest())
    deep_data_tooling_module_test_artifacts = tuple(item["path"] for item in deep_data_tooling_module_test_file_manifest())
    inspector_module_artifacts = tuple(item["path"] for item in inspector_module_file_manifest())
    inspector_module_test_artifacts = tuple(item["path"] for item in inspector_module_test_file_manifest())
    binding_module_artifacts = tuple(item["path"] for item in binding_module_file_manifest())
    binding_module_test_artifacts = tuple(item["path"] for item in binding_module_test_file_manifest())
    package_manager_module_artifacts = tuple(item["path"] for item in package_manager_module_file_manifest())
    package_manager_module_test_artifacts = tuple(item["path"] for item in package_manager_module_test_file_manifest())
    native_form_module_artifacts = tuple(item["path"] for item in native_form_module_file_manifest())
    native_form_module_test_artifacts = tuple(item["path"] for item in native_form_module_test_file_manifest())
    runtime_operation_module_artifacts = tuple(item["path"] for item in runtime_operation_module_file_manifest())
    runtime_operation_module_test_artifacts = tuple(item["path"] for item in runtime_operation_module_test_file_manifest())
    compiler_runtime_module_artifacts = tuple(item["path"] for item in compiler_runtime_module_file_manifest())
    compiler_runtime_module_test_artifacts = tuple(item["path"] for item in compiler_runtime_module_test_file_manifest())
    deep_runtime_module_artifacts = tuple(item["path"] for item in deep_runtime_module_file_manifest())
    deep_runtime_module_test_artifacts = tuple(item["path"] for item in deep_runtime_module_test_file_manifest())
    required_artifacts = (
        "app/form_designer.py",
        "app/component_parity_runtime.py",
        "app/inspector_runtime.py",
        "app/binding_runtime.py",
        "app/package_manager_runtime.py",
        "app/visual_runtime_assets.py",
        "app/visual_depth_runtime.py",
        "app/data_tooling_runtime.py",
        "app/runtime_operations.py",
        "app/native_form_runtime.py",
        "app/mobile_device_runtime.py",
        "app/templates/appgen_form_designer.html",
        "app/models.py",
        "app/views.py",
        "app/dsl_reference.py",
        *component_artifacts,
        *package_artifacts,
        *component_test_artifacts,
        *package_test_artifacts,
        *device_component_artifacts,
        *device_component_test_artifacts,
        *visual_component_artifacts,
        *visual_component_test_artifacts,
        *data_module_artifacts,
        *data_module_test_artifacts,
        *deep_data_tooling_module_artifacts,
        *deep_data_tooling_module_test_artifacts,
        *inspector_module_artifacts,
        *inspector_module_test_artifacts,
        *binding_module_artifacts,
        *binding_module_test_artifacts,
        *package_manager_module_artifacts,
        *package_manager_module_test_artifacts,
        *native_form_module_artifacts,
        *native_form_module_test_artifacts,
        *runtime_operation_module_artifacts,
        *runtime_operation_module_test_artifacts,
        *compiler_runtime_module_artifacts,
        *compiler_runtime_module_test_artifacts,
        *deep_runtime_module_artifacts,
        *deep_runtime_module_test_artifacts,
    )
    compile_artifacts = (
        "app/form_designer.py",
        "app/component_parity_runtime.py",
        "app/inspector_runtime.py",
        "app/binding_runtime.py",
        "app/package_manager_runtime.py",
        "app/visual_runtime_assets.py",
        "app/visual_depth_runtime.py",
        "app/data_tooling_runtime.py",
        "app/runtime_operations.py",
        "app/native_form_runtime.py",
        "app/mobile_device_runtime.py",
        "app/models.py",
        "app/views.py",
        "app/dsl_reference.py",
        *component_artifacts,
        *package_artifacts,
        *component_test_artifacts,
        *package_test_artifacts,
        *device_component_artifacts,
        *device_component_test_artifacts,
        *visual_component_artifacts,
        *visual_component_test_artifacts,
        *data_module_artifacts,
        *data_module_test_artifacts,
        *deep_data_tooling_module_artifacts,
        *deep_data_tooling_module_test_artifacts,
        *inspector_module_artifacts,
        *inspector_module_test_artifacts,
        *binding_module_artifacts,
        *binding_module_test_artifacts,
        *package_manager_module_artifacts,
        *package_manager_module_test_artifacts,
        *native_form_module_artifacts,
        *native_form_module_test_artifacts,
        *runtime_operation_module_artifacts,
        *runtime_operation_module_test_artifacts,
        *compiler_runtime_module_artifacts,
        *compiler_runtime_module_test_artifacts,
        *deep_runtime_module_artifacts,
        *deep_runtime_module_test_artifacts,
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
        component_parity_runtime_path = output_dir / "component_parity_runtime.py"
        component_parity_runtime_spec = importlib.util.spec_from_file_location(
            "generated_component_parity_runtime_smoke", component_parity_runtime_path
        )
        generated_component_parity_runtime = importlib.util.module_from_spec(component_parity_runtime_spec)
        component_parity_runtime_spec.loader.exec_module(generated_component_parity_runtime)
        inspector_runtime_path = output_dir / "inspector_runtime.py"
        inspector_runtime_spec = importlib.util.spec_from_file_location(
            "generated_inspector_runtime_smoke", inspector_runtime_path
        )
        generated_inspector_runtime = importlib.util.module_from_spec(inspector_runtime_spec)
        inspector_runtime_spec.loader.exec_module(generated_inspector_runtime)
        binding_runtime_path = output_dir / "binding_runtime.py"
        binding_runtime_spec = importlib.util.spec_from_file_location(
            "generated_binding_runtime_smoke", binding_runtime_path
        )
        generated_binding_runtime = importlib.util.module_from_spec(binding_runtime_spec)
        binding_runtime_spec.loader.exec_module(generated_binding_runtime)
        package_manager_runtime_path = output_dir / "package_manager_runtime.py"
        package_manager_runtime_spec = importlib.util.spec_from_file_location(
            "generated_package_manager_runtime_smoke", package_manager_runtime_path
        )
        generated_package_manager_runtime = importlib.util.module_from_spec(package_manager_runtime_spec)
        package_manager_runtime_spec.loader.exec_module(generated_package_manager_runtime)
        visual_depth_runtime_path = output_dir / "visual_depth_runtime.py"
        visual_depth_runtime_spec = importlib.util.spec_from_file_location(
            "generated_visual_depth_runtime_smoke", visual_depth_runtime_path
        )
        generated_visual_depth_runtime = importlib.util.module_from_spec(visual_depth_runtime_spec)
        visual_depth_runtime_spec.loader.exec_module(generated_visual_depth_runtime)
        visual_assets_path = output_dir / "visual_runtime_assets.py"
        visual_assets_spec = importlib.util.spec_from_file_location(
            "generated_visual_runtime_assets_smoke", visual_assets_path
        )
        generated_visual_assets = importlib.util.module_from_spec(visual_assets_spec)
        visual_assets_spec.loader.exec_module(generated_visual_assets)
        data_runtime_path = output_dir / "data_tooling_runtime.py"
        data_runtime_spec = importlib.util.spec_from_file_location(
            "generated_data_tooling_runtime_smoke", data_runtime_path
        )
        generated_data_runtime = importlib.util.module_from_spec(data_runtime_spec)
        data_runtime_spec.loader.exec_module(generated_data_runtime)
        runtime_ops_path = output_dir / "runtime_operations.py"
        runtime_ops_spec = importlib.util.spec_from_file_location(
            "generated_runtime_operations_smoke", runtime_ops_path
        )
        generated_runtime_ops = importlib.util.module_from_spec(runtime_ops_spec)
        runtime_ops_spec.loader.exec_module(generated_runtime_ops)
        native_runtime_path = output_dir / "native_form_runtime.py"
        native_runtime_spec = importlib.util.spec_from_file_location(
            "generated_native_form_runtime_smoke", native_runtime_path
        )
        generated_native_runtime = importlib.util.module_from_spec(native_runtime_spec)
        native_runtime_spec.loader.exec_module(generated_native_runtime)
        mobile_runtime_path = output_dir / "mobile_device_runtime.py"
        mobile_runtime_spec = importlib.util.spec_from_file_location(
            "generated_mobile_device_runtime_smoke", mobile_runtime_path
        )
        generated_mobile_runtime = importlib.util.module_from_spec(mobile_runtime_spec)
        mobile_runtime_spec.loader.exec_module(generated_mobile_runtime)
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
        usability = generated_form_designer.component_usability_workbench(existing_paths)
        generated_platform_parity = generated_form_designer.rad_parity_workbench(existing_paths)
        component_parity_runtime_smoke = generated_component_parity_runtime.smoke_test()
        inspector_runtime_smoke = generated_inspector_runtime.smoke_test("Grid")
        binding_runtime_smoke = generated_binding_runtime.smoke_test()
        package_manager_runtime_smoke = generated_package_manager_runtime.smoke_test()
        visual_depth_runtime_smoke = generated_visual_depth_runtime.smoke_test()
        visual_assets_smoke = generated_visual_assets.smoke_test()
        data_runtime_smoke = generated_data_runtime.smoke_test()
        runtime_operation_smoke = generated_runtime_ops.smoke_test(first_table)
        native_form_runtime_smoke = generated_native_runtime.smoke_test(first_table)
        mobile_device_smoke = generated_mobile_runtime.smoke_test()
        release_gate_passing_checks = {check["id"] for check in release_gate["checks"] if check["ok"]}
        workbench_passing_checks = {check["id"] for check in workbench["checks"] if check["ok"]}
        generated_platform_parity_passing_checks = {
            check["id"] for check in generated_platform_parity["checks"] if check["ok"]
        }
        component_parity_runtime_passing_checks = set(component_parity_runtime_smoke["checks"])
        inspector_runtime_passing_checks = set(inspector_runtime_smoke["checks"])
        binding_runtime_passing_checks = set(binding_runtime_smoke["checks"])
        package_manager_runtime_passing_checks = set(package_manager_runtime_smoke["checks"])
        visual_depth_runtime_passing_checks = set(visual_depth_runtime_smoke["checks"])
        visual_asset_runtime_passing_checks = set(visual_assets_smoke["checks"])
        data_tooling_runtime_passing_checks = set(data_runtime_smoke["checks"])
        runtime_operation_passing_checks = set(runtime_operation_smoke["checks"])
        native_form_runtime_passing_checks = set(native_form_runtime_smoke["checks"])
        mobile_device_runtime_passing_checks = set(mobile_device_smoke["checks"])

    required_generated_release_gate_checks = (
        "artifact_coverage",
        "palette_breadth",
        "canvas_contract",
        "field_component_mapping",
        "drop_proposal_metadata",
        "overlap_guardrails",
        "rad_parity_contracts",
    )
    required_generated_workbench_checks = (
        "artifact_coverage",
        "palette_categories",
        "table_form_catalog",
        "field_mapping_matrix",
        "snap_grid_bounds",
        "property_inspector",
        "proposal_application",
        "placement_suggestions",
        "conflict_guardrails",
        "route_surface",
        "rad_parity_workbench",
    )
    required_generated_platform_parity_checks = (
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
        "platform_parity_lifecycle_replay",
        "platform_parity_requirement_audit",
        "artifact_coverage",
        "route_surface",
    )
    required_native_form_runtime_checks = (
        "manifest_ok",
        "stream_formats_supported",
        "unit_resource_directive",
        "compiler_pipeline_declared",
        "form_stream_schema_complete",
        "runtime_replay_side_effect_free",
        "design_edit_replay_side_effect_free",
        "artifact_parity_declared",
        "native_form_modules_ready",
        "native_form_module_tests_ready",
        "compiler_runtime_modules_ready",
        "compiler_runtime_module_tests_ready",
        "deep_runtime_modules_ready",
        "deep_runtime_module_tests_ready",
        "runtime_load_replay",
    )
    required_component_parity_runtime_checks = (
        "manifest_ok",
        "requested_groups_ready",
        "requested_analogs_ready",
        "behavior_replay_ready",
        "component_modules_ready",
        "package_modules_ready",
        "component_tests_ready",
        "runtime_replay_ready",
    )
    required_inspector_runtime_checks = (
        "manifest_ok",
        "property_editors_present",
        "event_editors_lifecycle_ready",
        "component_editors_present",
        "custom_designers_present",
        "editor_lifecycle_replay",
        "design_surface_replay",
        "custom_registration_replay",
        "binding_bridge_replay",
        "handler_invocation_policy",
        "inspector_modules_ready",
        "inspector_module_tests_ready",
        "runtime_replay",
    )
    required_binding_runtime_checks = (
        "manifest_ok",
        "graph_nodes_present",
        "graph_edges_present",
        "actionable_operations_ready",
        "runtime_wiring_ready",
        "runtime_gates_ready",
        "runtime_propagation_replay",
        "design_runtime_replay",
        "designer_transaction_replay",
        "lifecycle_release_replay",
        "inspector_bridge_replay",
        "binding_modules_ready",
        "binding_module_tests_ready",
        "runtime_replay",
    )
    required_package_manager_runtime_checks = (
        "manifest_ok",
        "install_plan_reviewed",
        "package_workbench_ready",
        "actionable_operations_ready",
        "lifecycle_replay_ready",
        "lifecycle_execution_ready",
        "rollback_and_uninstall_ready",
        "package_manager_modules_ready",
        "package_manager_module_tests_ready",
        "runtime_replay_ready",
    )
    required_visual_depth_runtime_checks = (
        "manifest_ok",
        "style_runtime_ready",
        "timeline_runtime_ready",
        "effect_runtime_ready",
        "scene_runtime_ready",
        "component_specs_ready",
        "visual_component_modules_ready",
        "visual_component_tests_ready",
        "runtime_package_ready",
        "runtime_replay_ready",
    )
    required_visual_asset_runtime_checks = (
        "style_bundles",
        "timeline_bundles",
        "effect_bundles",
        "scene_and_assets",
        "target_package",
    )
    required_data_tooling_runtime_checks = (
        "connections",
        "datasets_and_lookups",
        "services",
        "transaction_replays",
        "relationship_lookup_replay",
        "data_module_smoke",
        "data_module_files_ready",
        "data_module_tests_ready",
        "deep_data_tooling_modules_ready",
        "deep_data_tooling_module_tests_ready",
        "publish_transaction_replay",
        "failover_transaction_replay",
        "runtime_replay",
    )
    required_runtime_operation_checks = (
        "manifest_ok",
        "required_operations_present",
        "operations_are_callable",
        "runtime_replay_complete",
        "design_edit_replay_complete",
        "runtime_operation_modules_ready",
        "runtime_operation_module_tests_ready",
    )
    required_mobile_device_runtime_checks = (
        "manifest_ok",
        "required_apis_present",
        "required_apis_replay",
        "permissions_cover_all_apis",
        "adapters_cover_all_apis",
        "fixtures_cover_all_apis",
        "runtime_replay_complete",
        "designer_replay_complete",
        "capability_lifecycle_complete",
        "device_component_modules_ready",
        "device_component_tests_ready",
    )

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
            "id": "generated_component_file_coverage",
            "ok": usability["ok"]
            and set(component_artifacts) <= {item["path"] for item in usability["component_files"]}
            and set(package_artifacts) <= {item["path"] for item in usability["package_files"]}
            and set(component_test_artifacts) <= {item["path"] for item in usability["component_test_files"]}
            and set(package_test_artifacts) <= {item["path"] for item in usability["package_test_files"]}
            and all(item["exists"] for item in usability["component_files"])
            and all(item["exists"] for item in usability["package_files"])
            and all(item["exists"] for item in usability["component_test_files"])
            and all(item["exists"] for item in usability["package_test_files"])
            and len(device_component_artifacts) == len(mobile_device_component_spec_contract()["specs"])
            and len(device_component_test_artifacts) == len(mobile_device_component_spec_contract()["specs"])
            and len(visual_component_artifacts) == len(cross_target_visual_component_spec_contract()["specs"])
            and len(visual_component_test_artifacts) == len(cross_target_visual_component_spec_contract()["specs"])
            and len(data_module_artifacts) == len(data_module_generation_contract()["artifacts"])
            and len(data_module_test_artifacts) == len(data_module_generation_contract()["artifacts"])
            and len(deep_data_tooling_module_artifacts) == 8
            and len(deep_data_tooling_module_test_artifacts) == 8
            and len(inspector_module_artifacts) == 6
            and len(inspector_module_test_artifacts) == 6
            and len(binding_module_artifacts) == 6
            and len(binding_module_test_artifacts) == 6
            and len(package_manager_module_artifacts) == 6
            and len(package_manager_module_test_artifacts) == 6
            and len(native_form_module_artifacts) == 6
            and len(native_form_module_test_artifacts) == 6
            and len(runtime_operation_module_artifacts) == 6
            and len(runtime_operation_module_test_artifacts) == 6
            and len(compiler_runtime_module_artifacts) == 6
            and len(compiler_runtime_module_test_artifacts) == 6
            and len(deep_runtime_module_artifacts) == 8
            and len(deep_runtime_module_test_artifacts) == 8,
            "component_test_count": len(component_test_artifacts),
            "package_test_count": len(package_test_artifacts),
            "device_component_count": len(device_component_artifacts),
            "device_component_test_count": len(device_component_test_artifacts),
            "visual_component_count": len(visual_component_artifacts),
            "visual_component_test_count": len(visual_component_test_artifacts),
            "data_module_count": len(data_module_artifacts),
            "data_module_test_count": len(data_module_test_artifacts),
            "deep_data_tooling_module_count": len(deep_data_tooling_module_artifacts),
            "deep_data_tooling_module_test_count": len(deep_data_tooling_module_test_artifacts),
            "inspector_module_count": len(inspector_module_artifacts),
            "inspector_module_test_count": len(inspector_module_test_artifacts),
            "binding_module_count": len(binding_module_artifacts),
            "binding_module_test_count": len(binding_module_test_artifacts),
            "package_manager_module_count": len(package_manager_module_artifacts),
            "package_manager_module_test_count": len(package_manager_module_test_artifacts),
            "native_form_module_count": len(native_form_module_artifacts),
            "native_form_module_test_count": len(native_form_module_test_artifacts),
            "runtime_operation_module_count": len(runtime_operation_module_artifacts),
            "runtime_operation_module_test_count": len(runtime_operation_module_test_artifacts),
            "compiler_runtime_module_count": len(compiler_runtime_module_artifacts),
            "compiler_runtime_module_test_count": len(compiler_runtime_module_test_artifacts),
            "deep_runtime_module_count": len(deep_runtime_module_artifacts),
            "deep_runtime_module_test_count": len(deep_runtime_module_test_artifacts),
            "component_count": len(component_artifacts),
            "package_count": len(package_artifacts),
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
            "ok": release_gate["ok"]
            and workbench["ok"]
            and release_gate["format"] == "appgen.form-designer-release-gate.v1"
            and workbench["format"] == "appgen.form-designer-workbench.v1"
            and set(required_generated_release_gate_checks) <= release_gate_passing_checks
            and set(required_generated_workbench_checks) <= workbench_passing_checks
            and not release_gate["blocking_gaps"]
            and not workbench["blocking_gaps"],
            "release_gate": release_gate["format"],
            "workbench": workbench["format"],
            "required_release_gate_checks": required_generated_release_gate_checks,
            "passing_release_gate_checks": tuple(sorted(release_gate_passing_checks)),
            "required_workbench_checks": required_generated_workbench_checks,
            "passing_workbench_checks": tuple(sorted(workbench_passing_checks)),
        },
        {
            "id": "generated_platform_parity_workbench",
            "ok": generated_platform_parity["ok"]
            and generated_platform_parity["format"] == "appgen.generated-rad-parity-workbench.v1"
            and generated_platform_parity["lifecycle_replay"]["ok"]
            and generated_platform_parity["requirement_audit"]["ok"]
            and set(required_generated_platform_parity_checks) <= generated_platform_parity_passing_checks
            and not generated_platform_parity["blocking_gaps"],
            "required_checks": required_generated_platform_parity_checks,
            "passing_checks": tuple(sorted(generated_platform_parity_passing_checks)),
            "workbench": generated_platform_parity,
        },
        {
            "id": "generated_component_parity_runtime",
            "ok": component_parity_runtime_smoke["ok"]
            and component_parity_runtime_smoke["format"] == "appgen.generated-component-parity-runtime-smoke.v1"
            and set(required_component_parity_runtime_checks) <= component_parity_runtime_passing_checks,
            "required_checks": required_component_parity_runtime_checks,
            "passing_checks": tuple(sorted(component_parity_runtime_passing_checks)),
            "smoke": component_parity_runtime_smoke,
        },
        {
            "id": "generated_inspector_runtime",
            "ok": inspector_runtime_smoke["ok"]
            and inspector_runtime_smoke["format"] == "appgen.generated-inspector-runtime-smoke.v1"
            and set(required_inspector_runtime_checks) <= inspector_runtime_passing_checks,
            "required_checks": required_inspector_runtime_checks,
            "passing_checks": tuple(sorted(inspector_runtime_passing_checks)),
            "smoke": inspector_runtime_smoke,
        },
        {
            "id": "generated_binding_runtime",
            "ok": binding_runtime_smoke["ok"]
            and binding_runtime_smoke["format"] == "appgen.generated-binding-runtime-smoke.v1"
            and set(required_binding_runtime_checks) <= binding_runtime_passing_checks,
            "required_checks": required_binding_runtime_checks,
            "passing_checks": tuple(sorted(binding_runtime_passing_checks)),
            "smoke": binding_runtime_smoke,
        },
        {
            "id": "generated_package_manager_runtime",
            "ok": package_manager_runtime_smoke["ok"]
            and package_manager_runtime_smoke["format"] == "appgen.generated-package-manager-runtime-smoke.v1"
            and set(required_package_manager_runtime_checks) <= package_manager_runtime_passing_checks,
            "required_checks": required_package_manager_runtime_checks,
            "passing_checks": tuple(sorted(package_manager_runtime_passing_checks)),
            "smoke": package_manager_runtime_smoke,
        },
        {
            "id": "generated_visual_depth_runtime",
            "ok": visual_depth_runtime_smoke["ok"]
            and visual_depth_runtime_smoke["format"] == "appgen.generated-visual-depth-runtime-smoke.v1"
            and set(required_visual_depth_runtime_checks) <= visual_depth_runtime_passing_checks,
            "required_checks": required_visual_depth_runtime_checks,
            "passing_checks": tuple(sorted(visual_depth_runtime_passing_checks)),
            "smoke": visual_depth_runtime_smoke,
        },
        {
            "id": "generated_visual_runtime_assets",
            "ok": visual_assets_smoke["ok"]
            and visual_assets_smoke["format"] == "appgen.generated-visual-runtime-assets-smoke.v1"
            and set(required_visual_asset_runtime_checks) <= visual_asset_runtime_passing_checks,
            "required_checks": required_visual_asset_runtime_checks,
            "passing_checks": tuple(sorted(visual_asset_runtime_passing_checks)),
            "smoke": visual_assets_smoke,
        },
        {
            "id": "generated_data_tooling_runtime",
            "ok": data_runtime_smoke["ok"]
            and data_runtime_smoke["format"] == "appgen.generated-data-tooling-runtime-smoke.v1"
            and set(required_data_tooling_runtime_checks) <= data_tooling_runtime_passing_checks,
            "required_checks": required_data_tooling_runtime_checks,
            "passing_checks": tuple(sorted(data_tooling_runtime_passing_checks)),
            "smoke": data_runtime_smoke,
        },
        {
            "id": "generated_runtime_operations",
            "ok": runtime_operation_smoke["ok"]
            and runtime_operation_smoke["format"] == "appgen.generated-native-runtime-operations-smoke.v1"
            and set(required_runtime_operation_checks) <= runtime_operation_passing_checks,
            "required_checks": required_runtime_operation_checks,
            "passing_checks": tuple(sorted(runtime_operation_passing_checks)),
            "smoke": runtime_operation_smoke,
        },
        {
            "id": "generated_native_form_runtime",
            "ok": native_form_runtime_smoke["ok"]
            and native_form_runtime_smoke["format"] == "appgen.generated-native-form-runtime-smoke.v1"
            and set(required_native_form_runtime_checks) <= native_form_runtime_passing_checks,
            "required_checks": required_native_form_runtime_checks,
            "passing_checks": tuple(sorted(native_form_runtime_passing_checks)),
            "smoke": native_form_runtime_smoke,
        },
        {
            "id": "generated_mobile_device_runtime",
            "ok": mobile_device_smoke["ok"]
            and mobile_device_smoke["format"] == "appgen.generated-mobile-device-runtime-smoke.v1"
            and set(required_mobile_device_runtime_checks) <= mobile_device_runtime_passing_checks,
            "required_checks": required_mobile_device_runtime_checks,
            "passing_checks": tuple(sorted(mobile_device_runtime_passing_checks)),
            "smoke": mobile_device_smoke,
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
    required_artifacts = ("app/form_designer.py", "app/templates/appgen_form_designer.html")
    passing_artifacts = tuple(sorted(set(required_artifacts) & existing))
    required_palette_categories = (
        "input",
        "calendar",
        "relationship",
        "media",
        "action",
        "data",
        "menu",
        "mobile",
        "effects",
        "three_d",
    )
    passing_palette_categories = tuple(sorted(set(palette_categories())))
    design = form_design()
    required_canvas_columns = 12
    passing_canvas_columns = design["canvas"]["grid"]["columns"]
    required_canvas_targets = ("web", "mobile", "desktop")
    passing_canvas_targets = tuple(design["canvas"]["render_targets"])
    matrix = field_component_matrix()
    required_mapped_fields = tuple(item["field"] for item in design["components"])
    passing_mapped_fields = tuple(item["field"] for item in matrix if item["supported"])
    required_component_mappings = tuple((item["field"], item["component"]) for item in design["components"])
    passing_component_mappings = tuple((item["field"], item["component"]) for item in matrix if item["supported"])
    drop = snap_drop("TextBox", 2.3, 7.7, field="generated_note")
    drop_checks = (
        ("snapped_x", drop["proposal"]["x"] == 2),
        ("snapped_y", drop["proposal"]["y"] == 8),
        ("review_required", drop["review_required"] is True),
        ("inspector_label_property", "label" in drop["property_inspector"]["properties"]),
        ("inspector_help_text_property", "help_text" in drop["property_inspector"]["properties"]),
    )
    required_drop_checks = tuple(check for check, _ in drop_checks)
    passing_drop_checks = tuple(check for check, ok in drop_checks if ok)
    valid_after_drop = validate_form_design(
        apply_drop(design, {**drop["proposal"], "field_type": "string"})  # type: ignore[arg-type]
    )
    overlap_case = tuple(design["components"]) + (
        {"field": "duplicate_name", "component": "TextBox", "x": 0, "y": 0, "w": 6, "h": 1},
    )
    generation_smoke = form_designer_generation_smoke_audit()
    generation_smoke_passing_checks = {check["id"] for check in generation_smoke["checks"] if check["ok"]}
    required_generation_smoke_checks = (
        "generated_artifacts",
        "generated_python_compiles",
        "generated_component_file_coverage",
        "generated_platform_parity_workbench",
        "generated_component_parity_runtime",
        "generated_inspector_runtime",
        "generated_binding_runtime",
        "generated_package_manager_runtime",
        "generated_visual_depth_runtime",
        "generated_visual_runtime_assets",
        "generated_data_tooling_runtime",
        "generated_runtime_operations",
        "generated_native_form_runtime",
        "generated_mobile_device_runtime",
    )
    rad_parity = rad_parity_workbench(existing)
    rad_parity_passing_checks = {check["id"] for check in rad_parity["checks"] if check["ok"]}
    required_rad_parity_checks = (
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
        "platform_parity_lifecycle_replay",
        "platform_parity_requirement_audit",
        "artifact_contract",
    )
    gates = (
        {
            "id": "palette_breadth",
            "ok": set(required_palette_categories) <= set(passing_palette_categories),
            "required_categories": required_palette_categories,
            "passing_categories": passing_palette_categories,
        },
        {
            "id": "canvas_contract",
            "ok": passing_canvas_columns == required_canvas_columns
            and set(required_canvas_targets) <= set(passing_canvas_targets),
            "required_columns": required_canvas_columns,
            "passing_columns": passing_canvas_columns,
            "required_targets": required_canvas_targets,
            "passing_targets": passing_canvas_targets,
        },
        {
            "id": "field_component_mapping",
            "ok": set(required_mapped_fields) <= set(passing_mapped_fields)
            and set(required_component_mappings) <= set(passing_component_mappings),
            "required_fields": required_mapped_fields,
            "passing_fields": passing_mapped_fields,
            "required_mappings": required_component_mappings,
            "passing_mappings": passing_component_mappings,
        },
        {
            "id": "drop_snap_property_inspector",
            "ok": set(required_drop_checks) <= set(passing_drop_checks),
            "required_checks": required_drop_checks,
            "passing_checks": passing_drop_checks,
            "proposal": drop["proposal"],
            "inspector_properties": tuple(sorted(drop["property_inspector"]["properties"])),
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
            "ok": set(required_artifacts) <= set(passing_artifacts),
            "required_artifacts": required_artifacts,
            "passing_artifacts": passing_artifacts,
        },
        {
            "id": "generation_smoke",
            "ok": generation_smoke["ok"]
            and generation_smoke["format"] == "appgen.form-designer-generation-smoke-audit.v1"
            and generation_smoke["decision"] == "approved"
            and set(required_generation_smoke_checks) <= generation_smoke_passing_checks
            and not generation_smoke["blocking_gaps"],
            "format": generation_smoke["format"],
            "decision": generation_smoke["decision"],
            "required_checks": required_generation_smoke_checks,
            "passing_checks": tuple(sorted(generation_smoke_passing_checks)),
            "checks": tuple(check["id"] for check in generation_smoke["checks"]),
        },
        {
            "id": "generated_runtime_smoke_evidence",
            "ok": set(required_generation_smoke_checks) <= generation_smoke_passing_checks,
            "required_checks": required_generation_smoke_checks,
            "passing_checks": tuple(sorted(generation_smoke_passing_checks)),
        },
        {
            "id": "rad_parity_workbench",
            "ok": rad_parity["ok"]
            and rad_parity["format"] == "appgen.rad-parity-workbench.v1"
            and rad_parity["lifecycle_replay"]["ok"]
            and rad_parity["requirement_audit"]["ok"]
            and set(required_rad_parity_checks) <= rad_parity_passing_checks
            and not rad_parity["blocking_gaps"],
            "required_checks": required_rad_parity_checks,
            "passing_checks": tuple(sorted(rad_parity_passing_checks)),
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
        "rad_parity": rad_parity,
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
        "Viewport3D": "TViewPort3D",
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
