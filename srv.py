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

        self.send_respond(content) #используем аргумень контент и значение оттуда подставляется

    def handle_404(self):
        msg = """NOT FOUND!!!!!!!"""

        self.send_respond(msg, сode=404)

    def respond(self, message,code=200):  #функция которая будет передаватьяс в 404, 200 и так длаее
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", str(len(content)))
        self.end_headers()
        self.wfile.write(message.encode())

    def do_GET(self): #метод, в котором мы задаем условия
        path = self.build_path() # Тут не очень понял

        if self.path == "/":
            self.handle_root() #вызываем  функцию, что хотим показывать
        elif self.path == "/hello/": #elif значит, что образуется  цепочка и если  на первом iF выполниться, то  мы не выйдем, а если не выполнится - то выйдем из условия
            self.handle_hello() #вызываем  функцию, что хотим показывать
        else:
            self.handle_404() #вызываем  функцию, что хотим показывать

    def build_path(self) -> str: #разобраться, -> подсказка типа - в данном случае возврат данных строка
        result = self.path #тут оператор присваивания, нужно понять что такое self.path

        if self.path[-1] != "/": #Говорим, что тут мы доставляем / . Последний символ -1 не равно /, то доставляем /
            result = f"{result}/" #показываем результат со слешем
        return result #иначе мы просто показываем путь со слэшем

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("it" + " works")
        httpd.serve_forever(poll_interval=1)
