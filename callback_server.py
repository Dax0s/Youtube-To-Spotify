from json_manager import JsonManager

from http.server import HTTPServer, BaseHTTPRequestHandler
import threading


class Serv(BaseHTTPRequestHandler):
    code = ''

    def do_GET(self):
        if '/callback?c' in self.path:
            self.code = self.path[15:]

            code_json = {"code": self.code}

            JsonManager.dump_into_json_file('jsons/code.json', code_json)
            JsonManager.move_code_to_ploads('jsons/ploads.json', 'jsons/code.json')

            HttpServer.shutdown_server()

        elif '/callback?e' in self.path:
            print("Error: Access Denied")
            HttpServer.shutdown_server()




class HttpServer():
    code = ''

    httpd = HTTPServer(('localhost', 8000), Serv)
    shutdown_thread = threading.Thread(target=httpd.shutdown)

    @classmethod
    def start_server(cls):
        cls.httpd.serve_forever()

    @classmethod
    def shutdown_server(cls):
        cls.shutdown_thread.start()