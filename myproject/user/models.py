from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager, Permission
from django.contrib.auth.models import User, Group
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
        '''
        This method was done after a long hours of trouble shooting
        the models that are created by the contrib.auth.models should be
        studied in much more detail

        This method checks if the user has a permisssion either through the
        groups or through the individual permission
        '''
        if self.is_active and self.is_superuser:
            return True
        # from group_permissions get the permitted permission_id
        # permission_id is related to permission in auth_permission
        print(self.id)
        user_id = self.id
        #User,Permission, are models that django creates
        user = User.objects.get(id=user_id)
        user_groups = user.groups.all() 
        group_permissions = Permission.objects.filter(group__in=user_groups)
        individual_permissions = user.user_permissions.filter(codename=perm) 
        
        print("indivial permission", individual_permissions.exists())
        print(group_permissions)
        print(group_permissions.filter(codename=perm).exists())
        
        return group_permissions.filter(codename=perm).exists() or \
                individual_permissions.exists()

    def has_module_perms(self, app_label):
        return self.is_superuser


