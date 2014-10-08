from polygons.tests import Base_Test
from polygons.utils.degree_planning import get_core_subjects
from polygons.utils.degree_planning import get_program_subjects
from polygons.models.Program import Program
from polygons.models.Subject import Subject
from polygons.models.Semester import Semester
from polygons.utils.views import get_cse_programs


class Test_Subject_List_Logic (Base_Test):
    
    fixtures = ['Acad_Obj_Group_Type.json', 'Acad_Obj_Group.json',
                'Org_Unit_Type.json', 'Org_Unit.json', 'Career.json',
                'Degree.json', 'Program.json', 'Program_Group_Member.json',
                'Subject.json', 'Rule_Type.json', 'Rule.json',
                'Program_Rule.json', 'Subject_Group_Member.json',
                'Stream.json', 'Stream_Group_Member.json', 'Stream_Rule.json']
        
    def test_get_program_subjects(self):
        print 'Testing get_program_subjects returns a result set'
        program = Program.objects.get(name='Computer Science')
        semester = Semester.objects.filter(name='Semester 1')
        
        
        existing = get_core_subjects(program)
        subjects = get_program_subjects(program,semester,existing)
        
        self.assertIsNotNone(subjects)
