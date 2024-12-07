from django import forms
from .models import EmployeeDT

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeDT
        fields = ['name', 'email', 'phone', 'address', 'active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
