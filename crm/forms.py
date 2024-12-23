from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        # fields = '__all__'
        fields =['name','email','phone','phone_number','address','preferred_medium','source'] 
        widgets = {
            'date_created': forms.DateInput(attrs={'type': 'date'}),
            'date_updated': forms.DateInput(attrs={'type': 'date'}),
        }


class LeadsForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields =['name','email','phone','phone_number','source'] # '__all__'
        widgets = {
            'date_created': forms.DateInput(attrs={'type': 'date'}),
            'date_updated': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'name': 'Name',
            'email': 'Email',
            'phone': 'Phone',
            'phone_number': 'Alternate Phone',
            'source': 'Source',
        }
# forms.py
from django import forms
# from .models import Sale

class SaleForm(forms.ModelForm):
    # Customizing the sale date field to include a date picker widget
    sale_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        )
    )



