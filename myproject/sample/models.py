from django.db import models
from django import utils

import datetime

from patient.models import Patient

# Create your models here.
class Sample(models.Model):
    class Meta:
        verbose_name = "Sample Information"

    def __str__(self):
        return f'{self.patient.name} {self.sample_id} \
            {self.date_time_arrived}'

    '''
    def save(self, *args, **kwargs):
        # if there is no instance with a primary key
        # if the instance is new instance
        if not self.pk:
            self.sample_id = kwargs.pop('sample_id') 
            self.sample_id = sample_id
        super().save(*args, **kwargs)

    '''




    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    #the following is a the id that is entered by the user but still should be
    #unique
    unique_specimen_id = models.CharField(max_length=200, unique=True,
                                 verbose_name = "Specimen Id")

    #The following is a unique specimen id that is created automatically
    sample_id = models.CharField(max_length=50, unique=True, editable=False)
    SAMPLE_TYPE_CHOICES = (
        ('Biopsy', "Biopsy"),
        ('FNAC', "FNAC"),
    )
    sample_type = models.CharField(
        max_length=50,
        choices=SAMPLE_TYPE_CHOICES,
        verbose_name = "Sample Type"
    )

    DEPARTMENT_CHOICES = sorted(
        (

            ('Ent', "Ent"),
            ('Opthalmology', "Opthalmology"),
            ('ForensicMedicine', "Forensic Medicine"),
            ('GeneralMedicine', "General Medicine"),
            ('GS', "General Surgery"),
            ('OG', "O & G"),
            ('Pe', "Paediatrics"),
            ('NS', "Neurosurgery"),
            ('N', "Neurology"),
            ('P', "Plastic Surgery"),
            ('Ur', "Urology"),
            ('Ne', "Paediatrics"),
            ('NS', "Neurosurgery"),

        ), key=lambda x: x[1]
    )

    department = models.CharField(
        max_length=100,
        choices = DEPARTMENT_CHOICES,
        verbose_name = "Department"
        )
    date_time_arrived = models.DateTimeField(
        auto_now_add=True
    )

    procedure_performed = models.TextField(
                    max_length = 200,
                    blank=True,
                    verbose_name="Procedure Performed"
    )

    specimen = models.TextField(
        max_length = 200,
        blank = True,
        verbose_name="Specimen"
    )

    
    '''
    def save(self, *args, **kwargs):
        # if there is no such sample 
        if not self.pk:
            date_str = self.date_arrived.strftime("%Y%m%d")
            last_sample = Sample.objects.filter(
                date_arrived__year = self.date_arrived.year,
                date_arrived__month = self.date_arrived.month,
                date_arrived__day = self.date_arrived.day
            ).last()

            # if there is a last sample
            if last_sample:

                sample_id = "{}-{:05d}".format(
                            date_str,
                            int(last_sample.sample_id.split("-")[-1])+1
                            )
            else:
                sample_id = "{}-00001".format(date_str)
            self.sample_id = sample_id

        super().save(*args, **kwargs)

    '''


