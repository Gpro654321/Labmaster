# This file shall hold some custom functions that may be needed for sample app
from .models import Sample

def generate_sample_id():
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
        #self.fields['sample_id'].initial = latest_sample_id

        #self.sample_id = latest_sample_id

        sample_id = latest_sample_id
    else:
        #self.sample_id = \
        #        f"{datetime.date.today().strftime('%Y%m%d')}-00001"


        sample_id = \
                f"{datetime.date.today().strftime('%Y%m%d')}-00001"

    return sample_id

def generate_date_time_arrived():

    #initialize it to the current time and date

    #Even though the attribute is a datetime one, the form becomes valid
    # only when the date alone is put in the form field
    date_time_arrived = \
        datetime.datetime.now().strftime("%Y-%m-%d") 
    return date_time_arrived

