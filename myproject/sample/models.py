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
    SAMPLE_TYPE_CHOICES = sorted(
        (
            #('Biopsy', "Biopsy"),
            #('FNAC', "FNAC"),
            ('H', 'General'),                     # H-1/23
            ('GY', 'Gynaec'),                       # GY-1/23 
            ('ML', 'MLC'),                             # ML-1/23
            ('PS', 'Peripheral Smear'),   # PS 1/23 
            ('BM', 'Bone Marrow'),             # BM 1/23
            ('FN','Cytopathology'),          # FN 1/23
            ('PAP', 'PAP Smear'),                 # PAP 1/23
            ('CY', 'Fluid cytology')        # CY 1/23
        ),key= lambda x:x[1]
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

    def generate_unique_specimen_id(self):
        
        '''
        Generates the unique_specimen_id based on the sample type and the
        latest sample of that specific type
        Eg. if the last cytopathology sample was CY 1/23, then this specimen id
        will be fetcted and split into 3 parts namely 
        CY (type of sample)
        1   (running serial number of the sample type)
        23 (year)
        '''
        try:
            #try to get the latest sample of the given type
            latest_sample = \
            Sample.objects.filter(sample_type=self.sample_type).latest('date_time_arrived')
        except Sample.DoesNotExist:
            # if such a sample does not exist at all
            latest_sample = False

        current_year = str(datetime.date.today().year % 100)

        if latest_sample: 
            print(" i am inside if true latest_sample \
                  generate_unique_specimen_id")
            # if the lastest_sample is True
            latest_unique_specimen_id = latest_sample.unique_specimen_id
            # assuming the unique_specimen_id is of the form CY-1/23
            latest_sample_unique_specimen_id_split_1 = \
                    latest_unique_specimen_id.split("-")
            print("latest_sample_unique_specimen_id_split_1")
            print(latest_sample_unique_specimen_id_split_1)

            latest_sample_unique_specimen_id_split_2 = \
                    latest_sample_unique_specimen_id_split_1[1].split("/")
            print("latest_sample_unique_specimen_id_split_2")
            print(latest_sample_unique_specimen_id_split_2)

            latest_unique_specimen_id_serial = \
                    latest_sample_unique_specimen_id_split_2[0]

            print("latest_unique_specimen_id_serial")
            print(latest_unique_specimen_id_serial)

            latest_unique_specimen_id_year = \
                    latest_sample_unique_specimen_id_split_2[1]
            print("latest_unique_specimen_id_year")
            print(latest_unique_specimen_id_year)

            # what is the 2 digit version of the current year

            # if the latest_unique_specimen_id belongs to current year
            if latest_unique_specimen_id_year == current_year:
                unique_specimen_id_serial = int(latest_unique_specimen_id_serial) + 1

            # if the latest_unique_specimen_id belongs to another year
            else:
                unique_specimen_id_serial = 1

            unique_specimen_id = latest_sample_unique_specimen_id_split_1[0] +\
                                    "-" +\
                                    str(unique_specimen_id_serial) +\
                                    "/" +\
                                    str(current_year)

        else:
            print("sample_type" )
            print(self.sample_type)
            unique_specimen_id = self.sample_type + \
                                    "-" + \
                                    str(1) + \
                                    "/" + \
                                    str(current_year)

        print("generate_unique_specimen_id called")
        return unique_specimen_id
                                    

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

        if self.sample_type.strip() != "":
            # if the sample_type is NOT blank
            self.unique_specimen_id = self.generate_unique_specimen_id()

        if not self.date_time_arrived:
            self.date_time_arrived = self.generate_date_time_arrived()

        super().save(*args, **kwargs)





