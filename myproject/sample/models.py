from django.db import models
from django import utils

import datetime

from patient.models import Patient



# Create your models here.
class Sample(models.Model):
    class Meta:
        verbose_name = "Sample Information"
        #permissions = [
        #    ("view_sample", "Can view sample"),
        #    ("add_sample", "Can add sample"),
        #    ("change_sample", "Can change sample"),
        #    ("delete_sample", "Can delete sample")
        #]

    def __str__(self):
        return f'{self.patient.name} {self.sample_id} \
            {self.date_time_arrived}'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,
                                editable=False)

    #the following is a the id that is entered by the user but still should be
    #unique
    unique_specimen_id = models.CharField(max_length=200, unique=True,
                                blank=True,
                                 verbose_name = "Specimen Id")

    #The following is a unique specimen id that is created automatically
    sample_id = models.CharField(max_length=50, unique=True, editable=False)
    SAMPLE_TYPE_CHOICES = (
        ('Biopsy', "Biopsy"),
        ('FNAC', "FNAC"),
    )
    sample_type = models.CharField(
        max_length=50,
        blank=True,
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
        blank=True,
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


    #################################################
    # Custom functions required for the save()method#
    #################################################
    def generate_sample_id(self):

        try:
            latest_sample = Sample.objects.latest('date_time_arrived')
            print("latest sample", latest_sample.sample_id)
        except Sample.DoesNotExist:
            latest_sample = False 

        if latest_sample:
            latest_sample_id = latest_sample.sample_id
            print(latest_sample_id)
            latest_sample_id_serial = int(latest_sample_id.split("-")[1])
            print("latest_sample_id_serial", latest_sample_id_serial)
            latest_sample_id_serial = latest_sample_id_serial + 1
            latest_sample_id = \
            f"{datetime.date.today().strftime('%Y%m%d')}-{str(latest_sample_id_serial).zfill(5)}"
            #self.fields['sample_id'].initial = latest_sample_id

            #self.sample_id = latest_sample_id

            sample_id = latest_sample_id
        else:
            #self.sample_id = \
            #        f"{datetime.date.today().strftime('%Y%m%d')}-00001"


            sample_id = \
                    f"{datetime.date.today().strftime('%Y%m%d')}-00001"
        print("generate_sample_id called")

        return sample_id

    def generate_date_time_arrived(self):

        #initialize it to the current time and date

        #Even though the attribute is a datetime one, the form becomes valid
        # only when the date alone is put in the form field
        date_time_arrived = \
            datetime.datetime.now().strftime("%Y-%m-%d") 
        print("generate_date_time_arrived called")
        return date_time_arrived

    #########################################
    # The overloaded save() method          # 
    #########################################

    def save(self,*args, **kwargs):
        print("Save method sample method called")
        if not self.sample_id:
            self.sample_id = self.generate_sample_id()
        if not self.date_time_arrived:
            self.date_time_arrived = self.generate_date_time_arrived()

        super().save(*args, **kwargs)





