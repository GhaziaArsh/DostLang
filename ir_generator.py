"""
ir_generator.py - Intermediate Representation Generator for DostLang Compiler
=============================================================================

Generates three-address code (TAC) from the DostLang AST. The IR is a
linear sequence of IRInstruction objects suitable for optimization and
code generation.
"""

from ast_nodes import *


class IRInstruction:
    """
    Represents a single three-address code instruction.

    Attributes:
        op (str): The operation code (e.g., 'ASSIGN', 'ADD', 'LABEL', 'GOTO').
        arg1: First operand (variable name, literal, or temp).
        arg2: Second operand (for binary operations).
        result: Destination variable/temp or label name.
    """

    def __init__(self, op, arg1=None, arg2=None, result=None):
        self.op = op        # str: 'ASSIGN', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'POW',
                            #       'EQ', 'NEQ', 'GT', 'LT', 'GTE', 'LTE',
                            #       'AND', 'OR', 'NOT', 'NEG',
                            #       'LABEL', 'GOTO', 'IF_TRUE', 'IF_FALSE',
                            #       'PARAM', 'CALL', 'RETURN',
                            #       'PRINT', 'INPUT',
                            #       'ARRAY_NEW', 'ARRAY_LOAD', 'ARRAY_STORE'
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __repr__(self):
        """Format as human-readable TAC."""
        if self.op == 'ASSIGN':
            return f"{self.result} = {self.arg1}"
        elif self.op in ('ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'POW',
                         'EQ', 'NEQ', 'GT', 'LT', 'GTE', 'LTE',
                         'AND', 'OR'):
            op_symbols = {
                'ADD': '+', 'SUB': '-', 'MUL': '*', 'DIV': '/', 'MOD': '%', 'POW': '^',
                'EQ': '==', 'NEQ': '!=', 'GT': '>', 'LT': '<', 'GTE': '>=', 'LTE': '<=',
                'AND': 'and', 'OR': 'or'
            }
            return f"{self.result} = {self.arg1} {op_symbols[self.op]} {self.arg2}"
        elif self.op == 'NEG':
            return f"{self.result} = -{self.arg1}"
        elif self.op == 'NOT':
            return f"{self.result} = not {self.arg1}"
        elif self.op == 'LABEL':
            return f"{self.result}:"
        elif self.op == 'GOTO':
            return f"GOTO {self.result}"
        elif self.op == 'IF_TRUE':
            return f"IF {self.arg1} GOTO {self.result}"
        elif self.op == 'IF_FALSE':
            return f"IF_FALSE {self.arg1} GOTO {self.result}"
        elif self.op == 'PARAM':
            return f"PARAM {self.arg1}"
        elif self.op == 'CALL':
            return f"{self.result} = CALL {self.arg1}, {self.arg2}"
        elif self.op == 'RETURN':
            return f"RETURN {self.arg1}"
        elif self.op == 'PRINT':
            return f"PRINT {self.arg1}"
        elif self.op == 'INPUT':
            return f"INPUT {self.result}"
        elif self.op == 'ARRAY_NEW':
            return f"{self.result} = ARRAY [{self.arg1}]"
        elif self.op == 'ARRAY_LOAD':
            return f"{self.result} = {self.arg1}[{self.arg2}]"
        elif self.op == 'ARRAY_STORE':
            return f"{self.result}[{self.arg1}] = {self.arg2}"
        return f"{self.op} {self.arg1} {self.arg2} {self.result}"


