from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.template.response import TemplateResponse
from apps.accounts.models import Account, Word

import json
import time

# Create your views here.
def home(request):

    return TemplateResponse(request, 'web/home.html', {})

def search(request):
    start_time = time.time()
    search_string = request.GET.get("q")

    page = int(request.GET.get("p", 0))

    start = page * 50
    end = start + 50

    terms = search_string.split(",")
    matches = None
    for term in terms:
        print term
        term_matches = set()
        for word in Word.objects.filter(word__contains=term.strip().lower()):
            for account in word.accounts.all():
                term_matches.add(account)

        if matches == None:
            matches = term_matches
        else:
            matches = matches.intersection(term_matches)


    accounts = []
    for account in matches:
        accounts.append(account.serialize())

    data = {
        "results":accounts[start:end],
        "meta":{
            "page":page,
            "count":len(accounts),
            "time":str(time.time()-start_time)[0:6]
        }
    }

    return HttpResponse(json.dumps(data))
