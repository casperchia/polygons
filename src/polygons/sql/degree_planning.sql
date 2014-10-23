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
	from polygons_org_unit u join polygons_org_unit_type t on (u.type_id=t.id)
   where u.id = _org_unit_id;

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
            if (_subject_faculty_id <> _faculty_id) then
               return next _subject.id;
            end if;
         else
            return next _subject.id;
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
   _negation boolean;
   _org_unit_code text;
   _constraint_faculty_id integer;
   _subject_faculty_id integer;
begin

   _faculty_matches := regexp_matches(_pattern, '([^/]+)/F=(!?)([a-zA-Z]+)');
   if (_faculty_matches is not null) then
      
      _clean_pattern := _faculty_matches[1];
      _negation := _faculty_matches[2] = '!';
      _org_unit_code := _faculty_matches[3];
         
      select get_faculty(id) into _constraint_faculty_id
      from polygons_org_unit
      where code = _org_unit_code;

      for _subject_id in (
         select expand_clean_subject_pattern(_clean_pattern, _faculty_id)
      ) loop
         
         select * into _subject
         from polygons_subject
         where id = _subject_id;

         _subject_faculty_id := get_faculty(_subject.offered_by_id);

         if (_constraint_faculty_id is null) then
            return next _subject_id;
         elsif (_subject_faculty_id = _constraint_faculty_id) then
            if (not _negation) then
               return next _subject_id;
            end if;
         else
            if (_negation) then
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
   _negation boolean;
   _org_unit_code text;
   _constraint_faculty_id integer;
   _program_faculty_id integer;
begin

   _faculty_matches := regexp_matches(_pattern, '([^/]+)/F=(!?)([a-zA-Z]+)');
   if (_faculty_matches is not null) then
      
      _clean_pattern := _faculty_matches[1];
      _negation := _faculty_matches[2] = '!';
      _org_unit_code := _faculty_matches[3];
         
      select get_faculty(id) into _constraint_faculty_id
      from polygons_org_unit
      where code = _org_unit_code;

      for _program_id in (
         select expand_clean_program_pattern(_clean_pattern)
      ) loop
         
         select * into _program
         from polygons_program
         where id = _program_id;

         _program_faculty_id := get_faculty(_program.offered_by_id);

         if (_constraint_faculty_id is null) then
            return next _program_id;
         elsif (_program_faculty_id = _constraint_faculty_id) then
            if (not _negation) then
               return next _program_id;
            end if;
         else
            if (_negation) then
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

create function get_maturity_subjects(_program_id integer, _faculty_id integer,
                                     _uoc_tally integer)
returns setof integer
AS $$
declare
   _maturity_rule_ids integer array;
   _temp_maturity_rule_ids integer array;
   _ds_acad_obj_group_id integer;
   _maturity_rule_id integer;
   _maturity_rule record;
   _subject_id integer;
begin

   select array_agg(r.id) into _maturity_rule_ids
   from polygons_program_rule pr join polygons_rule r on (r.id=pr.rule_id) join
      polygons_rule_type rt on (r.type_id=rt.id)
   where pr.program_id = _program_id and rt.abbreviation = 'MR';
   
   for _ds_acad_obj_group_id in (
      select r.acad_obj_group_id
      from polygons_program_rule pr join polygons_rule r on (pr.rule_id=r.id)
         join polygons_rule_type rt on (r.type_id=rt.id)
      where pr.program_id = _program_id and rt.abbreviation = 'DS'
   ) loop
      
      select array_agg(r.id) into _temp_maturity_rule_ids
      from polygons_stream_group_member sgm join polygons_stream_rule sr on 
         (sgm.stream_id=sr.stream_id) join polygons_rule r on 
         (sr.rule_id=r.id) join polygons_rule_type rt on (r.type_id=rt.id)
      where sgm.acad_obj_group_id = _ds_acad_obj_group_id and
         rt.abbreviation = 'MR';
   
      _maturity_rule_ids := _maturity_rule_ids || _temp_maturity_rule_ids;

   end loop;

   for _maturity_rule_id in (
      select unnest(_maturity_rule_ids)
   ) loop

      select * into _maturity_rule
      from polygons_rule
      where id = _maturity_rule_id;
         
      if (_maturity_rule.min > _uoc_tally) then
     
         for _subject_id in (
            select expand_subject_rule(_maturity_rule.acad_obj_group_id,
               _faculty_id)
         ) loop
            return next _subject_id;
         end loop;
      
      end if;

   end loop;

