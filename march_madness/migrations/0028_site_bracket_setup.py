# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0027_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='bracket_setup',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
