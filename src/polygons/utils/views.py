from polygons.models.Program import Program
from polygons.models.Program_Group_Member import Program_Group_Member

_CSE_PLANS_ID = 20382

def get_cse_programs():
    ids = Program_Group_Member.objects.filter(acad_obj_group=_CSE_PLANS_ID).values_list('program',
                                                                                        flat=True)
    return Program.objects.filter(id__in=ids) 