
from django.urls import path
from django.contrib import admin

from .views import ApprovalCreateView   

urlpatterns =[
    path('approve_ap/<int:result_pk>/', ApprovalCreateView.as_view(), name='approve_ap'),
	
]