end;
$$ language plpgsql;

create function get_limit_subjects(_program_id integer, _faculty_id integer,
                                  _existing_subjects integer array)
returns setof integer
AS $$
declare
   _limit_rule_ids integer array;
   _temp_limit_rule_ids integer array;
   _ds_acad_obj_group_id integer;
   _limit_rule_id integer;
   _limit_rule record;
   _uoc_tally integer;
   _subject_id integer;
   _subject record;
   _limit_rule_subjects integer array;
begin

   select array_agg(r.id) into _limit_rule_ids
   from polygons_program_rule pr join polygons_rule r on (r.id=pr.rule_id) join
      polygons_rule_type rt on (r.type_id=rt.id)
   where pr.program_id = _program_id and rt.abbreviation = 'LR';
   
   for _ds_acad_obj_group_id in (
      select r.acad_obj_group_id
      from polygons_program_rule pr join polygons_rule r on (pr.rule_id=r.id)
         join polygons_rule_type rt on (r.type_id=rt.id)
      where pr.program_id = _program_id and rt.abbreviation = 'DS'
   ) loop
      
      select array_agg(r.id) into _temp_limit_rule_ids
      from polygons_stream_group_member sgm join polygons_stream_rule sr on 
         (sgm.stream_id=sr.stream_id) join polygons_rule r on 
         (sr.rule_id=r.id) join polygons_rule_type rt on (r.type_id=rt.id)
      where sgm.acad_obj_group_id = _ds_acad_obj_group_id and
         rt.abbreviation = 'LR';
   
      _limit_rule_ids := _limit_rule_ids || _temp_limit_rule_ids;

   end loop;

   for _limit_rule_id in (
      select unnest(_limit_rule_ids)
   ) loop

      select * into _limit_rule
      from polygons_rule
      where id = _limit_rule_id;

      _limit_rule_subjects := array[]::integer[];
      select array_agg(expand_subject_rule) into _limit_rule_subjects
      from expand_subject_rule(_limit_rule.acad_obj_group_id, _faculty_id);

      _uoc_tally := 0;
      for _subject_id in (
         select unnest(_existing_subjects)
         intersect
         select unnest(_limit_rule_subjects)
      ) loop

         select * into _subject
         from polygons_subject
         where id = _subject_id;

         _uoc_tally := _uoc_tally + _subject.uoc;

      end loop;

      if (_uoc_tally >= _limit_rule.max) then
         
         for _subject_id in (
            select unnest(_limit_rule_subjects)
         ) loop
            return next _subject_id;
         end loop;

      end if;

   end loop;

end;
$$ language plpgsql;

create function generate_program_subjects(_program_id integer,
                                          _faculty_id integer,
                                          _existing_subjects integer array)
returns setof integer
AS $$
declare
   _subject_id integer;
   _ds_acad_obj_group_id integer;
   _rule record;
   _rule_ids integer array;
   _temp_rule_ids integer array;
   _uoc_tally integer;
   _subject_ids integer array;
   _subject record;
