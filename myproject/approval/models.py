from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

from result.models import Result

# Create your models here.
User = get_user_model()

class Approval(models.Model):

    class Meta:
        verbose_name = "Approval"

    
    def __str__(self):
        return str(self.result.id)

    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    assistant_professor = models.ForeignKey(User, 
                                            related_name ='assistant_approval',
                                            on_delete = models.SET_NULL,
                                            null = True
                                           )
    assistant_approval_date = models.DateTimeField(blank=True, null=True)
    associate_professor = models.ForeignKey(User,
                                            related_name = 'associate_approval',
                                            on_delete = models.SET_NULL,
                                            null=True
                                            )
    associate_approval_date = models.DateTimeField(blank=True, null=True)
    result_content = RichTextField(verbose_name = 'Result')
    


