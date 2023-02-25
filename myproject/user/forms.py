from django import forms
from django.core.exceptions import ValidationError

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