begin
   
   select array_agg(r.id) into _rule_ids
   from polygons_program_rule pr join polygons_rule r on (pr.rule_id=r.id)
      join polygons_rule_type rt on (r.type_id=rt.id)
   where pr.program_id=_program_id and rt.abbreviation not in
      ('DS', 'LR', 'MR', 'RQ');

   for _ds_acad_obj_group_id in (
      select r.acad_obj_group_id
      from polygons_program_rule pr join polygons_rule r on (pr.rule_id=r.id)
         join polygons_rule_type rt on (r.type_id=rt.id)
      where pr.program_id=_program_id and rt.abbreviation = 'DS'
   ) loop
      
      select array_agg(r.id) into _temp_rule_ids
      from polygons_stream_group_member sgm join polygons_stream_rule sr on 
         (sgm.stream_id=sr.stream_id) join polygons_rule r on 
         (sr.rule_id=r.id) join polygons_rule_type rt on (r.type_id=rt.id)
      where sgm.acad_obj_group_id = _ds_acad_obj_group_id and
         rt.abbreviation not in ('LR', 'MR', 'RQ');

      _rule_ids := _rule_ids || _temp_rule_ids;

   end loop;
        
   for _rule in (
      select *
      from polygons_rule r join polygons_rule_type rt on (r.type_id=rt.id)
      where r.id = any(_rule_ids)
      order by rt.id
   ) loop

      select array_agg(expand_subject_rule) into _subject_ids
      from expand_subject_rule(_rule.acad_obj_group_id, _faculty_id);

      _uoc_tally := 0;

      for _subject_id in (
         select unnest(_subject_ids)
         intersect
         select unnest(_existing_subjects)
      ) loop
         
         select array_agg(unnest) into _existing_subjects
         from (
            select unnest(_existing_subjects)
            except
            select _subject_id
         ) sub;

         select * into _subject
         from polygons_subject
         where id = _subject_id;

         _uoc_tally := _uoc_tally + _subject.uoc;
         
      end loop;

      for _subject_id in (
         select unnest(_subject_ids)
      ) loop
         
         if (_rule.max is null) then
            return next _subject_id;
         else
      
            select * into _subject
            from polygons_subject
            where id = _subject_id;

            if ((_uoc_tally + _subject.uoc) <= _rule.max) then
               return next _subject_id;
            end if;

         end if;
         
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

create function meets_subject_prereqs(_rule_id integer, _faculty_id integer,
                                      _existing_subjects integer array)
returns boolean
AS $$
declare
   _uoc_tally integer := 0;
   _subject_id integer;
   _subject_ids integer array;
   _rule record;
   _subject record;
begin

   select * into _rule
   from polygons_rule
   where id = _rule_id;

   select array_agg(expand_subject_rule) into _subject_ids
   from expand_subject_rule(_rule.acad_obj_group_id, _faculty_id);

   for _subject_id in (
      select unnest(_existing_subjects)
   ) loop

      if (
         exists (
            select *
            from unnest(_subject_ids)
            where unnest = _subject_id
         )
      ) then

         select * into _subject
         from polygons_subject
         where id = _subject_id;

         _uoc_tally := _uoc_tally + _subject.uoc;

      end if;

   end loop;

   if (_uoc_tally >= _rule.min) then
      return true;
   else
      return false;
   end if;

end;
$$ language plpgsql;

create function get_program_subjects(_program_id integer, _semester_id integer,
                                     _existing_subjects integer array,
                                     _past_subjects integer array,
                                     _max_uoc integer)
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
   _uoc_tally integer := 0;
   _subject record;
   _subjects integer array;
   _maturity_subjects integer array;
   _limit_subjects integer array;
begin
   
   select * into _program
   from polygons_program
   where id = _program_id;

   _faculty_id := get_faculty(_program.offered_by_id);
   
   for _subject_id in (
      select unnest(_existing_subjects)
   ) loop

      select * into _subject
      from polygons_subject
      where id = _subject_id;

      _uoc_tally := _uoc_tally + _subject.uoc;

   end loop;

   for _subject_id in (
      select generate_program_subjects(_program_id, _faculty_id,
         _existing_subjects)
      except
      select get_exclusion_subjects(_existing_subjects, _faculty_id)
   ) loop
         
      select * into _subject
      from polygons_subject
      where id = _subject_id;

      if (_subject.uoc > _max_uoc) then
         -- Subject cannot fit in semester
         continue;
      end if;

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
         where aog.id = _rule.acad_obj_group_id;

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
               not(
                  select meets_subject_prereqs(_rule.id, _faculty_id,
                     _past_subjects)
               )
            ) then
               _meets_prereqs := false;
               exit;
            end if;

         end if;

      end loop;

      if (not _meets_prereqs) then
         continue;
      elsif (_subject.career_id <> _program.career_id) then

         if (
            exists(
               select *
               from polygons_subject_prereq sp join polygons_rule r on 
                  (sp.rule_id=r.id)
               where subject_id = _subject_id and
                  career_id <> _program.career_id
            )
         ) then
            continue;
         end if;
   
      end if;
 
      _subjects := array_append(_subjects, _subject_id);
      
   end loop;
      
   for _subject_id in (
      select get_maturity_subjects(_program_id, _faculty_id, _uoc_tally)
   ) loop
      _maturity_subjects := array_append(_maturity_subjects, _subject_id);
   end loop;

   for _subject_id in (
      select get_limit_subjects(_program_id, _faculty_id, _existing_subjects)
   ) loop
      _limit_subjects := array_append(_limit_subjects, _subject_id);
   end loop;

   for _subject_id in (
      select unnest(_subjects)
      except
      select unnest(_maturity_subjects)
      except
      select unnest(_limit_subjects)
   ) loop
      return next _subject_id;
   end loop;

