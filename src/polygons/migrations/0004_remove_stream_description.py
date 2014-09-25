# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0003_auto_20140922_2229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stream',
            name='description',
        ),
    ]
