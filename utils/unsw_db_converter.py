#!/usr/bin/env python

import sys
import re
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'comp4920.settings'
django.setup()

from polygons.models.Acad_Obj_Group_Type import Acad_Obj_Group_Type
from polygons.models.Career import Career
from polygons.models.Rule_Type import Rule_Type
from polygons.models.Semester import Semester

VALUE_DELIMITER = '\t'
COLUMN_DELIMITER = ', '
NULL = r'\N'
CACHE_DELIMITER = ' '
HANDBOOK_PROGRAMS_CACHE_FILE = 'handbook_programs.txt'
HANDBOOK_SUBJECTS_CACHE_FILE = 'handbook_subjects.txt'
ADFA_SUBJECTS_FILE = 'adfa_subjects.txt'

TABLE_ORDER = [
    'acad_object_groups',
    'rules',
    'orgunits',
    'subject_areas',
    'subjects',
    'program_degrees',
    'programs',
    'orgunit_groups',
    'courses',
    'program_group_members',
    'program_rules',
    'streams',
    'stream_group_members',
    'stream_rules',
    'subject_group_members',
    'subject_prereqs'
]

ADFA_SUBJECT_CACHE = {}
UNIQUE_DEGREES = {}
HANDBOOK_CACHE = {
    'programs' : {},
    'subjects' : {}
}
FILTERED_RECORDS = {
    'rules' : {},
    'subjects' : {},
    'programs' : {}
}
UNIQUE_FIELDS = {
    'programs' : {
        'code' : {}
    },
    'program_degrees' : {
        'name' : {}
    }
}
PROGRAM_RULES = {}
SUBJECT_AREAS = {}
MISC_SUBJECT_AREA = 'MISC'

def die(message):
    sys.stderr.write('%s\n'%message)
    sys.exit(1)

# Functions used to generate values for new columns

def acad_obj_groups__enumerated(**kwargs):
    if kwargs['gdefby'] == 'enumerated':
        return 't'
    else:
        return 'f'

def programs__degree(**kwargs):
    try:
        degree_name = UNIQUE_DEGREES[kwargs['id']]
    except KeyError:
        return NULL

    return UNIQUE_FIELDS['program_degrees']['name'][degree_name]

def subjects__subject_area(**kwargs):
    subject_area_code = re.sub(r'[0-9]+$', '', kwargs['code'])
    try:
        return SUBJECT_AREAS[subject_area_code]
    except KeyError:
        return SUBJECT_AREAS[MISC_SUBJECT_AREA]

# Functions used to alter existing columns

def acad_obj_groups__gtype(**kwargs):
    return str(Acad_Obj_Group_Type.objects.get(name=kwargs['gtype']).id)

def acad_obj_groups__glogic(**kwargs):
    if kwargs['glogic'] == 'or':
        return 'true'
    else:
        return 'false'

def subjects__career(**kwargs):
    return str(Career.objects.get(abbreviation=kwargs['career']).id)

def programs__career(**kwargs):
    return str(Career.objects.get(abbreviation=kwargs['career']).id)

def rules__type(**kwargs):
    return str(Rule_Type.objects.get(abbreviation=kwargs['type']).id)

def subject_prereqs__career(**kwargs):
    return str(Career.objects.get(abbreviation=kwargs['career']).id)

def courses__semester(**kwargs):
    if kwargs['semester'] == '201':
        return str(Semester.objects.get(abbreviation='S1').id)
    elif kwargs['semester'] == '203':
        return str(Semester.objects.get(abbreviation='S2').id)

# Functions used to determine whether a record should make it through

def do_nothing_filter(**kwargs):
    return True

def subjects__filter(**kwargs):
    career = Career.objects.filter(abbreviation=kwargs['career']).exists()
    uoc = kwargs['uoc'] != NULL
    try:
        ADFA_SUBJECT_CACHE[kwargs['id']]
        adfa = True
    except KeyError:
        adfa = False
    valid = career and uoc and not adfa
    valid = valid and HANDBOOK_CACHE['subjects'][kwargs['id']]

    if not valid:
        FILTERED_RECORDS['subjects'][kwargs['id']] = True
    
    return valid

