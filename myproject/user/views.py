from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

from django.views.generic import FormView, TemplateView 

from .forms import ChangePasswordForm

# Create your views here.

class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = '/home/'

    def form_valid(self, form):
        print("form valid")
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            return render(self.request, self.template_name,{'form':form,
                                        'error': 'Invalid Credentials'})

    def form_invalid(self, form):
        print("form invalid")
        return render(self.request, self.template_name, {'form': form})


class HomeView(LoginRequiredMixin, TemplateView):
    """
    The home page. This will be visible only on successful login
    """
    print("successful login")
    template_name = 'registration/success_login.html'

class LogoutView(LogoutView):
    #next_page takes the url to redirect the user after loggin out
    next_page = reverse_lazy('login')

class ChangePasswordView(LoginRequiredMixin, PermissionRequiredMixin,FormView):
    form_class = ChangePasswordForm
    template_name = 'change_password.html'
    success_url = reverse_lazy('home')
    permission_required = 'change_user'

    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data['new_password'])
        user.save()
        update_session_auth_hash(self.request, user)
        return super().form_valid(form)

