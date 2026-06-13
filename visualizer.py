"""
visualizer.py - AST Visualization for DostLang Compiler
========================================================

Uses Graphviz to generate DOT representation of the Abstract Syntax Tree (AST)
and compile it to PNG/SVG images.
"""

import os
try:
    import graphviz
except ImportError:
    graphviz = None

from ast_nodes import *

class ASTVisualizer:
    """
    Generates Graphviz DOT graphs for DostLang ASTs.
    Color-codes nodes:
    - Program/Statement Nodes: Light Blue
    - Expression Nodes: Light Green
    - Constant/Literal/Identifier Nodes: Peach/Orange
    """
    
    def __init__(self):
        self.dot = None
        self.node_count = 0
        
    def _next_node_id(self):
        self.node_count += 1
        return f"node_{self.node_count}"
        
    def generate_ast_graph(self, ast, output_dir="outputs", file_name="ast_graph"):
        """
        Walk the AST and build a Graphviz graph. Saves to output_dir.
        Returns the path to the generated file or None if graphviz is missing.
        """
        if graphviz is None:
            print("Graphviz python library not installed. AST visualization skipped.")
            return None
            
        os.makedirs(output_dir, exist_ok=True)
        
        self.dot = graphviz.Digraph(comment='DostLang AST', format='png')
        self.dot.attr(bgcolor='#1e1e1e', fontcolor='white')
        self.dot.attr('node', style='filled', fontname='Helvetica', fontsize='10')
        self.dot.attr('edge', color='#888888', arrowsize='0.8')
        self.node_count = 0
        
        root_id = self._visit(ast)
        
        output_path = os.path.join(output_dir, file_name)
        try:
            self.dot.render(output_path, cleanup=True)
            return output_path + ".png"
        except Exception as e:
            print(f"Error rendering Graphviz AST: {e}")
            return None

    def _visit(self, node):
        """Walk the AST nodes and add them to the digraph."""
        if node is None:
            return None
            
        node_id = self._next_node_id()
        node_name = type(node).__name__
        
        # Color coding configuration
        # Hex colors: #3a3a3a dark gray, #5c85d6 blue, #5cd65c green, #ffad33 orange
        label = node_name
        fillcolor = '#444444'
        fontcolor = 'white'
        
        if isinstance(node, ProgramNode):
            fillcolor = '#1f4e79'
            label = "Program"
            
        elif isinstance(node, (VarDeclNode, AssignNode, ArrayAssignNode, PrintNode, InputNode, ReturnNode)):
            fillcolor = '#2e5b82'
            if isinstance(node, VarDeclNode):
                label = f"VarDecl\\nrakho {node.name}"
            elif isinstance(node, AssignNode):
                label = f"Assign\\n{node.name} ="
            elif isinstance(node, ArrayAssignNode):
                label = f"ArrayAssign\\n{node.name}[i] ="
            elif isinstance(node, PrintNode):
                label = "Print\\ndikhao()"
            elif isinstance(node, InputNode):
                label = f"Input\\npocho {node.name}"
            elif isinstance(node, ReturnNode):
                label = "Return\\nwapas"
                
        elif isinstance(node, (IfNode, WhileNode, FuncDefNode)):
            fillcolor = '#d9534f' # reddish for control flow
            if isinstance(node, IfNode):
                label = "If (agar)"
            elif isinstance(node, WhileNode):
                label = "While (jabtak)"
            elif isinstance(node, FuncDefNode):
                label = f"FuncDef\\nkaam {node.name}({', '.join(node.params)})"
                
        elif isinstance(node, BinOpNode):
            fillcolor = '#2b7a3e' # green for operators
            label = f"BinOp\\n'{node.op}'"
            
        elif isinstance(node, UnaryOpNode):
            fillcolor = '#2b7a3e'
            label = f"UnaryOp\\n'{node.op}'"
            
        elif isinstance(node, (NumberNode, StringNode, BoolNode, IdentifierNode, ArrayLiteralNode, ArrayAccessNode, FuncCallNode)):
            fillcolor = '#b35c00' # orange/peach for leaves/atoms
            if isinstance(node, NumberNode):
                label = f"Number\\n{node.value}"
            elif isinstance(node, StringNode):
                label = f"String\\n\\\"{node.value}\\\""
            elif isinstance(node, BoolNode):
                label = f"Bool\\n{'sach' if node.value else 'jhoot'}"
            elif isinstance(node, IdentifierNode):
                label = f"ID\\n{node.name}"
            elif isinstance(node, ArrayLiteralNode):
                label = "ArrayLiteral"
            elif isinstance(node, ArrayAccessNode):
                label = f"ArrayAccess\\n{node.name}[i]"
            elif isinstance(node, FuncCallNode):
                label = f"FuncCall\\n{node.name}()"
                
        self.dot.node(node_id, label, fillcolor=fillcolor, fontcolor=fontcolor, color='white')
        
        # Add edges recursively
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                child_id = self._visit(stmt)
                if child_id:
                    self.dot.edge(node_id, child_id)
                    
        elif isinstance(node, VarDeclNode):
            child_id = self._visit(node.value)
            if child_id:
                self.dot.edge(node_id, child_id, label="val")
                
        elif isinstance(node, AssignNode):
            child_id = self._visit(node.value)
            if child_id:
                self.dot.edge(node_id, child_id, label="val")
                
        elif isinstance(node, ArrayAssignNode):
            idx_id = self._visit(node.index)
            val_id = self._visit(node.value)
            if idx_id:
                self.dot.edge(node_id, idx_id, label="idx")
            if val_id:
                self.dot.edge(node_id, val_id, label="val")
                
        elif isinstance(node, PrintNode):
            for expr in node.expressions:
                child_id = self._visit(expr)
                if child_id:
                    self.dot.edge(node_id, child_id)
                    
        elif isinstance(node, IfNode):
            cond_id = self._visit(node.condition)
            if cond_id:
                self.dot.edge(node_id, cond_id, label="cond")
            
            # Group statements under virtual nodes or draw directly
            for stmt in node.if_body:
                child_id = self._visit(stmt)
                if child_id:
                    self.dot.edge(node_id, child_id, label="then")
            
            if node.else_body:
                for stmt in node.else_body:
                    child_id = self._visit(stmt)
                    if child_id:
                        self.dot.edge(node_id, child_id, label="else")
                        
        elif isinstance(node, WhileNode):
            cond_id = self._visit(node.condition)
            body_nodes = []
            if cond_id:
                self.dot.edge(node_id, cond_id, label="cond")
            for stmt in node.body:
                child_id = self._visit(stmt)
                if child_id:
                    self.dot.edge(node_id, child_id, label="body")
                    
        elif isinstance(node, FuncDefNode):
            for stmt in node.body:
                child_id = self._visit(stmt)
                if child_id:
                    self.dot.edge(node_id, child_id, label="body")
                    
        elif isinstance(node, ReturnNode):
            if node.value:
                child_id = self._visit(node.value)
                if child_id:
                    self.dot.edge(node_id, child_id)
                    
        elif isinstance(node, BinOpNode):
            left_id = self._visit(node.left)
            right_id = self._visit(node.right)
            if left_id:
                self.dot.edge(node_id, left_id, label="L")
            if right_id:
                self.dot.edge(node_id, right_id, label="R")
                
        elif isinstance(node, UnaryOpNode):
            child_id = self._visit(node.operand)
            if child_id:
                self.dot.edge(node_id, child_id)
                
        elif isinstance(node, ArrayLiteralNode):
            for elem in node.elements:
                child_id = self._visit(elem)
                if child_id:
                    self.dot.edge(node_id, child_id)
                    
        elif isinstance(node, ArrayAccessNode):
            child_id = self._visit(node.index)
            if child_id:
                self.dot.edge(node_id, child_id, label="idx")
                
        elif isinstance(node, FuncCallNode):
            for arg in node.args:
                child_id = self._visit(arg)
                if child_id:
                    self.dot.edge(node_id, child_id, label="arg")
                    
        return node_id
