# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0015_auto_20150506_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='brackets',
            name='total_score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
