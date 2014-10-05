from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.template.response import TemplateResponse
from apps.accounts.models import Account

import json

# Create your views here.
def home(request):

    return TemplateResponse(request, 'web/home.html', {})

def search(request):
    search_string = request.GET.get("q")

    page = int(request.GET.get("p", 0))

    start = page * 20
    end = start + 20

    terms = search_string.split(",")
    query = Account.objects
    for term in terms:
        query = query.filter(bio__icontains=term.strip())

    accounts = []
    for account in query:
        accounts.append(account.serialize())

    data = {
        "results":accounts[start:end],
        "meta":{
            "page":page,
            "count":len(accounts)
        }
    }

    return HttpResponse(json.dumps(data))
