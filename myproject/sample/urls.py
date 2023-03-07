from django.urls import path
from django.contrib import admin

from .views import SampleFormView, SampleListView,\
SampleUpdateView,SampleDeleteView, SampleFormFromPatientView 


urlpatterns =[
    #path('sample_form/', sample_form_view, name='sample_form'),
    path('sample_form/', SampleFormView.as_view(), name='sample_form'),
    path('samples/', SampleListView.as_view(), name='sample_list'),
	path('sample/<int:pk>/update/', SampleUpdateView.as_view(), name = 'sample_update'),
    # the following update will be used when the user arrives from patient list
    # page
	path('sample_create/<int:pk>/', SampleFormFromPatientView.as_view(), name =
      'sample_create'),

    path('sample/<int:pk>/delete/', SampleDeleteView.as_view(), name = 'sample_delete'),
	
]
