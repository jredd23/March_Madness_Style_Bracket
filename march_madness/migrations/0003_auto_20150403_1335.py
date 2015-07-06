# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0002_auto_20150403_1333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='games',
            old_name='game_region_id',
            new_name='game_region',
        ),
        migrations.RenameField(
            model_name='games',
            old_name='game_round_id',
            new_name='game_round',
        ),
        migrations.RenameField(
            model_name='games',
            old_name='hteam_id',
            new_name='hteam',
        ),
        migrations.RenameField(
            model_name='games',
            old_name='vteam_id',
            new_name='vteam',
        ),
        migrations.RenameField(
            model_name='teams',
            old_name='team_region_id',
            new_name='team_region',
        ),
    ]
