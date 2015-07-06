# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0018_auto_20150511_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='teams',
            name='picks_to_win',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
