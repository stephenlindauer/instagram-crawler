import os
import django
import pika
import json
from instagram.client import InstagramAPI


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crawler.settings")
django.setup()

from apps.accounts.models import Account


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='crawl_account')

api = InstagramAPI(client_id='fe5e81e9fdd142b7bbd031e118c9fc35', client_secret='9e5dc8ee56ff46ae975072934483fdc8') 


def process_user(user):
    try:
        Account.objects.get(username=user.username)
    except:
        new_account = Account.objects.create(username=user.username, account_id=user.id)
        new_account.bio = user.bio
        new_account.save()

        channel.basic_publish(exchange='',
                  routing_key='crawl_account',
                  body=json.dumps({'id':new_account.pk}))


def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

    data = json.loads(body)

    account = Account.objects.get(pk=data['id'])
    print "Crawl ", account.username

    follower_count = 0
    followed_by_count = 0
    try:
        follows, next_url = api.user_follows(user_id=account.account_id)
        for user in follows:
            process_user(user)
            follower_count += 1

        while next_url:
            follows, next_url = api.user_follows(with_next_url=next_url)
            for user in follows:
                process_user(user)
                follower_count += 1
    except Exception, e:
        print "<WARN> ", e


    try:
        follows, next_url = api.user_followed_by(user_id=account.account_id)
        for user in follows:
            process_user(user)
            followed_by_count += 1

        while next_url:
            follows, next_url = api.user_followed_by(with_next_url=next_url)
            for user in follows:
                process_user(user)
                followed_by_count += 1
    except Exception, e:
        print "<WARN> ", e

    account.follower_count = follower_count
    account.followed_by_count = followed_by_count
    account.status='done'
    account.save()




channel.basic_consume(callback,
                      queue='crawl_account',
                      no_ack=True)


# Use this if we want it to have it run constantly, otherwise it checks for any queued up messages
print ' [*] Waiting for messages. To exit press CTRL+C'
channel.start_consuming()