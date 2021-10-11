from __future__ import annotations
import os
from subprocess import PIPE, Popen
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any


class ServerException(Exception):
    pass


# Cases for request handling

class BaseCase(object):
    def handle_file(self, handler: RequestHandler, full_path: str):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            handler.send_content(content)
        except IOError as msg:
            msg_str = f'{full_path} cannot be read: {msg}'
            handler.handle_error(msg_str)

    def index_path(self, handler: RequestHandler):
        return os.path.join(handler.full_path, 'index.html')

    def test(self, handler: RequestHandler):
        assert False, 'Not implemented'

    def act(self, handler: RequestHandler):
        assert False, 'Not implemented'


class CaseNoFile(BaseCase):
    def test(self, handler: RequestHandler):
        return not os.path.exists(handler.full_path)

    def act(self, handler: RequestHandler):
        return ServerException(f'{handler.path} not found')


class CaseExistingFile(BaseCase):
    def test(self, handler: RequestHandler):
        return os.path.isfile(handler.full_path)

    def act(self, handler: RequestHandler):
        self.handle_file(handler, handler.full_path)


class CaseAlwaysFail(BaseCase):
    def test(self, handler: RequestHandler):
        return True

    def act(self, handler: RequestHandler):
        return ServerException(f'Unknown object {handler.path}')


class CaseDirectoryIndexFile(BaseCase):
    def test(self, handler: RequestHandler):
        return os.path.isdir(handler.full_path) and \
            os.path.isfile(self.index_path(handler))

    def act(self, handler: RequestHandler):
        return self.handle_file(handler, self.index_path(handler))


class CaseDirectoryNoIndexFile(CaseDirectoryIndexFile):
    LISTING_PAGE = '''
        <html>
        <body>
        <ul>
        {0}
        </ul>
        </body>
        </html>
    '''

    def test(self, handler: RequestHandler):
        return os.path.isdir(handler.full_path) and \
            not os.path.isfile(self.index_path(handler))

    def act(self, handler: RequestHandler):
        return self.list_dir(handler, handler.full_path)

    def list_dir(self, handler, full_path):
        try:
            entries = os.listdir(full_path)
            bullets = [f'<li>{e}</li>' for e in entries if not e.startswith('.')]
            page = self.LISTING_PAGE.format('\n'.join(bullets))
            handler.send_content(str.encode(page))
        except OSError as msg:
            msg_str = f'{self.path} cannot be listen: {msg}'
            handler.handle_error(msg_str)


class CaseCGIFile(BaseCase):
    def test(self, handler: RequestHandler):
        return os.path.isfile(handler.full_path) and \
            handler.full_path.endswith('.py')

    def act(self, handler: RequestHandler):
        return self.run_cgi(handler, handler.full_path)

    def run_cgi(self, handler, full_path):
        popen = Popen(['python', full_path], stdout=PIPE)
        data = popen.stdout.read()
        handler.send_content(data)

# Request handler that handles every request


class RequestHandler(BaseHTTPRequestHandler):
    ERROR_PAGE = '''
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
    '''

    cases = [CaseNoFile(),
             CaseCGIFile(),
             CaseExistingFile(),
             CaseDirectoryIndexFile(),
             CaseDirectoryNoIndexFile(),
             CaseAlwaysFail()]

    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path

            for case in self.cases:
                handler = case
                if handler.test(self):
                    handler.act(self)
                    break
        except Exception as msg:
            self.handle_error(msg)

    def send_content(self, content: bytes, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def handle_error(self, msg: Any):
        content = self.ERROR_PAGE.format(path=self.path, msg=msg)
        self.send_content(str.encode(content), 404)


if __name__ == '__main__':
    server_addr = ('', 8080)
    server = HTTPServer(server_addr, RequestHandler)
    server.serve_forever()
