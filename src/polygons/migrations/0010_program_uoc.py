# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0009_auto_20140926_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='uoc',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
