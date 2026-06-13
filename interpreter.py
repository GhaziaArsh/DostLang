"""
interpreter.py - Tree-Walking Interpreter for DostLang
======================================================

Executes DostLang ASTs by walking the tree and evaluating nodes.
Supports variables, arithmetic, strings, booleans, control flow,
functions with closures, arrays, and input/output.
"""

from ast_nodes import *


class ReturnException(Exception):
    """Used to unwind the call stack on return."""

    def __init__(self, value):
        self.value = value


class RuntimeError_(Exception):
    """DostLang runtime error."""

    def __init__(self, message, line=0):
        self.message = message
        self.line = line
        super().__init__(message)


class Environment:
    """
    Variable environment with scope chain.

    Each environment has a dict of variables and an optional parent
    environment. Variable lookup walks the chain upward.
    """

    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def get(self, name):
        """Look up a variable by name, walking the scope chain."""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        return None

    def set(self, name, value):
        """Set a variable in the current environment."""
        self.variables[name] = value

    def update(self, name, value):
        """Update an existing variable in the nearest scope that contains it."""
        if name in self.variables:
            self.variables[name] = value
            return True
        if self.parent:
            return self.parent.update(name, value)
        return False

    def exists(self, name):
        """Check if a variable exists in this environment or any parent."""
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.exists(name)
        return False


