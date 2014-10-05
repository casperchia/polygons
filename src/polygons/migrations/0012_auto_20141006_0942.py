# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0011_org_unit_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject_Pattern',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pattern', models.TextField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject_Pattern_Cache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.ForeignKey(to='polygons.Subject', on_delete=django.db.models.deletion.PROTECT)),
                ('subject_pattern', models.ForeignKey(to='polygons.Subject_Pattern', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='subject_pattern_cache',
            unique_together=set([('subject_pattern', 'subject')]),
        ),
    ]
