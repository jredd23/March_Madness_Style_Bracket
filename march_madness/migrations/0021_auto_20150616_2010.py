# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0020_scoringvalues_last_scored'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scores',
            name='bracket_id',
        ),
        migrations.DeleteModel(
            name='Scores',
        ),
    ]
