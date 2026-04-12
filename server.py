import http.server
import urllib.request
import urllib.parse
import os

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/proxy'):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            target = params.get('url', [''])[0]

            if not target.startswith('https://drive.google.com/'):
                self.send_response(403)
                self.end_headers()
                return

            try:
                req = urllib.request.Request(target, headers={
                    'User-Agent': 'Mozilla/5.0'
                })
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = resp.read()
                    ctype = resp.headers.get('Content-Type', 'application/pdf')
                    self.send_response(200)
                    self.send_header('Content-Type', ctype)
                    self.send_header('Content-Length', str(len(data)))
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                self.send_response(502)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            super().do_GET()

    def log_message(self, fmt, *args):
        # 프록시 로그 생략
        path = str(args[0]) if args else ''
        if '/proxy' not in path:
            super().log_message(fmt, *args)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    httpd = http.server.HTTPServer(('', 8888), Handler)
    print('서버 시작 → http://localhost:8888')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n서버 종료')
