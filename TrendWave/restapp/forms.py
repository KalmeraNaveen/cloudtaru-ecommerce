from django import forms
from django.core.exceptions import ValidationError
from .models import usersmodel

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    
    class Meta:
        model = usersmodel
        fields = ['username', 'email', 'password','orders','cart','address']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.isalpha():
            raise ValidationError("Username must contain only alphabets and no spaces.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise ValidationError("Email must contain '@'.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(c.islower() for c in password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not any(c.isupper() for c in password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(c.isdigit() for c in password):
            raise ValidationError("Password must contain at least one digit.")
        if not any(not c.isalnum() for c in password):
            raise ValidationError("Password must contain at least one special character.")
        return password