def courses__filter(**kwargs):
    semester = kwargs['semester'] in ['201', '203']
    try:
        FILTERED_RECORDS['subjects'][kwargs['subject']]
        subject = False
    except KeyError:
        subject = True

    return semester and subject

def program_degrees__filter(**kwargs):
    UNIQUE_DEGREES[kwargs['program']] = kwargs['name']

    try:
        UNIQUE_FIELDS['program_degrees']['name'][kwargs['name']]
        return False
    except KeyError:
        UNIQUE_FIELDS['program_degrees']['name'][kwargs['name']] = kwargs['id']

    return True

def rules__filter(**kwargs):
    rule_type = Rule_Type.objects.filter(abbreviation=kwargs['type']).exists()
    acad_obj_group = kwargs['ao_group'] != NULL
    result = rule_type and acad_obj_group
    
    if result and kwargs['type'] == 'LR':
        if kwargs['min'] != NULL or kwargs['max'] == NULL:
            result = False

    if not result:
        FILTERED_RECORDS['rules'][kwargs['id']] = True

    return result

def program_rules__filter(**kwargs):
    try:
        FILTERED_RECORDS['rules'][kwargs['rule']]
        return False
    except KeyError:
        pass

    try:
        FILTERED_RECORDS['programs'][kwargs['program']]
        return False
    except KeyError:
        return True

def stream_rules__filter(**kwargs):
    try:
        FILTERED_RECORDS['rules'][kwargs['rule']]
        return False
    except KeyError:
        return True

def subject_group_members__filter(**kwargs):
    try:
        FILTERED_RECORDS['subjects'][kwargs['subject']]
        return False
    except KeyError:
        return True

def subject_prereqs__filter(**kwargs):
    try:
        FILTERED_RECORDS['rules'][kwargs['rule']]
        return False
    except KeyError:
        pass
    
    try:
        FILTERED_RECORDS['subjects'][kwargs['subject']]
        return False
    except KeyError:
        return True

def programs__filter(**kwargs):
    try:
        UNIQUE_FIELDS['programs']['code'][kwargs['code']]
        FILTERED_RECORDS['programs'][kwargs['id']] = True
        return False
    except KeyError:
        UNIQUE_FIELDS['programs']['code'][kwargs['code']] = True

    if not HANDBOOK_CACHE['programs'][kwargs['id']]:
        FILTERED_RECORDS['programs'][kwargs['id']] = True
        return False

    if not PROGRAM_RULES:
        for program_rule in kwargs['python_rep']['program_rules']:
            PROGRAM_RULES[program_rule['program']] = True

    try:
        PROGRAM_RULES[kwargs['id']]
    except KeyError:
        FILTERED_RECORDS['programs'][kwargs['id']] = True
        return False

    if kwargs['uoc'] == NULL:
        FILTERED_RECORDS['programs'][kwargs['id']] = True
        return False 
    
    return True

def program_group_members__filter(**kwargs):
    try:
        FILTERED_RECORDS['programs'][kwargs['program']]
        return False
    except KeyError:
        return True

def subject_areas__filter(**kwargs):
    SUBJECT_AREAS[kwargs['code']] = kwargs['id']
    return True

