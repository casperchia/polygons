from django.db import models

from Program import Program
from Rule import Rule

class Program_Rule(models.Model):
    
    program = models.ForeignKey(Program, on_delete=models.PROTECT)
    rule = models.ForeignKey(Rule, on_delete=models.PROTECT)
    
    class Meta:
        app_label = 'polygons'
        unique_together = [program, rule]