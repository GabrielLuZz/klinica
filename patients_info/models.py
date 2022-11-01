from django.db import models


# Create your models here.
class PatientInfo(models.Model):

    comorbidities=models.TextField(null=True)
    comments=models.TextField(null=True)
