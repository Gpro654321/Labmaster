
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
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


class AssistantApprovedList(LoginRequiredMixin, PermissionRequiredMixin,
                            ListView):
    '''
    This will render a list of results approved by the assitant professor
    '''

    permission_required = 'add_associate_approval'
    model = Approval
    template_name = 'assistant_professor_approved_list.html'
    context_object_name = 'assistant_approved_results'

 
class AssociateProfessorApprovalView(LoginRequiredMixin,PermissionRequiredMixin,FormView):
    '''
    only those results approved by the assistant professor will be shown to
    associate professors
    Logic is 

    '''
    permission_required = 'add_associate_approval'

    form_class = ApprovalForm
    template_name = 'associate_approval_form.html'
    success_url = reverse_lazy('assistant_approved_list')

    '''
    def get(self, request, pk):
        print("hai")
        approval = get_object_or_404(Approval, pk=pk)

        if not approval.assistant_approval_date:
            messages.error(request, "Assistant Professor approval required")
            #need to create a associate professor approval list
            return redirect(reverse('assistant_approved_list'))
        else:
            return redirect(reverse('approve_asp', kwargs={'pk':pk})) 

    '''

    def get_initial(self):
        initial = super().get_initial()
        print(self.kwargs)
        # since we are dealing with approvals, lets get the approval
        approval = Approval.objects.get(pk=self.kwargs['pk'])
        # then from the approval's result content we'll populate 
        result_id = approval.result.pk
        print(result_id)
        result = Result.objects.get(pk=result_id)
        
        #result = Result.objects.get(pk=self.kwargs['result_pk'])
        print(result)
        initial['result_content'] = result.result_data
        return initial
    
    def form_valid(self, form):
        # Get the existing result instance
        print("form_valid kwargs", self.kwargs)
        approval = Approval.objects.get(pk=self.kwargs['pk'])
        print(approval.assistant_approval_date)
        result_id = approval.result.pk
        result = Result.objects.get(pk=result_id)
        # Update the result content
        result.result_data = form.cleaned_data['result_content']
        result.save()

        # Check if an approval instance already exists for this result instance
        try:
            #approval = Approval.objects.get(pk=pk)
            approval.associate_professor = self.request.user
            approval.associate_approval_date = timezone.now() 
            approval.result_content = result.result_data 

        # if the approval for a result does not exist then create a approval
        # for the result , then set the other attributes
        except Approval.DoesNotExist:
            print("APprovla does not exit")
            print(timezone.now())
        else:
            approval.associate_professor = self.request.user
            approval.associate_approval_date = timezone.now() 

        
        #after Approval is done update the result status and again save the\
        #result
        result.result_status = "ASP"
        result.save()

        approval.save()

        return super().form_valid(form)

