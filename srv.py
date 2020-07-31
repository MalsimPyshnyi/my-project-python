import os
import socketserver
from http.server import SimpleHTTPRequestHandler

PORT = int(os.getenv("PORT", 8000))
print(PORT)

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self): #метод, в котором мы задаем условия
        content = f"""
        <html>
        <head>
        <title>XXX</title>
        </head>
        <body>
        <h1>Hello world</h1> 
        <p>path: {self.path}</p>
        <p>x: {}</p>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html") #Заголовки = устанавливаем тип
        self.send_header("Content-length", str(len(content))) #Заголовки = устанавливаем длину и задаем тип символы
        self.end_headers() #обязательна пустая строкаа вставляется - разобраться
        self.wfile.write(content.encode()) #Записываем файл

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("it" + " works")
        httpd.serve_forever(poll_interval=1)
