''' Server test '''
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT_NUMBER = 50001
HOST = '127.0.0.1'

#This class will handles any incoming request from
#the browser
class MyHandler(BaseHTTPRequestHandler):
    ''' server class '''

	#Handler for the GET requests
    def do_GET(self):
        ''' get action '''
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(b"Hello World !")

try:
	#Create a web server and define the handler to manage the
	#incoming request
    SERVER = HTTPServer((HOST, PORT_NUMBER), MyHandler)
    print(f'Started httpserver on {HOST} with port on {PORT_NUMBER} ')

	#Wait forever for incoming htto requests
    SERVER.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    SERVER.socket.close()
