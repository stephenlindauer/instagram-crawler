# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='bio',
            field=models.CharField(default=b'', max_length=5000, blank=True),
            preserve_default=True,
        ),
    ]
