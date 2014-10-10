# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polygons', '0012_auto_20141006_0942'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program_Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uoc_tally', models.PositiveIntegerField(default=0)),
                ('current_year', models.PositiveIntegerField(default=1)),
                ('current_semester', models.ForeignKey(to='polygons.Semester', on_delete=django.db.models.deletion.PROTECT)),
                ('program', models.ForeignKey(to='polygons.Program', on_delete=django.db.models.deletion.PROTECT)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Semester_Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.PositiveIntegerField()),
                ('program_plan', models.ForeignKey(to='polygons.Program_Plan', on_delete=django.db.models.deletion.PROTECT)),
                ('semester', models.ForeignKey(to='polygons.Semester', on_delete=django.db.models.deletion.PROTECT)),
                ('subject', models.ForeignKey(to='polygons.Subject', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='semester_plan',
            unique_together=set([('program_plan', 'subject')]),
        ),
    ]
