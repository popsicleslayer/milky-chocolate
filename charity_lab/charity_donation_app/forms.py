from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError



User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Imię',
    }))
    surname = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Nazwisko',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Hasło',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Powtórz hasło',
    }))

    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': "Email"
            })
        }

    def clean(self):
        """ Compares if both of the given passwords are the same """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError('Passwords are not the same')


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': "Email",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Hasło',
    }))
