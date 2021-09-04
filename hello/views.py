from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

import json

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")

def results(request):
    response_data = {}
    response_data['urls'] = ['joshriley.tech', 'walley892..github.io']
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
