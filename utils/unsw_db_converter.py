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
    degrees = kwargs['python_dump_rep']['program_degrees']
    unique_degrees = {}
    for degree in degrees:
        try:
            unique_degrees[degree['abbrev']]
        except KeyError:
            unique_degrees[degree['abbrev']] = degree

        if degree['program'] == kwargs['id']:
            return unique_degrees[degree['abbrev']]['id']

    return NULL;

# Functions used to alter existing columns

def acad_obj_groups__gtype(**kwargs):
    return str(Acad_Obj_Group_Type.objects.get(name=kwargs['gtype']).id)

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
    return career and uoc

def courses__filter(**kwargs):
    return kwargs['semester'] in ['201', '203']

def program_degrees__filter(**kwargs):
    records = kwargs['python_dump_rep']['program_degrees']

    unique_names = {}
    unique_abbreviations = {}
    for record in records:
        if record['id'] == kwargs['id']:
            break
        unique_names[record['name']] = True
        unique_abbreviations[record['abbrev']] = True

    try:
        unique_names[kwargs['name']]
        return False
    except KeyError:
        pass

    try:
        unique_abbreviations[kwargs['abbrev']]
        return False
    except KeyError:
        pass

    return True

def rules__filter(**kwargs):
    return Rule_Type.objects.filter(abbreviation=kwargs['type']).exists()

# Configuration to convert the UNSW PostgreSQL dumped data into a dump that is
# compatible with our application.
TABLES_TO_EDIT = {
    'acad_object_groups' : {
        'new_table_name' : 'polygons_acad_obj_group',
        'delete_columns' : ['glogic', 'gdefby', 'negated'],
        'rename_columns' : {
            'gtype' : 'type_id',
            'parent' : 'parent_id'
        },
        'alter_columns' : {
            'gtype' : acad_obj_groups__gtype 
        }, 
        'new_columns' : {
            'enumerated' : acad_obj_groups__enumerated
        },
        'filter_func' : do_nothing_filter
    },
    'orgunits' : {
        'new_table_name' : 'polygons_org_unit',
        'delete_columns' : ['name', 'unswid', 'phone', 'email', 'website',
                            'starting', 'ending'],
        'rename_columns' : {
            'utype' : 'type_id',
            'longname' : 'name'
        },
        'alter_columns' : {}, 
        'new_columns' : {},
        'filter_func' : do_nothing_filter
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
        'new_columns' : {},
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
        'delete_columns' : ['code', 'uoc', 'duration', 'description'],
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
        'filter_func' : do_nothing_filter
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
        'filter_func' : do_nothing_filter
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
        'filter_func' : do_nothing_filter
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
        'filter_func' : do_nothing_filter
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
        'filter_func' : do_nothing_filter
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
        'filter_func' : do_nothing_filter
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

def alter_record(line, table_name, delete_column_indices,
                 original_column_names, python_dump_rep):
    table = TABLES_TO_EDIT[table_name]
    values = line.split(VALUE_DELIMITER)
    original_column_names = original_column_names.split(COLUMN_DELIMITER)
    new_values = []

    original_data = {'python_dump_rep':python_dump_rep}
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

def should_write_record(line, table_name, column_names, python_dump_rep):
    column_names = column_names.split(COLUMN_DELIMITER)
    original_data = {'python_dump_rep':python_dump_rep}
    table = TABLES_TO_EDIT[table_name]

    for column_name, value in zip(column_names, line.split(VALUE_DELIMITER)):
        original_data[column_name] = value

    return table['filter_func'](**original_data)

def convert_db_dump(dump, python_rep, out_file):
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
                    column_names, python_rep)

        if to_write:
            out_file.write('%s\n'%line)

def gen_python_rep(dump):
    rep = {}
    is_data = False
    table_name = ''
    column_names = ''

    for line in dump:
        line = line.strip()
        match = re.search(r'^COPY ([a-z_]+) \(([a-z_ ,]+)\) FROM stdin;', line)
        if match:
            is_data = True
            (table_name, column_names) = match.groups()
            column_names = column_names.split(COLUMN_DELIMITER)
            rep[table_name] = []            
        elif re.search(r'^\\\.$', line):
            is_data = False
        elif is_data:
            record = {}
            for column_name, value in zip(column_names, 
                                          line.split(VALUE_DELIMITER)):
                record[column_name] = value
            rep[table_name].append(record)

    return rep

def main():
    if len(sys.argv) != 2:
        die('Usage: %s dumpFilePath'%sys.argv[0])

    try:
        with open(sys.argv[1], 'r') as f:
            dump = f.readlines()
    except (IOError, OSError):
        die('Error: could not read from dump file "%s"!'%sys.argv[1])

    python_rep = gen_python_rep(dump)
    convert_db_dump(dump, python_rep, sys.stdout)

if __name__ == '__main__':
    main()
