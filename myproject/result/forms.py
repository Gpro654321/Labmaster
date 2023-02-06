from django import forms
#from trix.widgets import TrixEditor
from django.contrib.admin.widgets import AdminDateWidget
#from ckeditor_uploader.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from .models import Result 

class ResultForm(forms.ModelForm):
    #medical_history = forms.CharField(widget=CKEditorWidget())
    
    #notes = RichTextField(blank=True)
    #dob = forms.CharField(widget=AdminDateWidget(attrs={'type':'date',}))
    class Meta:
        model = Result 
        # exclude the following fields from the form
        exclude = ['result_status', 'result_date']