# Configuration to convert the UNSW PostgreSQL dumped data into a dump that is
# compatible with our application.
TABLES_TO_EDIT = {
    'acad_object_groups' : {
        'new_table_name' : 'polygons_acad_obj_group',
        'delete_columns' : ['gdefby', 'negated'],
        'rename_columns' : {
            'gtype' : 'type_id',
            'parent' : 'parent_id',
            'glogic' : 'logical_or'
        },
        'alter_columns' : {
            'gtype' : acad_obj_groups__gtype,
            'glogic' : acad_obj_groups__glogic
        }, 
        'new_columns' : {
            'enumerated' : acad_obj_groups__enumerated
        },
        'filter_func' : do_nothing_filter
    },
    'orgunits' : {
        'new_table_name' : 'polygons_org_unit',
        'delete_columns' : ['name', 'phone', 'email', 'website', 'starting',
                            'ending'],
        'rename_columns' : {
            'utype' : 'type_id',
            'longname' : 'name',
            'unswid' : 'code'
        },
        'alter_columns' : {}, 
        'new_columns' : {},
        'filter_func' : do_nothing_filter
    },
    'subject_areas' : {
        'new_table_name' : 'polygons_subject_area',
        'delete_columns' : [],
        'rename_columns' : {},
        'alter_columns' : {}, 
        'new_columns' : {},
        'filter_func' : subject_areas__filter
    },
    'subjects' : {
        'new_table_name' : 'polygons_subject',
        'delete_columns' : ['name', 'eftsload', 'syllabus', 'contacthpw',
                            'equivalent'],
        'rename_columns' : {
            'longname' : 'name',
            'offeredby' : 'offered_by_id',
            'career' : 'career_id',
            'excluded' : 'excluded_id'
        },
        'alter_columns' : {
            'career' : subjects__career
        }, 
        'new_columns' : {
            'subject_area_id' : subjects__subject_area
        },
        'filter_func' : subjects__filter
    },
    'courses' : {
        'new_table_name' : 'polygons_course',
        'delete_columns' : ['homepage'],
        'rename_columns' : {
            'subject' : 'subject_id',
            'semester' : 'semester_id'
        },
        'alter_columns' : {
            'semester' : courses__semester
        }, 
        'new_columns' : {},
        'filter_func' : courses__filter
    },
    'program_degrees' : {
        'new_table_name' : 'polygons_degree',
        'delete_columns' : ['program', 'dtype'],
        'rename_columns' : {
            'abbrev' : 'abbreviation'
        },
        'alter_columns' : {}, 
        'new_columns' : {},
        'filter_func' : program_degrees__filter
    },
    'orgunit_groups' : {
        'new_table_name' : 'polygons_org_unit_group',
        'delete_columns' : [],
        'rename_columns' : {
            'owner' : 'owner_id',
            'member' : 'member_id'
        },
        'alter_columns' : {}, 
        'new_columns' : {},
        'filter_func' : do_nothing_filter
    },
    'programs' : {
        'new_table_name' : 'polygons_program',
        'delete_columns' : ['duration', 'description'],
        'rename_columns' : {
            'offeredby' : 'offered_by_id',
            'career' : 'career_id'
        },
        'alter_columns' : {
            'career' : programs__career
        }, 
        'new_columns' : {
            'degree_id' : programs__degree
        },
        'filter_func' : programs__filter
    },
    'rules' : {
        'new_table_name' : 'polygons_rule',
        'delete_columns' : [],
        'rename_columns' : {
            'type' : 'type_id',
            'ao_group' : 'acad_obj_group_id'
        },
        'alter_columns' : {
            'type' : rules__type
        }, 
        'new_columns' : {},
        'filter_func' : rules__filter
    },
    'streams' : {
        'new_table_name' : 'polygons_stream',
        'delete_columns' : ['offeredby', 'stype', 'description'],
        'rename_columns' : {},
        'alter_columns' : {}, 
        'new_columns' : {},
        'filter_func' : do_nothing_filter
    },
    'subject_group_members' : {
        'new_table_name' : 'polygons_subject_group_member',
        'delete_columns' : [],
        'rename_columns' : {
            'subject' : 'subject_id',
            'ao_group' : 'acad_obj_group_id'
        },
        'alter_columns' : {}, 
        'new_columns' : {},
        'filter_func' : subject_group_members__filter
    },
    'subject_prereqs' : {
        'new_table_name' : 'polygons_subject_prereq',
        'delete_columns' : [],
        'rename_columns' : {
            'subject' : 'subject_id',
            'career' : 'career_id',
            'rule' : 'rule_id'
        },
        'alter_columns' : {
            'career' : subject_prereqs__career
        }, 
        'new_columns' : {},
        'filter_func' : subject_prereqs__filter
    },
    'program_group_members' : {
        'new_table_name' : 'polygons_program_group_member',
        'delete_columns' : [],
        'rename_columns' : {
            'program' : 'program_id',
            'ao_group' : 'acad_obj_group_id'
        },
        'alter_columns' : {}, 
        'new_columns' : {},
        'filter_func' : program_group_members__filter
    },
    'program_rules' : {
        'new_table_name' : 'polygons_program_rule',
        'delete_columns' : [],
        'rename_columns' : {
            'program' : 'program_id',
            'rule' : 'rule_id'
        },
        'alter_columns' : {}, 
        'new_columns' : {},
        'filter_func' : program_rules__filter
    },
    'stream_group_members' : {
        'new_table_name' : 'polygons_stream_group_member',
        'delete_columns' : [],
        'rename_columns' : {
            'stream' : 'stream_id',
            'ao_group' : 'acad_obj_group_id'
        },
        'alter_columns' : {}, 
        'new_columns' : {},
        'filter_func' : do_nothing_filter
    },
    'stream_rules' : {
        'new_table_name' : 'polygons_stream_rule',
        'delete_columns' : [],
        'rename_columns' : {
            'stream' : 'stream_id',
            'rule' : 'rule_id'
        },
        'alter_columns' : {}, 
        'new_columns' : {},
        'filter_func' : stream_rules__filter
    }
}

