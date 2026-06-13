// Embed example programs
const EXAMPLES = {
    hello: `shuru
    # DostLang hello world program
    dikhao("Assalam-o-Alaikum, DostLang!");
khatam`,

    variables: `shuru
    # Variable declarations using 'rakho'
    rakho a = 10;
    rakho b = 20.5;
    rakho c = "Hello World";
    rakho d = sach; # True boolean

    # Printing variables
    dikhao("a =", a);
    dikhao("b =", b);
    dikhao("c =", c);
    dikhao("d =", d);

    # Variable assignment update
    a = a + 5;
    dikhao("Updated a =", a);
khatam`,

    arithmetic: `shuru
    rakho x = 10;
    rakho y = 3;

    # Basic arithmetic
    dikhao("Addition:", x + y);
    dikhao("Subtraction:", x - y);
    dikhao("Multiplication:", x * y);
    dikhao("Division:", x / y);
    dikhao("Modulo:", x % y);
    dikhao("Power:", x ^ y);

    # Operator precedence and grouping
    rakho expr1 = x + y * 2; # 10 + 6 = 16
    rakho expr2 = (x + y) * 2; # 13 * 2 = 26
    dikhao("Precedence 1:", expr1);
    dikhao("Precedence 2:", expr2);
khatam`,

    if_else: `shuru
    rakho score = 75;

    # Basic if-else logic
    agar score >= 50 {
        dikhao("Pass! Mubarak ho.");
    } warna {
        dikhao("Fail! Dobara koshish karein.");
    }

    # Nested if conditions
    agar score >= 80 {
        dikhao("Grade: A");
    } warna {
        agar score >= 70 {
            dikhao("Grade: B");
        } warna {
            dikhao("Grade: C or lower");
        }
    }
khatam`,

    while_loop: `shuru
    rakho i = 1;
    
    # Loop from 1 to 5
    jabtak i <= 5 {
        dikhao("Iteration count:", i);
        i = i + 1;
    }
khatam`,

    functions: `shuru
    # Function to calculate sum
    kaam jamah(x, y) {
        wapas x + y;
    }

    # Function without return value
    kaam salam(name) {
        dikhao("Salam,", name);
    }

    # Call functions
    rakho result = jamah(15, 25);
    dikhao("Sum result =", result);

    salam("Ali");
khatam`,

    recursion: `shuru
    # Recursive function for factorial
    kaam factorial(n) {
        agar n <= 1 {
            wapas 1;
        } warna {
            wapas n * factorial(n - 1);
        }
    }

    rakho result = factorial(5);
    dikhao("Factorial of 5 =", result); # Should print 120
khatam`,

    array_test: `shuru
    # Array literal declaration
    rakho arr = [10, 20, 30, 40];

    # Array access
    dikhao("Element at index 0:", arr[0]);
    dikhao("Element at index 2:", arr[2]);

    # Array value update
    arr[1] = 99;
    dikhao("Updated element at index 1:", arr[1]);
    
    # Complete array printing
    dikhao("Entire array:", arr);
khatam`
};

let editorInstance = null;

// Monaco Editor Initialization
require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.39.0/min/vs' } });

