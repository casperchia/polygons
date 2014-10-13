from django.db import models
from django.contrib.auth.models import User

from polygons.models.Semester import Semester
from polygons.models.Program import Program

START_YEAR = 1

class Program_Plan(models.Model):
    
    program = models.ForeignKey(Program, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    uoc_tally = models.PositiveIntegerField(default=0)
    current_semester = models.ForeignKey(Semester, on_delete=models.PROTECT)
    current_year = models.PositiveIntegerField(default=START_YEAR)

    class Meta:
        app_label = 'polygons'