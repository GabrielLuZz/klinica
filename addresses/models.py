from django.db import models

# Create your models here.
class Address(models.Model):
    
    cep=models.CharField(max_length=11, null=True)
    state=models.CharField(max_length=2, null=True)
    street=models.CharField(max_length=50, null=True)
    number=models.CharField(max_length=8, null=True)
