from email.policy import default
from pyexpat import model
from django.db import models
import uuid

# Create your models here.
class Clinic(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    clinic_name = models.CharField(max_length=126)
    is_ocuped = models.BooleanField(default=False)
    is_ok = models.BooleanField(default=False)
