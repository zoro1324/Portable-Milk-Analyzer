# core/forms.py

from django import forms
from .models import MilkSubmission

class MilkSubmissionForm(forms.ModelForm):
    class Meta:
        model = MilkSubmission
        # We only need the user to select the quality
        fields = ['quality_of_milk']
        widgets = {
            'quality_of_milk': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'quality_of_milk': 'Current Milk Quality'
        }