class Interpreter:
    """
    Tree-walking interpreter for DostLang.

    Executes AST nodes directly by visiting them. Supports custom I/O
    functions for GUI integration.
    """

    # Maximum iterations for while loops to prevent infinite loops
    MAX_ITERATIONS = 10000

    def __init__(self, input_func=None, output_func=None):
        self.global_env = Environment()
        self.current_env = self.global_env
        self.functions = {}   # {name: FuncDefNode}
        self.output = []      # list of output strings
        self.errors = []      # list of runtime error strings
        self.input_func = input_func or input    # for GUI: custom input
        self.output_func = output_func           # for GUI: custom output callback

    def execute(self, ast):
        """Execute the AST. Returns (output_text, errors)."""
        self.output = []
        self.errors = []
        try:
            self.visit(ast)
        except ReturnException:
            self.errors.append("Runtime Error: 'wapas' used outside of function")
        except RuntimeError_ as e:
            self.errors.append(f"Runtime Error at line {e.line}: {e.message}")
        except Exception as e:
            self.errors.append(f"Runtime Error: {str(e)}")
        return '\n'.join(self.output), self.errors

    def visit(self, node):
        """Dispatch to the appropriate visit method based on node type."""
        if node is None:
            return None
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Fallback for unhandled node types."""
        raise RuntimeError_(
            f"Unknown node type: {type(node).__name__}",
            getattr(node, 'line', 0)
        )

    # ----------------------------------------------------------------
    # Output formatting
    # ----------------------------------------------------------------

    def format_value(self, value):
        """
        Format a value for output.

        - Booleans: 'sach' / 'jhoot'
        - Floats that are whole numbers: printed as int
        - Lists (arrays): formatted recursively
        - Everything else: str()
        """
        if isinstance(value, bool):
            return 'sach' if value else 'jhoot'
        elif isinstance(value, float) and value == int(value):
            return str(int(value))
        elif isinstance(value, list):
            return '[' + ', '.join(self.format_value(v) for v in value) + ']'
        return str(value)

    # ----------------------------------------------------------------
    # Visitor methods
    # ----------------------------------------------------------------

    def visit_ProgramNode(self, node):
        """Execute each statement in the program."""
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VarDeclNode(self, node):
        """Evaluate the value and set the variable in the current environment."""
        value = self.visit(node.value)
        self.current_env.set(node.name, value)

    def visit_AssignNode(self, node):
        """Evaluate the value and update an existing variable."""
        if not self.current_env.exists(node.name):
            raise RuntimeError_(
                f"Variable '{node.name}' is not declared",
                node.line
            )
        value = self.visit(node.value)
        if not self.current_env.update(node.name, value):
            raise RuntimeError_(
                f"Variable '{node.name}' is not declared",
                node.line
            )

    def visit_BinOpNode(self, node):
        """
        Evaluate a binary operation.

        Supports arithmetic (+, -, *, /, %, ^), string concatenation,
        comparisons (==, !=, >, <, >=, <=), and logical operators (aur, ya).
        """
        left = self.visit(node.left)
        right = self.visit(node.right)

        op = node.op

        try:
            if op == '+':
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left + right
                raise RuntimeError_(
                    f"Cannot add types {type(left).__name__} and {type(right).__name__}",
                    node.line
                )

            elif op == '-':
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left - right
                raise RuntimeError_(
                    f"Cannot subtract types {type(left).__name__} and {type(right).__name__}",
                    node.line
                )

            elif op == '*':
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left * right
                raise RuntimeError_(
                    f"Cannot multiply types {type(left).__name__} and {type(right).__name__}",
                    node.line
                )

            elif op == '/':
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    if right == 0:
                        raise RuntimeError_("Division by zero", node.line)
                    result = left / right
                    # Return int if both operands are int and division is exact
                    if isinstance(left, int) and isinstance(right, int) and left % right == 0:
                        return left // right
                    return result
                raise RuntimeError_(
                    f"Cannot divide types {type(left).__name__} and {type(right).__name__}",
                    node.line
                )

            elif op == '%':
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    if right == 0:
                        raise RuntimeError_("Modulo by zero", node.line)
                    return left % right
                raise RuntimeError_(
                    f"Cannot apply modulo to types {type(left).__name__} and {type(right).__name__}",
                    node.line
                )

            elif op == '^':
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left ** right
                raise RuntimeError_(
                    f"Cannot apply power to types {type(left).__name__} and {type(right).__name__}",
                    node.line
                )

            elif op == '==':
                return left == right
            elif op == '!=':
                return left != right
            elif op == '>':
                return left > right
            elif op == '<':
                return left < right
            elif op == '>=':
                return left >= right
            elif op == '<=':
                return left <= right

            elif op == 'aur':
                return bool(left) and bool(right)
            elif op == 'ya':
                return bool(left) or bool(right)

            else:
                raise RuntimeError_(
                    f"Unknown operator '{op}'",
                    node.line
                )

        except RuntimeError_:
            raise
        except TypeError as e:
            raise RuntimeError_(str(e), node.line)

    def visit_UnaryOpNode(self, node):
        """Evaluate a unary operation: negation or logical not."""
        operand = self.visit(node.operand)

        if node.op == '-':
            if isinstance(operand, (int, float)):
                return -operand
            raise RuntimeError_(
                f"Cannot negate type {type(operand).__name__}",
                node.line
            )
        elif node.op == 'nahi':
            return not bool(operand)
        else:
            raise RuntimeError_(
                f"Unknown unary operator '{node.op}'",
                node.line
            )

    def visit_NumberNode(self, node):
        """Return the numeric value."""
        return node.value

    def visit_StringNode(self, node):
        """Return the string value."""
        return node.value

    def visit_BoolNode(self, node):
        """Return the boolean value."""
        return node.value

    def visit_IdentifierNode(self, node):
        """Look up a variable in the environment chain."""
        value = self.current_env.get(node.name)
        if value is None and not self.current_env.exists(node.name):
            raise RuntimeError_(
                f"Variable '{node.name}' is not declared",
                node.line
            )
        return value

    def visit_PrintNode(self, node):
        """
        Evaluate all expressions, format them, join with space,
        and add to output. Each dikhao() call produces one line.
        """
        values = []
        for expr in node.expressions:
            val = self.visit(expr)
            values.append(self.format_value(val))

        line = ' '.join(values)
        self.output.append(line)

        if self.output_func:
            self.output_func(line)

    def visit_InputNode(self, node):
        """
        Read input from the user (or custom input function).
        Try to convert to int, then float, else keep as string.
        Store result in the environment.
        """
        if not self.current_env.exists(node.name):
            raise RuntimeError_(
                f"Variable '{node.name}' is not declared",
                node.line
            )

        try:
            prompt = f"{node.name}? "
            raw = self.input_func(prompt)
        except EOFError:
            raw = ""
        except Exception as e:
            raise RuntimeError_(f"Input error: {str(e)}", node.line)

        # Try to convert to int, then float, else keep as string
        value = raw
        try:
            value = int(raw)
        except (ValueError, TypeError):
            try:
                value = float(raw)
            except (ValueError, TypeError):
                pass  # keep as string

        self.current_env.update(node.name, value)

    def visit_IfNode(self, node):
        """
        Evaluate condition. If truthy, execute if_body in a new environment;
        otherwise execute else_body (if exists) in a new environment.
        """
        condition = self.visit(node.condition)

        if self._is_truthy(condition):
            # Execute if body in new scope
            prev_env = self.current_env
            self.current_env = Environment(parent=prev_env)
            try:
                for stmt in node.if_body:
                    self.visit(stmt)
            finally:
                self.current_env = prev_env
        elif node.else_body is not None:
            # Execute else body in new scope
            prev_env = self.current_env
            self.current_env = Environment(parent=prev_env)
            try:
                for stmt in node.else_body:
                    self.visit(stmt)
            finally:
                self.current_env = prev_env

    def visit_WhileNode(self, node):
        """
        Loop while condition is truthy, executing body in a new environment
        each iteration. Enforces iteration limit to prevent infinite loops.
        """
        iterations = 0

        while True:
            condition = self.visit(node.condition)
            if not self._is_truthy(condition):
                break

            iterations += 1
            if iterations > self.MAX_ITERATIONS:
                raise RuntimeError_(
                    f"Loop exceeded maximum iterations ({self.MAX_ITERATIONS})",
                    node.line
                )

            # Execute body in new scope
            prev_env = self.current_env
            self.current_env = Environment(parent=prev_env)
            try:
                for stmt in node.body:
                    self.visit(stmt)
            finally:
                self.current_env = prev_env

    def visit_FuncDefNode(self, node):
        """Store function definition in the functions dictionary."""
        self.functions[node.name] = node

    def visit_FuncCallNode(self, node):
        """
        Execute a function call:
        - Look up function in self.functions
        - Check arg count matches param count
        - Create new environment with parent = global_env
        - Bind params to evaluated args
        - Execute body, catch ReturnException for return value
        - Restore env
        - Return the return value or None
        """
        if node.name not in self.functions:
            raise RuntimeError_(
                f"Function '{node.name}' is not defined",
                node.line
            )

        func_def = self.functions[node.name]

        # Check argument count
        if len(node.args) != len(func_def.params):
            raise RuntimeError_(
                f"Function '{node.name}' expects {len(func_def.params)} arguments, got {len(node.args)}",
                node.line
            )

        # Evaluate arguments in the current environment
        arg_values = []
        for arg in node.args:
            arg_values.append(self.visit(arg))

        # Create new environment for the function call
        func_env = Environment(parent=self.global_env)

        # Bind parameters to argument values
        for param, value in zip(func_def.params, arg_values):
            func_env.set(param, value)

        # Save current environment and switch to function environment
        prev_env = self.current_env
        self.current_env = func_env

        return_value = None
        try:
            for stmt in func_def.body:
                self.visit(stmt)
        except ReturnException as e:
            return_value = e.value
        finally:
            # Restore environment
            self.current_env = prev_env

        return return_value

    def visit_ReturnNode(self, node):
        """Evaluate the return value and raise ReturnException to unwind."""
        value = None
        if node.value is not None:
            value = self.visit(node.value)
        raise ReturnException(value)

    def visit_ArrayLiteralNode(self, node):
        """Evaluate all elements and return as a Python list."""
        elements = []
        for element in node.elements:
            elements.append(self.visit(element))
        return elements

    def visit_ArrayAccessNode(self, node):
        """Look up array, evaluate index, return element with bounds check."""
        array = self.current_env.get(node.name)
        if array is None and not self.current_env.exists(node.name):
            raise RuntimeError_(
                f"Variable '{node.name}' is not declared",
                node.line
            )

        if not isinstance(array, list):
            raise RuntimeError_(
                f"Variable '{node.name}' is not an array",
                node.line
            )

        index = self.visit(node.index)

        if not isinstance(index, int):
            raise RuntimeError_(
                f"Array index must be an integer, got {type(index).__name__}",
                node.line
            )

        if index < 0 or index >= len(array):
            raise RuntimeError_(
                f"Array index {index} out of bounds (size {len(array)})",
                node.line
            )

        return array[index]

    def visit_ArrayAssignNode(self, node):
        """Look up array, evaluate index and value, set element with bounds check."""
        array = self.current_env.get(node.name)
        if array is None and not self.current_env.exists(node.name):
            raise RuntimeError_(
                f"Variable '{node.name}' is not declared",
                node.line
            )

        if not isinstance(array, list):
            raise RuntimeError_(
                f"Variable '{node.name}' is not an array",
                node.line
            )

        index = self.visit(node.index)
        value = self.visit(node.value)

        if not isinstance(index, int):
            raise RuntimeError_(
                f"Array index must be an integer, got {type(index).__name__}",
                node.line
            )

        if index < 0 or index >= len(array):
            raise RuntimeError_(
                f"Array index {index} out of bounds (size {len(array)})",
                node.line
            )

        array[index] = value

    # ----------------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------------

    def _is_truthy(self, value):
        """
        Determine if a value is truthy in DostLang.

        - False, 0, 0.0, '', None, [] → falsy
        - Everything else → truthy
        """
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        if isinstance(value, list):
            return len(value) > 0
        return True
