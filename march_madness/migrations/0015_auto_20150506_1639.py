# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0014_auto_20150506_1617'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scoringvalues',
            old_name='round_1',
            new_name='points',
        ),
        migrations.RemoveField(
            model_name='scoringvalues',
            name='round_2',
        ),
        migrations.RemoveField(
            model_name='scoringvalues',
            name='round_3',
        ),
        migrations.RemoveField(
            model_name='scoringvalues',
            name='round_4',
        ),
        migrations.RemoveField(
            model_name='scoringvalues',
            name='round_5',
        ),
        migrations.RemoveField(
            model_name='scoringvalues',
            name='round_6',
        ),
        migrations.RemoveField(
            model_name='scoringvalues',
            name='round_7',
        ),
        migrations.RemoveField(
            model_name='scoringvalues',
            name='round_8',
        ),
    ]
