# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtended',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('users_following', models.ForeignKey(blank=True, to='twitter_style_app_1.UserExtended', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.TextField()),
                ('date_created', models.DateField(default=datetime.date(2015, 1, 14))),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, to='twitter_style_app_1.UserExtended', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
