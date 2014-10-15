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
		select owner_id into _parent
		from polygons_org_unit_group where member_id = _org_unit_id;
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

create function expand_clean_program_pattern(_pattern text)
returns setof integer
AS $$
declare
   _program_id integer;
begin

   for _program_id in (
      select id
      from polygons_program
      where code ~ _pattern
   ) loop
      return next _program_id;
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

create function expand_program_pattern(_pattern text)
returns setof integer
AS $$
declare
   _program_id integer;
   _program record;
   _faculty_matches text array;
   _clean_pattern text;
   _negation text;
   _org_unit_code text;
   _constraint_faculty_id integer;
   _program_faculty_id integer;
begin

   _faculty_matches := regexp_matches(_pattern, '([^/]+)/F=(!?)([a-zA-Z]+)');
   if (_faculty_matches) then
      
      _clean_pattern := _faculty_matches[0];
      _negation := _faculty_matches[1];
      _org_unit_code := _faculty_matches[2];

      for _program_id in (
         select expand_clean_program_pattern(_clean_pattern)
      ) loop
         
         select * into _program
         from polygons_program
         where id = _program_id;

         _program_faculty_id := get_faculty(_program.offered_by_id);
         select id into _constraint_faculty_id
         from polygons_org_unit
         where code = _org_unit_code;

         if (_constraint_faculty_id is null) then
            return next _program_id;
         elsif (_program_faculty_id = _constraint_faculty_id) then
            if (!negation) then
               return next _program_id;
            end if;
         else
            if (negation) then
               return next _program_id;
            end if;
         end if;

      end loop;

   elsif regexp_matches(_pattern, '^!') then

      for _program_id in (
         select id from polygons_program
         except
         select expand_clean_program_pattern(_pattern)
      ) loop
         return next _program_id;
      end loop;

   else 
      
      for _program_id in (
         select expand_clean_program_pattern(_pattern)
      ) loop
         return next _program_id;
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

create function expand_program_patterns(_patterns text)
returns setof integer
AS $$
declare
   _program_id integer;
   _unit_pattern text;
begin

   _patterns := regexp_replace(_patterns, ';', ',', 'g');
   for _unit_pattern in (
      select regexp_split_to_table(_patterns, ',')
   ) loop
      
      for _program_id in (
         select expand_program_pattern(_unit_pattern)
      ) loop
         return next _program_id;
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

create function expand_program_rule(_acad_obj_group_id integer)
returns setof integer
AS $$
declare
   _acad_obj_group record;
   _program_id integer;
begin

   select * into _acad_obj_group
   from polygons_acad_obj_group
   where id = _acad_obj_group_id;

   if (_acad_obj_group.enumerated = true) then
      for _program_id in (
         select program_id
         from polygons_program_group_member
         where acad_obj_group_id = _acad_obj_group_id
      ) loop
         return next _program_id;
      end loop;
   else
      
      for _program_id in (
         select expand_program_patterns(_acad_obj_group.definition)
      ) loop
         return next _program_id;
      end loop;

   end if;

   if (_acad_obj_group.parent_id is not null) then
      for _program_id in (
         select expand_program_rule(_acad_obj_group.parent_id)
      ) loop
         return next _program_id;
      end loop;
   end if;

end;
$$ language plpgsql;

create function generate_program_subjects(_program_id integer,
                                          _faculty_id integer)
returns setof integer
AS $$
declare
   _subject_id integer;
   _acad_obj_group_id integer;
   _ds_acad_obj_group_id integer;
begin
   
   for _acad_obj_group_id in (
      select r.acad_obj_group_id
      from polygons_program_rule pr join polygons_rule r on (pr.rule_id=r.id)
         join polygons_rule_type rt on (r.type_id=rt.id)
      where pr.program_id=_program_id and rt.abbreviation <> 'DS'
   ) loop
      
      for _subject_id in (
         select expand_subject_rule(_acad_obj_group_id, _faculty_id)
      ) loop
         return next _subject_id;
      end loop;

   end loop;

   for _ds_acad_obj_group_id in (
      select r.acad_obj_group_id
      from polygons_program_rule pr join polygons_rule r on (pr.rule_id=r.id)
         join polygons_rule_type rt on (r.type_id=rt.id)
      where pr.program_id=_program_id and rt.abbreviation = 'DS'
   ) loop
      
      for _acad_obj_group_id in (
         select r.acad_obj_group_id
         from polygons_stream_group_member sgm join polygons_stream_rule sr on 
            (sgm.stream_id=sr.stream_id) join polygons_rule r on 
            (sr.rule_id=r.id)
         where sgm.acad_obj_group_id = _ds_acad_obj_group_id
      ) loop

         for _subject_id in (
            select expand_subject_rule(_acad_obj_group_id, _faculty_id)
         ) loop
            return next _subject_id;
         end loop;
         
      end loop;

   end loop;

end;
$$ language plpgsql;

create function get_exclusion_subjects(_existing_subjects integer array,
                                       _faculty_id integer)
returns setof integer
AS $$
declare
   _subject_id integer;
   _existing_subject_id integer;
   _excluded_id integer;
begin

   for _existing_subject_id in (
      select unnest(_existing_subjects)
   ) loop

      select excluded_id into _excluded_id
      from polygons_subject where id = _existing_subject_id;

      for _subject_id in (
         select expand_subject_rule(_excluded_id, _faculty_id)
      ) loop
         return next _subject_id;
      end loop;
   
   end loop;

