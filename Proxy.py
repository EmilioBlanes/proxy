import socketserver
import http.server
import urllib.request

PORT = 9012

class Proxy(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        url = self.path[1:]
        try:
            with urllib.request.urlopen(url) as respuesta:
                datos = respuesta.read()
                self.send_response(200)
                self.send_header('Content-Type', respuesta.getheader('Content-Type'))
                self.send_header('Content-Length', len(datos))
                self.end_headers()
                self.wfile.write(datos)
        except Exception as a:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(a).encode())


httpd = socketserver.ThreadingTCPServer(('localhost',PORT),Proxy)
print("Escuchando en puerto" , str(PORT))
httpd.serve_forever()

