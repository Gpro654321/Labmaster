from django.contrib.auth.views import LoginView 
from . import views 
from django.urls import path

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    #note that the LogoutView is from the views that was written
    path('logout/', views.LogoutView.as_view(), name = 'logout'),
    path('change_password/', views.ChangePasswordView.as_view(),name='change_password')
]
