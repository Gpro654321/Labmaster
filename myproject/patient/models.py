from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Patient(models.Model):
    name = models.CharField(max_length=255, verbose_name = "Name")
    dob = models.DateField(verbose_name = "DOB")
    GENDER_CHOICES = (
        ('M', "Male"),
        ('F', "Female"),
        ('O', "Other"),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES, 
        verbose_name = "Gender"
    )

    ip_number = models.CharField(max_length=50, unique = True,verbose_name="IP Number")
    address = models.CharField(max_length=255, verbose_name = "Address")
    phone = models.CharField(max_length=15, blank=True, verbose_name = "Phone")
    email = models.EmailField(max_length=255, blank=True, verbose_name = "Email")
    medical_history = RichTextField(blank=True, verbose_name = "Medical History")
    notes = RichTextField(blank=True, verbose_name = "Notes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = "DOC")

    class Meta:
        verbose_name = "Patient Information"
        #permissions = [
        #    ("view_patient", "Can view patient"),
        #    ("add_patient", "Can add patient"),
        #    ("change_patient", "Can change patient"),
        #    ("delete_patient", "Can delete patient")
        #]

    def __str__(self):
        return f'{self.name} {self.name}'

