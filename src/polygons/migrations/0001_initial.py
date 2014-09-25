# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acad_Obj_Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('enumerated', models.BooleanField(default=False)),
                ('definition', models.TextField(null=True)),
                ('parent', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='polygons.Acad_Obj_Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Acad_Obj_Group_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbreviation', models.CharField(unique=True, max_length=2)),
                ('name', models.TextField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(unique=True)),
                ('abbreviation', models.TextField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Org_Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Org_Unit_Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('member', models.ForeignKey(related_name=b'member', on_delete=django.db.models.deletion.PROTECT, to='polygons.Org_Unit')),
                ('owner', models.ForeignKey(related_name=b'owner', on_delete=django.db.models.deletion.PROTECT, to='polygons.Org_Unit')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Org_Unit_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('career', models.ForeignKey(to='polygons.Career', on_delete=django.db.models.deletion.PROTECT)),
                ('degree', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='polygons.Degree', null=True)),
                ('offered_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='polygons.Org_Unit', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Program_Group_Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('acad_obj_group', models.ForeignKey(to='polygons.Acad_Obj_Group', on_delete=django.db.models.deletion.PROTECT)),
                ('program', models.ForeignKey(to='polygons.Program', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Program_Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('program', models.ForeignKey(to='polygons.Program', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(null=True)),
                ('min', models.PositiveIntegerField(null=True)),
                ('max', models.PositiveIntegerField(null=True)),
                ('description', models.TextField(null=True)),
                ('acad_obj_group', models.ForeignKey(to='polygons.Acad_Obj_Group', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rule_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(unique=True)),
                ('abbreviation', models.CharField(unique=2, max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbreviation', models.CharField(unique=True, max_length=2)),
                ('name', models.TextField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('code', models.CharField(unique=True, max_length=6)),
                ('description', models.TextField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stream_Group_Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('acad_obj_group', models.ForeignKey(to='polygons.Acad_Obj_Group', on_delete=django.db.models.deletion.PROTECT)),
                ('stream', models.ForeignKey(to='polygons.Stream', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stream_Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rule', models.ForeignKey(to='polygons.Rule', on_delete=django.db.models.deletion.PROTECT)),
                ('stream', models.ForeignKey(to='polygons.Stream', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=8)),
                ('name', models.TextField()),
                ('uoc', models.PositiveIntegerField()),
                ('acad_obj_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='polygons.Acad_Obj_Group', null=True)),
                ('career', models.ForeignKey(to='polygons.Career', on_delete=django.db.models.deletion.PROTECT)),
                ('offered_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='polygons.Org_Unit', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject_Group_Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('acad_obj_group', models.ForeignKey(to='polygons.Acad_Obj_Group', on_delete=django.db.models.deletion.PROTECT)),
                ('subject', models.ForeignKey(to='polygons.Subject', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject_Prereq',
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
            name='subject_group_member',
            unique_together=set([('subject', 'acad_obj_group')]),
        ),
        migrations.AlterUniqueTogether(
            name='stream_rule',
            unique_together=set([('stream', 'rule')]),
        ),
        migrations.AlterUniqueTogether(
            name='stream_group_member',
            unique_together=set([('stream', 'acad_obj_group')]),
        ),
        migrations.AddField(
            model_name='rule',
            name='type',
            field=models.ForeignKey(to='polygons.Rule_Type', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program_rule',
            name='rule',
            field=models.ForeignKey(to='polygons.Rule', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='program_rule',
            unique_together=set([('program', 'rule')]),
        ),
        migrations.AlterUniqueTogether(
            name='program_group_member',
            unique_together=set([('program', 'acad_obj_group')]),
        ),
        migrations.AddField(
            model_name='org_unit',
            name='type',
            field=models.ForeignKey(to='polygons.Org_Unit_Type', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.ForeignKey(to='polygons.Semester', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(to='polygons.Subject', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('subject', 'semester')]),
        ),
        migrations.AddField(
            model_name='acad_obj_group',
            name='type',
            field=models.ForeignKey(to='polygons.Acad_Obj_Group_Type', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
    ]
