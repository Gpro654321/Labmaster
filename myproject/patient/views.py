
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q

from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from functools import reduce
import operator

from .models import Patient
from .forms import PatientForm, PatientSearchForm

from sample.models import Sample
from sample.forms import SampleForm

# Create your views here.

class PatientSampleRedirectView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
	'''
	The logic i am trying to implement,
	The user should add a patient, 
	On addition , immediately a instance for a sample should be created
	and associated with this patien
	For that i should override the save method in the sample model
	Then the user should be redirected to the updateView of that sample to further add details of the 
	sample.
	'''

	permission_required = ['view_patient', 'add_patient']
	template_name = "patient_sample_form.html"
	form_class = PatientForm 

	def form_valid(self, form):
		patient = form.save()
		sample_instance = Sample.objects.create(patient=patient)
		self.sample_instance_pk = sample_instance.pk
		print(self.sample_instance_pk)
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy('sample_update', kwargs={'pk': self.sample_instance_pk})






class PatientFormView(LoginRequiredMixin,PermissionRequiredMixin ,FormView):
	permission_required = ['view_patient', 'add_patient']
	template_name = 'patient_form.html'
	form_class = PatientForm
	success_url = reverse_lazy('patient_form')

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)


class PatientListView(LoginRequiredMixin,PermissionRequiredMixin ,ListView):
	permission_required = 'view_patient'
	model = Patient
	template_name = 'patient_list.html'
	context_object_name = 'patients'

	def get_queryset(self):
		'''
		To order the patient list in the descending order of the created_at
		'''
		return self.model.objects.order_by('-created_at')

class PatientUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
	permission_required = 'change_patient'
	model = Patient
	form_class = PatientForm
	template_name = 'patient_update.html'
	success_url = reverse_lazy('patient_list') 

	#to check if there exists another instance with the same ip number other the one being updated
	def form_valid(self, form):
		ip_number = form.cleaned_data['ip_number']

		if Patient.objects.filter(ip_number=ip_number).exclude(pk=self.object.pk).exists():
			form.add_error('ip_number',"IP number already exists")
			return self.form_invalid(form)
		return super().form_valid(form)

	
	
    
class PatientDeleteView(LoginRequiredMixin,PermissionRequiredMixin ,DeleteView):
	permission_required = 'delete_patient'
	model = Patient
	success_url = reverse_lazy('patient_list')
	template_name = 'patient_confirm_delete.html'

	def post(self, request, *args, **kwargs):
		if "cancel" in request.POST:
			return redirect('patient_list')
		else:
			return super().post(request,*args, **kwargs)


class PatientSearchView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	model = Patient
	template_name = 'patient_search.html'
	permission_required = 'view_patient'
	paginate_by = 10
	context_object_name = 'patients'
	search_fields = ['name', 'dob', 'gender', 'ip_number'] 

	def get_queryset(self):
		queryset = super().get_queryset()
		form = PatientSearchForm(data=self.request.GET)


		if form.is_valid():
		# this will call the clean method in the PatientSearchForm
			#create a dictionary of query_params with all other keys other than csrfmiddlewaretoken
			query_params = {k: v for k,v in self.request.GET.items() if (v and k != 'csrfmiddlewaretoken') }
			queries = [Q(**{f'{field}__icontains': query_params[field]}) for field in query_params]
			queryset = queryset.filter(reduce(operator.and_, queries))
		else:
			queryset = queryset.none()
		return queryset.order_by('-created_at')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['search_form'] = PatientSearchForm()
		return context

