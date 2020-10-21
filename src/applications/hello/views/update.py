from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from applications.hello.forms import HelloForm

@csrf_exempt
def update(request: HttpRequest) -> HttpResponse:
    form = HelloForm(request.POST)
    if form.is_valid():

        request.session["name"] = form.cleaned_data["name"]
        request.session["age"] = form.cleaned_data["age"]
        return redirect("/hello")

    return HttpResponse(form.errors)