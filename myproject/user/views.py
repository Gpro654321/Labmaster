from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.views import LogoutView, LoginView
# to destroy the user session after logout
from django.contrib.auth import logout

# to prevent caching page
from django.views.decorators.cache import never_cache
# to decorate methods
from django.utils.decorators import method_decorator

from .mixins import NeverCacheMixin


from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

from django.views.generic import FormView, TemplateView 

from .forms import ChangePasswordForm, CustomLoginForm

# Create your views here.

class CustomLoginView(FormView):
    template_name = 'registration/login.html'
    #form_class = AuthenticationForm

    form_class = CustomLoginForm 
    success_url = '/home/'
    print("I am inside LoginView")

    '''
    def form_valid(self, form):
        print("successful form_valid")


    def post(self, request, *args, **kwargs):
        
        print("POST request received")

        return super().post(request,*args, **kwargs)

    def get(self, request, *args, **kwargs):
        print("GET request")
        return super().get(request, *args, **kwargs)

    '''

    def form_valid(self, form):
        print("form valid")
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            print("login successful")
            login(self.request, user)
            return redirect(self.success_url)
        else:
            # if the authentication fails, then add a custom error
            # call the form_invalid method with the form with added errors
            print("invalid creds")
            form.add_error(None,'Invalid Credentials')
            print(form.errors)
            
            return self.form_invalid(form)




class HomeView(LoginRequiredMixin,NeverCacheMixin,TemplateView):
    """
    The home page. This will be visible only on successful login
    """
    print("successful login1")
    template_name = 'base1.html'

class LogoutView(LogoutView):
    #next_page takes the url to redirect the user after loggin out
    next_page = reverse_lazy('login')

    # prevent caching the page
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        print("I am inside logotuview dispatch")
        logout(request)
        return super().dispatch(request, *args, **kwargs)

class ChangePasswordView(LoginRequiredMixin, PermissionRequiredMixin,FormView):
    form_class = ChangePasswordForm
    template_name = 'change_password.html'
    success_url = reverse_lazy('home')

    permission_required = 'change_user'

    def form_valid(self, form):
        #if form.!= form.new_password:
        new_password = form.cleaned_data.get('new_password')
        confirm_password = form.cleaned_data.get('confirm_password')
        if new_password != confirm_password :
            form.add_error(None, "Passwords do not match")
            return self.form_invalid(form)

        else:
            user = self.request.user
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            update_session_auth_hash(self.request, user)
            return super().form_valid(form)


    def form_invalid(self, form):
        #This method will be called if the form is considered invalid
        #This will call the get_context_data method
        print("form invalid_password change")
        return self.render_to_response(self.get_context_data(form=form))


    '''
    def get_context_data(self, **kwargs):
        #if the form is called by get method a normal form will be shown
        #else a form with errors will be shown

        context = super().get_context_data(**kwargs)
        print(kwargs)
        if 'form' not in kwargs:
            # if 'form' is not there in kwargs, then create a context with a
            # new form instance with self.form_class()
            context['form'] = self.form_class()
        if self.request.method == "POST":
            context['form'] = kwargs['form']
            context['form_errors'] = kwargs['form'].errors

        #form1 = context['form']
        #form1.add_error('confirm_password', "Passwords didn't match")
        print("get context data for password change is being called")
        print(context)
        #context['form'].add_error('confirm_password', "passwords did't match")
        return context

    '''







