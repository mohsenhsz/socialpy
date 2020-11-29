from django import forms
from django.contrib.auth.models import User

class UserRegisterationForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', max_length=30,
                                widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', max_length=30,
                                widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean_email(self):
        data = self.cleaned_data['email']
        email = User.objects.filter(email=data)
        if email.exists():
            raise forms.ValidationError('This email is exist!')
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2:
            if p1 != p2:
                raise forms.ValidationError('Passwords must be same')

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control'}))
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class':'form-control'}))
