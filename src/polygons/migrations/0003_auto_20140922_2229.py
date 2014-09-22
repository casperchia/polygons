# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0002_auto_20140922_1808'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='acad_obj_group',
            new_name='excluded',
        ),
    ]
