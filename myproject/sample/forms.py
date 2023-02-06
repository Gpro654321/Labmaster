import datetime

from django import forms
from django import utils

from .models import Sample

class SampleForm(forms.ModelForm):
    sample_id = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    date_time_arrived = forms.DateField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    ) 

    class Meta:
        model = Sample
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("I am inside sample forms - Patient forms")
        try:
            latest_sample = Sample.objects.latest('date_time_arrived')
            print("latest sample", latest_sample.sample_id)
        except Sample.DoesNotExist:
            latest_sample = False 

        if latest_sample:
            latest_sample_id = latest_sample.sample_id
            print(latest_sample_id)
            latest_sample_id_serial = int(latest_sample_id.split("-")[1])
            print("latest_sample_id_serial", latest_sample_id_serial)
            latest_sample_id_serial = latest_sample_id_serial + 1
            latest_sample_id = \
            f"{datetime.date.today().strftime('%Y%m%d')}-{str(latest_sample_id_serial).zfill(5)}"
            self.fields['sample_id'].initial = latest_sample_id
        else:
            self.fields['sample_id'].initial = \
                    f"{datetime.date.today().strftime('%Y%m%d')}-00001"

        #initialize it to the current time and date

        #Even though the attribute is a datetime one, the form becomes valid
        # only when the date alone is put in the form field
        self.fields['date_time_arrived'].initial = \
            datetime.datetime.now().strftime("%Y-%m-%d") 



