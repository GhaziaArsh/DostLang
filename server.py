import os
import json
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Import DostLang pipeline
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import main

class DostLangRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/run':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                code = data.get('code', '')
                
                # We can mock a simple interactive input if needed, or run standard pipeline
                # For now, let's run the standard pipeline.
                # If there's input, we could support a step-by-step or predefined inputs list,
                # but standard non-blocking execution is default.
                result = main.run_pipeline(code)
                
                # Make AST serializeable by converting representation to string if it is not serializable
                if result.get('ast'):
                    result['ast_str'] = repr(result['ast'])
                    # Remove non-serializable AST node object
                    result['ast'] = None
                
                # Convert symbols table to list of serializable dicts
                if 'symbol_table' in result and result['symbol_table']:
                    symbols = []
                    for sym in result['symbol_table'].get_all_symbols():
                        symbols.append({
                            'name': sym.name,
                            'sym_type': sym.sym_type,
                            'scope': sym.scope,
                            'value': str(sym.value),
                            'line': sym.line
                        })
                    result['symbol_table'] = symbols
                else:
                    result['symbol_table'] = []
                
                response_data = json.dumps(result).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Length', str(len(response_data)))
                self.end_headers()
                self.wfile.write(response_data)
                
            except Exception as e:
                import traceback
                error_info = {
                    'status': 'Error',
                    'errors': [{'type': 'System', 'message': f"Server error: {str(e)}\n{traceback.format_exc()}", 'line': 0}],
                    'tokens': [],
                    'ir_code': '',
                    'output': ''
                }
                response_data = json.dumps(error_info).encode('utf-8')
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Length', str(len(response_data)))
                self.end_headers()
                self.wfile.write(response_data)
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        # Support CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def translate_path(self, path):
        # Serve static assets from 'web' directory
        root = os.path.join(os.getcwd(), 'web')
        # SimpleHTTPRequestHandler by default uses cwd. Let's map request path relative to root.
        if path.startswith('/'):
            path = path[1:]
        # Prevent directory traversal
        parts = path.split('/')
        if '..' in parts:
            return None
        return os.path.join(root, *parts)

def run(port=8000):
    # Ensure web directory exists
    os.makedirs('web', exist_ok=True)
    server_address = ('', port)
    httpd = HTTPServer(server_address, DostLangRequestHandler)
    print(f"DostLang Playground Server running at http://localhost:{port} ...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()

if __name__ == '__main__':
    run()
