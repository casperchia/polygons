# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polygons', '0017_acad_obj_group_logical_or'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject_Coreq',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('career', models.ForeignKey(to='polygons.Career', on_delete=django.db.models.deletion.PROTECT)),
                ('rule', models.ForeignKey(to='polygons.Rule', on_delete=django.db.models.deletion.PROTECT)),
                ('subject', models.ForeignKey(to='polygons.Subject', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='subject_coreq',
            unique_together=set([('subject', 'career', 'rule')]),
        ),
    ]
