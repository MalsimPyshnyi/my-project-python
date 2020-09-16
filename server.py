
import traceback
from datetime import date
from http.server import SimpleHTTPRequestHandler
from typing import Optional
from jinja2 import Template

import consts
import custom_types
import errors
import utils
# test

class MyHttp(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.dispatch("get")

    def do_POST(self):
        self.dispatch("post")

    def dispatch(self, http_method):
        req = custom_types.HttpRequest.build(
            self.path, method=http_method, headers=self.headers
        )

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
            "/0/": [self.handle_zde, []],
            "/hello-reset/": [self.handle_hello_reset, [req]],
            "/hello-update/": [self.handle_hello_update, [req]],
            "/hello/": [self.handle_hello, [req]],
            "/i/": [self.handle_static, [f"images/{req.file_name}", req.content_type]],
            "/s/": [self.handle_static, [f"styles/{req.file_name}", req.content_type]],
            "/theme/": [self.handle_theme, [req]],
        }

        # endpoints = {
        #     "/": [self.handle_static, ["index.html", "text/html"]],
        #     "/hello/": [self.handle_hello, [endpoint]],
        #     "/i/": [self.handle_static, [f"images/{endpoint.file_name}", content_type]],
        #     "/s/": [self.handle_static, [f"styles/{endpoint.file_name}", content_type]],
        # }

        try:
            try:
                handler, args = endpoints[req.normal]
            except KeyError:
                raise errors.NotFound
            handler(*args)
        except errors.NotFound:
            self.handle_404()
        except errors.MethodNotAllowed:
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

    def handle_hello(self, request: custom_types.HttpRequest) -> None:
        if request.method != "get":
            raise errors.MethodNotAllowed

        profile = utils.load_profile(request.session)
        user = custom_types.User.build(profile)

        content = self.render_hello_page(request, user, user)

        self.respond(content)

    def handle_hello_update(self, request: custom_types.HttpRequest) -> None:
        if request.method != "post":
            raise errors.MethodNotAllowed

        form_data = self.get_form_data()
        new_user = custom_types.User.build(form_data)

        response_kwargs = {}
        session = request.session
        if not session:
            session = utils.generate_new_session()
            response_kwargs["session"] = session

        if new_user.errors:
            saved_data = utils.load_profile(session)
            saved_user = custom_types.User.build(saved_data)
            html = self.render_hello_page(request, new_user, saved_user)
            self.respond(html, **response_kwargs)
        else:
            utils.store_profile(session, form_data)
            self.redirect("/hello", **response_kwargs)

    def render_hello_page(
        self,
        request: custom_types.HttpRequest,
        new_user: custom_types.User,
        saved_user: custom_types.User,
    ) -> str:
        css_class_for_name = css_class_for_age = ""
        label_for_name = "Your name: "
        label_for_age = "Your age: "

        age_new = age_saved = saved_user.age
        name_new = name_saved = saved_user.name

        year = date.today().year - age_saved

        if new_user.errors:
            if "name" in new_user.errors:
                error = new_user.errors["name"]
                label_for_name = f"ERROR: {error}"
                css_class_for_name = consts.CSS_CLASS_ERROR

            if "age" in new_user.errors:
                error = new_user.errors["age"]
                label_for_age = f"ERROR: {error}"
                css_class_for_age = consts.CSS_CLASS_ERROR

            name_new = new_user.name
            age_new = new_user.age

        theme = utils.load_theme(request.session)

        html = utils.read_static("hello.html").decode()
        template = Template(html)

        context = {
            "age_new": age_new or "",
            "label_for_age": label_for_age,
            "label_for_name": label_for_name,
            "name_new": name_new or "",
            "name_saved": name_saved or "",
            "class_for_age": css_class_for_age,
            "class_for_name": css_class_for_name,
            "year": year,
            "theme": theme,
        }

        content = template.render(**context)

        return content

    def handle_hello_reset(self, request: custom_types.HttpRequest) -> None:
        if request.method != "post":
            raise errors.MethodNotAllowed

        utils.drop_profile(request.session)
        self.redirect("/hello/")

    def handle_theme(self, request: custom_types.HttpRequest) -> None:
        if request.method != "post":
            raise errors.MethodNotAllowed

        response_kwargs = {}
        session = request.session
        if not session:
            session = utils.generate_new_session()
            response_kwargs["session"] = session

        current_theme = utils.load_theme(session)
        new_theme = utils.switch_theme(current_theme)
        utils.store_theme(session, new_theme)

        self.redirect("/hello", **response_kwargs)



    def handle_zde(self):
        x = 1 / 0
        print(x)

    def handle_static(self, file_path, content_type) -> None:
        content = utils.read_static(file_path)
        self.respond(content, content_type=content_type)

    def handle_404(self):
        msg = """CHECK YOU"""
        self.respond(msg, code=404, content_type="text/plain")

    def handle_405(self):
        self.respond("", code=405, content_type="text/plain")

    def handle_500(self):
        msg = traceback.format_exc()
        self.respond(msg, code=500, content_type="text/plain")

    def respond(
        self, message, code=200, content_type="text/html", session: Optional[str] = None
    ) -> None:
        payload = utils.to_bytes(message)

        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header_session(session)
        self.end_headers()
        self.wfile.write(payload)

    def redirect(self, to, session: Optional[str] = None) -> None:
        self.send_response(302)
        self.send_header("Location", to)
        self.send_header_session(session)
        self.end_headers()

    def send_header_session(self, session: Optional[str]) -> None:
        if session is None:
            return

        if session:
            header = utils.build_session_header(session)
        else:
            header = utils.build_session_header("expires", expires=True)

        self.send_header("Set-Cookie", header)

    def get_form_data(self) -> str:
        content_length_as_str = self.headers.get("Content-Length", 0)
        content_length = int(content_length_as_str)

        if not content_length:
            return ""

        payload_as_bytes = self.rfile.read(content_length)
        payload = utils.to_str(payload_as_bytes)

        return payload


    # @staticmethod
    # def load_user_data(session: str) -> str:
    #     if not  session:
    #         return ""
    #
    #     session_file = STORAGE_DIR / ("user_{session}.txt")
    #     if not USERS_DATA.is_file():
    #         return ""
    #
    #     with USERS_DATA.open("r") as src:
    #         data = src.read()
    #
    #     data = to_str(data)
    #
    #     return data
    #
    # @staticmethod
    # def save_user_data(data: str) -> None:
    #     with USERS_DATA.open("w") as dst:
    #         dst.write(data)

    # def handle_hello(self, request: HttpRequest):
    #     if request.method != "get":
    #         raise MethodNotAllowed
    #
    #     query_string = self.get_user_qs_from_file() #query_string = request.query_string or self.get_user_qs_from_file()
    #     user = User.from_query(query_string)
    #     #age = get_age_from_qs(endpoint.query_string)
    #     year = datetime.now().year - user.age
    #
    #     query = self.load_user_data()
    #     user = User.build(query)
    #
    #     content = self.render_hello_page(user, user)
    #
    #     self.respond(content)
    #
    #     content = f"""
    #     <html>
    #     <head><title>Hello Page</title></head>
    #     <body>
    #     <h1>Hello {user.name}!</h1>
    #     <h1>You was born at {year}!</h1>
    #     <p>path: {self.path}</p>
    #
    #     <form method="post" action=/"hello-update">
    #         <label for="name-id">Your name:</label>
    #         <input type="text" name="name" id="name-id" value="{user.name}">
    #         <label for="age-id">Your age:</label>
    #         <input type="text" name="age" id="age-id" value="{user.age}">
    #         <button type="submit">Greet</button>
    #     </form>
    #
    #     </body>
    #     </html>
    #     """
    #
    #     self.respond(content)
    #
    #
    # #def handle_style(self):
    #     #css = read_static("styles/style.css")
    #     #self.respond(css, content_type="text/css")
    #
    # #def handle_style(self):
    #     #css_file = settings.PROJECT_DIR / "styles" / "style.css" #файл если в папке то "styles" / "styles.css"
    #     #if not css_file.exists():
    #         #return self.handle_404()
    #     #with css_file.open("r") as fp: #открываем файл в роежиме чтения
    #         #css = fp.read()
    # #self.respond(css, content_type="text/css")
    #
    # #def handle_images(self):
    #     #image = read_static("images/images.svg")
    #     #self.respond(image, content_type="image/svg+xml")
    #
    #
    # #def handle_images(self):
    #     #img_file = settings.PROJECT_DIR / "images" / "images.png"
    #     #if not img_file.exists():
    #         #return self.handle_404()
    #     #with img_file.open("rb") as fp:
    #         #img = fp.read()
    #
    #     #self.respond() # Тут нужно дописать код, разобраться
    #
    # def handle_hello_update(self, request: HttpRequest):
    #     if request.method != "post":
    #         raise MethodNotAllowed
    #
    #     qs = self.get_request_payload()
    #     self.save_user_qs_to_file(qs)
    #     self.redirect("/hello")
    #
    #
    # def handle_static(self, file_path, content_type):
    #     content = read_static(file_path)
    #     self.respond(content, content_type=content_type)
    #
    # def handle_404(self):
    #     msg = """CHECK YOU"""
    #     self.respond(msg, code=404, content_type="text/plain")
    #
    # def handle_405(self):
    #     self.respond("", code=405, content_type="text/plain")
    #
    # def handle_500(self):
    #     msg = traceback.format_exc()
    #     self.respond(msg, code=500, content_type="text/plain")
    #
    # # def handle_static(self, file_path, conent_type):
    # #     content = read_static()
    # #     self.respond(content) #Разобраться с этим кусокм пока неясно
    #
    #
    # def respond(self, message, code=200, content_type="text/html"):
    #     payload = to_bytes(message)
    #
    #     self.send_response(code)
    #     self.send_header("Content-type", content_type)
    #     self.send_header("Content-length", str(len(payload)))
    #     self.end_headers()
    #     self.wfile.write(payload)
    #
    # def redirect(self, to):
    #     self.send_response(302)
    #     self.send_header("Location", to)
    #     self.end_headers()
    #
    #
    # def get_request_payload(self) -> str:
    #     content_length_in_str = self.headers.get("content-length", 0)
    #     content_length = int(content_length_in_str)
    #
    #     if not content_length:
    #         return ""
    #
    #     payload_in_bytes = self.rfile.read(content_length)
    #     payload = payload_in_bytes.decode()
    #     return payload
    #
    #
    # @staticmethod
    # def get_user_qs_from_file() -> str:
    #     if not USERS_DATA.is_file():
    #         return ""
    #
    #     with USERS_DATA.open("r") as src:
    #         content = src.read()
    #
    #     content = to_str(content)
    #
    #     return content
    #
    #
    # @staticmethod
    # def save_user_qs_to_file(query: str) -> None:
    #
    #     with USERS_DATA.open("w") as dst:
    #         dst.write(query)
