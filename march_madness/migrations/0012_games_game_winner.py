# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0011_brackets_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='games',
            name='game_winner',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
