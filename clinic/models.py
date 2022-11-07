from email.policy import default
from pyexpat import model
from django.db import models
import uuid

# Create your models here.
class Clinic(models.Model):
    clinic_name = models.CharField(max_length=126, unique=True)
    is_ocuped = models.BooleanField(default=False)
    is_ok = models.BooleanField(default=False)
    doctor = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="clinic", null=True
    )
