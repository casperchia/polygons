# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0004_remove_stream_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acad_obj_group',
            name='parent',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='polygons.Acad_Obj_Group'),
        ),
    ]
