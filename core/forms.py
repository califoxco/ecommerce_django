from django import forms

COUNTRY_CHOICES = (
    ('US', 'United States'),
    ('CAN', 'Canada'),
)

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'firstName',
    }))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'lastName',
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'placeholder': 'you@example.com',
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'phone',
    }))
    address_1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'placeholder': '123 Main St',
    }))
    address_2 = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address2',
        'placeholder': 'Apartment or suite',
    }))
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select(attrs={
        'class': 'custom-select d-block w-100',
        'id': 'country',
    }))
    state = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control d-block w-100',
        'id': 'state',
        'placeholder': '--',
    }))

    zip = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'zip',
        'placeholder': '00000',
    }))



