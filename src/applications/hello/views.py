# from django.http import HttpRequest, HttpResponse
# from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
#
#
# def index(request: HttpRequest) -> HttpResponse:
#
#     name = request.session.get("name", "anon")
#     age = request.session.get("age") or -100
#
#     context = {
#         "theme": "dark",
#         "name_saved": name,
#         "year": age,
#     }
#
#     resp = render(request, "hello/hello.html", context)
#     return resp
#
# @csrf_exempt
# def update(request: HttpRequest) -> HttpResponse:
#     name = request.POST.get("name")
#     age = request.POST.get("age")
#
#     request.session["name"] = name
#     request.session["age"] = age
#
#     return redirect("/hello")