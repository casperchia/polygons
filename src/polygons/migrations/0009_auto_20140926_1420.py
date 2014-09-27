# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0008_program_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='degree',
            name='abbreviation',
            field=models.TextField(),
        ),
    ]
