from django import forms
from django.contrib.auth.models import User


""" Customize form error masseges """
messages = {
    'required':'This field is required',
    'invalid':'Please enter your email address in format:\nyourname@example.com',
    'max_length': 'The maximum length allowed for this field is 30 characters!',
}
class UserRegisterationForm(forms.Form):
    username = forms.CharField(
                               error_messages=messages, max_length=30, widget=forms.TextInput(
                               attrs={'class': 'form-control'})
                                )
    email = forms.EmailField(
                            error_messages=messages, widget=forms.EmailInput(
                            attrs={'class': 'form-control'})
                            )
    password1 = forms.CharField(
                                error_messages=messages, max_length=30,
                                widget=forms.PasswordInput(attrs={'class':'form-control'})
                                )
    password2 = forms.CharField(
                                error_messages=messages, max_length=30,
                                widget=forms.PasswordInput(attrs={'class':'form-control'})
                                )

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError('This email is exist!')
        else:
            return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2:
            if p1 != p2:
                raise forms.ValidationError('passwords must be same')

class UserLoginForm(forms.Form):
    username = forms.CharField(
                                error_messages=messages, max_length=30,widget=forms.TextInput(
                                attrs={'class':'form-control'})
                               )
    password = forms.CharField(
                                error_messages=messages, max_length=30, widget=forms.PasswordInput(
                                attrs={'class':'form-control'})
                               )
