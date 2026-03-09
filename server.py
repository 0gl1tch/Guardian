"""
Guardian DFIR CLI - Simple HTTP Server
Serves the Guardian application for remote IEX execution

Usage:
    python3 server.py            # Default: http://localhost:8080
    python3 server.py 0.0.0.0 9999   # Custom host and port

Then clients can execute:
    PowerShell: iex(New-Object Net.WebClient).DownloadString('http://your-ip:8080/guardian')
    Bash: curl http://your-ip:8080/guardian | python3
"""

import http.server
import socketserver
import os
import sys
import json
from pathlib import Path


class GuardianHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler for Guardian serving"""
    
    def do_GET(self):
        """Handle GET requests"""
        
        # Routes
        if self.path == '/guardian' or self.path == '/guardian.py':
            self.serve_guardian_python()
        elif self.path == '/guardian.ps1' or self.path == '/loader':
            self.serve_powershell_loader()
        elif self.path == '/info':
            self.serve_info()
        elif self.path == '/':
            self.serve_homepage()
        else:
            self.send_error(404)
    
    def serve_guardian_python(self):
        """Serve the standalone Guardian Python script"""
        guardian_file = Path(__file__).parent / 'guardian_standalone.py'
        
        if not guardian_file.exists():
            self.send_error(404, "guardian_standalone.py not found")
            return
        
        try:
            with open(guardian_file, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', len(content))
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            
            self.wfile.write(content)
            
            # Log access
            print(f"[+] Served Guardian Python to {self.client_address[0]}")
        
        except Exception as e:
            self.send_error(500, str(e))
    
    def serve_powershell_loader(self):
        """Serve pre-configured PowerShell loader"""
        host = self.headers.get('Host', 'localhost:8080')
        protocol = 'https' if self.headers.get('X-Forwarded-Proto') == 'https' else 'http'
        
        loader_script = f"""# PowerShell Guardian DFIR CLI Loader
# Drop-in loader that downloads and executes Guardian

$ErrorActionPreference = 'SilentlyContinue'

Write-Host "🛡️  Guardian DFIR CLI - Loading..." -ForegroundColor Green

# Check Python
try {{
    $null = python3 --version 2>&1
}} catch {{
    Write-Host "[!] Python 3 is required" -ForegroundColor Red
    exit 1
}}

Write-Host "[*] Downloading Guardian..." -ForegroundColor Cyan

try {{
    $webClient = New-Object Net.WebClient
    $pythonCode = $webClient.DownloadString('{protocol}://{host}/guardian')
    $pythonCode | python3
}} catch {{
    Write-Host "[!] Error: $_" -ForegroundColor Red
    exit 1
}}
"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', len(loader_script))
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.end_headers()
        
        self.wfile.write(loader_script.encode('utf-8'))
        print(f"[+] Served PowerShell loader to {self.client_address[0]}")
    
    def serve_info(self):
        """Serve server information and usage instructions"""
        host = self.headers.get('Host', 'localhost:8080')
        protocol = 'https' if self.headers.get('X-Forwarded-Proto') == 'https' else 'http'
        
        info = {
            "name": "Guardian DFIR CLI Server",
            "version": "0.2.0",
            "status": "running",
            "endpoints": {
                "guardian": f"{protocol}://{host}/guardian",
                "guardian_ps1": f"{protocol}://{host}/guardian.ps1",
                "info": f"{protocol}://{host}/info"
            },
            "usage": {
                "windows_powershell": f"iex(New-Object Net.WebClient).DownloadString('{protocol}://{host}/guardian')",
                "linux_bash": f"curl {protocol}://{host}/guardian | python3",
                "macos_bash": f"curl {protocol}://{host}/guardian | python3"
            }
        }
        
        info_json = json.dumps(info, indent=2)
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(info_json))
        self.end_headers()
        
        self.wfile.write(info_json.encode('utf-8'))
        print(f"[+] Served info to {self.client_address[0]}")
    
    def serve_homepage(self):
        """Serve a simple HTML homepage"""
        host = self.headers.get('Host', 'localhost:8080')
        protocol = 'https' if self.headers.get('X-Forwarded-Proto') == 'https' else 'http'
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Guardian DFIR CLI</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #1e1e1e; color: #fff; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        h1 {{ color: #4CAF50; }}
        code {{ background: #2d2d2d; padding: 10px; border-radius: 5px; display: block; margin: 10px 0; overflow-x: auto; }}
        .section {{ margin: 20px 0; }}
        .warning {{ color: #ff9800; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️  Guardian DFIR CLI Server</h1>
        <p>Remote forensic analysis toolkit running.</p>
        
        <div class="section">
            <h2>Windows (PowerShell)</h2>
            <code>iex(New-Object Net.WebClient).DownloadString('{protocol}://{host}/guardian')</code>
        </div>
        
        <div class="section">
            <h2>Linux / macOS (Bash)</h2>
            <code>curl {protocol}://{host}/guardian | python3</code>
        </div>
        
        <div class="section">
            <h2>Available Endpoints</h2>
            <ul>
                <li><a href="/guardian">/guardian</a> - Python standalone script</li>
                <li><a href="/guardian.ps1">/guardian.ps1</a> - PowerShell loader</li>
                <li><a href="/info">/info</a> - Server information (JSON)</li>
            </ul>
        </div>
        
        <div class="section warning">
            <h3>⚠️  Security Notes</h3>
            <ul>
                <li>This server serves remote code execution capabilities</li>
                <li>Deploy only in controlled environments</li>
                <li>Use with proper network segmentation</li>
                <li>Consider using HTTPS in production</li>
                <li>Implement authentication if exposed</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(html))
        self.end_headers()
        
        self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


def run_server(host='0.0.0.0', port=8080):
    """Run the Guardian server"""
    
    handler = GuardianHTTPHandler
    
    with socketserver.TCPServer((host, port), handler) as httpd:
        print(f"🛡️  Guardian DFIR CLI Server Started")
        print(f"┌─ Listening on: {host}:{port}")
        print(f"├─ Windows (PowerShell):")
        print(f"│  iex(New-Object Net.WebClient).DownloadString('http://{host}:{port}/guardian')")
        print(f"├─ Linux/macOS (Bash):")
        print(f"│  curl http://{host}:{port}/guardian | python3")
        print(f"└─ Info endpoint: http://{host}:{port}/info")
        print()
        print("[*] Press Ctrl+C to stop server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[*] Server stopped")


if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
    
    try:
        run_server(host, port)
    except OSError as e:
        print(f"[!] Error: {e}")
        sys.exit(1)
