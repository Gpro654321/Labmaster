from django.urls import path
from django.contrib import admin
from .views import patient_form_view, PatientListView, PatientUpdateView, PatientDeleteView

urlpatterns =[
    path('patient_form/', patient_form_view, name='patient_form'),
    #path('success_page/', success_page, name='success_page')
    path('patients/', PatientListView.as_view(), name='patient_list'),
	path('patient/<int:pk>/update/', PatientUpdateView.as_view(), name = 'patient_update'),
	path('patient/<int:pk>/delete/', PatientDeleteView.as_view(), name = 'patient_delete'),
	
]
