# In your_app/forms.py

import base64
from django import forms
from .models import District, MilkSubmission, Supplier

class MilkSubmissionFilterForm(forms.Form):
    """
    A form for filtering and searching milk submissions.
    """
    # Search field for farmer name or RF number.
    # It's not required, so the form is valid even if it's empty.
    search_query = forms.CharField(
        max_length=100,
        required=False,
        label="", # No visible label
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by Farmer Name, RF ID...',
            'class': 'search-input' # Add a class for styling
        })
    )

    # Dropdown to filter by district.
    # It queries the District model to get all available districts.
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        required=False,
        empty_label="Filter by District", # Placeholder text
        label="", # No visible label
        widget=forms.Select(attrs={'class': 'filter-select'}) # Add a class for styling
    )

    # Date field to filter by a specific date.
    # Uses a DateInput widget which renders as <input type="date">.
    date = forms.DateField(
        required=False,
        label="", # No visible label
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'filter-date' # Add a class for styling
        })
    )

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['farmer_photo', 'name', 'rf_no', 'phone_no', 'district', 'address']
        


class Base64ImageField(forms.Field):
    """
    A form field that handles Base64-encoded image strings.
    It decodes the string and converts it into a ContentFile.
    """
    def to_python(self, data):
        if data is None:
            return None
        
        try:
            # Assuming data is a simple base64 string
            decoded_file = base64.b64decode(data)
        except TypeError:
            raise forms.ValidationError("Invalid image data. Must be a Base64 encoded string.")
        
        # We don't need to save the image to a file, just decode it for the ML model
        return decoded_file

