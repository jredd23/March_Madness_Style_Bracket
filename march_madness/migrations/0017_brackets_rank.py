# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0016_brackets_total_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='brackets',
            name='rank',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
