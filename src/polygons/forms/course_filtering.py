import django.forms as forms



class Course_Filter_Form(forms.Form):
    CHOICES = (
        ("LETTER","Letter"),
        ("SUBJECT_AREA","Subject Area"),
        ("CAREER","Career")
    )
    choice_field = forms.ChoiceField(widget=forms.RadioSelect,
                                     choices=CHOICES,
                                     initial='LETTER')
    
    

