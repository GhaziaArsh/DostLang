"""
symbol_table.py - Scope-aware Symbol Table for DostLang Compiler
================================================================

Provides Symbol and SymbolTable classes for tracking variable declarations,
types, scopes, and values throughout semantic analysis and execution.
"""


class Symbol:
    """Represents a single symbol in the symbol table."""

    def __init__(self, name, sym_type, scope, value, line):
        self.name = name          # str: the identifier name
        self.sym_type = sym_type  # str: 'int', 'float', 'string', 'bool', 'function', 'array', 'unknown'
        self.scope = scope        # str: 'global', function name, 'if', 'else', 'while', etc.
        self.value = value        # actual value (or None)
        self.line = line          # int: declaration line number

    def __repr__(self):
        return f"Symbol({self.name}, {self.sym_type}, {self.scope}, {self.value}, line={self.line})"


class SymbolTable:
    """
    A scope-aware symbol table using a stack of dictionaries.

    Each scope is a dictionary mapping variable names to Symbol objects.
    The stack allows nested scopes (functions, if/else, while loops) to
    shadow outer variables and be cleaned up when exited.
    """

    def __init__(self):
        self.scopes = [{}]            # stack of {name: Symbol}
        self.scope_names = ['global']
        self.all_symbols = []         # flat list of all Symbols ever declared

    def push_scope(self, name):
        """Enter a new scope."""
        self.scopes.append({})
        self.scope_names.append(name)

    def pop_scope(self):
        """Exit current scope. Returns the scope dict."""
        if len(self.scopes) > 1:
            self.scope_names.pop()
            return self.scopes.pop()
        return None

    def declare(self, name, sym_type, value, line):
        """Declare a variable in the current scope. Returns True if successful, False if duplicate."""
        current = self.scopes[-1]
        if name in current:
            return False
        sym = Symbol(name, sym_type, self.current_scope_name(), value, line)
        current[name] = sym
        self.all_symbols.append(sym)
        return True

    def lookup(self, name):
        """Look up a variable in current and enclosing scopes. Returns Symbol or None."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def update(self, name, value, sym_type=None):
        """Update an existing variable's value. Returns True if found, False otherwise."""
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name].value = value
                if sym_type:
                    scope[name].sym_type = sym_type
                return True
        return False

    def current_scope_name(self):
        """Return the name of the current (innermost) scope."""
        return self.scope_names[-1]

    def get_all_symbols(self):
        """Return the flat list of all symbols ever declared."""
        return self.all_symbols