def generate_column_indices_to_delete(table_name, column_names):
    table = TABLES_TO_EDIT[table_name]
    columns = {}
    result = []
    
    i = 0
    for column_name in column_names.split(COLUMN_DELIMITER):
        columns[column_name] = i
        i += 1

    for column_name in table['delete_columns']:
        result.append(columns[column_name])

    return result

def alter_schema(table_name, column_names, delete_column_indices):
    table = TABLES_TO_EDIT[table_name]
    result = 'COPY %s (%s) FROM stdin;'
    table_name = table['new_table_name']

    column_name_list = []
    i = 0
    for column_name in column_names.split(COLUMN_DELIMITER):
        try:
            delete_column_indices.index(i)
            to_delete = True
        except ValueError:
            to_delete = False

        if not to_delete:
            try:
                column_name = table['rename_columns'][column_name]
            except KeyError:
                pass

            column_name_list.append(column_name)

        i += 1

    for new_column_name in table['new_columns'].keys():
        column_name_list.append(new_column_name)

    column_names = COLUMN_DELIMITER.join(column_name_list)

    return result%(table_name, column_names)

def alter_record(line, table_name, delete_column_indices, original_column_names):
    table = TABLES_TO_EDIT[table_name]
    values = line.split(VALUE_DELIMITER)
    original_column_names = original_column_names.split(COLUMN_DELIMITER)
    new_values = []

    original_data = {}
    for column_name, value in zip(original_column_names, values):
        original_data[column_name] = value

    i = 0
    for value in values:
        try:
            delete_column_indices.index(i)
            to_delete = True
        except ValueError:
            to_delete = False

        if not to_delete:
            try:
                value = table['alter_columns'][original_column_names[i]](**original_data)
            except KeyError:
                pass
            new_values.append(value)

        i += 1

    for gen_value_function in table['new_columns'].values():
        new_values.append(gen_value_function(**original_data))

    return VALUE_DELIMITER.join(new_values)

def should_write_record(line, table_name, column_names, python_rep):
    column_names = column_names.split(COLUMN_DELIMITER)
    original_data = {'python_rep':python_rep}
    table = TABLES_TO_EDIT[table_name]

    for column_name, value in zip(column_names, line.split(VALUE_DELIMITER)):
        original_data[column_name] = value

    return table['filter_func'](**original_data)

def convert_db_dump(dump, out_file, python_rep):
    needs_edit = False

    for line in dump:
        to_write = True
        line = line.strip()
        match = re.search(r'^COPY ([a-z_]+) \(([a-z_ ,]+)\) FROM stdin;', line)
        if match:
            (table_name, column_names) = match.groups()
            try:
                TABLES_TO_EDIT[table_name]
                needs_edit = True
            except KeyError:
                pass

            if needs_edit:
                delete_column_indices = generate_column_indices_to_delete(table_name, 
                    column_names)
                line = alter_schema(table_name, column_names,
                    delete_column_indices)

        elif re.search(r'^\\\.$', line):
            needs_edit = False
        elif needs_edit:
            to_write = should_write_record(line, table_name, column_names,
                                           python_rep)
            if to_write:
                line = alter_record(line, table_name, delete_column_indices,
                    column_names)

        if to_write:
            out_file.write('%s\n'%line)

