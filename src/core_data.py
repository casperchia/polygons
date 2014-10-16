#!/usr/bin/env python

import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'comp4920.settings'
django.setup()

from django.db import IntegrityError, transaction

from polygons.models.Acad_Obj_Group_Type import Acad_Obj_Group_Type
from polygons.models.Career import Career
from polygons.models.Org_Unit_Type import Org_Unit_Type
from polygons.models.Rule_Type import Rule_Type
from polygons.models.Semester import Semester

def insert_records(records):
    for record in records:
        try:
            # Will only insert the record if it doesn't already exist according
            # to unique constraints.
            with transaction.atomic():
                record.save()
        except IntegrityError:
            pass
                
def acad_obj_group_types():
    print 'Inserting Acad_Obj_Group_Type records...'
    records = []
    
    record = Acad_Obj_Group_Type(name='program')
    records.append(record)
    
    record = Acad_Obj_Group_Type(name='subject')
    records.append(record)
    
    record = Acad_Obj_Group_Type(name='stream')
    records.append(record)
    
    insert_records(records)
    
def careers():
    print 'Inserting Career records...'
    records = []
    
    record = Career(name='undergraduate', abbreviation='UG')
    records.append(record)
    
    record = Career(name='postgraduate', abbreviation='PG')
    records.append(record)
    
    record = Career(name='nonaward', abbreviation='NA')
    records.append(record)
    
    record = Career(name='research', abbreviation='RS')
    records.append(record)
    
    insert_records(records)
    
def org_unit_types():
    print 'Inserting Org_Unit_Type records...'
    records = []
    
    i = 0
    
    record = Org_Unit_Type(id=i, name='University')
    i += 1
    records.append(record)
    
    record = Org_Unit_Type(id=i, name='Faculty')
    i += 1
    records.append(record)
    
    record = Org_Unit_Type(id=i, name='School')
    i += 1
    records.append(record)
    
    record = Org_Unit_Type(id=i, name='Division')
    i += 1
    records.append(record)
    
    record = Org_Unit_Type(id=i, name='Department')
    i += 1
    records.append(record)
    
    record = Org_Unit_Type(id=i, name='Centre')
    i += 1
    records.append(record)
    
    record = Org_Unit_Type(id=i, name='Special')
    i += 1
    records.append(record)
    
    record = Org_Unit_Type(id=i, name='Institute')
    i += 1
    records.append(record)
    
    record = Org_Unit_Type(id=i, name='Unit')
    i += 1
    records.append(record)
    
    record = Org_Unit_Type(id=i, name='Committee')
    i += 1
    records.append(record)
    
    insert_records(records)
    
def rule_types():
    print 'Inserting Rule_Type records...'
    records = []
    
    record = Rule_Type(abbreviation='PE', name='Program Elective')
    records.append(record)
    
    record = Rule_Type(abbreviation='RQ', name='Prerequisite')
    records.append(record)
    
    record = Rule_Type(abbreviation='RC', name='Recommended')
    records.append(record)
    
    record = Rule_Type(abbreviation='GE', name='General Education')
    records.append(record)
    
    record = Rule_Type(abbreviation='FE', name='Free Elective')
    records.append(record)
    
    record = Rule_Type(abbreviation='CC', name='Core Course')
    records.append(record)
    
    record = Rule_Type(abbreviation='DS', name='Stream')
    records.append(record)
    
    record = Rule_Type(abbreviation='LR', name='Limit')
    records.append(record)
    
    record = Rule_Type(abbreviation='MR', name='Maturity')
    records.append(record)
    
    insert_records(records)
    
def semesters():
    print 'Inserting Semester records...'
    records = []
    
    record = Semester(abbreviation='S1', name='Semester 1')
    records.append(record)
    
    record = Semester(abbreviation='S2', name='Semester 2')
    records.append(record)
    
    insert_records(records)

def main():
    print 'Inserting core data into the database...\n'
    
    acad_obj_group_types()
    careers()
    org_unit_types()
    rule_types()
    semesters()
    
    print '\nDone :)'

if __name__ == '__main__':
    main()