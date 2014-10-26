SELECT setval('polygons_acad_obj_group_id_seq', (SELECT MAX(id) FROM polygons_acad_obj_group)+1);
SELECT setval('polygons_subject_group_member_id_seq', (SELECT MAX(id) FROM polygons_subject_group_member)+1);
SELECT setval('polygons_program_group_member_id_seq', (SELECT MAX(id) FROM polygons_program_group_member)+1);
SELECT setval('polygons_rule_id_seq', (SELECT MAX(id) FROM polygons_rule)+1);
