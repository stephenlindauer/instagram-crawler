import os
import django
import pika
import json
import sys
import time
import re

from instagram.client import InstagramAPI


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crawler.settings")
django.setup()

from apps.accounts.models import Account, Word


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='crawl_account')

api = InstagramAPI(client_id='fe5e81e9fdd142b7bbd031e118c9fc35', client_secret='9e5dc8ee56ff46ae975072934483fdc8')  # stephenlindauer
# api = InstagramAPI(client_id='1e7fdb33000d4cfcb9631837dc50b9a5', client_secret='1cf6b7805c5e40a29535385ff557cc54')  # sdlyr8


keywords = ["colorado", "nightlife", "denver", "boulder", "st. louis", "stl", "missouri", "314", "303", "chicago", "columbia", "mizzou", "como"]

def process_user(user):
    account = None
    try:
        account = Account.objects.get(username=user.username)
        account.avatar_url = user.profile_picture
        account.name = user.full_name
        account.bio = user.bio
        account.save()
    except:
        account = Account.objects.create(username=user.username, account_id=user.id)
        account.avatar_url = user.profile_picture
        account.name = user.full_name
        account.bio = user.bio
        account.save()

    # Create words
    for s in [account.bio, account.username]:
        for w in re.findall(r'[\w]+', s):
            word, created = Word.objects.get_or_create(word=w.lower())
            word.accounts.add(account)
            word.save()

    if account.status != "done":
        for keyword in keywords:
            if keyword in user.bio.lower():
                channel.basic_publish(exchange='',
                          routing_key='crawl_account',
                          body=json.dumps({'id':account.pk}))
                return
        
        else:
            account.status='ignored'
            account.save()


def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

    try:

        data = json.loads(body)

        account = Account.objects.get(pk=data['id'])
        account.status='queued'
        account.save()

        print "Crawl ", account.username

        follower_count = 0
        followed_by_count = 0
        try:
            follows, next_url = api.user_follows(user_id=account.account_id)
            for user in follows:
                process_user(user)
                follower_count += 1

            while next_url:
                sys.stdout.write('.')
                follows, next_url = api.user_follows(with_next_url=next_url)
                for user in follows:
                    process_user(user)
                    follower_count += 1

        except Account.DoesNotExist, e:
            print "<WARN> ", e

        try:
            follows, next_url = api.user_followed_by(user_id=account.account_id)
            for user in follows:
                process_user(user)
                followed_by_count += 1

            while next_url:
                sys.stdout.write('.')
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

        print "done"

    except Exception, e:
        print "<ERROR> ", e


channel.basic_consume(callback,
                      queue='crawl_account',
                      no_ack=True)


# Use this if we want it to have it run constantly, otherwise it checks for any queued up messages
print ' [*] Waiting for messages. To exit press CTRL+C'
channel.start_consuming()
