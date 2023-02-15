

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django import forms

from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView

from .models import Result
from .forms import ResultForm

# Create your views here.

# this is view that handle to create a new result record
class ResultCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required = 'add_result'
    form_class = ResultForm
    template_name = 'result_form.html'
    success_url = reverse_lazy('result_list')

    def form_valid(self, form):
        '''
        This method actually inserts who the logged in user is to add it to the
        database. Hence should be kept in mind when in future the views are
        migrated to APIs
        '''
        form.instance.created_by = self.request.user
        form.save()
        return super().form_valid(form)


class ResultListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required = 'view_result'
    model = Result 
    template_name = 'result_list.html'
    context_object_name = 'results'

class ResultUpdateView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    permission_required = 'change_result'

    model = Result 
    form_class = ResultForm 
    template_name = 'result_update.html'
    success_url = reverse_lazy('result_list') 

    #to check if there exists another instance with the same pk other the one being updated
    def form_valid(self, form):
        pk = form.cleaned_data['pk']

        if Result.objects.filter(pk=pk).exclude(pk=self.object.pk).exists():
            form.add_error('pk',"Result with this primary key already exists")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_form(self, form_class =None):
        '''
        This method is a hook provided by the 'FormMixin'
        Allow to customize the form instance like passing extra arguments
        form_class=None makes sure that this method works even when the form_class
        isn't specified

        '''
        form = super().get_form(form_class)
        #form.fields['sample'].widget.attrs['readonly'] = True

        form.fields['pk'] = forms.CharField(widget=forms.HiddenInput(),
                                            initial= self.object.pk)

        form.fields['sample'] = forms.CharField(
            widget = forms.TextInput(attrs={'readonly': True}),
            initial = self.object.sample.unique_specimen_id  
        )

        form.fields['UNIQUE-SPECIMEN-ID'] = forms.CharField(

            widget = forms.TextInput(attrs={'readonly': True}),
            initial = self.object.sample.unique_specimen_id

        )
        print(self.object.sample.unique_specimen_id)
        print(self.object.sample.pk)

        return form


class ResultDeleteView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    permission_required = 'delete_result'
    model = Result 
    success_url = reverse_lazy('result_list')
    template_name = 'result_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect('result_list')
        else:
            return super().post(request,*args, **kwargs)

