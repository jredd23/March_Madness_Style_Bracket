# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='games',
            name='hteam_id',
            field=models.OneToOneField(to='march_madness.Teams'),
            preserve_default=True,
        ),
    ]
