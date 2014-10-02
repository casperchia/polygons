from django import forms

class PageForm(forms.Form):
    create_at = forms.DateField()

