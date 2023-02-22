from django.urls import path
from django.contrib import admin

from .views import ResultCreateView, ResultListView, ResultUpdateView,\
                    ResultDeleteView, ResultListView1 ,ResultPDFView 

urlpatterns =[
    path('result_form/', ResultCreateView.as_view(), name='result_form'),
    path('result_list/', ResultListView.as_view(), name='result_list'),
    path('result_list_download/', ResultListView1.as_view(), name='result_list_download'),
	path('result/<int:pk>/update/', ResultUpdateView.as_view(), name = 'result_update'),
    path('result/<int:pk>/delete/', ResultDeleteView.as_view(), name = 'result_delete'),
    path('result/<int:pk>/download-pdf/', ResultPDFView.as_view(), name = 'result_download'),
	
]
