from django.test import TestCase, Client
from django.urls import reverse
from datetime import date
from django.contrib.auth import authenticate

from user.models import User
from .models import Patient
from sample.models import Sample

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission, Group

from django.core.management import call_command

import uuid
import random
import datetime

# Create your tests here.

class PatientSampleRedirectViewTest(TestCase):
    fixtures = [
        'contenttype/contenttype.json',
        'auth/auth_permission.json',
        'auth/group.json',
        'user/user.json'
    ]

    data = {
        'name' : 'test_patient',
        'dob' : date.today(),
        'gender' : "M",
        'ip_number' : str(uuid.uuid4()),
        'address' : 'test_address',
        'phone' : '123456789',
        'email' : 'test_patient@test.com',
        'notes' : 'test_notes',
        'medical_history' : 'test_history'

    }

    sample_type = [
            ('H', 'General'),                     # H-1/23
            ('GY', 'Gynaec'),                       # GY-1/23 
            ('ML', 'MLC'),                             # ML-1/23
            ('PS', 'Peripheral Smear'),   # PS 1/23 
            ('BM', 'Bone Marrow'),             # BM 1/23
            ('FN','Cytopathology'),          # FN 1/23
            ('PAP', 'PAP Smear'),                 # PAP 1/23
            ('CY', 'Fluid cytology')        # CY 1/23
    ]

    random_sample_type = random.choice(sample_type)[0]

    department = [
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

    ]

    random_deparment = random.choice(department)[0]

    
    @classmethod
    def setUpClass(cls):
        '''
            This method will be run once when the class is instantiated
            as opposed to the setUp method which will be run before every
            test method call
        '''
        super().setUpClass()    
        cls.client =  Client()
        cls.user = get_user_model().objects.get(name='test_tech1')
        cls.user1 = get_user_model().objects.get(name = 'test_no_permissions')
        #Load fixtures

    def test_should_be_forbidden_for_result_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('result_form'))
        self.assertEqual(response.status_code, 403)

    def test_add_patient_and_redirect_to_sample_update_page(self):
        '''
        The logic of the PatientSampleRedirectView is as follows
        1. Create a patient object
        2. Then create a sample object that is related to the patient
        3. Redirect to that created sample object's update page
        4. Wait for the user to chose the sample type and get updated
        '''
        self.client.force_login(self.user)
        response = self.client.post(reverse('patient_form'),data=self.data)



        patient = Patient.objects.latest('pk')
        sample_update_url = reverse('sample_update', kwargs={'pk':patient.pk})
        self.assertRedirects(response, sample_update_url)


        self.assertEqual(Sample.objects.filter(patient=patient).count(), 1)
        sample = Sample.objects.get(patient=patient)

        sample_type_data = {
            'sample_id' : sample.sample_id,
            'date_time_arrived': datetime.datetime.now().strftime("%Y-%m-%d"),
            'sample_type':self.random_sample_type,
            'department': self.random_deparment,
            'procedure_performed': "Test_procedure",
            'specimen' : "Test_specimen"
        }
        print(sample_type_data)
        response = self.client.post(sample_update_url,data=sample_type_data)
        self.assertEqual(response.status_code, 302)

        #self.assertEqual(sample.sample_type, self.random_sample_type)



    def test_check_if_login_required(self):
        response = self.client.get(reverse('patient_form'))
        self.assertRedirects(response,
                             f"{reverse('login')}?next={reverse('patient_form')}")

    def test_check_if_permission_add_patient_required(self):
        #print(self.user.get_all_permissions())
        self.client.force_login(self.user1)
        response = self.client.get(reverse('patient_form'))
        #print(response.content.decode())
        self.assertEqual(response.status_code, 403)

