# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('march_madness', '0012_games_game_winner'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScoringValues',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round_1', models.IntegerField(default=0)),
                ('round_2', models.IntegerField(default=0)),
                ('round_3', models.IntegerField(default=0)),
                ('round_4', models.IntegerField(default=0)),
                ('round_5', models.IntegerField(default=0)),
                ('round_6', models.IntegerField(default=0)),
                ('round_7', models.IntegerField(default=0)),
                ('round_8', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sores',
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
    ]