end;
$$ language plpgsql;

create function get_core_subjects(_program_id integer)
returns setof integer
AS $$
declare
   _program record;
   _subject_id integer;
   _faculty_id integer;
   _acad_obj_group_id integer;
   _ds_acad_obj_group_id integer;
begin
   
   select * into _program
   from polygons_program
   where id = _program_id;

   _faculty_id := get_faculty(_program.offered_by_id);

   for _acad_obj_group_id in (
      select r.acad_obj_group_id
      from polygons_program_rule pr join polygons_rule r on (pr.rule_id=r.id)
         join polygons_rule_type rt on (r.type_id=rt.id)
      where pr.program_id = _program_id and rt.abbreviation = 'CC'
   ) loop

      for _subject_id in (
         select expand_subject_rule(_acad_obj_group_id, _faculty_id)
      ) loop
         return next _subject_id;
      end loop;

   end loop;
   
   for _ds_acad_obj_group_id in (
      select r.acad_obj_group_id
      from polygons_program_rule pr join polygons_rule r on (pr.rule_id=r.id)
         join polygons_rule_type rt on (r.type_id=rt.id)
      where pr.program_id = _program_id and rt.abbreviation = 'DS'
   ) loop

      for _acad_obj_group_id in (
         select r.acad_obj_group_id
         from polygons_stream_group_member sgm join polygons_stream_rule sr on
            (sgm.stream_id=sr.stream_id) join polygons_rule r on 
            (sr.rule_id=r.id) join polygons_rule_type rt on (r.type_id=rt.id)
         where sgm.acad_obj_group_id = _ds_acad_obj_group_id and
            rt.abbreviation = 'CC'
      ) loop

         for _subject_id in (
            select expand_subject_rule(_acad_obj_group_id, _faculty_id)
         ) loop
            return next _subject_id;
         end loop;

      end loop;

   end loop;

end;
$$ language plpgsql;

create function get_program_subjects(_program_id integer, _semester_id integer,
                                     _existing_subjects integer array)
returns setof integer
AS $$
declare
   _program record;
   _subject_id integer;
   _faculty_id integer;
   _acad_obj_group_id integer;
   _rule record;
   _aog_type_name text;
   _meets_prereqs boolean;
begin
   
   select * into _program
   from polygons_program
   where id = _program_id;

   _faculty_id := get_faculty(_program.offered_by_id);

   for _subject_id in (
      select generate_program_subjects(_program_id, _faculty_id)
      except
      select get_exclusion_subjects(_existing_subjects, _faculty_id)
   ) loop

      if (_existing_subjects @> array[_subject_id]) then
         -- Subject is already in plan
         continue;
      end if;
         
      if (
         not exists(
            select *
            from polygons_course c
            where semester_id = _semester_id and subject_id = _subject_id
         )
      ) then
         -- Subject is not offered in specified semester
         continue;
      end if;

      _meets_prereqs := true;

      for _rule in (
         select r.*
         from polygons_subject_prereq sp join polygons_rule r on 
            (sp.rule_id=r.id)
         where subject_id = _subject_id and career_id = _program.career_id
      ) loop

         select aogt.name into _aog_type_name
         from polygons_acad_obj_group_type aogt join polygons_acad_obj_group aog
            on (aogt.id=aog.type_id) 
         where aog.id = _rule.id;

         if (_aog_type_name = 'program') then

            if (
               not exists(
                  select *
                  from expand_program_rule(_rule.acad_obj_group_id)
                  where expand_program_rule = _program_id
               )
            ) then
               _meets_prereqs := false;
               exit;
            end if;

         elsif (_aog_type_name = 'subject') then

            if (
               exists(
                  select expand_subject_rule(_rule.acad_obj_group_id, _faculty_id)
                  except
                  select unnest(_existing_subjects)
               )
            ) then
               _meets_prereqs := false;
               exit;
            end if;

         end if;

      end loop;

      if (_meets_prereqs) then
         return next _subject_id;
      end if;
      
   end loop;

end;
$$ language plpgsql;

create function get_dependent_subjects(_program_id integer,
                                       _pending_subject_id integer,
                                       _existing_subjects integer array)
returns setof integer
AS $$
declare
   _program record;
   _rule record;
   _faculty_id integer;
   _existing_subject_id integer;
   _subject_id integer;
begin
   
   select * into _program
   from polygons_program
   where id = _program_id;
   
   _faculty_id := get_faculty(_program.offered_by_id);
   
   for _existing_subject_id in (
      select unnest(_existing_subjects)
   ) loop

      for _rule in (
         select r.*
         from polygons_subject_prereq sp join polygons_rule r on 
            (sp.rule_id=r.id) join polygons_acad_obj_group aog on
            (r.acad_obj_group_id=aog.id) join polygons_acad_obj_group_type aogt
            on (aog.type_id=aogt.id)
         where subject_id = _existing_subject_id and
            career_id = _program.career_id and aogt.name = 'subject'
      ) loop

         if (
            exists(
               select *
               from expand_subject_rule(_rule.acad_obj_group_id, _faculty_id)
               where expand_subject_rule = _pending_subject_id
            )
         ) then

            return next _existing_subject_id;

            for _subject_id in (
               select get_dependent_subjects(_program.id, _existing_subject_id,
                  array_remove(_existing_subjects, _existing_subject_id))
            ) loop
               return next _subject_id;
            end loop;

         end if;

      end loop;

   end loop;

end;
$$ language plpgsql;
