'''
This base file has a view BaseView which will be inherited by other views in
all apps. That way login is mandatory for views
'''
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class BaseView(LoginRequiredMixin, TemplateView):
    template_name = 'base.html'
