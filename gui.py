"""
gui.py - Modern Dark-Themed IDE for DostLang
============================================

Implements a feature-rich graphical user interface for DostLang.
Features:
- Syntax highlighting editor with real-time line numbers
- Integrated toolbar (New, Open, Save, Run, Clear, View History)
- Tabbed workspace showing: Output, Tokens, AST/Graphviz, Symbol Table, IR Code, Error Logs, History
- Custom input handling for the `pocho` instruction
- Database and file integration
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk

# Import compiler pipeline
from lexer import DostLexer
from parser import DostParser
from semantic import SemanticAnalyzer
from ir_generator import IRGenerator
from interpreter import Interpreter
from visualizer import ASTVisualizer
import database
import main

class TextLineNumbers(tk.Canvas):
    """Draws line numbers for the associated text widget."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textwidget = None

    def associate(self, textwidget):
        self.textwidget = textwidget

    def redraw(self, *args):
        self.delete("all")
        if not self.textwidget:
            return

        i = self.textwidget.index("@0,0")
        while True :
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="#7a7a7a", font=("Consolas", 11))
            i = self.textwidget.index("%s+1line" % i)

class CustomText(tk.Text):
    """Text widget with scroll and change tracking."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        try:
            cmd = (self._orig,) + args
            result = self.tk.call(cmd)
            # Generate event on changes that affect line layout
            if args[0] in ("insert", "delete", "replace") or \
               args[0] in ("xview", "yview") or \
               (len(args) > 1 and args[1] in ("moveto", "scroll")):
                self.event_generate("<<Change>>", when="tail")
            return result
        except Exception:
            return None

class DostIDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DostLang Compiler & IDE")
        self.geometry("1100x750")
        
        # Dark Theme Palette
        self.bg_color = "#1e1e1e"
        self.fg_color = "#f5f5f5"
        self.accent_color = "#4a90e2"
        self.panel_bg = "#252526"
        self.editor_bg = "#1e1e1e"
        
        self.configure(bg=self.bg_color)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background=self.bg_color, foreground=self.fg_color, font=("Segoe UI", 10))
        self.style.configure('TNotebook', background=self.panel_bg, borderwidth=0)
        self.style.configure('TNotebook.Tab', background=self.bg_color, foreground=self.fg_color, borderwidth=0, padding=(10, 4))
        self.style.map('TNotebook.Tab', background=[('selected', self.panel_bg)], foreground=[('selected', self.accent_color)])
        self.style.configure('TButton', background='#333333', foreground=self.fg_color, borderwidth=0, padding=(8, 4))
        self.style.map('TButton', background=[('active', self.accent_color)])
        
        self.current_file = None
        
        self._build_menu()
        self._build_toolbar()
        self._build_main_pane()
        self._build_status_bar()
        
        # Initialize Database
        database.init_db()
        
        # Initial empty document setup
        self.new_file()

    def _build_menu(self):
        menubar = tk.Menu(self, bg=self.panel_bg, fg=self.fg_color, activebackground=self.accent_color)
        
        filemenu = tk.Menu(menubar, tearoff=0, bg=self.panel_bg, fg=self.fg_color)
        filemenu.add_command(label="New (Naya)", command=self.new_file, accelerator="Ctrl+N")
        filemenu.add_command(label="Open (Kholo)", command=self.open_file, accelerator="Ctrl+O")
        filemenu.add_command(label="Save (Mahfooz)", command=self.save_file, accelerator="Ctrl+S")
        filemenu.add_command(label="Save As...", command=self.save_as_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        
        runmenu = tk.Menu(menubar, tearoff=0, bg=self.panel_bg, fg=self.fg_color)
        runmenu.add_command(label="Run Program (Chalao)", command=self.run_program, accelerator="F5")
        
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Run", menu=runmenu)
        self.config(menu=menubar)
        
        # Bindings
        self.bind("<Control-n>", lambda e: self.new_file())
        self.bind("<Control-o>", lambda e: self.open_file())
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<F5>", lambda e: self.run_program())

    def _build_toolbar(self):
        toolbar = tk.Frame(self, bg=self.panel_bg, height=40)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Toolbar buttons
        btn_config = {"bg": "#333333", "fg": "white", "relief": "flat", "padx": 10, "pady": 4, "activebackground": self.accent_color}
        
        self.new_btn = tk.Button(toolbar, text="📄 New", command=self.new_file, **btn_config)
        self.new_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.open_btn = tk.Button(toolbar, text="📂 Open", command=self.open_file, **btn_config)
        self.open_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.save_btn = tk.Button(toolbar, text="💾 Save", command=self.save_file, **btn_config)
        self.save_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.run_btn = tk.Button(toolbar, text="▶ Run", command=self.run_program, bg="#2d7a3e", fg="white", relief="flat", padx=12, pady=4, activebackground=self.accent_color)
        self.run_btn.pack(side=tk.LEFT, padx=15, pady=5)
        
        self.clear_btn = tk.Button(toolbar, text="🧹 Clear Output", command=self.clear_output, **btn_config)
        self.clear_btn.pack(side=tk.LEFT, padx=5, pady=5)

    def _build_main_pane(self):
        # Vertical split
        self.main_split = tk.PanedWindow(self, orient=tk.VERTICAL, bg=self.bg_color, sashwidth=4)
        self.main_split.pack(fill=tk.BOTH, expand=True)
        
        # Top split (Horizontal split for Editor & Sidebar)
        self.top_split = tk.PanedWindow(self.main_split, orient=tk.HORIZONTAL, bg=self.bg_color, sashwidth=4)
        
        # Editor Pane
        editor_frame = tk.Frame(self.top_split, bg=self.editor_bg)
        
        # Line numbers
        self.line_numbers = TextLineNumbers(editor_frame, width=35, bg=self.panel_bg, bd=0, highlightthickness=0)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Text Editor Widget
        self.editor = CustomText(editor_frame, bg=self.editor_bg, fg=self.fg_color, insertbackground="white",
                                 font=("Consolas", 11), wrap=tk.NONE, bd=0, highlightthickness=0)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        vsb = tk.Scrollbar(editor_frame, orient=tk.VERTICAL, command=self.editor.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb = tk.Scrollbar(editor_frame, orient=tk.HORIZONTAL, command=self.editor.xview)
        # HSB needs to expand below editor, so we use pack carefully
        self.editor.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.line_numbers.associate(self.editor)
        
        # Events
        self.editor.bind("<<Change>>", self._on_editor_change)
        self.editor.bind("<Configure>", lambda e: self.line_numbers.redraw())
        self.editor.bind("<KeyRelease>", self._highlight_syntax)
        
        editor_frame.pack(fill=tk.BOTH, expand=True)
        self.top_split.add(editor_frame, minsize=400)
        
        # Bottom tab panels
        self.bottom_tabs = ttk.Notebook(self.main_split)
        
        # Tab 1: Output
        self.output_text = tk.Text(self.bottom_tabs, bg=self.panel_bg, fg="#a8ffb2", font=("Consolas", 10), state=tk.DISABLED, bd=0)
        self.bottom_tabs.add(self.output_text, text="Output (Dikhao)")
        
        # Tab 2: Tokens
        self.token_tree = ttk.Treeview(self.bottom_tabs, columns=("Type", "Value", "Line", "Position"), show='headings')
        self.token_tree.heading("Type", text="Token Type")
        self.token_tree.heading("Value", text="Lexeme / Value")
        self.token_tree.heading("Line", text="Line")
        self.token_tree.heading("Position", text="Position")
        self.token_tree.column("Type", width=150)
        self.token_tree.column("Value", width=200)
        self.token_tree.column("Line", width=60)
        self.token_tree.column("Position", width=80)
        self.bottom_tabs.add(self.token_tree, text="Tokens Stream")
        
        # Tab 3: AST graph Image
        self.ast_frame = tk.Frame(self.bottom_tabs, bg=self.panel_bg)
        self.ast_canvas = tk.Canvas(self.ast_frame, bg=self.panel_bg, bd=0, highlightthickness=0)
        self.ast_canvas.pack(fill=tk.BOTH, expand=True)
        self.bottom_tabs.add(self.ast_frame, text="AST Viewer")
        
        # Tab 4: Symbol Table
        self.symbol_tree = ttk.Treeview(self.bottom_tabs, columns=("Name", "Type", "Scope", "Value", "Line"), show='headings')
        self.symbol_tree.heading("Name", text="Identifier")
        self.symbol_tree.heading("Type", text="Type")
        self.symbol_tree.heading("Scope", text="Scope")
        self.symbol_tree.heading("Value", text="Current Value")
        self.symbol_tree.heading("Line", text="Line Declared")
        self.bottom_tabs.add(self.symbol_tree, text="Symbol Table")
        
        # Tab 5: IR Code
        self.ir_text = tk.Text(self.bottom_tabs, bg=self.panel_bg, fg="#e5c07b", font=("Consolas", 10), state=tk.DISABLED, bd=0)
        self.bottom_tabs.add(self.ir_text, text="IR (3-Address Code)")
        
        # Tab 6: Error Logs
        self.error_text = tk.Text(self.bottom_tabs, bg=self.panel_bg, fg="#ff6b6b", font=("Consolas", 10), state=tk.DISABLED, bd=0)
        self.bottom_tabs.add(self.error_text, text="Error Log")
        
        # Tab 7: Exec History
        self.history_tree = ttk.Treeview(self.bottom_tabs, columns=("ID", "Code", "Output", "Status", "Time"), show='headings')
        self.history_tree.heading("ID", text="ID")
        self.history_tree.heading("Code", text="Snippet")
        self.history_tree.heading("Output", text="Output")
        self.history_tree.heading("Status", text="Status")
        self.history_tree.heading("Time", text="Timestamp")
        self.history_tree.column("ID", width=40)
        self.history_tree.column("Code", width=250)
        self.history_tree.column("Output", width=250)
        self.history_tree.column("Status", width=85)
        self.history_tree.column("Time", width=120)
        self.history_tree.bind("<Double-1>", self._load_history_item)
        self.bottom_tabs.add(self.history_tree, text="Database History")
        
        self.main_split.add(self.top_split, minsize=250)
        self.main_split.add(self.bottom_tabs, minsize=200)

    def _build_status_bar(self):
        self.status_bar = tk.Label(self, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg=self.panel_bg, fg=self.fg_color)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.editor.bind("<KeyRelease>", self._update_status_cursor, add="+")
        self.editor.bind("<ButtonRelease>", self._update_status_cursor)

    def _update_status_cursor(self, event=None):
        cursor_pos = self.editor.index(tk.INSERT)
        line, col = cursor_pos.split(".")
        filename = os.path.basename(self.current_file) if self.current_file else "Untitled"
        self.status_bar.config(text=f"File: {filename}   |   Line: {line}  Col: {col}   |   Editor Mode: DostLang")

    def _on_editor_change(self, event):
        self.line_numbers.redraw()

    # --- Syntax Highlighting ---
    def _highlight_syntax(self, event=None):
        # Clear tags
        for tag in self.editor.tag_names():
            if tag != "sel":
                self.editor.tag_remove(tag, "1.0", tk.END)
                
        # Setup tag colors
        # HSL Tailored Palettes
        self.editor.tag_configure("KEYWORD", foreground="#56b6c2", font=("Consolas", 11, "bold"))
        self.editor.tag_configure("LITERAL_NUM", foreground="#d19a66")
        self.editor.tag_configure("LITERAL_STR", foreground="#98c379")
        self.editor.tag_configure("COMMENT", foreground="#5c6370", font=("Consolas", 11, "italic"))
        self.editor.tag_configure("DELIMITER", foreground="#abb2bf")
        
        # DostLang Keywords
        keywords = {
            'shuru', 'khatam', 'rakho', 'dikhao', 'pocho', 'agar',
            'warna', 'jabtak', 'kaam', 'wapas', 'sach', 'jhoot',
            'aur', 'ya', 'nahi'
        }
        
        content = self.editor.get("1.0", tk.END)
        
        # Multi-line comment highlighting
        import re
        for m in re.finditer(r'\#\#\#[\s\S]*?\#\#\#', content):
            start = self.editor.index(f"1.0 + {m.start()} chars")
            end = self.editor.index(f"1.0 + {m.end()} chars")
            self.editor.tag_add("COMMENT", start, end)
            
        # Single line comment highlighting
        for m in re.finditer(r'\#[^\n]*', content):
            start = self.editor.index(f"1.0 + {m.start()} chars")
            end = self.editor.index(f"1.0 + {m.end()} chars")
            self.editor.tag_add("COMMENT", start, end)
            
        # Strings highlighting
        for m in re.finditer(r'"[^"]*"', content):
            start = self.editor.index(f"1.0 + {m.start()} chars")
            end = self.editor.index(f"1.0 + {m.end()} chars")
            self.editor.tag_add("LITERAL_STR", start, end)

        # Words & numbers
        for m in re.finditer(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b|\b\d+(\.\d+)?\b', content):
            word = m.group(0)
            start = self.editor.index(f"1.0 + {m.start()} chars")
            end = self.editor.index(f"1.0 + {m.end()} chars")
            
            # Check comment status to avoid overriding comments
            tag_names = self.editor.tag_names(start)
            if "COMMENT" in tag_names or "LITERAL_STR" in tag_names:
                continue
                
            if word in keywords:
                self.editor.tag_add("KEYWORD", start, end)
            elif word.replace('.', '', 1).isdigit():
                self.editor.tag_add("LITERAL_NUM", start, end)

    # --- Document Actions ---
    def new_file(self):
        self.editor.delete("1.0", tk.END)
        # Load a default sample template
        template = (
            "shuru\n"
            "    # DostLang Program\n"
            "    rakho name = \"Dost\";\n"
            "    dikhao(\"Assalam-o-Alaikum,\", name);\n"
            "khatam\n"
        )
        self.editor.insert("1.0", template)
        self.current_file = None
        self._highlight_syntax()
        self._update_status_cursor()
        self._load_executions_history()

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("DostLang Source", "*.dost"), ("Text Files", "*.txt"), ("All Files", "*.*")])
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                code = f.read()
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", code)
            self.current_file = path
            self._highlight_syntax()
            self._update_status_cursor()

    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(self.editor.get("1.0", tk.END))
            messagebox.showinfo("Saved", "File saved successfully!")
        else:
            self.save_as_file()

    def save_as_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".dost", filetypes=[("DostLang Source", "*.dost")])
        if path:
            self.current_file = path
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.editor.get("1.0", tk.END))
            self._update_status_cursor()
            messagebox.showinfo("Saved", "File saved successfully!")

    def clear_output(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        
        self.error_text.config(state=tk.NORMAL)
        self.error_text.delete("1.0", tk.END)
        self.error_text.config(state=tk.DISABLED)

    # --- Execution and Compiler Integration ---
    def run_program(self):
        self.clear_output()
        self.bottom_tabs.select(0) # Select output tab
        
        code = self.editor.get("1.0", tk.END).strip()
        if not code:
            return
            
        # Input dialog callback for the compiler's `pocho` instruction
        def gui_input(prompt):
            val = simpledialog.askstring("Input Needed (Pocho)", prompt, parent=self)
            return val or ""
            
        self.status_bar.config(text="Running compile pipeline...")
        self.update_idletasks()
        
        # Execute pipeline
        res = main.run_pipeline(code, input_func=gui_input)
        
        # 1. Update Output
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, res['output'])
        self.output_text.config(state=tk.DISABLED)
        
        # 2. Update Token list view
        self.token_tree.delete(*self.token_tree.get_children())
        for tok in res['tokens']:
            self.token_tree.insert("", tk.END, values=(tok['type'], tok['value'], tok['lineno'], tok['lexpos']))
            
        # 3. Update Symbol Table view
        self.symbol_tree.delete(*self.symbol_tree.get_children())
        if 'symbol_table' in res:
            for sym in res['symbol_table'].get_all_symbols():
                self.symbol_tree.insert("", tk.END, values=(sym.name, sym.sym_type, sym.scope, str(sym.value), sym.line))
                
        # 4. Update IR Code view
        self.ir_text.config(state=tk.NORMAL)
        self.ir_text.delete("1.0", tk.END)
        self.ir_text.insert(tk.END, res['ir_code'])
        self.ir_text.config(state=tk.DISABLED)
        
        # 5. Update AST Canvas (Graphviz Rendering)
        if res['ast']:
            viz = ASTVisualizer()
            img_path = viz.generate_ast_graph(res['ast'])
            if img_path and os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    # Resize to fit canvas roughly
                    img.thumbnail((450, 450))
                    self.ast_image = ImageTk.PhotoImage(img)
                    self.ast_canvas.delete("all")
                    self.ast_canvas.create_image(10, 10, anchor="nw", image=self.ast_image)
                    self.ast_canvas.config(scrollregion=self.ast_canvas.bbox("all"))
                except Exception as ex:
                    print(f"Canvas error loading visualizer: {ex}")
            else:
                self.ast_canvas.delete("all")
                self.ast_canvas.create_text(20, 20, anchor="nw", text="Install Graphviz for AST visualization.\n\nAST AST Structure:\n" + repr(res['ast']), fill="white")
        else:
            self.ast_canvas.delete("all")
            
        # 6. Update Error pane
        self.error_text.config(state=tk.NORMAL)
        if res['status'] == 'Error':
            self.error_text.insert(tk.END, "--- Execution Failed with Errors ---\n")
            for err in res['errors']:
                self.error_text.insert(tk.END, f"[{err['type']} Error] {err['message']}\n")
            self.bottom_tabs.select(5) # Select error tab
        else:
            self.error_text.insert(tk.END, "--- Analysis Completed Successfully! No Errors. ---\n")
            
        if res.get('warnings'):
            self.error_text.insert(tk.END, "\n--- Semantic Warnings ---\n")
            for warn in res['warnings']:
                self.error_text.insert(tk.END, f"[Warning] {warn}\n")
        self.error_text.config(state=tk.DISABLED)
        
        # Log to Database
        tokens_str = "\n".join(f"{t['type']}: {t['value']}" for t in res['tokens'])
        database.log_execution(
            source_code=code,
            output=res['output'],
            tokens=tokens_str,
            ir_code=res['ir_code'],
            status=res['status'],
            errors_list=res['errors']
        )
        
        # Refresh history
        self._load_executions_history()
        
        status_text = "Execution completed successfully!" if res['status'] == 'Success' else "Execution terminated with errors."
        self.status_bar.config(text=status_text)

    # --- History Management ---
    def _load_executions_history(self):
        self.history_tree.delete(*self.history_tree.get_children())
        hist = database.get_history()
        for h in hist:
            code_line = h['source_code'].replace("\n", " ")[:40]
            out_line = h['output'].replace("\n", " ")[:40]
            self.history_tree.insert("", tk.END, values=(h['id'], code_line, out_line, h['status'], h['timestamp']))

    def _load_history_item(self, event):
        item = self.history_tree.focus()
        if not item:
            return
        values = self.history_tree.item(item, 'values')
        exec_id = values[0]
        
        conn = database.sqlite3.connect(database.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT source_code FROM executions WHERE id = ?", (exec_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", row[0])
            self._highlight_syntax()
            self._update_status_cursor()

def launch_ide():
    app = DostIDE()
    app.mainloop()

if __name__ == '__main__':
    launch_ide()
