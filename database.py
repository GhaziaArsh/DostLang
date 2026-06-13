"""
database.py - SQLite Database for DostLang execution history and errors
========================================================================

Handles persistence of code executions, tokens, intermediate representation (IR),
program output, execution status, and detailed compile-time/runtime errors.
"""

import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dostlang.db")

def init_db():
    """Initialize the SQLite database and create schemas if not exists."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Executions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS executions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_code TEXT,
        output TEXT,
        tokens TEXT,
        ir_code TEXT,
        status TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Errors table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS errors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        execution_id INTEGER,
        error_type TEXT,
        message TEXT,
        line_number INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (execution_id) REFERENCES executions(id)
    );
    """)
    
    conn.commit()
    conn.close()

def log_execution(source_code, output, tokens, ir_code, status, errors_list=None):
    """
    Log a DostLang execution run and any associated errors.
    
    Args:
        source_code (str): Raw DostLang code
        output (str): Captured program output
        tokens (str): Serialized token stream or text representation
        ir_code (str): Three-address code listing
        status (str): 'Success' or 'Error'
        errors_list (list[dict]): List of error dicts, each with keys 'type', 'message', 'line'
        
    Returns:
        int: The generated execution ID.
    """
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO executions (source_code, output, tokens, ir_code, status)
    VALUES (?, ?, ?, ?, ?)
    """, (source_code, output, tokens, ir_code, status))
    
    execution_id = cursor.lastrowid
    
    if errors_list:
        for err in errors_list:
            cursor.execute("""
            INSERT INTO errors (execution_id, error_type, message, line_number)
            VALUES (?, ?, ?, ?)
            """, (execution_id, err.get('type', 'Unknown'), err.get('message', ''), err.get('line', 0)))
            
    conn.commit()
    conn.close()
    return execution_id

def get_history():
    """Retrieve execution history sorted by newest first."""
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, source_code, output, status, timestamp FROM executions ORDER BY id DESC")
    rows = cursor.fetchall()
    
    history = []
    for r in rows:
        history.append({
            'id': r[0],
            'source_code': r[1],
            'output': r[2],
            'status': r[3],
            'timestamp': r[4]
        })
    conn.close()
    return history
