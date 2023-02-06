from django.urls import path
from django.contrib import admin

from .views import ResultCreateView, ResultListView, ResultUpdateView, ResultDeleteView

urlpatterns =[
    path('result_form/', ResultCreateView.as_view(), name='result_form'),
    path('result_list/', ResultListView.as_view(), name='result_list'),
	path('result/<int:pk>/update/', ResultUpdateView.as_view(), name = 'result_update'),
    path('result/<int:pk>/delete/', ResultDeleteView.as_view(), name = 'result_delete'),
	
]
