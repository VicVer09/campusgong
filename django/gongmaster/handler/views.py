from django.shortcuts import render
from django.http import HttpResponse
import json

def get_schedule(request):
    data = {
        "message": "Hello World"
    }
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


def check_update(request):
    pass


def check_valid(request):
    pass


def message(request):
    pass



