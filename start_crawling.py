import os
import django
import pika
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crawler.settings")
django.setup()

from apps.accounts.models import Account


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='crawl_account')

pk=Account.objects.filter(status='pending')[0].pk

channel.basic_publish(exchange='',
                      routing_key='crawl_account',
                      body=json.dumps({'id':pk}))

print "Good luck..."


