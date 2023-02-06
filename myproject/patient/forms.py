from django import forms
#from trix.widgets import TrixEditor
from django.contrib.admin.widgets import AdminDateWidget
#from ckeditor_uploader.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from .models import Patient

class PatientForm(forms.ModelForm):
    #medical_history = forms.CharField(widget=CKEditorWidget())
    
    #notes = RichTextField(blank=True)
    dob = forms.CharField(widget=AdminDateWidget(attrs={'type':'date',}))
    class Meta:
        model = Patient
        fields = '__all__'

