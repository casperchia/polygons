# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0007_auto_20140923_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='code',
            field=models.CharField(default='xxxx', unique=True, max_length=4),
            preserve_default=False,
        ),
    ]
