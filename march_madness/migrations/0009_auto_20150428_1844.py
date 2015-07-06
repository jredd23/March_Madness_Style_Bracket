# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0008_auto_20150428_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brackets',
            name='submission_time',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