def reorder_dump(dump):
    reordered_dump = []
    preamble = []
    in_table = False
    ordered_tables = {}

    for line in dump:
        match = re.search(r'^COPY ([a-z_]+) \([a-z_ ,]+\) FROM stdin;', line)
        if match:
            table_name = match.groups()[0]
            ordered_tables[table_name] = []
            in_table = True
        elif re.search(r'^SET ', line):
            preamble.append(line)
        elif re.search(r'^\\\.$', line):
            if in_table:
                ordered_tables[table_name].append(line)    
            in_table = False

        if in_table:
            ordered_tables[table_name].append(line)

    reordered_dump += preamble

    for table_name in TABLE_ORDER:
        reordered_dump += ordered_tables[table_name]
    
    return reordered_dump

def gen_python_rep(dump):
    rep = {}
    is_data = False
    table_name = ''
    column_names = ''

    i = 0
    for line in dump:
        line = line.strip()
        match = re.search(r'^COPY ([a-z_]+) \(([a-z_ ,]+)\) FROM stdin;', line)
        if match:
            is_data = True
            (table_name, column_names) = match.groups()
            column_names = column_names.split(COLUMN_DELIMITER)
            rep[table_name] = []
            i = 0
        elif re.search(r'^\\\.$', line):
            is_data = False
        elif is_data:
            record = {}
            record_id = ''
            for column_name, value in zip(column_names, 
                                          line.split(VALUE_DELIMITER)):
                record[column_name] = value
                if column_name == 'id':
                    record_id = value

            rep[table_name].append(record)
            i += 1

    return rep

def parallel_handbook_requests(records, cache_key, out_file, base_url):
    for record in records[5290:]:
        try:
            career = Career.objects.get(abbreviation=record['career']).name
        except Career.DoesNotExist:
            continue
        url = base_url%(career, record['code'])
        result = 1
        try:
            urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            if e.code == 404:
                result = 0
            else:
                raise e

        out_file.write('%s %d\n'%(record['id'], result))

def saturate_handbook_cache():
    try:
        with open(HANDBOOK_PROGRAMS_CACHE_FILE, 'r') as f:
            programs = f.readlines()
    except IOError:
        die('Could not open handbook programs cache file!')
    
    for program in programs:
        program = program.strip()
        (program_id,result) = program.split(CACHE_DELIMITER)
        HANDBOOK_CACHE['programs'][program_id] = bool(int(result))

    try:
        with open(HANDBOOK_SUBJECTS_CACHE_FILE, 'r') as f:
            subjects = f.readlines()
    except IOError:
        die('Could not open handbook subjects cache file!')
    
    for subject in subjects:
        subject = subject.strip()
        (subject_id,result) = subject.split(CACHE_DELIMITER)
        HANDBOOK_CACHE['subjects'][subject_id] = bool(int(result))

def saturate_adfa_subject_cache():
    try:
        with open(ADFA_SUBJECTS_FILE, 'r') as f:
            subjects = f.read().strip()
    except IOError:
        die ('Could not open ADFA subjects file!')

    for subject in subjects.split(','):
        ADFA_SUBJECT_CACHE[subject] = True

def main():
    if len(sys.argv) != 2:
        die('Usage: %s dumpFilePath'%sys.argv[0])

    try:
        with open(sys.argv[1], 'r') as f:
            dump = f.readlines()
    except (IOError, OSError):
        die('Error: could not read from dump file "%s"!'%sys.argv[1])

    python_rep = gen_python_rep(dump)
    saturate_handbook_cache()
    saturate_adfa_subject_cache()
    dump = reorder_dump(dump)
    convert_db_dump(dump, sys.stdout, python_rep)

if __name__ == '__main__':
    main()
