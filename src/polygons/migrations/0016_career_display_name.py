# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0015_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='career',
            name='display_name',
            field=models.TextField(default='', unique=True),
            preserve_default=False,
        ),
    ]
