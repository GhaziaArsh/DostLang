"""
semantic.py - Semantic Analyzer for DostLang Compiler
=====================================================

Walks the AST and performs semantic checks including:
- Variable declaration / usage validation
- Type inference and type checking
- Function definition and call validation
- Scope management for blocks, functions, loops
- Duplicate declaration detection
"""

from ast_nodes import *
from symbol_table import SymbolTable


class SemanticAnalyzer:
    """
    Performs semantic analysis on a DostLang AST.

    Checks for undeclared variables, type mismatches, duplicate declarations,
    function call arity, return statement placement, and more.
    """

    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []           # list of error message strings
        self.warnings = []         # list of warning strings
        self.in_function = False   # track if inside a function
        self.current_function = None  # name of current function (or None)

    def analyze(self, ast):
        """Analyze the AST. Returns (symbol_table, errors, warnings)."""
        self.visit(ast)
        return self.symbol_table, self.errors, self.warnings

    def visit(self, node):
        """Dispatch to the appropriate visit method based on node type."""
        if node is None:
            return None
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Fallback visitor for unhandled node types."""
        pass

    # ----------------------------------------------------------------
    # Type inference helper
    # ----------------------------------------------------------------

    def infer_type(self, node):
        """
        Infer the type of an expression node.

        Returns one of: 'int', 'float', 'string', 'bool', 'array',
        'function', 'unknown'.
        """
        if node is None:
            return 'unknown'

        if isinstance(node, NumberNode):
            if isinstance(node.value, float):
                return 'float'
            return 'int'

        if isinstance(node, StringNode):
            return 'string'

        if isinstance(node, BoolNode):
            return 'bool'

        if isinstance(node, IdentifierNode):
            sym = self.symbol_table.lookup(node.name)
            if sym:
                return sym.sym_type
            return 'unknown'

        if isinstance(node, ArrayLiteralNode):
            return 'array'

        if isinstance(node, FuncCallNode):
            return 'unknown'

        if isinstance(node, BinOpNode):
            left_type = self.infer_type(node.left)
            right_type = self.infer_type(node.right)

            # Comparison and logical operators always return bool
            if node.op in ('==', '!=', '>', '<', '>=', '<=', 'aur', 'ya'):
                return 'bool'

            # String concatenation
            if node.op == '+' and left_type == 'string' and right_type == 'string':
                return 'string'

            # Arithmetic: float wins over int
            if left_type == 'float' or right_type == 'float':
                return 'float'
            if left_type == 'int' and right_type == 'int':
                return 'int'

            return 'unknown'

        if isinstance(node, UnaryOpNode):
            if node.op == 'nahi':
                return 'bool'
            return self.infer_type(node.operand)

        if isinstance(node, ArrayAccessNode):
            sym = self.symbol_table.lookup(node.name)
            if sym and sym.sym_type == 'array':
                return 'unknown'  # element type is not tracked
            return 'unknown'

        return 'unknown'

    # ----------------------------------------------------------------
    # Visitor methods
    # ----------------------------------------------------------------

    def visit_ProgramNode(self, node):
        """Visit all top-level statements."""
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VarDeclNode(self, node):
        """
        Handle variable declaration.
        - Infer type from value expression.
        - Check for duplicate declaration in current scope.
        - Declare in symbol table.
        - Visit value expression.
        """
        # Visit value first to catch errors inside the expression
        self.visit(node.value)

        # Infer type
        var_type = self.infer_type(node.value)

        # Declare in current scope
        success = self.symbol_table.declare(node.name, var_type, None, node.line)
        if not success:
            self.errors.append(
                f"Semantic Error at line {node.line}: Variable '{node.name}' is already declared in this scope"
            )

    def visit_AssignNode(self, node):
        """
        Handle variable assignment.
        - Check variable is declared (lookup).
        - Visit value expression.
        - Update symbol table.
        """
        sym = self.symbol_table.lookup(node.name)
        if sym is None:
            self.errors.append(
                f"Semantic Error at line {node.line}: Variable '{node.name}' is not declared"
            )

        # Visit value expression
        self.visit(node.value)

        # Update type and value in symbol table
        if sym is not None:
            new_type = self.infer_type(node.value)
            self.symbol_table.update(node.name, None, new_type)

    def visit_BinOpNode(self, node):
        """
        Handle binary operations.
        - Visit left and right operands.
        - Type check: can't do arithmetic on incompatible types.
        - String + String is OK (concatenation).
        - Return inferred type.
        """
        self.visit(node.left)
        self.visit(node.right)

        left_type = self.infer_type(node.left)
        right_type = self.infer_type(node.right)

        # Skip checks if either type is unknown
        if left_type == 'unknown' or right_type == 'unknown':
            return self.infer_type(node)

        # Arithmetic operators
        if node.op in ('+', '-', '*', '/', '%', '^'):
            if node.op == '+':
                # String concatenation is allowed
                if left_type == 'string' and right_type == 'string':
                    return 'string'
                # Number + Number is allowed
                if left_type in ('int', 'float') and right_type in ('int', 'float'):
                    return 'float' if 'float' in (left_type, right_type) else 'int'
                # Mixed types: error
                if left_type != right_type:
                    self.errors.append(
                        f"Semantic Error at line {node.line}: Cannot apply '+' to types '{left_type}' and '{right_type}'"
                    )
                    return 'unknown'
            else:
                # Other arithmetic: both must be numeric
                if left_type not in ('int', 'float') or right_type not in ('int', 'float'):
                    self.errors.append(
                        f"Semantic Error at line {node.line}: Cannot apply '{node.op}' to types '{left_type}' and '{right_type}'"
                    )
                    return 'unknown'
                return 'float' if 'float' in (left_type, right_type) else 'int'

        # Comparison operators — any comparable types
        if node.op in ('==', '!=', '>', '<', '>=', '<='):
            return 'bool'

        # Logical operators
        if node.op in ('aur', 'ya'):
            return 'bool'

        return self.infer_type(node)

    def visit_UnaryOpNode(self, node):
        """Visit operand of a unary operation."""
        self.visit(node.operand)

        operand_type = self.infer_type(node.operand)
        if node.op == '-' and operand_type not in ('int', 'float', 'unknown'):
            self.errors.append(
                f"Semantic Error at line {node.line}: Cannot negate type '{operand_type}'"
            )
        return self.infer_type(node)

    def visit_PrintNode(self, node):
        """Visit all expressions in a print statement."""
        for expr in node.expressions:
            self.visit(expr)

    def visit_InputNode(self, node):
        """Check that the target variable is declared."""
        sym = self.symbol_table.lookup(node.name)
        if sym is None:
            self.errors.append(
                f"Semantic Error at line {node.line}: Variable '{node.name}' is not declared"
            )

    def visit_IfNode(self, node):
        """
        Handle if/else statements.
        - Visit condition.
        - Push scope 'if', visit if_body, pop scope.
        - If else_body: push scope 'else', visit, pop.
        """
        self.visit(node.condition)

        # if body
        self.symbol_table.push_scope('if')
        for stmt in node.if_body:
            self.visit(stmt)
        self.symbol_table.pop_scope()

        # else body
        if node.else_body is not None:
            self.symbol_table.push_scope('else')
            for stmt in node.else_body:
                self.visit(stmt)
            self.symbol_table.pop_scope()

    def visit_WhileNode(self, node):
        """
        Handle while loop.
        - Visit condition.
        - Push scope 'while', visit body, pop scope.
        """
        self.visit(node.condition)

        self.symbol_table.push_scope('while')
        for stmt in node.body:
            self.visit(stmt)
        self.symbol_table.pop_scope()

    def visit_FuncDefNode(self, node):
        """
        Handle function definition.
        - Declare function in symbol table (type='function').
        - Push scope with function name.
        - Declare parameters as variables (type='unknown').
        - Set in_function = True.
        - Visit body.
        - Restore in_function.
        - Pop scope.
        """
        # Declare function in current scope
        success = self.symbol_table.declare(node.name, 'function', node.params, node.line)
        if not success:
            self.errors.append(
                f"Semantic Error at line {node.line}: Function '{node.name}' is already declared in this scope"
            )

        # Enter function scope
        self.symbol_table.push_scope(node.name)

        # Declare parameters
        for param in node.params:
            self.symbol_table.declare(param, 'unknown', None, node.line)

        # Track function context
        prev_in_function = self.in_function
        prev_function = self.current_function
        self.in_function = True
        self.current_function = node.name

        # Visit body
        for stmt in node.body:
            self.visit(stmt)

        # Restore function context
        self.in_function = prev_in_function
        self.current_function = prev_function

        self.symbol_table.pop_scope()

    def visit_FuncCallNode(self, node):
        """
        Handle function call.
        - Look up function name.
        - Check it exists and is a function.
        - Check argument count matches parameter count.
        - Visit all arguments.
        """
        sym = self.symbol_table.lookup(node.name)

        if sym is None:
            self.errors.append(
                f"Semantic Error at line {node.line}: Function '{node.name}' is not defined"
            )
        elif sym.sym_type != 'function':
            self.errors.append(
                f"Semantic Error at line {node.line}: '{node.name}' is not a function"
            )
        else:
            # Check argument count vs parameter count
            expected = len(sym.value) if sym.value else 0
            actual = len(node.args)
            if expected != actual:
                self.errors.append(
                    f"Semantic Error at line {node.line}: Function '{node.name}' expects {expected} arguments, got {actual}"
                )

        # Visit all argument expressions
        for arg in node.args:
            self.visit(arg)

    def visit_ReturnNode(self, node):
        """
        Handle return statement.
        - Check we're inside a function.
        - Visit value expression.
        """
        if not self.in_function:
            self.errors.append(
                f"Semantic Error at line {node.line}: 'wapas' (return) used outside of a function"
            )

        if node.value is not None:
            self.visit(node.value)

    def visit_IdentifierNode(self, node):
        """Check that the variable is declared."""
        sym = self.symbol_table.lookup(node.name)
        if sym is None:
            self.errors.append(
                f"Semantic Error at line {node.line}: Variable '{node.name}' is not declared"
            )
        return sym

    def visit_NumberNode(self, node):
        """No checks needed for number literals."""
        pass

    def visit_StringNode(self, node):
        """No checks needed for string literals."""
        pass

    def visit_BoolNode(self, node):
        """No checks needed for boolean literals."""
        pass

    def visit_ArrayLiteralNode(self, node):
        """Visit all elements in the array literal."""
        for element in node.elements:
            self.visit(element)

    def visit_ArrayAccessNode(self, node):
        """
        Handle array access.
        - Check array variable exists.
        - Visit index expression.
        """
        sym = self.symbol_table.lookup(node.name)
        if sym is None:
            self.errors.append(
                f"Semantic Error at line {node.line}: Variable '{node.name}' is not declared"
            )
        elif sym.sym_type != 'array' and sym.sym_type != 'unknown':
            self.warnings.append(
                f"Warning at line {node.line}: Variable '{node.name}' may not be an array (type: {sym.sym_type})"
            )
        self.visit(node.index)

    def visit_ArrayAssignNode(self, node):
        """
        Handle array element assignment.
        - Check array variable exists.
        - Visit index and value expressions.
        """
        sym = self.symbol_table.lookup(node.name)
        if sym is None:
            self.errors.append(
                f"Semantic Error at line {node.line}: Variable '{node.name}' is not declared"
            )
        elif sym.sym_type != 'array' and sym.sym_type != 'unknown':
            self.warnings.append(
                f"Warning at line {node.line}: Variable '{node.name}' may not be an array (type: {sym.sym_type})"
            )
        self.visit(node.index)
        self.visit(node.value)
