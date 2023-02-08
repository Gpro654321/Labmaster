from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.generic import FormView, TemplateView

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

class HomeView(TemplateView):
    print("successful login")
    template_name = 'registration/success_login.html'
