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
  : componentPlacement
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
  : DEPLOY IDENT LBRACE agenticOption* RBRACE
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

agenticOption
  : IDENT COLON agenticValue (COMMA agenticValue)* SEMI?
  ;

agenticValue
  : literal ((DOT | MINUS) literal)*
  ;

ruleItem
  : IDENT REQUIRED STRING? SEMI?
  | IDENT ruleOperator ruleValue (ARROW IDENT)? SEMI?
  ;

ruleValue
  : literal (COMMA literal)*
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

expression
  : expressionAtom (operator expressionAtom)*
  ;

expressionAtom
  : target
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
