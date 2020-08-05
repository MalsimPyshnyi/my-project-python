from http.server import SimpleHTTPRequestHandler

import settings

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self): #метод, в котором мы задаем условия
        path = self.build_path() # Тут не очень понял

        if path == "/":
            self.handle_root() #вызываем  функцию, что хотим показывать
        elif path == "/hello/": #elif значит, что образуется  цепочка и если  на первом iF выполниться, то  мы не выйдем, а если не выполнится - то выйдем из условия
            self.handle_hello() #вызываем  функцию, что хотим показывать
        elif path == "/style/": #путь
            self.handle_style()
        else:
            self.handle_404() #вызываем  функцию, что хотим показывать

    def handle_root(self): #пищем функцию чтобы далее ее вызвать
        return super().do_GET() #обращаемся к родителю

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

        self.respond(content) #используем аргумень контент и значение оттуда подставляется

    def handle_style(self):
        css_file =".settings.PROJECT_DIR" / "style.css" #файл если в папке то "styles" / "styles.css"
        if not css_file.exists():
            return self.handle_404()
        with css_file.open("r") as fp: #открываем файл в роежиме чтения
            css = fp.read()

        self.respond(css, content_type="text/css")

    def handle_404(self):
        msg = """NOT FOUND!!!!!!!"""

        self.respond(msg, code=404, content_type="text/plain")

    def respond(self, message, code=200, content_type="text/html"):  #функция которая будет передаватьяс в 404, 200 и так длаее
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(content)))
        self.send_header("Cache-control", f"max-age={CACHE_AGE}")
        self.end_headers()
        self.wfile.write(message.encode())

        if isinstance(message, str):
            message = message.encode()

    def build_path(self) -> str: #разобраться, -> подсказка типа - в данном случае возврат данных строка
        result = self.path #тут оператор присваивания, нужно понять что такое self.path

        if self.path[-1] != "/": #Говорим, что тут мы доставляем / . Последний символ -1 не равно /, то доставляем /
            result = f"{result}/" #показываем результат со слешем
        return result #иначе мы просто показываем путь со слэше