from django.shortcuts import render


def index(request, template_name="index.html"):
    response = render(request, template_name)
    return response
