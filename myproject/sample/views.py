
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse, reverse_lazy



from .models import Sample
from patient.models import Patient

from .forms import SampleForm, SampleUpdateForm
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

'''
def sample_form_view(request):
    if request.method == "POST":
        form = SampleForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['sample_id'])
            #print(form.cleaned_data['date_time_arrived'])
            sample = form.save(commit=False)
            sample.sample_id = form.cleaned_data['sample_id']
            sample.save()
            return(redirect(reverse(sample_form_view)))

        else:
            print(form.errors)
            return render(request,'sample_form.html',{'form':form})

    else:
        form = SampleForm()
        return render(request,'sample_form.html',{'form':form})

'''

class SampleListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = 'view_sample'
    model = Sample 
    template_name = 'sample_list.html'
    context_object_name = 'samples'
    

class SampleUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = 'change_sample'
    model = Sample 
    #form_class = SampleForm 

    form_class = SampleUpdateForm
    template_name = 'sample_update.html'
    success_url = reverse_lazy('sample_list') 

	#to check if there exists another instance with the same ip number other the one being updated
    def form_valid(self, form):
        unique_specimen_id = form.cleaned_data['unique_specimen_id']

        if Sample.objects.filter(unique_specimen_id=unique_specimen_id).exclude(pk=self.object.pk).exists():
            form.add_error('unique_specimen_id',"Specimen Id number already exists")
            return self.form_invalid(form)
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
