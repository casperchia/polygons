from django.db import models
from django.contrib.auth.models import User

from polygons.models.Program import Program

class Program_Plan(models.Model):
    
    program = models.ForeignKey(Program, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    uoc = models.PositiveIntegerField()
    
    class Meta:
        app_label = 'polygons'