# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0017_brackets_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='games',
            name='hteam_from',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='games',
            name='vteam_from',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
