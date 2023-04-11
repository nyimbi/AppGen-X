grammar appgen;

appgen
    : (importDeclaration | projectBlock)*  (statement)+ EOF
    ;

importDeclaration
	: '#import'  fileNames
	| '#include'  fileNames
	;

fileNames
	: L_CURLY impFileName ((',')? impFileName)* R_CURLY  //with braces or not
	| impFileName ((',')? impFileName)*
	;

impFileName
	: (DOT | '/')? (ident | DOT |'*' | '/')
	;

projectBlock
    : 'project' projectName  project_property_list
    ;
projectName : ident;

project_property_list
    : L_CURLY (project_property (',' project_property)*)? R_CURLY
    | L_CURLY R_CURLY //empty list
    ;

project_property
    : 'project_name' '=' string
    | 'version' '=' string
    | 'description' '=' string
    | 'author' '=' string
    | 'created' '=' string
    | 'updated' '=' string
    | 'DB_URI' '=' string
    | ident '=' (string | INT)
    | config
    | deployment
    | language
    | report_spec
    | theme
    | appGenOptions
    ;

appGenOptions
	: 'generate' '=' L_CURLY appGenOption (',' appGenOption)* R_CURLY
	;

appGenOption
	: IOS
	| WEB
	| DESKTOP
	| ANDROID
	| SQL DIALECT db   //Generate just the sql for the tables
	;

deployment
    : 'deployment' '=' L_CURLY deployment_opt+ R_CURLY
    ;
deployment_opt
    : deploy_optName EQ (string | ident)
    ;

deploy_optName: (string | ident);

language
    : 'languages' EQ L_CURLY (string (',' string)*)? R_CURLY
    ;
theme
    : 'theme' '=' string
    ;


report_spec
    : 'report' reportName L_CURLY report_property_list R_CURLY
    ;
reportName: ident;
report_property_list
    : report_property (COMMA report_property)*
    ;
report_property
    : 'title' '=' string
    | 'type' '=' string
    | 'data' '=' string
    | 'query' '=' string
    | 'filters' '=' string
    | 'options' '=' string
    | 'height' '=' INT
    | 'width' '=' INT
    | ident '=' (string | INT)
    ;

chart_specification
    : 'chart' ident L_CURLY chart_property+ R_CURLY
    ;

chart_property
    : 'Title' '=' string
    | 'Type' '=' string
    | 'Data' '=' string
    | 'Filters' '=' string
    | 'Options' '=' string
    | 'Height' '=' INT
    | 'Width' '=' INT
    | 'X' '=' INT
    | 'Y' '=' INT
    ;

config
    : 'config' EQ L_CURLY (ident '=' string (',' ident '=' string)*)? R_CURLY
    ;


statement
    : object
    | ext_ref           //References defined outside the table definition
    | enum              // Enumeration
//    | Indexes            //Index definition
    | dbfunc            // Database function
//    | func              // External function
//    | rule              // Business Rule like drools
//    | view              // Flask-appbuilder view
//    | snippet           // Reusable code snippet
//    | vardecl           //variable declaration
    ;

dbfunc // A container for triggers and functions. Will be passed through directly
    : string
    ;

object
    : table
    | mixin
    | dbview
    ;

schema
    : ('public' | ident)
    ;

mixin
    : 'mixin' mixin_name L_CURLY column_list R_CURLY
    ;
mixin_name : name_attr;

column_list
    : column (',' column)*
    ;

column
    : column_name column_type (L_SQUARE column_option_list R_SQUARE)?
    ;

column_name: ident;

column_type
    : 'integer' | 'int' | 'long' | 'numeric' | 'decimal' | 'money'| 'tinyint'
    | 'bool'
    | 'string'
    | 'date' | 'time' | 'datetime' | 'timestamp' | 'unixtime'
    | 'text' | 'document'
    | 'serial'
    | 'json' | 'xml'
    | 'blob'
    | 'file'
    | 'point'
    | 'image'
    | 'interval'
//    | 'email' | 'url' | 'doi' | 'address'
    | enum_name
    | varchar
    | 'array' L_SQUARE int_list R_SQUARE 'of' column_type
    ;

int_list: INT (',' INT)*;

column_option_list
    : column_option (','  column_option)*
    ;

column_option
    : primary_key
    | 'default' EQ column_default
    | INCR | DECR
    | unique
    | NULLABLE
    | NOT_NULL
    | int_ref
    | 'enum'  EQ L_CURLY enum_list R_CURLY
    | 'default-expression' EQ L_CURLY string R_CURLY
    | 'min' EQ INT
    | 'max' EQ INT
    | 'check' check_expr
    | display_method
    | note_option
    ;

check_expr: '(' string ')';  //TODO refine the check expressions

column_default
    : NUMBER
    | STRING
    | BOOL
    | NOW | TODAY | TOMORROW
    | NULL
    ;

enum_value
    : string
    ;

