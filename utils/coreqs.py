#!/usr/bin/env python

import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'comp4920.settings'
django.setup()

from polygons.models.Acad_Obj_Group_Type import Acad_Obj_Group_Type
from polygons.models.Acad_Obj_Group import Acad_Obj_Group
from polygons.models.Subject import Subject
from polygons.models.Subject_Group_Member import Subject_Group_Member
from polygons.models.Program import Program
from polygons.models.Program_Group_Member import Program_Group_Member
from polygons.models.Rule_Type import Rule_Type
from polygons.models.Rule import Rule
from polygons.models.Subject_Coreq import Subject_Coreq

acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='ACCT5930')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='COMM5003')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='ACCT5906')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='ACCT5919')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='ACCT5942')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='ACCT5943')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='ACCT5930')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='COMM5003')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='ACCT5906')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='ACCT5996')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='ACTL5103')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='ACTL5106')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='ACTL5103')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='ACTL5109')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='AERO3650')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='AERO3630')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='AERO3640')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='AERO4110')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='COMM5001')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='COMM5002')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True, logical_or=True)
acad_obj_group.save()

subject = Subject.objects.get(code='COMM5002')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='COMM5003')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()

acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='program')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True, logical_or=True)
acad_obj_group.save()

program = Program.objects.get(code='8728')
member = Program_Group_Member(program=program, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=1, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='COMM5003')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MATH1081')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='COMP2111')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='COMP9171')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='COMP4001')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='COMP4511')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='COMP3311')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='INFS3608')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='COMP9321')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='CVEN2301')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='CVEN3301')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='ECON6001')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='ECON6002')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='ECON6003')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='ECON6004')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=24, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='ECON6350')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='FINS3775')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='FINS4775')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='FINS4774')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='ACCT5930')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='ECON5103')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=12, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='FINS5511')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True, logical_or=True)
acad_obj_group.save()

subject = Subject.objects.get(code='ACCT5906')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='FINS5512')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()

acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='program')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True, logical_or=True)
acad_obj_group.save()

program = Program.objects.get(code='9273')
member = Program_Group_Member(program=program, acad_obj_group=acad_obj_group)
member.save()

program = Program.objects.get(code='5273')
member = Program_Group_Member(program=program, acad_obj_group=acad_obj_group)
member.save()

program = Program.objects.get(code='7273')
member = Program_Group_Member(program=program, acad_obj_group=acad_obj_group)
member.save()

program = Program.objects.get(code='8007')
member = Program_Group_Member(program=program, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=1, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='FINS5512')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True, logical_or=True)
acad_obj_group.save()

subject = Subject.objects.get(code='COMM5003')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='FINS5512')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='FINS5566')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()

acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='program')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True, logical_or=True)
acad_obj_group.save()

program = Program.objects.get(code='8406')
member = Program_Group_Member(program=program, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=1, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='FINS5566')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='GMAT2120')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='GMAT2500')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='GMAT2700')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=18, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='GMAT2130')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='GMAT2500')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='GMAT2550')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True, logical_or=True)
acad_obj_group.save()

subject = Subject.objects.get(code='INFS5984')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='INFS5906')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()

acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='program')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True, logical_or=True)
acad_obj_group.save()

program = Program.objects.get(code='8407')
member = Program_Group_Member(program=program, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=1, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='INFS5906')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='ACCT5930')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='INFS5978')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='LEGT5511')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='LEGT5512')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=3, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='LEGT5541')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='LEGT5511')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='LEGT5512')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=3, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='LEGT5551')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MMAN2100')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MANF3100')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MARK2051')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='MARK52151')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MARK2999')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()

acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MARK2052')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MARK2999')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MARK5800')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='MARK5801')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MARK5810')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MARK5800')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='MARK5801')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MARK5811')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MARK5800')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='MARK5801')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MARK5812')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MARK5800')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='MARK5801')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MARK5813')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MARK5800')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='MARK5801')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MARK5814')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MARK5800')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='MARK5801')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MARK5815')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True, logical_or=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MARK5800')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='MARK5801')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MARK5816')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()

acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='program')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True, logical_or=True)
acad_obj_group.save()

program = Program.objects.get(code='8406')
member = Program_Group_Member(program=program, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=1, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MARK5816')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MARK5800')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='MARK5801')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MARK5819')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MECH4001')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=3, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MECH4004')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MGMT5601')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MGMT5603')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MGMT5601')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MGMT5604')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MMAN4000')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MMAN4020')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MNGT6271')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='MNGT6274')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='OPTM3211')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='OPTM3231')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='OPTM4131')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='OPTM4151')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='OPTM4231')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='OPTM4251')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MATH1231')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='MATH1241')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='PHYS1221')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MATH1231')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='MATH1241')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='PHYS1231')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MATH2011')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='PHYS2010')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MATH2011')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='PHYS2050')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MATH2120')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='MATH2130')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=3, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='PHYS3060')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='PHYS3210')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='PHYS3020')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='PHYS3080')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MATH2120')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='MATH2130')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=3, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='PHYS3210')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='PTRL2018')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='PTRL2019')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='SAED2491')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=3, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='SAED2402')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='SAED3491')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=3, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='SAED3402')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='SAED3402')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=3, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='SAED3491')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='SAED2491')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='SAED2491')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='COMP2111')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='SENG2010')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='COMP2111')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='SENG2011')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='SERV2004')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='SERV2003')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='SOCW3002')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='SOCW3001')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='SOMA9202')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='SOMA9751')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='MGMT5601')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='STRE5603')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
acad_obj_group = Acad_Obj_Group(type=acad_obj_group_type, enumerated=True)
acad_obj_group.save()

subject = Subject.objects.get(code='PHYS1121')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

subject = Subject.objects.get(code='PHYS1131')
member = Subject_Group_Member(subject=subject, acad_obj_group=acad_obj_group)
member.save()

rule_type = Rule_Type.objects.get(abbreviation='CQ')
rule = Rule(type=rule_type, min=6, acad_obj_group=acad_obj_group)
rule.save()

subject = Subject.objects.get(code='VISN1231')
coreq = Subject_Coreq(subject=subject, rule=rule)
coreq.save()
