# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20140926_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='followed_by_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='follower_count',
            field=models.IntegerField(default=0),
        ),
    ]
