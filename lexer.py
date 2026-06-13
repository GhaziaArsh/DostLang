"""
lexer.py - Lexical Analyzer for DostLang

This module implements the lexical analysis (tokenization) phase of the DostLang
compiler pipeline using PLY (Python Lex-Yacc). It converts raw DostLang source
code into a stream of tokens that the parser can consume.

DostLang uses Urdu/Hindi-inspired keywords such as `shuru` (start), `khatam` (end),
`rakho` (declare), `dikhao` (print), `agar` (if), `jabtak` (while), etc.

Usage:
    lexer = DostLexer()
    tokens = lexer.tokenize("shuru rakho x = 10; khatam")
    for tok in tokens:
        print(tok)
"""

import ply.lex as lex


class DostLexer:
    """PLY lex-based lexical analyzer for the DostLang language.

    This class encapsulates the PLY lexer, providing methods to tokenize
    DostLang source code. It handles reserved keywords, operators, literals,
    identifiers, comments, and lexical error reporting.

    Attributes:
        lexer: The underlying PLY lexer object.
        errors (list[str]): Accumulated lexical error messages from the
            most recent tokenization run.
    """

    # -------------------------------------------------------------------------
    # Reserved words mapping: DostLang keyword -> token type
    # -------------------------------------------------------------------------
    reserved = {
        'shuru':  'SHURU',
        'khatam': 'KHATAM',
        'rakho':  'RAKHO',
        'dikhao': 'DIKHAO',
        'pocho':  'POCHO',
        'agar':   'AGAR',
        'warna':  'WARNA',
        'jabtak': 'JABTAK',
        'kaam':   'KAAM',
        'wapas':  'WAPAS',
        'sach':   'SACH',
        'jhoot':  'JHOOT',
        'aur':    'AUR',
        'ya':     'YA',
        'nahi':   'NAHI',
    }

    # -------------------------------------------------------------------------
    # Complete list of token types
    # -------------------------------------------------------------------------
    tokens = list(reserved.values()) + [
        'NUMBER_INT', 'NUMBER_FLOAT', 'STRING', 'ID',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 'POWER',
        'EQ', 'NEQ', 'GT', 'LT', 'GTE', 'LTE',
        'ASSIGN',
        'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
        'SEMICOLON', 'COMMA',
    ]

    # -------------------------------------------------------------------------
    # Simple single-character token rules (string assignments)
    # -------------------------------------------------------------------------
    t_PLUS      = r'\+'
    t_MINUS     = r'-'
    t_TIMES     = r'\*'
    t_DIVIDE    = r'/'
    t_MODULO    = r'%'
    t_POWER     = r'\^'
    t_ASSIGN    = r'='
    t_LPAREN    = r'\('
    t_RPAREN    = r'\)'
    t_LBRACE    = r'\{'
    t_RBRACE    = r'\}'
    t_LBRACKET  = r'\['
    t_RBRACKET  = r'\]'
    t_SEMICOLON = r';'
    t_COMMA     = r','

    # Characters to ignore (spaces, tabs, carriage returns)
    t_ignore = ' \t\r'

    # -------------------------------------------------------------------------
    # Multi-character operator token rules (functions for priority)
    # PLY uses function definition order for priority among function-based rules.
    # Longer patterns must be defined BEFORE shorter ones.
    # -------------------------------------------------------------------------

    def t_GTE(self, t):
        r'>='
        return t

    def t_LTE(self, t):
        r'<='
        return t

    def t_EQ(self, t):
        r'=='
        return t

    def t_NEQ(self, t):
        r'!='
        return t

    def t_GT(self, t):
        r'>'
        return t

    def t_LT(self, t):
        r'<'
        return t

    # -------------------------------------------------------------------------
    # Comment rules (must come before other patterns that start with #)
    # Multi-line comments must be checked BEFORE single-line comments.
    # -------------------------------------------------------------------------

    def t_MULTILINE_COMMENT(self, t):
        r'\#\#\#[\s\S]*?\#\#\#'
        # Count newlines within the comment for accurate line tracking
        t.lexer.lineno += t.value.count('\n')
        # Skip this token (do not return it)

    def t_SINGLELINE_COMMENT(self, t):
        r'\#[^\n]*'
        # Single-line comment: skip to end of line, do not return token

    # -------------------------------------------------------------------------
    # Literal and identifier token rules (functions)
    # -------------------------------------------------------------------------

    def t_NUMBER_FLOAT(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_NUMBER_INT(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'"[^"]*"'
        # Strip the enclosing double quotes
        t.value = t.value[1:-1]
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        # Check if the identifier is a reserved keyword
        t.type = self.reserved.get(t.value, 'ID')
        return t

    # -------------------------------------------------------------------------
    # Newline tracking and error handling
    # -------------------------------------------------------------------------

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        error_msg = f"Lexical error at line {t.lexer.lineno}: unexpected character '{t.value[0]}'"
        self.errors.append(error_msg)
        t.lexer.skip(1)

    # -------------------------------------------------------------------------
    # Public interface
    # -------------------------------------------------------------------------

    def __init__(self):
        """Build the PLY lexer and initialize the error list."""
        self.errors = []
        self.lexer = lex.lex(module=self)

    def input(self, data):
        """Feed source code into the lexer for tokenization.

        Args:
            data (str): The DostLang source code string.
        """
        self.errors = []
        self.lexer.lineno = 1
        self.lexer.input(data)

    def token(self):
        """Return the next token from the input stream.

        Returns:
            lex.LexToken | None: The next token, or None if the input is exhausted.
        """
        return self.lexer.token()

    def tokenize(self, data):
        """Tokenize the entire input and return all tokens as a list of dicts.

        Each dict has keys: 'type', 'value', 'lineno', 'lexpos'.

        Args:
            data (str): The DostLang source code string.

        Returns:
            list[dict]: A list of token dictionaries.
        """
        self.input(data)
        result = []
        while True:
            tok = self.token()
            if tok is None:
                break
            result.append({
                'type': tok.type,
                'value': tok.value,
                'lineno': tok.lineno,
                'lexpos': tok.lexpos,
            })
        return result


# ---------------------------------------------------------------------------
# Module-level convenience: allow running `python lexer.py <file>` to test
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python lexer.py <source_file>")
        print("       python lexer.py --interactive")
        sys.exit(1)

    lexer = DostLexer()

    if sys.argv[1] == '--interactive':
        print("DostLang Lexer — Interactive Mode (type 'exit' to quit)")
        while True:
            try:
                line = input(">>> ")
            except EOFError:
                break
            if line.strip().lower() == 'exit':
                break
            tokens = lexer.tokenize(line)
            for tok in tokens:
                print(f"  {tok['type']:15s} {tok['value']!r:20s} line={tok['lineno']} pos={tok['lexpos']}")
            if lexer.errors:
                for err in lexer.errors:
                    print(f"  ERROR: {err}")
    else:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            source = f.read()
        tokens = lexer.tokenize(source)
        for tok in tokens:
            print(f"{tok['type']:15s} {tok['value']!r:20s} line={tok['lineno']} pos={tok['lexpos']}")
        if lexer.errors:
            print("\nLexical Errors:")
            for err in lexer.errors:
                print(f"  {err}")
