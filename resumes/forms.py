# resumes/forms.py
from django import forms

class ResumeForm(forms.Form):
    resume = forms.FileField()
    job_description = forms.CharField(widget=forms.Textarea)
