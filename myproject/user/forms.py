from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

from collections import OrderedDict

class ChangePasswordForm(forms.Form):
    #current_password = forms.CharField(widget=forms.PasswordInput)
    #new_password = forms.CharField(widget=forms.PasswordInput)
    #confirm_password = forms.CharField(widget=forms.PasswordInput)

    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":'form-control', 
                                          'placeholder': "current password"})
                                        )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control",
                                          "placeholder":"NEW PASSWORD"})

                                        )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control",
                                          "placeholder":"RE-ENTER NEW PASSWORD"})
                                        )

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
            print("Passwords donot match")
            raise ValidationError("passwords do not match")

        return 


class CustomLoginForm(AuthenticationForm):
    email = forms.EmailField(label='Email')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email'})

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })

        #OrderedDict remembere the order in which the keys are addded
        # to make the email field appear first we create a orderedDict
        customFields = OrderedDict()
        customFields['email'] = self.fields['email']
        customFields['password'] = self.fields['password']

        self.fields = customFields
        print(self.fields)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        '''

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password")

        '''


        return self.cleaned_data



