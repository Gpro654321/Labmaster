from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils import timezone

from django.contrib import admin
from .models import User 

# Register your models here.
# taken from https://docs.djangoproject.com/en/4.1/topics/auth/customizing/
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label = 'Password', 
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label = 'Password confirmation', 
                               widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email','name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2 :
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            if not user.pk:
                user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User

        fields = ('email', 'password', 'name','is_active', 'is_staff',
                  'is_superuser'  )

class UserAdmin(BaseUserAdmin):
    exclude = ('date_joined',)
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'name', 'is_staff', 'is_superuser', ) 
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields':('email', 'password', 'name', 'signature')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups',
                                    'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields': ('email', 'name', 'password1', 'password2', ),
        }),
    )
    ordering = ('email',)
    

admin.site.register(User, UserAdmin)

