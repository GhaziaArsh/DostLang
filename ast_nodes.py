"""
ast_nodes.py - AST Node Definitions for DostLang

This module defines all Abstract Syntax Tree (AST) node classes used by the
DostLang compiler pipeline. Each node represents a syntactic construct in the
DostLang language and carries a `line` attribute for precise error reporting.

DostLang is an Urdu/Hindi-inspired programming language. The AST serves as the
intermediate representation between parsing and semantic analysis / code generation.
"""


class ASTNode:
    """Base class for all AST nodes.

    Every AST node in the DostLang compiler inherits from this class.
    Subclasses must store a `line` attribute indicating the source line number
    where the construct was found, enabling accurate error diagnostics.
    """

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class ProgramNode(ASTNode):
    """Represents the entire DostLang program.

    A DostLang program is enclosed between `shuru` and `khatam` keywords.
    This node holds the top-level list of statements that constitute the program.

    Attributes:
        statements (list[ASTNode]): The ordered list of top-level statements.
        line (int): The source line number of the `shuru` keyword.
    """

    def __init__(self, statements, line=0):
        self.statements = statements  # list of ASTNode
        self.line = line

    def __repr__(self):
        return f"ProgramNode(statements={self.statements!r}, line={self.line})"


class VarDeclNode(ASTNode):
    """Represents a variable declaration using the `rakho` keyword.

    Syntax: `rakho <name> = <expr>;`

    Declares a new variable with the given name and initializes it to the
    value of the provided expression.

    Attributes:
        name (str): The variable identifier.
        value (ASTNode): The initialization expression.
        line (int): The source line number of the declaration.
    """

    def __init__(self, name, value, line=0):
        self.name = name    # str
        self.value = value  # ASTNode (expression)
        self.line = line

    def __repr__(self):
        return f"VarDeclNode(name={self.name!r}, value={self.value!r}, line={self.line})"


class AssignNode(ASTNode):
    """Represents a variable assignment statement.

    Syntax: `<name> = <expr>;`

    Assigns the value of the expression to an already-declared variable.

    Attributes:
        name (str): The variable identifier being assigned to.
        value (ASTNode): The expression whose value is assigned.
        line (int): The source line number of the assignment.
    """

    def __init__(self, name, value, line=0):
        self.name = name    # str
        self.value = value  # ASTNode (expression)
        self.line = line

    def __repr__(self):
        return f"AssignNode(name={self.name!r}, value={self.value!r}, line={self.line})"


class BinOpNode(ASTNode):
    """Represents a binary operation between two expressions.

    Covers arithmetic (+, -, *, /, ^, %), comparison (==, !=, >, <, >=, <=),
    and logical (aur, ya) operators.

    Attributes:
        op (str): The operator symbol or keyword. One of:
                  '+', '-', '*', '/', '^', '%', '==', '!=', '>', '<', '>=', '<=',
                  'aur', 'ya'.
        left (ASTNode): The left operand expression.
        right (ASTNode): The right operand expression.
        line (int): The source line number of the operator.
    """

    def __init__(self, op, left, right, line=0):
        self.op = op        # str
        self.left = left    # ASTNode
        self.right = right  # ASTNode
        self.line = line

    def __repr__(self):
        return (
            f"BinOpNode(op={self.op!r}, left={self.left!r}, "
            f"right={self.right!r}, line={self.line})"
        )


class UnaryOpNode(ASTNode):
    """Represents a unary operation on a single operand.

    Supports unary negation (`-`) and logical NOT (`nahi`).

    Attributes:
        op (str): The unary operator. One of: '-', 'nahi'.
        operand (ASTNode): The operand expression.
        line (int): The source line number of the operator.
    """

    def __init__(self, op, operand, line=0):
        self.op = op            # str: '-', 'nahi'
        self.operand = operand  # ASTNode
        self.line = line

    def __repr__(self):
        return f"UnaryOpNode(op={self.op!r}, operand={self.operand!r}, line={self.line})"


