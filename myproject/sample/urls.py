from django.urls import path
from django.contrib import admin

from .views import SampleFormView, SampleListView, SampleUpdateView,SampleDeleteView


urlpatterns =[
    #path('sample_form/', sample_form_view, name='sample_form'),
    path('sample_form/', SampleFormView.as_view(), name='sample_form'),
    path('samples/', SampleListView.as_view(), name='sample_list'),
	path('sample/<int:pk>/update/', SampleUpdateView.as_view(), name = 'sample_update'),
    path('sample/<int:pk>/delete/', SampleDeleteView.as_view(), name = 'sample_delete'),
	
]
