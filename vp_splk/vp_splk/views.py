from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>404</h1>')


