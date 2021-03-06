# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20140926_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='status',
            field=models.CharField(default=b'pending', max_length=20, choices=[(b'pending', b'Pending'), (b'queued', b'Queued'), (b'done', b'Done'), (b'failed', b'Failed'), (b'ignored', b'Ignored')]),
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
