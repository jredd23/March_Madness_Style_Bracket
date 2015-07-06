# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0024_auto_20150618_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scoringvalues',
            name='points',
        ),
    ]
