import os
import django
import pika
import json
from django.db.models import Q


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crawler.settings")
django.setup()

from apps.accounts.models import Account


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='crawl_account')

accounts = Account.objects.filter(status='pending').filter(Q(bio__icontains='lawrence') | Q(bio__icontains='denver'))
# pk = 285044 # nightlifeltown

channel.basic_publish(exchange='',
                      routing_key='crawl_account',
                      body=json.dumps({'id':accounts[0].pk}))

channel.basic_publish(exchange='',
                      routing_key='crawl_account',
                      body=json.dumps({'id':accounts[1].pk}))

channel.basic_publish(exchange='',
                      routing_key='crawl_account',
                      body=json.dumps({'id':accounts[2].pk}))

print "Good luck..."


