# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0007_brackets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brackets',
            name='game68',
        ),
        migrations.RemoveField(
            model_name='brackets',
            name='game69',
        ),
    ]
