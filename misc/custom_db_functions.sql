create function get_faculty(_org_unit_id integer)
 returns integer
AS $$
declare
	_name text;
	_parent integer;
begin
	if (_org_unit_id is null) then
		return null;
	end if;

	select t.name into _name
	from polygons_org_unit u join polygons_org_unit_type t on (u.type_id=t.id);

	if (_name is null) then
		return null;
	elsif (_name = 'University') then
		return null;
	elsif (_name = 'Faculty') then
		return _org_unit_id;
	else
		select owner into _parent
		from polygons_org_unit_group where member = _org_unit_id;
		return get_faculty(_parent);
	end if;
end;
$$ language plpgsql;

create function expand_clean_subject_pattern(_pattern text, _faculty_id integer)
returns setof integer
AS $$
declare
   _subject record;
   _subject_faculty_id integer;
   _gen_ed boolean;
begin

   _gen_ed := _pattern = 'GENG####';

   for _subject in (
      select s.*
      from polygons_subject_pattern_cache spc join polygons_subject_pattern sp on
         (spc.subject_pattern_id=sp.id) join polygons_subject s on 
         (spc.subject_id=s.id)
      where sp.pattern = _pattern
   ) loop
      
      if (_gen_ed) then

         select * into _subject_faculty_id
         from get_faculty(_subject.offered_by_id);

         if (_subject_faculty_id is not null) then
            if (_subject_faculty_id != _faculty_id) then
               return next _subject.id;
            end if;
         end if;

      else
         return next _subject.id;
      end if;

   end loop;

end;
$$ language plpgsql;

create function expand_subject_pattern(_pattern text, _faculty_id integer)
returns setof integer
AS $$
declare
   _subject_id integer;
   _subject record;
   _faculty_matches text array;
   _clean_pattern text;
   _negation text;
   _org_unit_code text;
   _constraint_faculty_id integer;
   _subject_faculty_id integer;
begin

   _faculty_matches := regexp_matches(_pattern, '([^/]+)/F=(!?)([a-zA-Z]+)');
   if (_faculty_matches) then
      
      _clean_pattern := _faculty_matches[0];
      _negation := _faculty_matches[1];
      _org_unit_code := _faculty_matches[2];

      for _subject_id in (
         select expand_clean_subject_pattern(_clean_pattern, _faculty_id)
      ) loop
         
         select * into _subject
         from polygons_subject
         where id = _subject_id;

         _subject_faculty_id := get_faculty(_subject.offered_by_id);
         select id into _constraint_faculty_id
         from polygons_org_unit
         where code = _org_unit_code;

         if (_constraint_faculty_id is null) then
            return next _subject_id;
         elsif (_subject_faculty_id = _constraint_faculty_id) then
            if (!negation) then
               return next _subject_id;
            end if;
         else
            if (negation) then
               return next _subject_id;
            end if;
         end if;

      end loop;

   elsif regexp_matches(_pattern, '^!') then

      for _subject_id in (
         select id from polygons_subject
         except
         select expand_clean_subject_pattern(_pattern, _faculty_id)
      ) loop
         return next _subject_id;
      end loop;

   else 
      
      for _subject_id in (
         select expand_clean_subject_pattern(_pattern, _faculty_id)
      ) loop
         return next _subject_id;
      end loop;

   end if;

end;
$$ language plpgsql;

create function expand_subject_patterns(_patterns text, _faculty_id integer)
returns setof integer
AS $$
declare
   _subject_id integer;
   _unit_pattern text;
begin

   _patterns := regexp_replace(_patterns, ';', ',', 'g');
   for _unit_pattern in (
      select regexp_split_to_table(_patterns, ',')
   ) loop
      
      for _subject_id in (
         select expand_subject_pattern(_unit_pattern, _faculty_id)
      ) loop
         return next _subject_id;
      end loop;

   end loop;

end;
$$ language plpgsql;

create function expand_subject_rule(_acad_obj_group_id integer,
                                    _faculty_id integer)
returns setof integer
AS $$
declare
   _acad_obj_group record;
   _subject_id integer;
begin

   select * into _acad_obj_group
   from polygons_acad_obj_group
   where id = _acad_obj_group_id;

   if (_acad_obj_group.enumerated = true) then
      for _subject_id in (
         select subject_id
         from polygons_subject_group_member
         where acad_obj_group_id = _acad_obj_group_id
      ) loop
         return next _subject_id;
      end loop;
   else
      
      for _subject_id in (
         select expand_subject_patterns(_acad_obj_group.definition, _faculty_id)
      ) loop
         return next _subject_id;
      end loop;

   end if;

   if (_acad_obj_group.parent_id is not null) then
      for _subject_id in (
         select expand_subject_rule(_acad_obj_group.parent_id, _faculty_id)
      ) loop
         return next _subject_id;
      end loop;
   end if;

end;
$$ language plpgsql;
