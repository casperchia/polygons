# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0012_auto_20141006_0942'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject_Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=4)),
                ('name', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
