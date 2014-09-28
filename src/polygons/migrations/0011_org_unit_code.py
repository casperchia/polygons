# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0010_program_uoc'),
    ]

    operations = [
        migrations.AddField(
            model_name='org_unit',
            name='code',
            field=models.CharField(max_length=16, null=True),
            preserve_default=True,
        ),
    ]
