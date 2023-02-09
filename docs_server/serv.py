
import io
import os
import sys
import shutil
import webbrowser
from pathlib import Path
from textwrap import dedent
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler

auto_reload_source = bytes()

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self._modify_html = False
        super().__init__(*args, directory=str(Path(sys.argv[2]).resolve()), **kwargs)

    def do_GET(self, *args, **kwargs):
        global auto_reload_source
        if (self.path.endswith('.html') or (self.path.find('.html?') > 0) or
            self.path.endswith('.htm') or (self.path.find('.htm?') > 0)):
            try:
                self._modify_html = True
                old = self.wfile
                self.wfile = io.BytesIO()
                res = super().do_GET(*args, **kwargs)
                buf = self.wfile.getbuffer().tobytes()
                buf = buf.replace(b'</body>', auto_reload_source + b'</body>')
                old.write(buf)
                return res
            finally:
                self._modify_html = False
        else:
            return super().do_GET(*args, **kwargs)

    def send_header(self, keyword, value):
        global auto_reload_source
        if self._modify_html and (keyword.lower() == 'content-length'):
            value = str(int(value) + len(auto_reload_source))
        return super().send_header(keyword, value)

    def log_message(self, format, *args, **kwargs):
        pass

def main():
    global auto_reload_source
    if len(sys.argv) != 3:
        print(f'Usage: {sys.executable} {sys.argv[0]} <port> <directory> ')
        exit(1)
    source = (Path(__file__).parent / 'auto_reload.js').read_bytes()
    auto_reload_source = b'<script>' + source + b'</script>'
    with HTTPServer(('localhost', int(sys.argv[1])), MyHTTPRequestHandler) as server:
        webbrowser.open(f'http://localhost:{server.server_port}/')
        server.serve_forever()

if __name__ == '__main__':
    exit(main() or 0)
