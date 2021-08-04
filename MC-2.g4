/* HV CHU XUAN TINH 1870583 */
grammar MC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text);
    else:
        return super().emit();
}

options{
	language=Python3;
}

//program  : mctype 'main' LB RB LP body? RP EOF ;
program: many_declaration+ EOF;  // dau ++
many_declaration: variable_declaration|function_declaration;

//2.1 Variable declaration:
variable_declaration: primitive_type variable_list SEMI ; // primitive_type moi doi
primitive_type: INT|FLOAT|STRING|BOOLEAN;
variable_list:  variable (COMMA variable)*; //variable COMMA variable_list | variable;
variable: ID (LSB INTLIT RSB)?;   //type_declaration ID (COMMA ID)* ; //xem lai

//2.2 Function declaration:
function_declaration: (VOID| primitive_type| arraypointer_type_out) ID LB parameter_list? RB block_statement  ; // xem lại có khai bao bien ben trong func khong
parameter_list:  parameter_declaration (COMMA parameter_declaration)*; // parameter_declaration COMMA parameter_list | parameter_declaration;
parameter_declaration:   primitive_type ID (LSB RSB)? ; // primitive_type ID | primitive_type ID LSB RSB;
//4.7 Array Pointer Type
arraypointer_type: arraypointer_type_in | arraypointer_type_out; // xem lai array_type;
arraypointer_type_in: primitive_type ID LSB RSB ;
arraypointer_type_out:  primitive_type LSB RSB;
array_type: primitive_type ID LB (INTLIT| expression) RB;  // check lai int i[5];
//type_declaration: primitive_type| array_type;
//7.8
block_statement: LP (variable_declaration | statement)* RP  ; // section 7.8;
//list_var_stmt: (variable_declaration | statement)+;
statement: if_statement| while_statement|  for_statement| break_statement| continuce_statement|return_statement| exp_statement | block_statement ;
if_statement: IF LB expression RB statement (ELSE statement)?;
while_statement: DO statement+ WHILE expression SEMI;
for_statement: FOR LB expression SEMI expression SEMI expression RB statement;
break_statement: BREAK SEMI;
continuce_statement: CONTINUE SEMI;
return_statement: RETURN expression? SEMI;
exp_statement: expression SEMI; // xem lai +++?
funcall: ID LB (expression (COMMA expression)*)? RB ;

index_exp: expression LSB expression RSB;
//expression: expression1+;
expression: expression1 ASSIGN_OP expression | expression1 ;
expression1: expression1 OR expression2| expression2;
expression2: expression2  AND expression3 | expression3;
expression3: expression4 (EQUAL| NOT_EQUAL) expression4 | expression4;
expression4: expression5 (LESS_THAN| LESS_THAN_EQUAL| GREATER_THAN| GREATER_THAN_EQUAL) expression5| expression5;
expression5: expression5 (ADD | SUB) expression6 | expression6;
expression6: expression6 (DIV| MUL | MOD) expression7 | expression7;
expression7: (SUB| NOT) expression7 | expression8;
expression8: term LSB expression RSB | term; // term (LSB expression RSB)?;
term:  BOOLEAN_LIT| FLOAT_LIT |INTLIT| STRING_LIT| ID| funcall | LB expression RB ; // index_exp;


BOOLEAN_LIT: TRUE|FALSE;
//Keywords
BOOLEAN: 'boolean';
BREAK: 'break';
CONTINUE: 'continue';
ELSE: 'else';
FOR: 'for';
FLOAT: 'float';
IF: 'if';
INT: 'int';
RETURN: 'return';
VOID: 'void';
DO: 'do';
WHILE: 'while';
TRUE: 'true';
FALSE: 'false';
STRING: 'string';

//3.3 Token Set

INTLIT: [0-9]+;
fragment Letters: [a-zA-Z];
fragment Digits: [0-9];
//ID: (Letters|'-') (Letters| Digits| '-')*;
//un-derscores '-';


fragment Expo: [eE][-]?Digits+;
fragment Fract: Digits+'.'Digits*| Digits*'.'Digits+;
FLOAT_LIT: Fract Expo? | Digits+ Expo;


//3.5 Literals

fragment EscapeSequence: '\\'[bfrnt'"\\];
STRING_LIT:	'"'(~["\\]|EscapeSequence)*'"'{
        self.text = self.text[1:-1]};

//FLOAT_LIT: INTLIT Decpart| Numpart  Decpart? ;
//fragment Numpart: INTLIT '.' | '.' INTLIT| INTLIT '.' INTLIT;
//fragment Decpart: ('e'| 'E') ('+' | '-')? INTLIT ;
// Check lại The following are not considered as ﬂoating literals: //e-12 (no digit before ’e’) 143e (no digits after ’e’
// \b backspace, \f formfeed, \r carriagereturn, \n newline, \t horizontaltab, \" doublequote, \\ backslash

ADD: '+';
MUL: '*';
NOT: '!';
OR: '||';
NOT_EQUAL: '!=';
LESS_THAN: '<';
LESS_THAN_EQUAL: '<=';
ASSIGN_OP: '=';
SUB: '-';
DIV: '/';
MOD: '%';
AND: '&&';
EQUAL: '==';
GREATER_THAN: '>';
GREATER_THAN_EQUAL: '>=';


// 3.4 Separators
LB: '(' ;
RB: ')' ;
LP: '{';
RP: '}';
LSB: '[';
RSB: ']';
SEMI: ';' ;
COMMA: ',';

ID: [a-zA-Z_][0-9a-zA-Z_]* ;
WS : [ \t\r\n]+ -> skip ;
BLANK: '\'' '\'';

//3.2 comment
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
LINE_COMMENT: '//' ~[\r\n]* ->skip ; // trừ tab, newline xem lai yeu cau '//' ~[\r\n]* ->skip

// skip spaces, tabs, newlines
ERROR_CHAR: . { raise ErrorToken(self.text)};
UNCLOSE_STRING: '"'(~["\\]|EscapeSequence)*{raise UncloseString(self.text[1:])};
ILLEGAL_ESCAPE: '"'(~["\\]|EscapeSequence)*'\\'~[bfrnt'"\\]?{raise IllegalEscape(self.text[1:])};