require(['vs/editor/editor.main'], function() {
    // Register custom language
    monaco.languages.register({ id: 'dostlang' });

    // Define tokenizer rules
    monaco.languages.setMonarchTokensProvider('dostlang', {
        keywords: [
            'shuru', 'khatam', 'rakho', 'dikhao', 'pocho', 'agar',
            'warna', 'jabtak', 'kaam', 'wapas', 'sach', 'jhoot',
            'aur', 'ya', 'nahi'
        ],
        operators: [
            '=', '>', '<', '!', '==', '<=', '>=', '!=',
            '+', '-', '*', '/', '%', '^'
        ],
        symbols:  /[=><!~?:&|+\-*\/\^%]+/,
        tokenizer: {
            root: [
                // Identifiers and keywords
                [/[a-zA-Z_][a-zA-Z0-9_]*/, {
                    cases: {
                        '@keywords': 'keyword',
                        '@default': 'identifier'
                    }
                }],

                // Whitespace
                { include: '@whitespace' },

                // Numbers
                [/\d+\.\d+/, 'number.float'],
                [/\d+/, 'number'],

                // Strings
                [/"([^"\\]|\\.)*"/, 'string'],

                // Operators and Delimiters
                [/[{}()\[\]]/, '@brackets'],
                [/@symbols/, {
                    cases: {
                        '@operators': 'operator',
                        '@default': ''
                    }
                }],
                [/;/, 'delimiter'],
                [/,/, 'delimiter']
            ],

            whitespace: [
                [/[ \t\r\n]+/, 'white'],
                [/###[\s\S]*?###/, 'comment'], // Multiline comment
                [/#.*$/, 'comment'],            // Single line comment
            ]
        }
    });

    // Custom dark theme configuration
    monaco.editor.defineTheme('dostlang-dark', {
        base: 'vs-dark',
        inherit: true,
        rules: [
            { token: 'keyword', foreground: '56b6c2', fontStyle: 'bold' },
            { token: 'identifier', foreground: 'abb2bf' },
            { token: 'number', foreground: 'd19a66' },
            { token: 'number.float', foreground: 'd19a66' },
            { token: 'string', foreground: '98c379' },
            { token: 'comment', foreground: '5c6370', fontStyle: 'italic' },
            { token: 'operator', foreground: '56b6c2' },
            { token: 'delimiter', foreground: 'abb2bf' }
        ],
        colors: {
            'editor.background': '#161821',
            'editor.foreground': '#abb2bf',
            'editor.lineHighlightBackground': '#1e2230',
            'editorCursor.foreground': '#06b6d4',
            'editorLineNumber.foreground': '#4b5263',
            'editorLineNumber.activeForeground': '#06b6d4'
        }
    });

    // Create Monaco editor instance
    editorInstance = monaco.editor.create(document.getElementById('editor-root'), {
        value: EXAMPLES.hello,
        language: 'dostlang',
        theme: 'dostlang-dark',
        fontSize: 14,
        fontFamily: 'Fira Code, Consolas, monospace',
        automaticLayout: true,
        minimap: { enabled: false },
        scrollbar: {
            verticalScrollbarSize: 8,
            horizontalScrollbarSize: 8
        }
    });
});

// App Flow & Controls UI
document.addEventListener('DOMContentLoaded', () => {
    const landingScreen = document.getElementById('landing-screen');
    const workspaceScreen = document.getElementById('workspace-screen');
    const startEditorBtn = document.getElementById('start-editor-btn');
    const backHomeBtn = document.getElementById('back-home-btn');
    
    const exampleSelect = document.getElementById('example-select');
    const runBtn = document.getElementById('run-btn');
    const clearBtn = document.getElementById('clear-btn');
    const consoleOutput = document.getElementById('console-output');
    const tokensBody = document.getElementById('tokens-body');
    const astOutput = document.getElementById('ast-output');
    const irOutput = document.getElementById('ir-output');
    const symbolTableBody = document.getElementById('symbol-table-body');
    const compilerStatus = document.getElementById('compiler-status');
    const statusDot = document.querySelector('.status-dot');

    // Transitions
    function showWorkspace() {
        landingScreen.classList.add('hidden');
        workspaceScreen.classList.remove('hidden');
        // Force monaco layout update
        if (editorInstance) {
            editorInstance.layout();
        }
    }

    function showLanding() {
        workspaceScreen.classList.add('hidden');
        landingScreen.classList.remove('hidden');
    }

    if (startEditorBtn) {
        startEditorBtn.addEventListener('click', () => {
            showWorkspace();
        });
    }

    if (backHomeBtn) {
        backHomeBtn.addEventListener('click', () => {
            showLanding();
        });
    }

    // View Source dialog
    const viewSourceBtn = document.getElementById('view-source-btn');
    if (viewSourceBtn) {
        viewSourceBtn.addEventListener('click', (e) => {
            e.preventDefault();
            alert(
                "DostLang Compiler Architecture Source Files:\n\n" +
                "1. Lexer (lexer.py) - Tokenizes Urdu/Hindi-inspired keywords.\n" +
                "2. Parser (parser.py) - Builds AST structure from PLY grammar rules.\n" +
                "3. AST (ast_nodes.py) - Definitions for 20 unique AST Node structures.\n" +
                "4. Semantic Analyzer (semantic.py) - Handles scope, arity and type validations.\n" +
                "5. IR Generator (ir_generator.py) - Outputs Three Address Code intermediate representation.\n" +
                "6. Interpreter (interpreter.py) - Execution walks the AST structure.\n" +
                "7. DB Storage (database.py) - Records run records dynamically.\n" +
                "8. Server backend (server.py) - Serves playground API."
            );
        });
    }

    // Modal overlay triggers
    const docsBtn = document.getElementById('docs-btn');
    const docsNavBtn = document.getElementById('docs-nav-btn');
    const docsModal = document.getElementById('docs-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');

    const openDocs = () => {
        if (docsModal) docsModal.classList.remove('hidden');
    };

    if (docsBtn) docsBtn.addEventListener('click', openDocs);
    if (docsNavBtn) docsNavBtn.addEventListener('click', openDocs);

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => {
            if (docsModal) docsModal.classList.add('hidden');
        });
    }

    // Close when clicking outside modal-card content
    if (docsModal) {
        docsModal.addEventListener('click', (e) => {
            if (e.target === docsModal) {
                docsModal.classList.add('hidden');
            }
        });
    }

    // Landing Screen Quick Test Selection
    document.querySelectorAll('.sample-card').forEach(card => {
        card.addEventListener('click', () => {
            const sampleKey = card.getAttribute('data-sample');
            if (EXAMPLES[sampleKey]) {
                if (editorInstance) {
                    editorInstance.setValue(EXAMPLES[sampleKey]);
                }
                if (exampleSelect) exampleSelect.value = sampleKey;
                showWorkspace();
                runCode();
            }
        });
    });

    // Handle Example Loading in Workspace
    if (exampleSelect) {
        exampleSelect.addEventListener('change', (e) => {
            const key = e.target.value;
            if (EXAMPLES[key] && editorInstance) {
                editorInstance.setValue(EXAMPLES[key]);
            }
        });
    }

    // Handle Tab Navigation
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            
            // Remove active classes
            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Add active classes
            btn.classList.add('active');
            const targetTab = document.getElementById(`tab-${tabId}`);
            if (targetTab) targetTab.classList.add('active');
        });
    });

    // Handle Output Clearing
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            if (consoleOutput) consoleOutput.innerHTML = '<span class="system-msg">Console cleared.</span>';
            if (tokensBody) tokensBody.innerHTML = '<tr><td colspan="4" class="empty-table-msg">Run program to see tokens</td></tr>';
            if (astOutput) astOutput.innerText = 'Run program to see Abstract Syntax Tree structure...';
            if (irOutput) irOutput.innerText = 'Run program to see Intermediate Representation (TAC)...';
            if (symbolTableBody) symbolTableBody.innerHTML = '<tr><td colspan="5" class="empty-table-msg">Run program to inspect symbol table</td></tr>';
        });
    }

    // Execute script
    async function runCode() {
        if (!editorInstance) return;

        const code = editorInstance.getValue().strip ? editorInstance.getValue().strip() : editorInstance.getValue().trim();
        if (!code) {
            if (consoleOutput) consoleOutput.innerHTML = '<span class="error-msg">[System] Editor is empty. Type some DostLang code first!</span>';
            return;
        }

        if (compilerStatus) compilerStatus.innerText = 'Running pipeline...';
        if (statusDot) statusDot.className = 'status-dot'; // Reset colors
        
        if (consoleOutput) consoleOutput.innerHTML = '<span class="system-msg">Compiling and running DostLang code...</span>';

        try {
            const response = await fetch('/run', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code })
            });

            if (!response.ok) {
                throw new Error(`HTTP Error status: ${response.status}`);
            }

            const res = await response.json();

            // 1. Process Output
            if (consoleOutput) {
                consoleOutput.innerHTML = '';
                if (res.output) {
                    const outSpan = document.createElement('span');
                    outSpan.className = 'output-stdout';
                    outSpan.innerText = res.output;
                    consoleOutput.appendChild(outSpan);
                }
            }

            // Show execution error inside the console
            if (res.status === 'Error') {
                if (statusDot) statusDot.classList.add('red');
                if (compilerStatus) compilerStatus.innerText = 'Execution Failed';

                res.errors.forEach(err => {
                    const errSpan = document.createElement('span');
                    errSpan.className = 'error-msg';
                    errSpan.innerText = `[${err.type} Error] ${err.message}`;
                    if (consoleOutput) consoleOutput.appendChild(errSpan);
                });
            } else {
                if (statusDot) statusDot.classList.add('green');
                if (compilerStatus) compilerStatus.innerText = 'Success';

                const successSpan = document.createElement('span');
                successSpan.className = 'success-msg';
                successSpan.innerText = '✓ Program execution finished successfully!';
                if (consoleOutput) consoleOutput.appendChild(successSpan);
            }

            // 2. Populate Tokens
            if (tokensBody) {
                if (res.tokens && res.tokens.length > 0) {
                    tokensBody.innerHTML = res.tokens.map(tok => `
                        <tr>
                            <td style="color: #56b6c2; font-weight: 600;">${tok.type}</td>
                            <td style="font-family: var(--font-mono); color: #98c379;">${tok.value !== null ? escapeHtml(tok.value.toString()) : ''}</td>
                            <td>${tok.lineno}</td>
                            <td>${tok.lexpos}</td>
                        </tr>
                    `).join('');
                } else {
                    tokensBody.innerHTML = '<tr><td colspan="4" class="empty-table-msg">No tokens generated</td></tr>';
                }
            }

            // 3. Populate AST
            if (astOutput) {
                if (res.ast_str) {
                    astOutput.innerText = res.ast_str;
                } else {
                    astOutput.innerText = 'No AST generated (Check syntax error logs)';
                }
            }

            // 4. Populate IR Code
            if (irOutput) {
                if (res.ir_code) {
                    irOutput.innerText = res.ir_code;
                } else {
                    irOutput.innerText = 'No IR generated (Check compilation error logs)';
                }
            }

            // 5. Populate Symbol Table
            if (symbolTableBody) {
                if (res.symbol_table && res.symbol_table.length > 0) {
                    symbolTableBody.innerHTML = res.symbol_table.map(sym => `
                        <tr>
                            <td style="font-weight: bold; color: #e5c07b;">${escapeHtml(sym.name)}</td>
                            <td style="color: #c678dd;">${escapeHtml(sym.sym_type)}</td>
                            <td>${escapeHtml(sym.scope)}</td>
                            <td style="font-family: var(--font-mono); color: #98c379;">${escapeHtml(sym.value)}</td>
                            <td>${sym.line}</td>
                        </tr>
                    `).join('');
                } else {
                    symbolTableBody.innerHTML = '<tr><td colspan="5" class="empty-table-msg">Symbol table is empty</td></tr>';
                }
            }

        } catch (error) {
            if (statusDot) statusDot.classList.add('red');
            if (compilerStatus) compilerStatus.innerText = 'Connection Error';
            if (consoleOutput) consoleOutput.innerHTML += `<span class="error-msg">[System Network Error] Could not connect to DostLang compiler. Make sure the backend server is running.\n\nDetails: ${error.message}</span>`;
        }
    }

    if (runBtn) runBtn.addEventListener('click', runCode);

    // Support Keyboard Shortcut: F5 or Ctrl+Enter to Run
    window.addEventListener('keydown', (e) => {
        if (e.key === 'F5' || (e.ctrlKey && e.key === 'Enter')) {
            e.preventDefault();
            runCode();
        }
    });

    // Helper to escape HTML characters
    function escapeHtml(text) {
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});
