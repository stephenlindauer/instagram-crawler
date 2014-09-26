# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='followed_by_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='follower_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
