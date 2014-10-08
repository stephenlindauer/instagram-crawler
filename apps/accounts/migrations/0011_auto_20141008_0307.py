# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_account_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='word',
            field=models.CharField(unique=True, max_length=100, db_index=True),
        ),
    ]
