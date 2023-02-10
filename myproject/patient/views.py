
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from .models import Patient
from .forms import PatientForm

# Create your views here.
class PatientFormView(LoginRequiredMixin, FormView):
	template_name = 'patient_form.html'
	form_class = PatientForm
	success_url = reverse_lazy('patient_form')

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)

'''
def patient_form_view(request):
	if request.method == "POST":
		print("I am inside if patient_form_view if post is True")
		form = PatientForm(request.POST)
		#ip_number = request.POST['ip_number']

		#ip_number = form.cleaned_data['ip_number']
'''
'''

		if Patient.objects.filter(ip_number=ip_number).exists():

			form.add_error('ip_number',"IP number already exists")
			return render(request, 'patient_form.html', {'form':form})

'''

'''
		if form.is_valid():
			print("I am inside patient_form_view form is valid")
			form.save()
			return redirect(reverse(patient_form_view))
		else:
			print(form.errors)
			return render(request, 'patient_form.html', {'form':form})
	else:
		form = PatientForm()
		return render(request, 'patient_form.html', {'form':form})

'''


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patient_list.html'
    context_object_name = 'patients'

class PatientUpdateView(LoginRequiredMixin, UpdateView):
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

	
	
    
class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    success_url = reverse_lazy('patient_list')
    template_name = 'patient_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect('patient_list')
        else:
            return super().post(request,*args, **kwargs)


