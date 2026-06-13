"""
parser.py - Syntactic Analyzer (Parser) for DostLang

This module implements the parsing phase of the DostLang compiler pipeline
using PLY (Python Lex-Yacc). It consumes a stream of tokens produced by the
DostLang lexer and constructs an Abstract Syntax Tree (AST) according to the
DostLang grammar.

The parser is built with PLY's LALR(1) yacc implementation. All grammar rule
functions are defined at module level (as required by PLY), and the DostParser
class provides a clean public interface.

Usage:
    parser = DostParser()
    ast = parser.parse("shuru rakho x = 10; dikhao(x); khatam")
    print(ast)
"""

import ply.yacc as yacc

from lexer import DostLexer
from ast_nodes import (
    ProgramNode, VarDeclNode, AssignNode, BinOpNode, UnaryOpNode,
    NumberNode, StringNode, BoolNode, IdentifierNode, PrintNode,
    InputNode, IfNode, WhileNode, FuncDefNode, FuncCallNode,
    ReturnNode, ArrayLiteralNode, ArrayAccessNode, ArrayAssignNode,
)

# =============================================================================
# Module-level PLY setup
# =============================================================================

# PLY requires `tokens` to be available at module level.
_lexer_instance = DostLexer()
tokens = _lexer_instance.tokens

# Module-level error collection list used by p_error and the DostParser class.
parser_errors = []

