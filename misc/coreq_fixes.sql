-- COMP4511
update acad_object_groups set definition = 'COMP3171' where id = 113960;
delete from subject_prereqs where rule = 3376;
delete from rules where ao_group = 113958;
delete from acad_object_groups where id = 113958;

-- GMAT2130
delete from subject_prereqs where rule = 2385;
delete from rules where ao_group = 113008;
delete from acad_object_groups where id = 113008;
delete from subject_prereqs where rule = 2384;
delete from rules where ao_group = 113007;
delete from acad_object_groups where id = 113007;
delete from subject_prereqs where rule = 2383;
delete from rules where ao_group = 113006;
delete from acad_object_groups where id = 113006;

-- MARK2999
delete from subject_prereqs where rule = 2515;
delete from rules where ao_group = 113137;
delete from acad_object_groups where id = 113137;
delete from subject_prereqs where rule = 2514;
delete from rules where ao_group = 113136;
delete from acad_object_groups where id = 113136;

-- MARK5816
delete from subject_prereqs where rule = 6859;
delete from rules where ao_group = 116857;
delete from acad_object_groups where id = 116857;

-- PHYS3060
delete from subject_prereqs where rule = 2873;
delete from rules where ao_group = 113463;
delete from acad_object_groups where id = 113463;

-- OPTM3231
delete from subject_prereqs where rule = 2781;
delete from rules where ao_group = 113376;
delete from acad_object_groups where id = 113376;

-- OPTM4251
delete from subject_prereqs where rule = 2783;
delete from rules where ao_group = 113378;
delete from acad_object_groups where id = 113378;

-- PHYS2050
delete from subject_prereqs where rule = 2846;
delete from rules where ao_group = 113436;
delete from acad_object_groups where id = 113436;

-- PTRL2019
update acad_object_groups set definition = 'MATH1231' where id = 113535;

-- SAED3491
delete from subject_prereqs where rule = 2970;
delete from rules where ao_group = 113560;
delete from acad_object_groups where id = 113560;

-- SENG2010
delete from subject_prereqs where rule = 3040;
delete from rules where ao_group = 113630;
delete from acad_object_groups where id = 113630;

-- VISN1231
delete from subject_prereqs where rule = 3154;
delete from rules where ao_group = 113740;
delete from acad_object_groups where id = 113740;

-- ACCT5943
delete from subject_prereqs where rule = 1117;
delete from rules where ao_group = 111858;
delete from acad_object_groups where id = 111858;

-- SOCW3001
delete from subject_prereqs where rule = 3072;
delete from rules where ao_group = 113662;
delete from acad_object_groups where id = 113662;

-- SAED2402
delete from subject_prereqs where rule = 2967;
delete from rules where ao_group = 113557;
delete from acad_object_groups where id = 113557;

-- AERO4110
delete from subject_prereqs where rule = 1731;
delete from rules where ao_group = 112458;
delete from acad_object_groups where id = 112458;

-- COMP9321
update acad_object_groups set definition = 'COMP2911' where id = 111946;

-- GMAT2550
delete from subject_prereqs where rule = 2387;
delete from rules where ao_group = 113010;
delete from acad_object_groups where id = 113010;

-- MANF3100
delete from subject_prereqs where rule = 2500;
delete from rules where ao_group = 113122;
delete from acad_object_groups where id = 113122;

-- SOMA9751
delete from subject_prereqs where rule = 1682;
delete from rules where ao_group = 112412;
delete from acad_object_groups where id = 112412;

-- CVEN3301
update acad_object_groups set definition = 'CVEN1300' where id = 112808;

-- PHYS3080
delete from subject_prereqs where rule = 2876;
delete from rules where ao_group = 113466;
delete from acad_object_groups where id = 113466;
delete from subject_prereqs where rule = 2875;
delete from rules where ao_group = 113465;
delete from acad_object_groups where id = 113465;

-- MECH4004
update acad_object_groups set definition = 'MECH4003' where id = 113247;
update rules set "max" = null, "min" = 6 where ao_group = 113247;

-- MMAN4020
delete from subject_prereqs where rule = 2708;
delete from rules where ao_group = 113307;
delete from acad_object_groups where id = 113307;

-- COMP2111
delete from subject_prereqs where rule = 2116;
delete from rules where ao_group = 112753;
delete from acad_object_groups where id = 112753;

-- PHYS1221
delete from subject_prereqs where rule = 2832;
delete from rules where ao_group = 113422;
delete from acad_object_groups where id = 113422;

-- PHYS1231
delete from subject_prereqs where rule = 2834;
delete from rules where ao_group = 113424;
delete from acad_object_groups where id = 113424;

-- PHYS2010
delete from subject_prereqs where rule = 2837;
delete from rules where ao_group = 113427;
delete from acad_object_groups where id = 113427;

-- PHYS3210
delete from subject_prereqs where rule = 2879;
delete from rules where ao_group = 113469;
delete from acad_object_groups where id = 113469;

-- SENG2011
delete from subject_prereqs where rule = 3042;
delete from rules where ao_group = 113632;
delete from acad_object_groups where id = 113632;

-- SERV2003
update acad_object_groups set definition = 'MARK2055' where id = 113642;














