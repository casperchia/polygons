# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0005_auto_20140923_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acad_obj_group',
            name='name',
            field=models.TextField(null=True),
        ),
    ]
