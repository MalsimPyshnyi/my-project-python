import traceback
from http.server import SimpleHTTPRequestHandler
import settings

from errors import MethodNotAllowed
from errors import NotFound
from utils import normalize_path
from utils import to_bytes
from utils import read_static

class MyHttp(SimpleHTTPRequestHandler):
    def do_GET(self): #метод, в котором мы задаем условия
        path = normalize_path(self.path) # self.path - то что нам приходит с браузера

        # try:
        #     path_parts  = path.split("/")
        # except ImportError:
        #     file_path = None
        # file_path = path_parts[2]
        # path = normalize_path(path_parts[1])
       # path = f"/{path}" if path != "/" else path

        handlers = {
            "/": self.handle_root,
            "/hello/": self.handle_hello,
            "/style/": self.handle_style,
            "/images/": self.handle_images,
        }

        try:
            handler = handlers[path]
            handler()
        except (NotFound, KeyError):
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()


    #if path == "/":
            #self.handle_root() #вызываем  функцию, что хотим показывать
        #elif path == "/hello/": #elif значит, что образуется  цепочка и если  на первом iF выполниться, то  мы не выйдем, а если не выполнится - то выйдем из условия
            #self.handle_hello() #вызываем  функцию, что хотим показывать
        #elif path == "/style/": #путь
            #self.handle_style()
        #elif path == "/images/"
            #self.handle_images()

        #else:
            #self.handle_404() #вызываем  функцию, что хотим показывать

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
        css = read_static("styles/style.css")
        self.respond(css, content_type="text/css")

    #def handle_style(self):
        #css_file = settings.PROJECT_DIR / "styles" / "style.css" #файл если в папке то "styles" / "styles.css"
        #if not css_file.exists():
            #return self.handle_404()
        #with css_file.open("r") as fp: #открываем файл в роежиме чтения
            #css = fp.read()
    #self.respond(css, content_type="text/css")

    def handle_images(self):
        image = read_static("images/images.svg")
        self.respond(image, content_type="image/svg+xml")

    def handle_static(self, file_path, ct):
        content = read_static(file_path)
        self.respond(content, content_type=ct)

    #def handle_images(self):
        #img_file = settings.PROJECT_DIR / "images" / "images.png"
        #if not img_file.exists():
            #return self.handle_404()
        #with img_file.open("rb") as fp:
            #img = fp.read()

        #self.respond() # Тут нужно дописать код, разобраться

    def handle_404(self):
        msg = """NOT FOUND!!!!!!!"""

        self.respond(msg, code=404, content_type="text/plain")

    def handle_405(self):

        self.respond("", code=405, content_type="text/plain")

    def handle_500(self):

        self.respond(traceback.format_exc(), code=500, content_type="text/plain")

    # def handle_static(self, file_path, conent_type):
    #     content = read_static()
    #     self.respond(content) #Разобраться с этим кусокм пока неясно


    def respond(self, message, code=200, content_type="text/html"):  #функция которая будет передаватьяс в 404, 200 и так длаее
        payload = to_bytes(message)

        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(payload)))
        self.send_header("Cache-control", f"max-age={settings.CACHE_AGE}")
        self.end_headers()
        self.wfile.write(payload)
