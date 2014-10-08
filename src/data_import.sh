#!/bin/bash

DB_DUMP_ARCHIVE_FILE=unsw_db_converted.tar.bz2
PATTERN_DUMP_ARCHIVE_FILE=pattern_cache.tar.bz2
DB_DUMP_ARCHIVE_PATH=../misc/"$DB_DUMP_ARCHIVE_FILE"
PATTERN_DUMP_ARCHIVE_PATH=../misc/"$PATTERN_DUMP_ARCHIVE_FILE"
DB_DUMP_FILE=dump.sql
DB_NAME=polygons
CUSTOM_SQL_PATH=polygons/sql/

psql -U postgres -l >/dev/null 2>&1
if [[ $? -ne 0 ]]; then
   echo "You must first ensure your PostgreSQL server is running!" >&2
   exit 1;
fi;

echo "Copying dump archive files..."
cp "$DB_DUMP_ARCHIVE_PATH" .
cp "$PATTERN_DUMP_ARCHIVE_PATH" .

echo "Untarring archive file..."
tar -xvf "$DB_DUMP_ARCHIVE_FILE" >/dev/null

echo "Deleting old polygons database (if it exists)..."
if [[ $(psql -U postgres -l | egrep "$DB_NAME" | wc -l) -ne 0 ]]; then
   dropdb -U postgres "$DB_NAME"
fi;

echo "Creating new polygons database..."
createdb -U postgres "$DB_NAME"

echo "Using migrations to define database..."
./manage.py migrate >/dev/null

echo "Inserting core data..."
./core_data.py >/dev/null

echo "Inserting UNSW data..."
psql -U postgres "$DB_NAME" -f "$DB_DUMP_FILE" >/dev/null

echo "Untarring archive file..."
tar -xvf "$PATTERN_DUMP_ARCHIVE_FILE" >/dev/null

echo "Inserting pattern cache data..."
psql -U postgres "$DB_NAME" -f "$DB_DUMP_FILE" >/dev/null

echo "Inserting custom DB functions..."
for filePath in $(find "$CUSTOM_SQL_PATH" -type f); do
   psql -U postgres polygons -f "$filePath" >/dev/null
done;

rm -f "$DB_DUMP_ARCHIVE_FILE" "$PATTERN_DUMP_ARCHIVE_FILE" "$DB_DUMP_FILE"
