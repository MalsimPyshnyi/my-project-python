import traceback
from datetime import datetime
from http.server import SimpleHTTPRequestHandler

import settings
from custom_types import HttpRequest
from errors import MethodNotAllowed
from errors import NotFound
from utils import get_user_data
from utils import read_static
from utils import to_bytes
from utils import to_str
from consts import USERS_DATA


class MyHttp(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.dispatch("get")

    def do_POST(self):
        self.dispatch("post")

    def dispatch(self, http_method):
        req = HttpRequest.from_path(self.path, method=http_method)

        #path = normalize_path(self.path) # self.path - то что нам приходит с браузера
        #endipoint = Endipoint.from_path

        # try:
        #     path_parts  = path.split("/")
        # except ImportError:
        #     file_path = None
        # file_path = path_parts[2]
        # path = normalize_path(path_parts[1])
       # path = f"/{path}" if path != "/" else path

        endpoints = {
            "/": [self.handle_static, ["index.html", "text/html"]],
            "/hello/": [self.handle_hello, [req]],
            "/hello-update/": [self.handle_hello_update, [req]],
            "/i/": [self.handle_static, [f"images/{req.file_name}", req.content_type]],
            "/s/": [self.handle_static, [f"styles/{req.file_name}", req.content_type]],
        }

        # endpoints = {
        #     "/": [self.handle_static, ["index.html", "text/html"]],
        #     "/hello/": [self.handle_hello, [endpoint]],
        #     "/i/": [self.handle_static, [f"images/{endpoint.file_name}", content_type]],
        #     "/s/": [self.handle_static, [f"styles/{endpoint.file_name}", content_type]],
        # }

        try:
            handler, args = endpoints[req.normal]
            handler(*args)
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

    #def handle_root(self): #пищем функцию чтобы далее ее вызвать
        #return super().do_GET() #обращаемся к родителю


    def handle_hello(self, request: HttpRequest):
        if request.method != "get":
            raise MethodNotAllowed

        query_string = self.get_user_qs_from_file() #query_string = request.query_string or self.get_user_qs_from_file()
        user = get_user_data(query_string)
        #age = get_age_from_qs(endpoint.query_string)
        year = datetime.now().year - user.age

        content = f"""
        <html>
        <head><title>Hello Page</title></head>
        <body>
        <h1>Hello {user.name}!</h1>
        <h1>You was born at {year}!</h1>
        <p>path: {self.path}</p>

        <form method="post" action=/"hello-update">
            <label for="name-id">Your name:</label>
            <input type="text" name="name" id="name-id">
            <label for="age-id">Your age:</label>
            <input type="text" name="age" id="age-id">
            <button type="submit">Greet</button>
        </form>

        </body>
        </html>
        """

        self.respond(content)


    #def handle_style(self):
        #css = read_static("styles/style.css")
        #self.respond(css, content_type="text/css")

    #def handle_style(self):
        #css_file = settings.PROJECT_DIR / "styles" / "style.css" #файл если в папке то "styles" / "styles.css"
        #if not css_file.exists():
            #return self.handle_404()
        #with css_file.open("r") as fp: #открываем файл в роежиме чтения
            #css = fp.read()
    #self.respond(css, content_type="text/css")

    #def handle_images(self):
        #image = read_static("images/images.svg")
        #self.respond(image, content_type="image/svg+xml")


    #def handle_images(self):
        #img_file = settings.PROJECT_DIR / "images" / "images.png"
        #if not img_file.exists():
            #return self.handle_404()
        #with img_file.open("rb") as fp:
            #img = fp.read()

        #self.respond() # Тут нужно дописать код, разобраться

    def handle_hello_update(self, request: HttpRequest):
        if request.method != "post":
            raise MethodNotAllowed

        qs = self.get_request_payload()
        self.save_user_qs_to_file(qs)
        self.redirect("/hello")


    def handle_static(self, file_path, content_type):
        content = read_static(file_path)
        self.respond(content, content_type=content_type)

    def handle_404(self):
        msg = """CHECK YOU"""
        self.respond(msg, code=404, content_type="text/plain")

    def handle_405(self):
        self.respond("", code=405, content_type="text/plain")

    def handle_500(self):
        msg = traceback.format_exc()
        self.respond(msg, code=500, content_type="text/plain")

    # def handle_static(self, file_path, conent_type):
    #     content = read_static()
    #     self.respond(content) #Разобраться с этим кусокм пока неясно


    def respond(self, message, code=200, content_type="text/html"):
        payload = to_bytes(message)

        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(payload)))
        self.send_header("Cache-control", f"max-age={settings.CACHE_AGE}")
        self.end_headers()
        self.wfile.write(payload)

    def redirect(self, to):
        self.send_response(302)
        self.send_header("Location", to)
        self.send_headers()


    def get_request_payload(self) -> str:
        content_length_in_str = self.headers.get("content-length", 0)
        content_length = int(content_length_in_str)

        if not content_length:
            return ""

        payload_in_bytes = self.rfile.read(content_length)
        payload = payload_in_bytes.decode()
        return payload


    @staticmethod
    def get_user_qs_from_file() -> str:
        if not USERS_DATA.is_file():
            return ""

        with USERS_DATA.open("r") as src:
            content = src.read()

        content = to_str(content)

        return content


    @staticmethod
    def save_user_qs_to_file(query: str) -> None:

        with USERS_DATA.open("w") as dst:
            dst.write(query)