class IRGenerator:
    """
    Generates three-address code (TAC) from a DostLang AST.

    Uses a visitor pattern to traverse AST nodes and emit IR instructions.
    Manages temporary variables (t1, t2, ...) and labels (L1, L2, ...).
    """

    def __init__(self):
        self.instructions = []  # list of IRInstruction
        self.temp_count = 0     # counter for temporary variables
        self.label_count = 0    # counter for labels

    def new_temp(self):
        """Generate a new unique temporary variable name."""
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        """Generate a new unique label name."""
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, op, arg1=None, arg2=None, result=None):
        """Emit an IR instruction and add it to the instruction list."""
        instr = IRInstruction(op, arg1, arg2, result)
        self.instructions.append(instr)
        return instr

    def generate(self, ast):
        """Generate IR from AST. Returns list of IRInstruction."""
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0
        self.visit(ast)
        return self.instructions

    def get_ir_text(self):
        """Return human-readable IR text."""
        return '\n'.join(str(instr) for instr in self.instructions)

    def visit(self, node):
        """Dispatch to the appropriate visit method based on node type."""
        if node is None:
            return None
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Fallback visitor for unhandled node types."""
        return None

    # ----------------------------------------------------------------
    # Visitor methods
    # ----------------------------------------------------------------

    def visit_ProgramNode(self, node):
        """Visit all statements in the program."""
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VarDeclNode(self, node):
        """Evaluate value expression and emit ASSIGN to variable name."""
        value_temp = self.visit(node.value)
        self.emit('ASSIGN', arg1=value_temp, result=node.name)

    def visit_AssignNode(self, node):
        """Evaluate value expression and emit ASSIGN."""
        value_temp = self.visit(node.value)
        self.emit('ASSIGN', arg1=value_temp, result=node.name)

    def visit_BinOpNode(self, node):
        """
        Visit left and right operands, determine IR op, emit binary operation
        to a new temp, and return the temp name.
        """
        left_temp = self.visit(node.left)
        right_temp = self.visit(node.right)

        # Map AST operators to IR ops
        op_map = {
            '+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV',
            '%': 'MOD', '^': 'POW',
            '==': 'EQ', '!=': 'NEQ', '>': 'GT', '<': 'LT',
            '>=': 'GTE', '<=': 'LTE',
            'aur': 'AND', 'ya': 'OR'
        }

        ir_op = op_map.get(node.op)
        if ir_op is None:
            ir_op = node.op  # fallback

        result = self.new_temp()
        self.emit(ir_op, arg1=left_temp, arg2=right_temp, result=result)
        return result

    def visit_UnaryOpNode(self, node):
        """Visit operand, emit NEG or NOT to a new temp, return temp."""
        operand_temp = self.visit(node.operand)

        result = self.new_temp()
        if node.op == '-':
            self.emit('NEG', arg1=operand_temp, result=result)
        elif node.op == 'nahi':
            self.emit('NOT', arg1=operand_temp, result=result)
        else:
            self.emit('NEG', arg1=operand_temp, result=result)

        return result

    def visit_NumberNode(self, node):
        """Return the number value as a string."""
        return str(node.value)

    def visit_StringNode(self, node):
        """Return the string value with quotes (using repr)."""
        return repr(node.value)

    def visit_BoolNode(self, node):
        """Return 'true' or 'false'."""
        return 'true' if node.value else 'false'

    def visit_IdentifierNode(self, node):
        """Return the variable name."""
        return node.name

    def visit_PrintNode(self, node):
        """Visit each expression and emit PRINT for each."""
        for expr in node.expressions:
            expr_temp = self.visit(expr)
            self.emit('PRINT', arg1=expr_temp)

    def visit_InputNode(self, node):
        """Emit INPUT instruction."""
        self.emit('INPUT', result=node.name)

    def visit_IfNode(self, node):
        """
        Generate IR for if/else:
        - Visit condition → cond_temp
        - Create else_label and end_label
        - Emit IF_FALSE cond_temp GOTO else_label
        - Visit if_body
        - Emit GOTO end_label
        - Emit LABEL else_label
        - Visit else_body (if exists)
        - Emit LABEL end_label
        """
        cond_temp = self.visit(node.condition)

        else_label = self.new_label()
        end_label = self.new_label()

        self.emit('IF_FALSE', arg1=cond_temp, result=else_label)

        # if body
        for stmt in node.if_body:
            self.visit(stmt)

        self.emit('GOTO', result=end_label)

        # else label
        self.emit('LABEL', result=else_label)

        # else body
        if node.else_body:
            for stmt in node.else_body:
                self.visit(stmt)

        # end label
        self.emit('LABEL', result=end_label)

    def visit_WhileNode(self, node):
        """
        Generate IR for while loop:
        - Create start_label and end_label
        - Emit LABEL start_label
        - Visit condition → cond_temp
        - Emit IF_FALSE cond_temp GOTO end_label
        - Visit body
        - Emit GOTO start_label
        - Emit LABEL end_label
        """
        start_label = self.new_label()
        end_label = self.new_label()

        # Loop start
        self.emit('LABEL', result=start_label)

        # Condition
        cond_temp = self.visit(node.condition)
        self.emit('IF_FALSE', arg1=cond_temp, result=end_label)

        # Body
        for stmt in node.body:
            self.visit(stmt)

        # Jump back to start
        self.emit('GOTO', result=start_label)

        # Loop end
        self.emit('LABEL', result=end_label)

    def visit_FuncDefNode(self, node):
        """
        Generate IR for function definition:
        - Emit LABEL with function name
        - Visit body statements
        """
        self.emit('LABEL', result=node.name)

        # Declare parameters (emit PARAM placeholders for documentation)
        for param in node.params:
            self.emit('PARAM', arg1=param)

        # Body
        for stmt in node.body:
            self.visit(stmt)

        # Implicit return if no explicit return was emitted
        # (Check if last instruction is already a RETURN)
        if not self.instructions or self.instructions[-1].op != 'RETURN':
            self.emit('RETURN', arg1=None)

    def visit_FuncCallNode(self, node):
        """
        Generate IR for function call:
        - Emit PARAM for each argument
        - Emit CALL with function name and arg count
        - Return result temp
        """
        # Evaluate and emit arguments
        arg_temps = []
        for arg in node.args:
            arg_temp = self.visit(arg)
            arg_temps.append(arg_temp)

        for arg_temp in arg_temps:
            self.emit('PARAM', arg1=arg_temp)

        result = self.new_temp()
        self.emit('CALL', arg1=node.name, arg2=len(node.args), result=result)
        return result

    def visit_ReturnNode(self, node):
        """Visit value expression and emit RETURN."""
        if node.value is not None:
            value_temp = self.visit(node.value)
            self.emit('RETURN', arg1=value_temp)
        else:
            self.emit('RETURN', arg1=None)

    def visit_ArrayLiteralNode(self, node):
        """
        Generate IR for array literal:
        - Evaluate each element
        - Emit ARRAY_NEW instruction
        - Return a temp representing the array
        """
        element_temps = []
        for element in node.elements:
            elem_temp = self.visit(element)
            element_temps.append(elem_temp)

        result = self.new_temp()
        elements_str = ', '.join(str(t) for t in element_temps)
        self.emit('ARRAY_NEW', arg1=elements_str, result=result)
        return result

    def visit_ArrayAccessNode(self, node):
        """
        Generate IR for array access:
        - Evaluate index
        - Emit ARRAY_LOAD instruction
        - Return result temp
        """
        index_temp = self.visit(node.index)
        result = self.new_temp()
        self.emit('ARRAY_LOAD', arg1=node.name, arg2=index_temp, result=result)
        return result

    def visit_ArrayAssignNode(self, node):
        """
        Generate IR for array element assignment:
        - Evaluate index and value
        - Emit ARRAY_STORE instruction
        """
        index_temp = self.visit(node.index)
        value_temp = self.visit(node.value)
        self.emit('ARRAY_STORE', arg1=index_temp, arg2=value_temp, result=node.name)
