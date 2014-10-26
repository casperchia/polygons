# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0016_career_display_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='acad_obj_group',
            name='logical_or',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
