from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.template.response import TemplateResponse
from apps.accounts.models import Account, Word

import json

# Create your views here.
def home(request):

    return TemplateResponse(request, 'web/home.html', {})

def search(request):
    search_string = request.GET.get("q")

    page = int(request.GET.get("p", 0))

    start = page * 50
    end = start + 50

    terms = search_string.split(",")
    matches = None
    for term in terms:
        try:
            word = Word.objects.get(word=term.strip())
        except Word.DoesNotExist, e:
            print "Not found: ", term
            data = {
                "results":0,
                "meta":{
                    "page":0,
                    "count":0
                }
            }
            return HttpResponse(json.dumps(data))

        if matches == None:
            matches = set(word.accounts.all())
        else:
            matches = matches.intersection(word.accounts.all())

    accounts = []
    for account in matches:
        accounts.append(account.serialize())

    data = {
        "results":accounts[start:end],
        "meta":{
            "page":page,
            "count":len(accounts)
        }
    }

    return HttpResponse(json.dumps(data))
