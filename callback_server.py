import json_manager

from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class Serv(BaseHTTPRequestHandler):
    code = ''

    def do_GET(self):
        if '/callback?c' in self.path:
            self.code = self.path[15:]

            code_json = {"code": self.code}

            json_manager.JsonManager.dump_into_json_file('jsons/code.json', code_json)
            json_manager.JsonManager.move_code_to_ploads('jsons/code.json', 'jsons/ploads.json')

            HttpServer.shutdown_server()

        elif '/callback?e' in self.path:
            print("Error: Access Denied")
            HttpServer.shutdown_server()




class HttpServer():
    code = ''

    httpd = HTTPServer(('localhost', 8000), Serv)
    server_thread = threading.Thread(target=httpd.serve_forever)

    @classmethod
    def start_server(cls):
        cls.httpd.serve_forever()

    @classmethod
    def shutdown_server(cls):
        raise SystemExit()