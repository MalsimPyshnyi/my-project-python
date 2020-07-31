import os
import socketserver
from http.server import SimpleHTTPRequestHandler

PORT = int(os.getenv("PORT", 8000))
print(PORT)

class MyHandler(SimpleHTTPRequestHandler):
    def handle_root(self): #пищем функцию чтобы далее ее вызвать
        pass

    def handle_hello(self): #пишем также функцию чтобы во втором if ее вызвать
        content = f"""
        <html>
        <head>
        <title>XXX</title>
        </head>
        <body>
        <h1>Hello world</h1> 
        <p>path: {self.path}</p>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html")  # Заголовки = устанавливаем тип
        self.send_header("Content-length", str(len(content)))  # Заголовки = устанавливаем длину и задаем тип символы
        self.end_headers()  # обязательна пустая строкаа вставляется - разобраться
        self.wfile.write(content.encode())  # Записываем файл

    def handle_404(self):
        pass

    def do_GET(self): #метод, в котором мы задаем условия
        if self.path == "/":
            self.handle_root() #вызываем  функцию, что хотим показывать
        elif self.path == "/hello": #elif значит, что образуется  цепочка и если  на первом iF выполниться, то  мы не выйдем, а если не выполнится - то выйдем из условия
            self.handle_hello() #вызываем  функцию, что хотим показывать
        else:
            self.handle_404() #вызываем  функцию, что хотим показывать

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("it" + " works")
        httpd.serve_forever(poll_interval=1)
