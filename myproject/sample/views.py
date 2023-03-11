
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView, CreateView, RedirectView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from django.db.models import Q
from functools import reduce
import operator


from .models import Sample
from patient.models import Patient

from .forms import SampleForm, SampleUpdateForm, SampleSearchForm
# Create your views here.

class SampleFormView(LoginRequiredMixin,PermissionRequiredMixin, FormView):
    permission_required = 'add_sample'
    form_class = SampleForm
    template_name = 'sample_form.html'
    success_url = reverse_lazy('sample_form_view')

    def form_valid(self, form):
        sample = form.save(commit=False)
        sample.sample_id = form.cleaned_data['sample_id']
        sample.save()
        return super().form_valid(form)

class SampleFormFromPatientView(LoginRequiredMixin, PermissionRequiredMixin,
                                RedirectView):
    '''
    This view will be called when a user wants to add another sample from the
    patients list page
    '''
    permission_required = ['add_sample', 'change_sample']

    def get_redirect_url(self, *args, **kwargs):
        #receive the primary key from the previous url
        patient_pk = kwargs.get('pk')

        # get the patient object
        patient = Patient.objects.get(pk=patient_pk)

        # create a sample instance
        sample_instance = Sample.objects.create(patient=patient)
        # get the prmary key for hte created sample object
        sample_instance_pk = sample_instance.pk
        # redirect to the sample_update
        return reverse_lazy('sample_update', kwargs={'pk':sample_instance_pk})


class SampleListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = 'view_sample'
    model = Sample 
    template_name = 'sample_list.html'
    context_object_name = 'samples'
    paginate_by = 5

    def get_queryset(self):
        '''
        To order the sample list in the descending order of the
        date_time_arrived 
        '''
        return self.model.objects.order_by('-date_time_arrived')

    

class SampleUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = 'change_sample'
    model = Sample 
    #form_class = SampleForm 

    form_class = SampleUpdateForm
    template_name = 'sample_update.html'
    success_url = reverse_lazy('sample_list') 

    def form_valid(self, form):
        try:
            #try if there is unique_specimen_id in the form
            unique_specimen_id = form.cleaned_data['unique_specimen_id']

            if Sample.objects.filter(unique_specimen_id=unique_specimen_id).exclude(pk=self.object.pk).exists():
                form.add_error('unique_specimen_id',"Specimen Id number already exists")
                return self.form_invalid(form)
        except:
            return super().form_valid(form)


class SampleDeleteView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    permission_required = 'delete_sample'
    model = Sample 
    success_url = reverse_lazy('sample_list')
    template_name = 'sample_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect('sample_list')
        else:
            return super().post(request,*args, **kwargs)


class SampleSearchView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	model = Sample 
	template_name = 'sample_search.html'
	permission_required = 'view_sample'
	paginate_by = 2 
	context_object_name = 'samples'
	#search_fields = ['patient', 'unique_specimen_id', 'sample_id',
    #              'sample_type', 'department'] 
	print("SampleSearchView Called")