end;
$$ language plpgsql;

create function get_broken_rules()
returns setof integer
AS $$
declare
   _rule record;
   _uoc_tally integer;
   _subject_id integer;
   _subject record;
begin

   for _rule in (
      select *
      from polygons_rule r join polygons_acad_obj_group aog on
         (r.acad_obj_group_id=aog.id) join polygons_acad_obj_group_type aogt
         on (aog.type_id=aogt.id) join polygons_rule_type rt on
         (r.type_id=rt.id)
      where aogt.name = 'subject' and rt.abbreviation not in ('DS', 'MR', 'LR', 'RQ')
   ) loop

      _uoc_tally := 0;

      for _subject_id in (
         select expand_subject_rule(_rule.acad_obj_group_id, 112)
      ) loop

         select * into _subject
         from polygons_subject
         where id = _subject_id;

         _uoc_tally := _uoc_tally + _subject.uoc;
      
         if (_uoc_tally >= _rule.min) then
            exit;
         end if;

      end loop;

      if (_uoc_tally < _rule.min) then
         return next _rule.id;
      end if;

   end loop;

end;
$$ language plpgsql;

create function get_cse_rules()
returns setof integer
AS $$
declare
   _rule_id integer;
   _rule_ids integer array;
   _temp_rule_ids integer array;
   _ds_acad_obj_group_id integer;
begin
   
   select array_agg(r.id) into _rule_ids
   from polygons_program_rule pr join polygons_rule r on (pr.rule_id=r.id)
      join polygons_rule_type rt on (r.type_id=rt.id)
   where pr.program_id in (6400, 554, 747, 529) and rt.abbreviation not in
      ('DS', 'LR', 'MR', 'RQ');

   for _ds_acad_obj_group_id in (
      select r.acad_obj_group_id
      from polygons_program_rule pr join polygons_rule r on (pr.rule_id=r.id)
         join polygons_rule_type rt on (r.type_id=rt.id)
      where pr.program_id in (6400, 554, 747, 529) and rt.abbreviation = 'DS'
   ) loop
      
      select array_agg(r.id) into _temp_rule_ids
      from polygons_stream_group_member sgm join polygons_stream_rule sr on 
         (sgm.stream_id=sr.stream_id) join polygons_rule r on 
         (sr.rule_id=r.id) join polygons_rule_type rt on (r.type_id=rt.id)
      where sgm.acad_obj_group_id = _ds_acad_obj_group_id and
         rt.abbreviation not in ('LR', 'MR', 'RQ');

      _rule_ids := _rule_ids || _temp_rule_ids;

   end loop;

   for _rule_id in (
      select unnest(_rule_ids)
   ) loop
      return next _rule_id;
   end loop;

end;
$$ language plpgsql;

create function get_broken_cse_rules()
returns setof integer
AS $$
declare
   _rule_id integer;
begin

   for _rule_id in (
      select get_broken_rules()
      intersect
      select get_cse_rules()
   ) loop
      return next _rule_id;
   end loop;

end;
$$ language plpgsql;

