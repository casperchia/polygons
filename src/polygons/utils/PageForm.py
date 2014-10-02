from django import forms

from polygons.models.Plan import Plan

class PageForm(forms.ModelForm):
    class Meta:    
        model = Plan
        exclude = ('user', 'datetime')

