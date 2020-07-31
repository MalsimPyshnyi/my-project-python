import os
import socketserver
from http.server import SimpleHTTPRequestHandler

PORT = int(os.getenv("PORT", 8000))
print(PORT)

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self): #метод, в котором мы задаем условия
        content = """
        <html>
        <head>
        <title>XXX</title>
        </head>
        <body>Hello world</body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html") #Заголовки = устанавливаем тип
        self.send_header("Content-length", str(len(content))) #Заголовки = устанавливаем длину и задаем тип символы
        self.end_headers()
        self.wfile.write(content.encode()) #Записываем файл

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("it" + " works")
        httpd.serve_forever(poll_interval=1)