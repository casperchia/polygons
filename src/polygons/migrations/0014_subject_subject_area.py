# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0013_subject_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='subject_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=1, to='polygons.Subject_Area'),
            preserve_default=False,
        ),
    ]
