"""
main.py - Entry point for the DostLang Compiler and Interpreter
===============================================================

Provides both a command-line interface (CLI) to execute DostLang files
and a fallback graphical user interface (GUI) mode.

Usage:
    python main.py                  # Launches the IDE (GUI)
    python main.py <source_file>    # Executes source file via CLI
"""

import sys
import os

from lexer import DostLexer
from parser import DostParser
from semantic import SemanticAnalyzer
from ir_generator import IRGenerator
from interpreter import Interpreter
import database

def run_pipeline(source_code, input_func=None, output_func=None):
    """
    Runs the entire compiler pipeline:
    Lexer -> Parser -> Semantic Analyzer -> IR Generator -> Interpreter
    
    Returns:
        dict: A dictionary containing the results, tables, and errors at each stage.
    """
    result = {
        'tokens': [],
        'ast': None,
        'ir_code': "",
        'output': "",
        'errors': [],
        'warnings': [],
        'status': 'Success'
    }
    
    # 1. Lexical Analysis
    lexer = DostLexer()
    try:
        tokens_list = lexer.tokenize(source_code)
        result['tokens'] = tokens_list
        if lexer.errors:
            for err in lexer.errors:
                result['errors'].append({'type': 'Lexical', 'message': err, 'line': 0})
            result['status'] = 'Error'
            return result
    except Exception as e:
        result['errors'].append({'type': 'Lexical', 'message': f"Unexpected lexer error: {e}", 'line': 0})
        result['status'] = 'Error'
        return result
        
    # 2. Syntax Analysis
    parser = DostParser()
    try:
        ast = parser.parse(source_code)
        result['ast'] = ast
        if parser.errors:
            for err in parser.errors:
                result['errors'].append({'type': 'Syntax', 'message': err, 'line': 0})
            result['status'] = 'Error'
            return result
        if not ast:
            result['errors'].append({'type': 'Syntax', 'message': "Empty AST generated", 'line': 0})
            result['status'] = 'Error'
            return result
    except Exception as e:
        result['errors'].append({'type': 'Syntax', 'message': f"Unexpected parser error: {e}", 'line': 0})
        result['status'] = 'Error'
        return result
        
    # 3. Semantic Analysis
    analyzer = SemanticAnalyzer()
    try:
        symbol_table, semantic_errors, semantic_warnings = analyzer.analyze(ast)
        result['symbol_table'] = symbol_table
        result['warnings'] = semantic_warnings
        if semantic_errors:
            for err in semantic_errors:
                result['errors'].append({'type': 'Semantic', 'message': err, 'line': 0})
            result['status'] = 'Error'
            return result
    except Exception as e:
        result['errors'].append({'type': 'Semantic', 'message': f"Unexpected semantic error: {e}", 'line': 0})
        result['status'] = 'Error'
        return result
        
    # 4. IR Generation
    ir_gen = IRGenerator()
    try:
        ir_instructions = ir_gen.generate(ast)
        result['ir_code'] = ir_gen.get_ir_text()
    except Exception as e:
        result['errors'].append({'type': 'IR Generation', 'message': f"Unexpected IR error: {e}", 'line': 0})
        result['status'] = 'Error'
        return result
        
    # 5. Interpretation/Execution
    interpreter = Interpreter(input_func=input_func, output_func=output_func)
    try:
        out_text, runtime_errors = interpreter.execute(ast)
        result['output'] = out_text
        if runtime_errors:
            for err in runtime_errors:
                result['errors'].append({'type': 'Runtime', 'message': err, 'line': 0})
            result['status'] = 'Error'
            return result
    except Exception as e:
        result['errors'].append({'type': 'Runtime', 'message': f"Unexpected interpreter error: {e}", 'line': 0})
        result['status'] = 'Error'
        return result
        
    return result

def execute_cli(file_path):
    """Executes a DostLang file from the command line."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
        
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
        
    print(f"Executing '{file_path}'...\n")
    res = run_pipeline(source_code)
    
    # Write execution to history DB
    tokens_str = "\n".join(f"{t['type']}: {t['value']}" for t in res['tokens'])
    database.log_execution(
        source_code=source_code,
        output=res['output'],
        tokens=tokens_str,
        ir_code=res['ir_code'],
        status=res['status'],
        errors_list=res['errors']
    )
    
    if res['status'] == 'Error':
        print("--- Execution Failed ---")
        for err in res['errors']:
            print(f"[{err['type']} Error] {err['message']}")
        sys.exit(1)
    else:
        print("--- Program Output ---")
        print(res['output'])
        print("\n--- Intermediate Representation (IR) ---")
        print(res['ir_code'])
        print("\nStatus: Execution Successful!")

def main():
    if len(sys.argv) > 1:
        # CLI Mode
        execute_cli(sys.argv[1])
    else:
        # GUI Mode
        print("Launching DostLang IDE...")
        try:
            import gui
            gui.launch_ide()
        except ImportError as e:
            print(f"Error launching GUI: {e}")
            print("Make sure gui.py is in the current directory.")

if __name__ == '__main__':
    main()
