#!/usr/bin/env python3
"""
Simple HTTP server to receive email captures from n8n
Runs on port 9999, saves to JSON file
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path
from datetime import datetime
import urllib.parse

EMAIL_FILE = Path("/root/.openclaw/workspace/.state/cleverdogmethod-emails.json")

class EmailHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        if self.path == '/save-email':
            # Read POST data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse form data
                params = urllib.parse.parse_qs(post_data.decode('utf-8'))
                
                email_data = {
                    'email': params.get('email', [''])[0],
                    'resource': params.get('resource', [''])[0],
                    'page': params.get('page', [''])[0],
                    'source': params.get('source', [''])[0],
                    'timestamp': params.get('timestamp', [''])[0],
                    'captured_at': datetime.now().isoformat()
                }
                
                # Load existing
                emails = []
                if EMAIL_FILE.exists():
                    with open(EMAIL_FILE, 'r') as f:
                        emails = json.load(f)
                
                # Check duplicate
                is_duplicate = any(e['email'] == email_data['email'] for e in emails)
                
                if not is_duplicate:
                    emails.append(email_data)
                    
                    # Save
                    EMAIL_FILE.parent.mkdir(exist_ok=True)
                    with open(EMAIL_FILE, 'w') as f:
                        json.dump(emails, f, indent=2)
                    
                    print(f"✅ Saved: {email_data['email']} → {email_data['resource']}")
                else:
                    print(f"⚠️  Duplicate: {email_data['email']}")
                
                # Response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': True,
                    'is_new': not is_duplicate,
                    'total': len(emails)
                }).encode())
                
            except Exception as e:
                print(f"❌ Error: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 9999), EmailHandler)
    print("🚀 Email Storage Server running on port 9999")
    print(f"📁 Saving to: {EMAIL_FILE}")
    print("="*60)
    server.serve_forever()
