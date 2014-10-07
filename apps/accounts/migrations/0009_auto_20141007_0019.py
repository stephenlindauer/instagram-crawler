# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re



def parse_account_info(apps, schema_editor):
    
    Account = apps.get_model("accounts", "Account")
    Word = apps.get_model("accounts", "Word")
    i=0
    accounts = Account.objects.all()
    num = len(accounts)
    for account in accounts:
        i+=1
        if i%100 == 0:
            print 100.0*i/num

        for s in [account.bio, account.username]:
            for w in re.findall(r'[\w]+', s):
                word, created = Word.objects.get_or_create(word=w.lower()[0:100])
                word.accounts.add(account)
                word.save()

            


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_word'),
    ]

    operations = [
        migrations.RunPython(parse_account_info),
    ]
