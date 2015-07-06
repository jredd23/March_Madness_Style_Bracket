# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hteam_id', models.IntegerField()),
                ('vteam_id', models.IntegerField()),
                ('win_game_id', models.IntegerField()),
                ('win_home', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Regions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bracket_name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rounds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round_name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('team_seed', models.IntegerField()),
                ('team_name', models.CharField(max_length=30)),
                ('team_region_id', models.ForeignKey(to='march_madness.Regions')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='games',
            name='game_region_id',
            field=models.ForeignKey(to='march_madness.Regions'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='games',
            name='game_round_id',
            field=models.ForeignKey(to='march_madness.Rounds'),
            preserve_default=True,
        ),
    ]
