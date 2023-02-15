
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from .models import Approval
from .forms import ApprovalForm
from result.models import Result

# Create your views here.

class ApprovalCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                         FormView):
    permission_required = 'add_approval'
    form_class = ApprovalForm
    template_name = 'approval_form.html'
    success_url = reverse_lazy('result_list')

    def get_initial(self):
        initial = super().get_initial()
        result = Result.objects.get(pk=self.kwargs['result_pk'])
        print(result)
        initial['result_content'] = result.result_data
        return initial
    
    def form_valid(self, form):
        # Get the existing result instance
        result = Result.objects.get(pk=self.kwargs['result_pk'])
        # Update the result content
        result.result_data = form.cleaned_data['result_content']
        result.save()

        # Check if an approval instance already exists for this result instance
        try:
            approval = Approval.objects.get(result=result)

        # if the approval for a result does not exist then create a approval
        # for the result , then set the other attributes
        except Approval.DoesNotExist:
            print("APprovla does not exit")
            approval = Approval(result=result)
            approval.assistant_professor = self.request.user
            approval.assistant_approval_date= timezone.now() 
            approval.result_content = result.result_data 
            print(timezone.now())
        else:
            approval.assistant_professor = self.request.user
            approval.assistant_approval_date= timezone.now() 

        
        #after Approval is done update the result status and again save the\
        #result
        result.result_status = "AP"
        result.save()

        approval.save()

        return super().form_valid(form)
        
