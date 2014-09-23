# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0006_auto_20140923_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acad_obj_group',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='polygons.Acad_Obj_Group', null=True),
        ),
    ]
