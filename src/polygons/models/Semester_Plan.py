from django.db import models

from polygons.models.Program_Plan import Program_Plan
from polygons.models.Subject import Subject
from polygons.models.Semester import Semester

class Semester_Plan(models.Model):
    
    program_plan = models.ForeignKey(Program_Plan, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT)
    year = models.PositiveIntegerField()
    
    class Meta:
        app_label = 'polygons'
        unique_together = ['program_plan', 'subject']