from http.server import HTTPServer, BaseHTTPRequestHandler
import json, requests
from pathlib import Path
from datetime import datetime

EMAIL_FILE = Path("/root/.openclaw/workspace/.state/cleverdogmethod-emails.json")

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(length))
        
        emails = []
        if EMAIL_FILE.exists():
            emails = json.load(open(EMAIL_FILE))
        
        entry = {**data, 'timestamp': datetime.now().isoformat()}
        emails.append(entry)
        
        EMAIL_FILE.parent.mkdir(exist_ok=True)
        json.dump(emails, open(EMAIL_FILE, 'w'), indent=2)
        
        # Telegram
        try:
            requests.post(
                "https://api.telegram.org/bot8318289285:AAGFvnbGoLh0uXO9Rcz9N23iW25DEYh-BBU/sendMessage",
                json={'chat_id': '8116230130', 'text': f"📧 {data['email']}\n📁 {data['resource']}"},
                timeout=3
            )
        except: pass
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'ok': True}).encode())
        print(f"✅ {data['email']}")
    
    def log_message(self, *args): pass

HTTPServer(('0.0.0.0', 8888), Handler).serve_forever()
