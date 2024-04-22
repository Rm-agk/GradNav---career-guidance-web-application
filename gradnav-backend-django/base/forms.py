from django import forms
from .models import *

GRADE_CHOICES = [
    ('', 'Select a grade'),
    ('H1', 'H1'),
    ('H2', 'H2'),
    ('H3', 'H3'),
    ('H4', 'H4'),
    ('H5', 'H5'),
    ('H6', 'H6'),
    ('H7', 'H7'),
    ('H8', 'H8'),
    ('O1', 'O1'),
    ('O2', 'O2'),
    ('O3', 'O3'),
    ('O4', 'O4'),
    ('O5', 'O5'),
    ('O6', 'O6'),
    ('O7', 'O7'),
    ('O8', 'O8'),
    ('N/A', 'N/A'),
]

class GradeForm(forms.Form):
    math_grade = forms.ChoiceField(choices=GRADE_CHOICES, label="Mathematics Grade")
    irish_grade = forms.ChoiceField(choices=GRADE_CHOICES, label="Irish Grade")
    subject_3_grade = forms.ChoiceField(choices=GRADE_CHOICES, label="Subject 3 Grade")
    subject_4_grade = forms.ChoiceField(choices=GRADE_CHOICES, label="Subject 4 Grade")
    subject_5_grade = forms.ChoiceField(choices=GRADE_CHOICES, label="Subject 5 Grade")
    subject_6_grade = forms.ChoiceField(choices=GRADE_CHOICES, label="Subject 6 Grade")
    subject_7_grade = forms.ChoiceField(choices=GRADE_CHOICES, required=False, label="Subject 7 Grade (Optional)")
    subject_8_grade = forms.ChoiceField(choices=GRADE_CHOICES, required=False, label="Subject 8 Grade (Optional)")
