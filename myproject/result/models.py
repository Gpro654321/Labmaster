from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model

from sample.models import Sample

# Create your models here.
class Result(models.Model):
    class Meta:
        verbose_name = 'Result'
        #permissions = [
        #    ("view_result", "Can view result"),
        #    ("add_result", "Can add result"),
        #    ("change_result", "Can change result"),
        #    ("delete_result", "Can delete result")

        #]

    def __str__(self):
        return f' {self.sample.sample_id} '

    #since each sample should be related to one result, we use onetoonefield
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE, unique=True)
    #result_data holds the test results eg, biopsy reports etc
    result_data = RichTextField(verbose_name = "Result")
    #result_date holds the date on which the first test report is entered
    result_date = models.DateTimeField(auto_now_add = True)

    RESULT_STATUS_CHOICES = (
        ('UnderVerification', "Under Verification"),
        ('AP', "Assistant Professor Verified"),
        ('ASP', "Associate Professor Verified")
    )

    result_status = models.CharField(
        max_length=50,
        choices=RESULT_STATUS_CHOICES, 
        default="UnderVerification",
        verbose_name = "Result Status"
    )

    created_by = models.ForeignKey(get_user_model(), 
                                   on_delete=models.SET_NULL,
                                   editable=False,
                                  blank=True,
                                  null = True)



    


