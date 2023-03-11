from django.urls import path
from django.contrib import admin
from .views import  PatientListView, PatientUpdateView, PatientDeleteView
from .views import PatientFormView, PatientSampleRedirectView, PatientSearchView
from .views import PatientSearchResultView

urlpatterns =[
    #path('patient_form/', patient_form_view, name='patient_form'),
	#path('patient_form/', PatientFormView.as_view(),name='patient_form'),

	path('patient_form/', PatientSampleRedirectView.as_view(),name='patient_form'),
    #path('success_page/', success_page, name='success_page')
    path('patients/', PatientListView.as_view(), name='patient_list'),
	path('patient/<int:pk>/update/', PatientUpdateView.as_view(), name = 'patient_update'),
	path('patient/<int:pk>/delete/', PatientDeleteView.as_view(), name = 'patient_delete'),
	path('patient_search/', PatientSearchView.as_view(), name='patient_search'),
	path('patient_search_result/', PatientSearchResultView.as_view(), name='patient_search_result')
	
]