enum_name: name_attr;

enum  //self standing enums
    : 'enum' enum_name L_CURLY enum_list R_CURLY
    ;

enum_list
    : enum_item (COMMA enum_item)*
    ;

enum_idx: INT;

enum_item
    : ((enum_idx EQ)? enum_value ('[' note_option ']')?) (COMMA (enum_idx EQ)? enum_value ('[' note_option ']')?)*
    ;

primary_key
    : 'pk'
    | 'primary_key'
    ;

display_method
    : 'display' EQ '{'display_option_list '}'
    ;

display_option_list
    : display_option? (COMMA display_option)*
    ;

display_option
    : 'widget' EQ ident
    | 'width' EQ INT
    | 'height' EQ INT
    | 'hint' EQ string
    | 'color' EQ string    //TODO enumerate colors?
    | 'text_color' EQ string
    ;

note_option
    : NOTE EQ string
    ;

varchar
    : VARCHAR L_PAR INT R_PAR
    ;

table
    : 'table' table_name ('(' mixin_list ')')? '{' column_list index_spec?'}'
    ;

mixin_list
    : mixin_name? (COMMA mixin_name)*
    ;

table_name: name_attr;

dbview //TODO develop a method of creating views
    : 'dbview' EQ '(' schema? DOT? table_name DOT column_name EQ schema? DOT? table_name DOT column_name (EQ schema? DOT? table_name DOT column_name)* ')'
    ;


ext_ref
    : 'ref' ref_name? COLON (schema DOT)? table_name DOT (column_name)+ ref_type table_name DOT (column_name)+
    ;

int_ref
    : 'ref' ref_name? COLON ref_type (schema DOT)? table_name DOT column_name
    ;

ref_name: name_attr;
ref_type
    : oneToOne
    | oneToMany
    | manyToOne
    | manyToMany
    ;

oneToOne: MINUS;
oneToMany: LT;
manyToOne: GT;
manyToMany: M2M;


index_spec
    : 'indexes' L_SQUARE index_item (',' index_item)* R_SQUARE
    ;

index_item
    : index_name L_CURLY column_name (',' column_name)* R_CURLY
    ;

index_name: name_attr;

// Covenience parser rules
string: STRING;

ident: IDENT;


name_attr
     : ident
     ;

unique: ('uniq' | '!' | 'unique') ;

db
    : PGSQL
    | MYSQL
    | SQLITE
    | ORACLE
    ;




// LEXER Part
// Lexer tokens
COMMA           : ',';
COLON           : ':';
SEMI_COLON      : ';';
EQ              : '=';
L_PAR           : '(';
R_PAR           : ')';
L_SQUARE         : '[';
R_SQUARE         : ']';
HASH_SYMBOL     : '#';
L_CURLY         : '{';
R_CURLY         : '}';
ASTERISK        : '*';
DOT             : '.';
MINUS           : '-';
GT              : '>';
LT              : '<';
M2M             : ('<>' | '*');


// Whitespace and comments
WS                  : [ \t\u000B\u000C\u0020\u00A0]+      -> skip;
NL                  : [\r\n\u2028\u2029]        -> skip;
C_LINE_COMMENT      : '//' ~[\r\n]*     -> channel(HIDDEN);
C_STYLE_COMMENT     : '/*' .*? '*/'     -> channel(HIDDEN);
P_STYLE_COMMENT     : '#' ~[(\r)? \n]*  -> skip;

fragment LetterOrDec
    : Letter
    | Digit
    ;
fragment Letter
    : [A-Za-z_]
    | ~[\u0000-\u00FF\uD800-\uDBFF]
    | [\uD800-\uDBFF] [\uDC00-\uDFFF]
    | [\u00E9]
    ;

fragment Digit
    : [0-9]
    ;

IDENT
    : Letter LetterOrDec*
    ;

//FILE_IDENT
//    : (LETTER | DIGIT | '_'|'-' |'/'| ':' | '.')+
//    ;

// Now to define a string
fragment
EscapeSequence
    :   '\\' ('b'|'B'|'t'|'n'|'f'|'r'|'\''|'\\'|'.'|'o'|
              'x'|'a'|'e'|'c'|'d'|'D'|'s'|'S'|'w'|'W'|'p'|'A'|
              'G'|'Z'|'z'|'Q'|'E'|'*'|'['|']'|'('|')'|'$'|'^'|
              '{'|'}'|'?'|'+'|'-'|'&'|'|')
    |   UnicodeEscape
    |   OctalEscape
    ;

fragment
OctalEscape
    :   '\\' ('0'..'3') ('0'..'7') ('0'..'7')
    |   '\\' ('0'..'7') ('0'..'7')
    |   '\\' ('0'..'7')
    ;

fragment
UnicodeEscape
    :   '\\' 'u' HexDigit HexDigit HexDigit HexDigit
    ;