# -----------------------------------------------------------------------------
# Operator precedence (lowest to highest)
# -----------------------------------------------------------------------------
precedence = (
    ('left', 'YA'),
    ('left', 'AUR'),
    ('right', 'NAHI'),
    ('nonassoc', 'EQ', 'NEQ', 'GT', 'LT', 'GTE', 'LTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'POWER'),
    ('right', 'UMINUS'),
)


# =============================================================================
# Grammar Rules
# =============================================================================

# ---- Program ----------------------------------------------------------------

def p_program(p):
    '''program : SHURU stmt_list KHATAM'''
    p[0] = ProgramNode(statements=p[2], line=p.lineno(1))


# ---- Statement List ---------------------------------------------------------

def p_stmt_list(p):
    '''stmt_list : stmt_list stmt'''
    p[0] = p[1] + [p[2]]


def p_stmt_list_empty(p):
    '''stmt_list : empty'''
    p[0] = []


# ---- Statements -------------------------------------------------------------

def p_stmt_var_decl(p):
    '''stmt : var_decl'''
    p[0] = p[1]


def p_stmt_assignment(p):
    '''stmt : assignment'''
    p[0] = p[1]


def p_stmt_array_assign(p):
    '''stmt : array_assign'''
    p[0] = p[1]


def p_stmt_print(p):
    '''stmt : print_stmt'''
    p[0] = p[1]


def p_stmt_input(p):
    '''stmt : input_stmt'''
    p[0] = p[1]


def p_stmt_if(p):
    '''stmt : if_stmt'''
    p[0] = p[1]


def p_stmt_while(p):
    '''stmt : while_stmt'''
    p[0] = p[1]


def p_stmt_func_def(p):
    '''stmt : func_def'''
    p[0] = p[1]


def p_stmt_return(p):
    '''stmt : return_stmt'''
    p[0] = p[1]


def p_stmt_expr(p):
    '''stmt : expr_stmt'''
    p[0] = p[1]


# ---- Variable Declaration ---------------------------------------------------

def p_var_decl(p):
    '''var_decl : RAKHO ID ASSIGN expr SEMICOLON'''
    p[0] = VarDeclNode(name=p[2], value=p[4], line=p.lineno(1))


# ---- Assignment -------------------------------------------------------------

def p_assignment(p):
    '''assignment : ID ASSIGN expr SEMICOLON'''
    p[0] = AssignNode(name=p[1], value=p[3], line=p.lineno(1))


# ---- Array Assignment -------------------------------------------------------

def p_array_assign(p):
    '''array_assign : ID LBRACKET expr RBRACKET ASSIGN expr SEMICOLON'''
    p[0] = ArrayAssignNode(name=p[1], index=p[3], value=p[6], line=p.lineno(1))


# ---- Print Statement --------------------------------------------------------

def p_print_stmt(p):
    '''print_stmt : DIKHAO LPAREN expr_list RPAREN SEMICOLON'''
    p[0] = PrintNode(expressions=p[3], line=p.lineno(1))


# ---- Input Statement --------------------------------------------------------

def p_input_stmt(p):
    '''input_stmt : POCHO ID SEMICOLON'''
    p[0] = InputNode(name=p[2], line=p.lineno(1))


# ---- If Statement ------------------------------------------------------------

def p_if_stmt(p):
    '''if_stmt : AGAR expr LBRACE stmt_list RBRACE'''
    p[0] = IfNode(condition=p[2], if_body=p[4], else_body=None, line=p.lineno(1))


def p_if_else_stmt(p):
    '''if_stmt : AGAR expr LBRACE stmt_list RBRACE WARNA LBRACE stmt_list RBRACE'''
    p[0] = IfNode(condition=p[2], if_body=p[4], else_body=p[8], line=p.lineno(1))


# ---- While Statement --------------------------------------------------------

def p_while_stmt(p):
    '''while_stmt : JABTAK expr LBRACE stmt_list RBRACE'''
    p[0] = WhileNode(condition=p[2], body=p[4], line=p.lineno(1))


# ---- Function Definition ----------------------------------------------------

def p_func_def_with_params(p):
    '''func_def : KAAM ID LPAREN param_list RPAREN LBRACE stmt_list RBRACE'''
    p[0] = FuncDefNode(name=p[2], params=p[4], body=p[7], line=p.lineno(1))


def p_func_def_no_params(p):
    '''func_def : KAAM ID LPAREN RPAREN LBRACE stmt_list RBRACE'''
    p[0] = FuncDefNode(name=p[2], params=[], body=p[6], line=p.lineno(1))


# ---- Return Statement -------------------------------------------------------

def p_return_stmt(p):
    '''return_stmt : WAPAS expr SEMICOLON'''
    p[0] = ReturnNode(value=p[2], line=p.lineno(1))


# ---- Expression Statement ---------------------------------------------------

def p_expr_stmt(p):
    '''expr_stmt : expr SEMICOLON'''
    p[0] = p[1]


# ---- Expressions: Binary Operations -----------------------------------------

def p_expr_binop_plus(p):
    '''expr : expr PLUS expr'''
    p[0] = BinOpNode(op='+', left=p[1], right=p[3], line=p.lineno(2))


def p_expr_binop_minus(p):
    '''expr : expr MINUS expr'''
    p[0] = BinOpNode(op='-', left=p[1], right=p[3], line=p.lineno(2))


def p_expr_binop_times(p):
    '''expr : expr TIMES expr'''
    p[0] = BinOpNode(op='*', left=p[1], right=p[3], line=p.lineno(2))


def p_expr_binop_divide(p):
    '''expr : expr DIVIDE expr'''
    p[0] = BinOpNode(op='/', left=p[1], right=p[3], line=p.lineno(2))


def p_expr_binop_modulo(p):
    '''expr : expr MODULO expr'''
    p[0] = BinOpNode(op='%', left=p[1], right=p[3], line=p.lineno(2))


def p_expr_binop_power(p):
    '''expr : expr POWER expr'''
    p[0] = BinOpNode(op='^', left=p[1], right=p[3], line=p.lineno(2))


def p_expr_binop_eq(p):
    '''expr : expr EQ expr'''
    p[0] = BinOpNode(op='==', left=p[1], right=p[3], line=p.lineno(2))


def p_expr_binop_neq(p):
    '''expr : expr NEQ expr'''
    p[0] = BinOpNode(op='!=', left=p[1], right=p[3], line=p.lineno(2))


def p_expr_binop_gt(p):
    '''expr : expr GT expr'''
    p[0] = BinOpNode(op='>', left=p[1], right=p[3], line=p.lineno(2))


def p_expr_binop_lt(p):
    '''expr : expr LT expr'''
    p[0] = BinOpNode(op='<', left=p[1], right=p[3], line=p.lineno(2))


def p_expr_binop_gte(p):
    '''expr : expr GTE expr'''
    p[0] = BinOpNode(op='>=', left=p[1], right=p[3], line=p.lineno(2))


def p_expr_binop_lte(p):
    '''expr : expr LTE expr'''
    p[0] = BinOpNode(op='<=', left=p[1], right=p[3], line=p.lineno(2))


def p_expr_binop_aur(p):
    '''expr : expr AUR expr'''
    p[0] = BinOpNode(op='aur', left=p[1], right=p[3], line=p.lineno(2))


def p_expr_binop_ya(p):
    '''expr : expr YA expr'''
    p[0] = BinOpNode(op='ya', left=p[1], right=p[3], line=p.lineno(2))


# ---- Expressions: Unary Operations ------------------------------------------

def p_expr_nahi(p):
    '''expr : NAHI expr'''
    p[0] = UnaryOpNode(op='nahi', operand=p[2], line=p.lineno(1))


def p_expr_uminus(p):
    '''expr : MINUS expr %prec UMINUS'''
    p[0] = UnaryOpNode(op='-', operand=p[2], line=p.lineno(1))


# ---- Expressions: Grouping --------------------------------------------------

def p_expr_paren(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]


# ---- Expressions: Function Call and Array Access -----------------------------

def p_expr_func_call(p):
    '''expr : func_call'''
    p[0] = p[1]


def p_expr_array_access(p):
    '''expr : array_access'''
    p[0] = p[1]


# ---- Expressions: Atoms -----------------------------------------------------

def p_expr_id(p):
    '''expr : ID'''
    p[0] = IdentifierNode(name=p[1], line=p.lineno(1))


def p_expr_number_int(p):
    '''expr : NUMBER_INT'''
    p[0] = NumberNode(value=p[1], line=p.lineno(1))


def p_expr_number_float(p):
    '''expr : NUMBER_FLOAT'''
    p[0] = NumberNode(value=p[1], line=p.lineno(1))


def p_expr_string(p):
    '''expr : STRING'''
    p[0] = StringNode(value=p[1], line=p.lineno(1))


def p_expr_sach(p):
    '''expr : SACH'''
    p[0] = BoolNode(value=True, line=p.lineno(1))


def p_expr_jhoot(p):
    '''expr : JHOOT'''
    p[0] = BoolNode(value=False, line=p.lineno(1))


def p_expr_array_literal(p):
    '''expr : array_literal'''
    p[0] = p[1]


# ---- Function Call -----------------------------------------------------------

def p_func_call_with_args(p):
    '''func_call : ID LPAREN arg_list RPAREN'''
    p[0] = FuncCallNode(name=p[1], args=p[3], line=p.lineno(1))


def p_func_call_no_args(p):
    '''func_call : ID LPAREN RPAREN'''
    p[0] = FuncCallNode(name=p[1], args=[], line=p.lineno(1))


# ---- Array Access ------------------------------------------------------------

def p_array_access(p):
    '''array_access : ID LBRACKET expr RBRACKET'''
    p[0] = ArrayAccessNode(name=p[1], index=p[3], line=p.lineno(1))


# ---- Array Literal -----------------------------------------------------------

def p_array_literal_with_elements(p):
    '''array_literal : LBRACKET expr_list RBRACKET'''
    p[0] = ArrayLiteralNode(elements=p[2], line=p.lineno(1))


def p_array_literal_empty(p):
    '''array_literal : LBRACKET RBRACKET'''
    p[0] = ArrayLiteralNode(elements=[], line=p.lineno(1))


# ---- Expression List (comma-separated) --------------------------------------

def p_expr_list_single(p):
    '''expr_list : expr'''
    p[0] = [p[1]]


def p_expr_list_multiple(p):
    '''expr_list : expr COMMA expr_list'''
    p[0] = [p[1]] + p[3]


# ---- Parameter List (comma-separated identifiers) ---------------------------

def p_param_list_single(p):
    '''param_list : ID'''
    p[0] = [p[1]]


def p_param_list_multiple(p):
    '''param_list : ID COMMA param_list'''
    p[0] = [p[1]] + p[3]


# ---- Argument List (comma-separated expressions) ----------------------------

def p_arg_list_single(p):
    '''arg_list : expr'''
    p[0] = [p[1]]


def p_arg_list_multiple(p):
    '''arg_list : expr COMMA arg_list'''
    p[0] = [p[1]] + p[3]


# ---- Empty Production -------------------------------------------------------

def p_empty(p):
    '''empty :'''
    p[0] = None


# ---- Error Handling ----------------------------------------------------------

def p_error(p):
    """Handle syntax errors detected by the PLY parser.

    Collects error messages into the module-level `parser_errors` list
    for later retrieval by the DostParser class.
    """
    if p:
        error_msg = f"Syntax error at line {p.lineno}: unexpected token '{p.value}'"
    else:
        error_msg = "Syntax error: unexpected end of input"
    parser_errors.append(error_msg)


# =============================================================================
# Build the PLY parser at module level
# =============================================================================

_parser = yacc.yacc(debug=False, write_tables=False)


# =============================================================================
# DostParser Class — Public Interface
# =============================================================================

class DostParser:
    """High-level parser interface for the DostLang language.

    Wraps the module-level PLY parser and lexer, providing a clean API
    for parsing DostLang source code into an AST.

    Attributes:
        lexer (DostLexer): The lexer instance used for tokenization.
        errors (list[str]): Syntax error messages from the most recent parse.
    """

    def __init__(self):
        """Initialize the parser with a fresh DostLexer instance."""
        self.lexer = DostLexer()
        self.errors = []

    def parse(self, data):
        """Parse DostLang source code and return the AST.

        Args:
            data (str): The DostLang source code string. Must be enclosed
                        in `shuru ... khatam`.

        Returns:
            ProgramNode | None: The root AST node representing the parsed
                program, or None if parsing failed.
        """
        global parser_errors
        parser_errors = []
        self.errors = []

        # Feed source into the lexer
        self.lexer.input(data)

        # Parse using the module-level parser and the lexer's internal PLY lexer
        result = _parser.parse(data, lexer=self.lexer.lexer, tracking=True)

        # Collect errors from both lexer and parser
        self.errors = list(self.lexer.errors) + list(parser_errors)

        return result


# =============================================================================
# Module-level convenience: allow running `python parser.py <file>` to test
# =============================================================================

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python parser.py <source_file>")
        print("       python parser.py --interactive")
        sys.exit(1)

    parser = DostParser()

    if sys.argv[1] == '--interactive':
        print("DostLang Parser — Interactive Mode (type 'exit' to quit)")
        print("Enter a complete program (shuru ... khatam) on one line:")
        while True:
            try:
                line = input(">>> ")
            except EOFError:
                break
            if line.strip().lower() == 'exit':
                break
            ast = parser.parse(line)
            if parser.errors:
                for err in parser.errors:
                    print(f"  ERROR: {err}")
            else:
                print(f"  AST: {ast!r}")
    else:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            source = f.read()
        ast = parser.parse(source)
        if parser.errors:
            print("Parse Errors:")
            for err in parser.errors:
                print(f"  {err}")
        else:
            print("Parse successful!")
            print(f"AST: {ast!r}")
