# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0013_scoringvalues_sores'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scores',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_score', models.IntegerField()),
                ('current_rank', models.IntegerField()),
                ('bracket_id', models.ForeignKey(to='march_madness.Brackets')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='sores',
            name='bracket_id',
        ),
        migrations.DeleteModel(
            name='Sores',
        ),
    ]
