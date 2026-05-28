grammar appgen;

options {
  language = Python3;
}

schema
  : appDecl? element* EOF
  ;

appDecl
  : APP (IDENT | STRING)? appBlock?
  ;

appBlock
  : LBRACE appOption* RBRACE
  ;

appOption
  : IDENT COLON literal (COMMA literal)* SEMI?
  ;

element
  : tableDecl
  | groupDecl
  | enumDecl
  | relationDecl
  | viewDecl
  | flowDecl
  | roleDecl
  | ruleDecl
  | llmDecl
  | agentDecl
  | pbcDecl
  | compositionDecl
  | auditDecl
  | deploymentDecl
  | versionDecl
  | operationDecl
  | securityDecl
  | apiDecl
  | eventDecl
  | jobDecl
  | reportDecl
  | menuDecl
  | componentDecl
  | packageDecl
  | testDecl
  ;

tableDecl
  : TABLE IDENT tableBody
  ;

tableBody
  : LBRACE tableItem* RBRACE
  ;

tableItem
  : fieldDecl
  | spreadDecl
  | relationDecl
  ;

fieldDecl
  : IDENT COLON typeRef derivedExpr? modifier* SEMI?
  ;

spreadDecl
  : ELLIPSIS IDENT SEMI?
  ;

groupDecl
  : IDENT tableBody
  ;

derivedExpr
  : EQ expression
  ;

typeRef
  : IDENT (LPAREN INT RPAREN)? (LBRACK RBRACK)?
  ;

modifier
  : PK
  | REQUIRED
  | UNIQUE
  | HIDE
  | SEARCH
  | DEFAULT literal
  | REF target relationCardinality?
  | ARROW target relationCardinality?
  ;

relationDecl
  : REF? target ARROW target relationCardinality? SEMI?
  ;

relationCardinality
  : LBRACK agenticValue RBRACK
  ;

target
  : IDENT DOT IDENT
  ;

enumDecl
  : ENUM IDENT LBRACE IDENT* RBRACE
  ;

viewDecl
  : VIEW IDENT FOR IDENT LBRACE viewItem* RBRACE
  ;

viewItem
  : handlerDecl
  | componentPlacement
  | IDENT (COLON IDENT (COMMA IDENT)* | (COMMA IDENT)*) SEMI?
  ;

componentPlacement
  : AT IDENT IDENT INT INT INT INT SEMI?
  ;

flowDecl
  : FLOW IDENT LBRACE flowStep* RBRACE
  ;

flowStep
  : IDENT ARROW IDENT SEMI?
  ;

roleDecl
  : ROLE IDENT LBRACE permission* RBRACE
  ;

permission
  : IDENT COLON IDENT (COMMA IDENT)* SEMI?
  ;

ruleDecl
  : RULE IDENT FOR IDENT LBRACE ruleItem* RBRACE
  ;

llmDecl
  : LLM IDENT LBRACE agenticOption* RBRACE
  ;

agentDecl
  : AGENT IDENT LBRACE agenticOption* RBRACE
  ;

pbcDecl
  : PBC IDENT LBRACE agenticOption* RBRACE
  ;

compositionDecl
  : COMPOSITION IDENT LBRACE compositionItem* RBRACE
  ;

compositionItem
  : INCLUDE PBC IDENT VERSION agenticValue SEMI?
  | REQUIRE IDENT agenticValue (COMMA agenticValue)* SEMI?
  | EXPOSE IDENT agenticValue (COMMA agenticValue)* SEMI?
  | CONNECT IDENT IDENT IDENT ARROW IDENT IDENT IDENT SEMI?
  | agenticOption
  ;

auditDecl
  : AUDIT IDENT LBRACE agenticOption* RBRACE
  ;

deploymentDecl
  : DEPLOY IDENT LBRACE deploymentItem* RBRACE
  ;

deploymentItem
  : deployUnit
  | deployScale
  | deployHealth
  | deployCheck
  | agenticOption
  ;

deployUnit
  : IDENT IDENT IDENT IDENT SEMI?
  ;

deployScale
  : IDENT IDENT IDENT INT IDENT INT SEMI?
  ;

deployHealth
  : IDENT IDENT STRING SEMI?
  ;

deployCheck
  : IDENT IDENT IDENT STRING SEMI?
  ;

versionDecl
  : VERSION IDENT LBRACE agenticOption* RBRACE
  ;

operationDecl
  : OPERATION IDENT LBRACE operationItem* RBRACE
  ;

operationItem
  : flowStep
  | agenticOption
  ;

securityDecl
  : SECURITY IDENT LBRACE securityItem* RBRACE
  ;

securityItem
  : permission
  | agenticOption
  ;

apiDecl
  : API IDENT LBRACE contractItem* RBRACE
  ;

eventDecl
  : EVENT IDENT LBRACE contractItem* RBRACE
  ;

