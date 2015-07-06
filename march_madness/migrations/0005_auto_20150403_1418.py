# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0004_auto_20150403_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='games',
            name='hteam',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
