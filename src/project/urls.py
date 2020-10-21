"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pathlib import Path

from django.contrib import admin
from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import path, include

#подключаем html
from django.views.decorators.csrf import csrf_exempt




def view_index(request: HttpRequest):
    index_html = Path(__file__).parent.parent.parent / "static" / "index.html"
    with index_html.open("r") as fp:
        content = fp.read()
    resp = HttpResponse(content, content_type="text/html", status=200)

    print(request)

    return resp



# def index(request: HttpRequest):
#     index_html = Path(__file__).parent.parent.parent / "static" / "index.html" #указывваем путь - три парента так кака мы выходим в корневую папку
#     with index_html.open("r") as f:
#         content = f.read()
#     return HttpResponse(content, content_type="text/html")

#подключаем css
# def styles(request: HttpRequest):
#     styles_css = Path(__file__).parent.parent.parent / "static" / "styles" / "style.css" #указывваем путь - три парента так кака мы выходим в корневую папку
#     with styles_css.open("r") as f:
#         content = f.read()
#     return HttpResponse(content, content_type="text/css")

def view_css(request: HttpRequest):
    css_file = Path(__file__).parent.parent.parent / "static" / "styles" / "style.css"
    with css_file.open("r") as fp:
        content = fp.read()
    return HttpResponse(content, content_type="text/css")

def hello(request: HttpRequest):
    hello_html = Path(__file__).parent.parent.parent / "static" / "hello.html"
    with hello_html.open("r") as f:
        content = f.read()
    return HttpResponse(content, content_type="text/html")


# @csrf_exempt
# def hello_update(request: HttpRequest):
#     name request.POST.get("name")
#     age = request.POST.get("age")
#
#     request.session["name"] = name
#     request.session["age"] = age
#
#     return redirect("/hello")
#
# @csrf_exempt
# def hello_reset(request: HttpRequest):
#
#     hello_reset_html = Path(__file__).parent.parent.parent / "static" / "hello.html"
#     with hello_reset_html.open("r") as f:
#         content = f.read()
#     return HttpResponse(content, content_type="text/html")

#указываем пути по которым подключаем соотвествующие фукнции
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path("", view_index),
#     path("s/style.css/", view_css),
#     # path("hello/", hello),
#     # path("hello-update", hello_update),
#     # path("hello-reset", hello_reset),
#     path("hello/", include("applications.hello.urls"))
# ]

urlpatterns = [
    path("", include("applications.home.urls")),
    path("admin/", admin.site.urls),
    path("hello/", include("applications.hello.urls")),
]