from django.test import TestCase, Client
from django.urls import reverse
from datetime import date

from .models import Patient
from sample.models import Sample

# Create your tests here.

class PatientSampleRedirectViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('patient_form')
        self.data = {
            'name' : 'Test Patient',
            'dob' : date(1990,1,1), 
            'gender': "M",
            'ip_number' : '12345',
            'address' : '123 Main',
            'phone' : '123456',
            'email': 'test@te.com',
            'medical_history' : 'test_medical history',
            'notes' : 'test notes'

        }

    def test_patient_sample_redirect(self):
        response = self.client.post(self.url, data=self.data, follow=True)
        

        patient = Patient.objects.get(name=self.data['name'],
                                      ip_number=self.data['ip_number'])

        self.assertTrue(Sample.objects.exists())

        sample = Sample.objects.get(patient=patient)
        self.assertTrue(sample.patient, patient)

        self.assertRedirects(response, reverse('sample_update',
                                               kwargs={'pk':sample.pk}))



