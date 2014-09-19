#!/bin/bash

if [ $# -ne 0 -a $# -ne 1 ]; then
   echo Usage: $0 "[test_file_name]"
   exit 1
fi;

if [ $# -eq 1 ]; then
   ./manage.py test -p "$1"
else
   ./manage.py test 
fi;
