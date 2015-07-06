# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0003_auto_20150403_1335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='regions',
            old_name='bracket_name',
            new_name='region_name',
        ),
    ]