class NumberNode(ASTNode):
    """Represents a numeric literal (integer or floating-point).

    Attributes:
        value (int | float): The numeric value.
        line (int): The source line number of the literal.
    """

    def __init__(self, value, line=0):
        self.value = value  # int or float
        self.line = line

    def __repr__(self):
        return f"NumberNode(value={self.value!r}, line={self.line})"


class StringNode(ASTNode):
    """Represents a string literal (with quotes already stripped).

    Attributes:
        value (str): The string content without enclosing quotes.
        line (int): The source line number of the literal.
    """

    def __init__(self, value, line=0):
        self.value = value  # str (without quotes)
        self.line = line

    def __repr__(self):
        return f"StringNode(value={self.value!r}, line={self.line})"


class BoolNode(ASTNode):
    """Represents a boolean literal (`sach` for True, `jhoot` for False).

    Attributes:
        value (bool): Python True or False.
        line (int): The source line number of the literal.
    """

    def __init__(self, value, line=0):
        self.value = value  # Python True or False
        self.line = line

    def __repr__(self):
        return f"BoolNode(value={self.value!r}, line={self.line})"


class IdentifierNode(ASTNode):
    """Represents a variable reference in an expression context.

    Attributes:
        name (str): The variable identifier.
        line (int): The source line number of the identifier.
    """

    def __init__(self, name, line=0):
        self.name = name  # str
        self.line = line

    def __repr__(self):
        return f"IdentifierNode(name={self.name!r}, line={self.line})"


class PrintNode(ASTNode):
    """Represents a print statement using the `dikhao` keyword.

    Syntax: `dikhao(<expr1>, <expr2>, ...);`

    Outputs the values of one or more expressions to standard output.

    Attributes:
        expressions (list[ASTNode]): The expressions to print.
        line (int): The source line number of the `dikhao` keyword.
    """

    def __init__(self, expressions, line=0):
        self.expressions = expressions  # list of ASTNode
        self.line = line

    def __repr__(self):
        return f"PrintNode(expressions={self.expressions!r}, line={self.line})"


class InputNode(ASTNode):
    """Represents an input statement using the `pocho` keyword.

    Syntax: `pocho <name>;`

    Reads user input from standard input and stores it in the named variable.

    Attributes:
        name (str): The variable identifier to store input into.
        line (int): The source line number of the `pocho` keyword.
    """

    def __init__(self, name, line=0):
        self.name = name  # str
        self.line = line

    def __repr__(self):
        return f"InputNode(name={self.name!r}, line={self.line})"


class IfNode(ASTNode):
    """Represents a conditional if/else statement.

    Syntax:
        `agar <condition> { <body> }`
        `agar <condition> { <body> } warna { <else_body> }`

    Attributes:
        condition (ASTNode): The boolean condition expression.
        if_body (list[ASTNode]): Statements executed when condition is truthy.
        else_body (list[ASTNode] | None): Statements executed when condition
            is falsy, or None if no `warna` block is present.
        line (int): The source line number of the `agar` keyword.
    """

    def __init__(self, condition, if_body, else_body=None, line=0):
        self.condition = condition  # ASTNode (expression)
        self.if_body = if_body      # list of ASTNode
        self.else_body = else_body  # list of ASTNode or None
        self.line = line

    def __repr__(self):
        return (
            f"IfNode(condition={self.condition!r}, if_body={self.if_body!r}, "
            f"else_body={self.else_body!r}, line={self.line})"
        )


class WhileNode(ASTNode):
    """Represents a while-loop using the `jabtak` keyword.

    Syntax: `jabtak <condition> { <body> }`

    Repeatedly executes the body statements as long as the condition is truthy.

    Attributes:
        condition (ASTNode): The loop condition expression.
        body (list[ASTNode]): The loop body statements.
        line (int): The source line number of the `jabtak` keyword.
    """

    def __init__(self, condition, body, line=0):
        self.condition = condition  # ASTNode (expression)
        self.body = body            # list of ASTNode
        self.line = line

    def __repr__(self):
        return (
            f"WhileNode(condition={self.condition!r}, body={self.body!r}, "
            f"line={self.line})"
        )


