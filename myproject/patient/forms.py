from django import forms
#from trix.widgets import TrixEditor
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
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



class PatientSearchForm(forms.ModelForm):
    dob = forms.CharField(widget=AdminDateWidget(attrs={'type':'date',}))
    class Meta:
        model = Patient
        fields = '__all__'
        exclude = ['medical_history', 'notes']

    def __init__(self, *args, **kwargs):
        '''
        Overriding the init method to make the fields requirement to False
        '''

        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            field.widget.attrs.update(
                {
                    'class':'form-control',
                    'placeholder': field.label,
                }

            )

    def clean(self):
        '''
        Raise a validation error if none of the fields are filled
        '''

        cleaned_data = super().clean()
        print("i am inside clean method patient seach form")
        print("I am inside clean method Patient Search form",cleaned_data)
        if not any(cleaned_data.values()):
            print("i am inside clean method  if  Patient Search form")
            raise ValidationError("Atleast one field must be filled")
        return cleaned_data



