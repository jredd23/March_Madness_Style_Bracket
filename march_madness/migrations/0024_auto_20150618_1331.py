# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0023_auto_20150617_2024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scoringvalues',
            name='round_name',
        ),
        migrations.AddField(
            model_name='scoringvalues',
            name='r1',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scoringvalues',
            name='r2',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scoringvalues',
            name='r3',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scoringvalues',
            name='r4',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scoringvalues',
            name='r5',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scoringvalues',
            name='r6',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scoringvalues',
            name='r7',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
