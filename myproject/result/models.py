from django.db import models
from ckeditor.fields import RichTextField

from sample.models import Sample

# Create your models here.
class Result(models.Model):
    class Meta:
        verbose_name = 'Result'

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
        ('Complete', "Complete"),
    )

    result_status = models.CharField(
        max_length=50,
        choices=RESULT_STATUS_CHOICES, 
        default="UnderVerification",
        verbose_name = "Result Status"
    )