jobDecl
  : JOB IDENT LBRACE contractItem* RBRACE
  ;

reportDecl
  : REPORT IDENT LBRACE contractItem* RBRACE
  ;

menuDecl
  : MENU IDENT LBRACE contractItem* RBRACE
  ;

componentDecl
  : COMPONENT IDENT LBRACE contractItem* RBRACE
  ;

packageDecl
  : PACKAGE IDENT LBRACE contractItem* RBRACE
  ;

testDecl
  : TEST IDENT LBRACE contractItem* RBRACE
  ;

contractItem
  : handlerDecl
  | contractArrow
  | agenticOption
  | permission
  ;

handlerDecl
  : IDENT IDENT ARROW IDENT SEMI?
  ;

contractArrow
  : IDENT agenticValue* ARROW IDENT SEMI?
  ;

agenticOption
  : IDENT COLON agenticValue (COMMA agenticValue)* SEMI?
  ;

agenticValue
  : valueAtom ((DOT | MINUS) valueAtom)*
  ;

valueAtom
  : literal
  | APP
  | TABLE
  | ENUM
  | VIEW
  | FOR
  | FLOW
  | ROLE
  | RULE
  | PBC
  | COMPOSITION
  | AUDIT
  | DEPLOY
  | VERSION
  | OPERATION
  | SECURITY
  | API
  | EVENT
  | JOB
  | REPORT
  | MENU
  | COMPONENT
  | PACKAGE
  | TEST
  | LLM
  | AGENT
  | INCLUDE
  | REQUIRE
  | EXPOSE
  | CONNECT
  ;

ruleItem
  : IDENT REQUIRED STRING? SEMI?
  | ruleExpression (ARROW IDENT)? SEMI?
  ;

ruleExpression
  : ruleTerm ((ruleOperator | IDENT) ruleTerm (COMMA ruleTerm)*)*
  ;

ruleTerm
  : qualifiedName
  | literal
  | LPAREN ruleExpression RPAREN
  ;

ruleOperator
  : EQEQ
  | NEQ
  | GTE
  | LTE
  | GT
  | LT
  | IN
  ;

literal
  : STRING
  | DECIMAL
  | INT
  | BOOL
  | IDENT
  ;

qualifiedName
  : IDENT (DOT IDENT)*
  ;

expression
  : expressionAtom (operator expressionAtom)*
  ;

expressionAtom
  : qualifiedName
  | literal
  | LPAREN expression RPAREN
  ;

operator
  : PLUS
  | MINUS
  | STAR
  | SLASH
  ;

APP      : 'app';
TABLE    : 'table';
REF      : 'ref';
ENUM     : 'enum';
VIEW     : 'view';
FOR      : 'for';
FLOW     : 'flow';
ROLE     : 'role';
RULE     : 'rule';
PBC      : 'pbc';
COMPOSITION : 'composition';
AUDIT    : 'audit';
DEPLOY   : 'deploy';
VERSION  : 'version';
OPERATION : 'operation';
SECURITY : 'security';
API      : 'api';
EVENT    : 'event';
JOB      : 'job';
REPORT   : 'report';
MENU     : 'menu';
COMPONENT : 'component';
PACKAGE  : 'package';
TEST     : 'test';
INCLUDE  : 'include';
REQUIRE  : 'require';
EXPOSE   : 'expose';
CONNECT  : 'connect';
LLM      : 'llm';
AGENT    : 'agent';
PK       : 'pk';
REQUIRED : 'required';
UNIQUE   : 'unique';
HIDE     : 'hidden';
SEARCH   : 'search';
DEFAULT  : 'default';
IN       : 'in';

ELLIPSIS : '...';
AT     : '@';
ARROW  : '->';
EQEQ   : '==';
NEQ    : '!=';
GTE    : '>=';
LTE    : '<=';
GT     : '>';
LT     : '<';
EQ     : '=';
PLUS   : '+';
MINUS  : '-';
STAR   : '*';
SLASH  : '/';
COLON  : ':';
COMMA  : ',';
DOT    : '.';
SEMI   : ';';
LPAREN : '(';
RPAREN : ')';
LBRACE : '{';
RBRACE : '}';
LBRACK : '[';
RBRACK : ']';

BOOL
  : 'true'
  | 'false'
  ;

DECIMAL
  : [0-9]+ '.' [0-9]+
  ;

INT
  : [0-9]+
  ;

IDENT
  : [A-Za-z_][A-Za-z0-9_]*
  ;

STRING
  : '"' ( '\\' . | ~["\\] )* '"'
  | '\'' ( '\\' . | ~['\\] )* '\''
  ;

LINE_COMMENT
  : ('//' | '#') ~[\r\n]* -> skip
  ;

BLOCK_COMMENT
  : '/*' .*? '*/' -> skip
  ;

WS
  : [ \t\r\n]+ -> skip
  ;
