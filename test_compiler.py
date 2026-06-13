"""
test_compiler.py - Unit and Integration Tests for DostLang Compiler Pipeline
=============================================================================

Run tests using:
    pytest tests/
"""

import os
import sys

# Add parent directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from lexer import DostLexer
from parser import DostParser
from semantic import SemanticAnalyzer
from ir_generator import IRGenerator
from interpreter import Interpreter
import main

def test_lexer():
    lexer = DostLexer()
    code = "shuru rakho x = 42.5; khatam"
    tokens = lexer.tokenize(code)
    
    types = [t['type'] for t in tokens]
    assert 'SHURU' in types
    assert 'RAKHO' in types
    assert 'NUMBER_FLOAT' in types
    assert 'KHATAM' in types

def test_parser():
    parser = DostParser()
    code = "shuru rakho x = 10; dikhao(x); khatam"
    ast = parser.parse(code)
    
    assert ast is not None
    assert type(ast).__name__ == "ProgramNode"
    assert len(ast.statements) == 2
    assert ast.statements[0].name == "x"

def test_semantic_analysis_success():
    parser = DostParser()
    analyzer = SemanticAnalyzer()
    
    code = """
    shuru
        rakho x = 10;
        x = x + 5;
        dikhao(x);
    khatam
    """
    ast = parser.parse(code)
    symbol_table, errors, warnings = analyzer.analyze(ast)
    
    assert len(errors) == 0
    assert symbol_table.lookup("x") is not None

def test_semantic_analysis_undeclared_error():
    parser = DostParser()
    analyzer = SemanticAnalyzer()
    
    code = """
    shuru
        x = 5;  # Error: x is not declared
    khatam
    """
    ast = parser.parse(code)
    symbol_table, errors, warnings = analyzer.analyze(ast)
    
    assert len(errors) > 0
    assert any("not declared" in err for err in errors)

def test_ir_generation():
    parser = DostParser()
    ir_gen = IRGenerator()
    
    code = """
    shuru
        rakho x = 5 + 10;
    khatam
    """
    ast = parser.parse(code)
    ir_instructions = ir_gen.generate(ast)
    ir_text = ir_gen.get_ir_text()
    
    assert "ADD" in ir_text or "t1 = 5 + 10" in ir_text
    assert "x = t1" in ir_text

def test_interpreter_execution():
    parser = DostParser()
    interpreter = Interpreter()
    
    code = """
    shuru
        rakho x = 2;
        rakho y = 3;
        dikhao(x * y);
    khatam
    """
    ast = parser.parse(code)
    output_text, errors = interpreter.execute(ast)
    
    assert len(errors) == 0
    assert output_text == "6"

def test_recursive_function():
    code = """
    shuru
        kaam fact(n) {
            agar n <= 1 {
                wapas 1;
            } warna {
                wapas n * fact(n - 1);
            }
        }
        dikhao(fact(4));
    khatam
    """
    res = main.run_pipeline(code)
    assert res['status'] == 'Success'
    assert res['output'].strip() == "24"
