#!/usr/bin/env python

import sys
import re
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'comp4920.settings'
django.setup()

from polygons.models.Acad_Obj_Group_Type import Acad_Obj_Group_Type

VALUE_DELIMITER = '\t'
COLUMN_DELIMITER = ', '

def die(message):
    sys.stderr.write('%s\n'%message)
    sys.exit(1)

# Functions used to generate values for new columns

def acad_obj_groups__enumerated(**kwargs):
    if kwargs['gdefby'] == 'enumerated':
        return 't'
    else:
        return 'f'

# Functions used to alter existing columns

def acad_obj_groups__gtype(**kwargs):
    return str(Acad_Obj_Group_Type.objects.get(name=kwargs['gtype']).id)

# Functions used to determine whether a record should make it through
def do_nothing_filter(**kwargs):
    return True

# Configuration to convert the UNSW PostgreSQL dumped data into a dump that is
# compatible with our application.
TABLES_TO_EDIT = {
    'acad_object_groups' : {
        'new_table_name' : 'acad_obj_group',
        'delete_columns' : ['glogic', 'gdefby', 'negated'],
        'rename_columns' : {
            'gtype' : 'type'
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
        'new_table_name' : 'org_unit',
        'delete_columns' : ['name', 'unswid', 'phone', 'email', 'website',
                            'starting', 'ending'],
        'rename_columns' : {
            'utype' : 'type',
            'longname' : 'name'
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
                 original_column_names):
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

def should_write_record(line, table_name, column_names):
    column_names = column_names.split(COLUMN_DELIMITER)
    original_data = {}
    table = TABLES_TO_EDIT[table_name]

    for column_name, value in zip(column_names, line.split(VALUE_DELIMITER)):
        original_data[column_name] = value

    return table['filter_func'](**original_data)

def convert_db_dump(dump, out_file):
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
            to_write = should_write_record(line, table_name, column_names)
            if to_write:
                line = alter_record(line, table_name, delete_column_indices,
                    column_names)

        if to_write:
            out_file.write('%s\n'%line)

def main():
    if len(sys.argv) != 2:
        die('Usage: %s dumpFilePath'%sys.argv[0])

    try:
        with open(sys.argv[1], 'r') as f:
            dump = f.readlines()
    except (IOError, OSError):
        die('Error: could not read from dump file "%s"!'%sys.argv[1])

    convert_db_dump(dump, sys.stdout)

if __name__ == '__main__':
    main()
