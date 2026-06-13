# DostLang Formal Grammar Specification

This document defines the formal grammar of DostLang using an EBNF (Extended Backus-Naur Form) notation.

## Lexical Structure

### Keywords
```
shuru       - Program start
khatam      - Program end
rakho       - Variable declaration
dikhao      - Print output
pocho       - Read input
agar        - Conditional If
warna       - Conditional Else
jabtak      - While loop
kaam        - Function definition
wapas       - Return statement
sach        - Boolean True
jhoot       - Boolean False
aur         - Logical AND
ya          - Logical OR
nahi        - Logical NOT
```

### Literals and Identifiers
```
NUMBER_INT   ::= [0-9]+
NUMBER_FLOAT ::= [0-9]+ "." [0-9]+
STRING       ::= "\"" [^"\n]* "\""
ID           ::= [a-zA-Z_][a-zA-Z0-9_]*
```

### Operators & Delimiters
```
PLUS         ::= "+"
MINUS        ::= "-"
TIMES        ::= "*"
DIVIDE       ::= "/"
MODULO       ::= "%"
POWER        ::= "^"
ASSIGN       ::= "="
EQ           ::= "=="
NEQ          ::= "!="
GT           ::= ">"
LT           ::= "<"
GTE          ::= ">="
LTE          ::= "<="
LPAREN       ::= "("
RPAREN       ::= ")"
LBRACE       ::= "{"
RBRACE       ::= "}"
LBRACKET     ::= "["
RBRACKET     ::= "]"
SEMICOLON    ::= ";"
COMMA        ::= ","
```

---

## Syntactic Grammar (BNF)

### Program Entry
```
program        ::= "shuru" stmt_list "khatam"
```

### Statements
```
stmt_list      ::= stmt_list stmt | ε

stmt           ::= var_decl
                 | assignment
                 | array_assign
                 | print_stmt
                 | input_stmt
                 | if_stmt
                 | while_stmt
                 | func_def
                 | return_stmt
                 | expr ";"
```

### Detailed Statement Definitions
```
var_decl       ::= "rakho" ID "=" expr ";"
assignment     ::= ID "=" expr ";"
array_assign   ::= ID "[" expr "]" "=" expr ";"
print_stmt     ::= "dikhao" "(" expr_list ")" ";"
input_stmt     ::= "pocho" ID ";"
if_stmt        ::= "agar" expr "{" stmt_list "}" ( "warna" "{" stmt_list "}" )?
while_stmt     ::= "jabtak" expr "{" stmt_list "}"
func_def       ::= "kaam" ID "(" param_list? ")" "{" stmt_list "}"
return_stmt    ::= "wapas" expr ";"
```

### Expressions
```
expr           ::= expr binop expr
                 | unaryop expr
                 | "(" expr ")"
                 | NUMBER_INT
                 | NUMBER_FLOAT
                 | STRING
                 | "sach"
                 | "jhoot"
                 | ID
                 | func_call
                 | array_access
                 | array_literal

binop          ::= "+" | "-" | "*" | "/" | "%" | "^"
                 | "==" | "!=" | ">" | "<" | ">=" | "<="
                 | "aur" | "ya"

unaryop        ::= "-" | "nahi"

func_call      ::= ID "(" arg_list? ")"
array_access   ::= ID "[" expr "]"
array_literal  ::= "[" expr_list? "]"
```

### Lists
```
expr_list      ::= expr ( "," expr )*
param_list     ::= ID ( "," ID )*
arg_list       ::= expr ( "," expr )*
```
