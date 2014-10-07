# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_account_avatar_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(unique=True, max_length=100)),
                ('accounts', models.ManyToManyField(to='accounts.Account', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
