# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0010_smacktalk'),
    ]

    operations = [
        migrations.AddField(
            model_name='brackets',
            name='name',
            field=models.CharField(default='bracket', max_length=45),
            preserve_default=False,
        ),
    ]
