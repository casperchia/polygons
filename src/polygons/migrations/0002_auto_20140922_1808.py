# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='org_unit_group',
            unique_together=set([('owner', 'member')]),
        ),
    ]
