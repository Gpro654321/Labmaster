from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager, Permission
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set.")

        user = self.model(
                    name = name, 
                    email=self.normalize_email(email),
                    )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, password, **extra_fields):
        user = self.create_user(name , email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_name(self):
        return self.name

    def has_perm(self, perm,  obj=None):
        if self.is_active and self.is_superuser:
            return True

        return self.user_permissions.filter(codename=perm).exists()

    def has_module_perms(self, app_label):
        return self.is_superuser