STRING
    :  ('"' ( EscapeSequence | ~('\\'|'"') )* '"')
    |  ('\'' ( EscapeSequence | ~('\\'|'\'') )* '\'')
    { // Semantic Action
        setText( normalizeString( getText() ) );
    }
    ;

// Now define numbers

// INT has no leading zeros
//Can use _ and , to separate digits in a integer 1,000 or 1_000_000 are valid numbers
INT
   : '0' | [1-9] (Digit|'_')*
   ;

NUMBER
   : '-'? INT (DOT Digit+)? EXP?
   | '-'? INT EXP
   | '-'? INT
   ;

FLOAT
    :   Digit+ DOT Digit* EXP? FloatTypeSuffix?
    |   '.' Digit+ EXP? FloatTypeSuffix?
    |   Digit+ EXP FloatTypeSuffix?
    |   Digit+ FloatTypeSuffix
    ;

BOOL
	: ('true'|'false')
	| ('T' | 'F')
	| ('True'|'False')
    ;

fragment
EXP : ('e'|'E') ('+'|'-')? Digit+ ;

fragment
FloatTypeSuffix : ('f'|'F'|'d'|'D'|'B') ;

fragment
HexDigit : ('0'..'9'|'a'..'f'|'A'..'F') ;

fragment
IntegerTypeSuffix : ('l'|'L'|'I') ;

HEX 	: '0' ('x'|'X') HexDigit+ IntegerTypeSuffix? ;

DECIMAL	: INT IntegerTypeSuffix? ;

// Now to define time and dates, complex
TIME_INTERVAL
    : (('0'..'9')+ 'd') (('0'..'9')+ 'h')?(('0'..'9')+ 'm')?(('0'..'9')+ 's')?(('0'..'9')+ 'ms'?)?
    | (('0'..'9')+ 'h') (('0'..'9')+ 'm')?(('0'..'9')+ 's')?(('0'..'9')+ 'ms'?)?
    | (('0'..'9')+ 'm') (('0'..'9')+ 's')?(('0'..'9')+ 'ms'?)?
    | (('0'..'9')+ 's') (('0'..'9')+ 'ms'?)?
    | (('0'..'9')+ 'ms'?)
    ;

DATE_TIME_LITERAL: Bound FullDate 'T' FullTime Bound;

fragment Bound: '"' | '\'';
fragment FullDate: Year '-' Month '-' Day;
fragment Year: Digit Digit (Digit Digit)?;  // EITHER 2 or 4 digits
fragment Month: [0][0-9]|[1][0-2];
fragment Day: [0-2][0-9]|[0-3][01];

fragment FullTime
    : PartialTime TimeOffset;

fragment TimeOffset
    : 'Z' | TimeNumOffset;

fragment TimeNumOffset
    : '-' [01][0-2] (':' (HalfHour))?
    | '+' [01][0-5] (':' (HalfHour | [4][5]))?
    ;
fragment HalfHour: [0][0] | [3][0];

fragment PartialTime
    : [0-2][0-3] ':' Sixty ':' Sixty ('.' [0-9]*)?;

fragment Sixty: [0-5] Digit;


VersionLiteral
  : [0-9]+ '.' [0-9]+ ('.' [0-9]+)? ;


// Keywords

//keywords
//REF: 'ref';
//TABLE: 'table';
//MIXIN: 'mixin';
//TABLEGROUP: 'tablegroup';
//REPORT: 'report';
//PROJECT: 'project';
//VIEW: 'view';
//DBVIEW: 'dbview';
//CONFIG: 'config';
//GENERATE: 'generate';
//DEPLOYMENT: 'deployment';
//LANGUAGES: 'languages';
//THEME: 'theme';
//ENUM: 'enum';
//CHART: 'chart';
////MIN: 'min';
////MAX: 'max';
//IMPORT: 'import';
//INCLUDE: 'include';
//DEFAULT: 'default';

//BLOB: 'blob';
//FILE: 'file';
//PK: ('pk' | 'primary_key');
REQUIRED: 'required';

NULLABLE: 'nullable';
INCR : ('increment' | 'incr' | '++');
DECR : ('decrement' | 'decr' | '--');
NOT_NULL: 'not null';
NULL: ('null' | 'nil' | 'naught');
DISPLAY: 'display';
NOTE: 'note';
TRUE: 'true';
FALSE: 'false';

IOS : 'ios';
WEB : 'web';
SQL : 'sql';
DESKTOP: 'desktop';
OS: 'os';
ANDROID: 'android';
DIALECT: 'dialect';
PGSQL: 'psql';
MYSQL: 'mysql';
SQLITE: 'sqlite';
ORACLE: 'oracle';
CACHE: 'cache';
TimeSeries: ('tseries' | 'time_series' | 'timeseries');   //so that we can handle
VARCHAR: 'varchar';

// Defaults
NOW: 'now';
TODAY : 'today';
YESTERDAY: 'yesterday';
TOMORROW: 'tomorrow';