class FuncDefNode(ASTNode):
    """Represents a function definition using the `kaam` keyword.

    Syntax:
        `kaam <name>(<params>) { <body> }`
        `kaam <name>() { <body> }`

    Defines a named function with optional parameters and a body of statements.

    Attributes:
        name (str): The function name.
        params (list[str]): The parameter names (may be empty).
        body (list[ASTNode]): The function body statements.
        line (int): The source line number of the `kaam` keyword.
    """

    def __init__(self, name, params, body, line=0):
        self.name = name      # str
        self.params = params  # list of str
        self.body = body      # list of ASTNode
        self.line = line

    def __repr__(self):
        return (
            f"FuncDefNode(name={self.name!r}, params={self.params!r}, "
            f"body={self.body!r}, line={self.line})"
        )


class FuncCallNode(ASTNode):
    """Represents a function call expression.

    Syntax: `<name>(<arg1>, <arg2>, ...)`

    Calls the named function with the provided argument expressions.

    Attributes:
        name (str): The function name being called.
        args (list[ASTNode]): The argument expressions (may be empty).
        line (int): The source line number of the function name.
    """

    def __init__(self, name, args, line=0):
        self.name = name  # str
        self.args = args  # list of ASTNode
        self.line = line

    def __repr__(self):
        return f"FuncCallNode(name={self.name!r}, args={self.args!r}, line={self.line})"


class ReturnNode(ASTNode):
    """Represents a return statement using the `wapas` keyword.

    Syntax: `wapas <expr>;`

    Returns a value from a function. The value expression is required.

    Attributes:
        value (ASTNode | None): The return value expression, or None for bare returns.
        line (int): The source line number of the `wapas` keyword.
    """

    def __init__(self, value, line=0):
        self.value = value  # ASTNode or None
        self.line = line

    def __repr__(self):
        return f"ReturnNode(value={self.value!r}, line={self.line})"


class ArrayLiteralNode(ASTNode):
    """Represents an array literal expression.

    Syntax: `[<expr1>, <expr2>, ...]` or `[]`

    Creates an array containing the given element expressions.

    Attributes:
        elements (list[ASTNode]): The element expressions (may be empty).
        line (int): The source line number of the opening bracket.
    """

    def __init__(self, elements, line=0):
        self.elements = elements  # list of ASTNode
        self.line = line

    def __repr__(self):
        return f"ArrayLiteralNode(elements={self.elements!r}, line={self.line})"


class ArrayAccessNode(ASTNode):
    """Represents an array element access expression.

    Syntax: `<name>[<index>]`

    Accesses an element of an array variable by index.

    Attributes:
        name (str): The array variable identifier.
        index (ASTNode): The index expression.
        line (int): The source line number of the array identifier.
    """

    def __init__(self, name, index, line=0):
        self.name = name    # str
        self.index = index  # ASTNode (expression)
        self.line = line

    def __repr__(self):
        return (
            f"ArrayAccessNode(name={self.name!r}, index={self.index!r}, "
            f"line={self.line})"
        )


class ArrayAssignNode(ASTNode):
    """Represents an array element assignment statement.

    Syntax: `<name>[<index>] = <value>;`

    Assigns a value to a specific index of an existing array variable.

    Attributes:
        name (str): The array variable identifier.
        index (ASTNode): The index expression.
        value (ASTNode): The value expression to assign.
        line (int): The source line number of the array identifier.
    """

    def __init__(self, name, index, value, line=0):
        self.name = name    # str
        self.index = index  # ASTNode
        self.value = value  # ASTNode
        self.line = line

    def __repr__(self):
        return (
            f"ArrayAssignNode(name={self.name!r}, index={self.index!r}, "
            f"value={self.value!r}, line={self.line})"
        )
