
from django.urls import path
from django.contrib import admin

from .views import ApprovalCreateView, AssistantApprovedList, AssociateProfessorApprovalView   

urlpatterns =[
    path('approve_ap/<int:result_pk>/', ApprovalCreateView.as_view(), name='approve_ap'),
    path('assitant_approved_list/', AssistantApprovedList.as_view(),
         name='assistant_approved_list'),
    path('approve_asp/<int:pk>/',
         AssociateProfessorApprovalView.as_view(), name = 'approve_asp' )
	
]
