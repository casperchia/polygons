# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0018_auto_20141026_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject_coreq',
            name='career',
        ),
        migrations.AlterUniqueTogether(
            name='subject_coreq',
            unique_together=set([('subject', 'rule')]),
        ),
    ]
