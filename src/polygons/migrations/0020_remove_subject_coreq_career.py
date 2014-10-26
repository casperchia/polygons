# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0019_auto_20141026_1305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject_coreq',
            name='career',
        ),
    ]
