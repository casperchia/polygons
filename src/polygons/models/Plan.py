from django.db import models

class Plan(models.Model):

    user = models.CharField(max_length = 100)
    datetime = models.DateTimeField(auto_now = True)

    def __unicode_(self):
       return unicode(self.user)
