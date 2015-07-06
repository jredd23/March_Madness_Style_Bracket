# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0019_teams_picks_to_win'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoringvalues',
            name='last_scored',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 16, 15, 26, 38, 872613, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
