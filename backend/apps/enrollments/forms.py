import re
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class EnrollmentDetailsForm(forms.ModelForm):
    # Field definitions with Bootstrap styling
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'index_number', 'whatsapp_number']
        widgets = {
            # Updated placeholder to reflect Alpha-numeric
            'index_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 220100ABCD'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 024XXXXXXX'}),
        }

    def clean_whatsapp_number(self):
        number = self.cleaned_data.get('whatsapp_number')
        ghana_pattern = r'^(0|\+233)\d{9}$'
        if not re.match(ghana_pattern, number):
            raise ValidationError("Please enter a valid Ghana number (e.g., 024XXXXXXX or +23324XXXXXXX).")
        return number

    def clean_index_number(self):
        index_no = self.cleaned_data.get('index_number')

        # NEW REGEX: Allows letters and numbers, must be exactly 10 characters
        alphanumeric_pattern = r'^[a-zA-Z0-9]{10}$'

        if not re.match(alphanumeric_pattern, index_no):
            raise ValidationError("Index Number must be exactly 10 characters (letters and numbers only).")

        # Returns it in uppercase (e.g., 'abc1234567' becomes 'ABC1234567')
        return index_no.upper()