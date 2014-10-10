# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0013_auto_20141010_1237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='program_plan',
            old_name='uoc',
            new_name='uoc_tally',
        ),
        migrations.AddField(
            model_name='program_plan',
            name='current_semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=1, to='polygons.Semester'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='program_plan',
            name='current_year',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
    ]
