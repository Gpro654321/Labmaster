from django import forms
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth import get_user_model
from .models import Approval

User = get_user_model()

class ApprovalForm(forms.ModelForm):
    result_content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Approval
        fields = ['result_content']

    def save(self, commit=True, *args, **kwargs):
        obj = super().save(commit=False, *args, **kwargs)


        if obj.assistant_approval_date is None and obj.assistant_professor is not None:
            print("i am inside assistant date set")
            obj.assistant_approval_date = datetime.now()

        if obj.associate_approval_date is None and obj.associate_professor is not None:
            print("i am inside associate date set")
            obj.associate_approval_date = datetime.now()

        obj.save()

        return obj
