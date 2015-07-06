# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0022_brackets_best'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoringvalues',
            name='round_name',
            field=models.ForeignKey(default=1, to='march_madness.Rounds'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scoringvalues',
            name='seed',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
