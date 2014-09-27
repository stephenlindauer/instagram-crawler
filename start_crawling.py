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

pk=Account.objects.filter(status='pending').filter(Q(bio__icontains='lawrence') | Q(bio__icontains='denver'))[0].pk
# pk = 285044 # nightlifeltown

channel.basic_publish(exchange='',
                      routing_key='crawl_account',
                      body=json.dumps({'id':pk}))

print "Good luck..."


