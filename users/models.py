from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):

    cpf = models.CharField(max_length=11, null=True)
    birth_date = models.DateField(null=True)
    is_doctor = models.BooleanField(default=False)
    is_receptionist = models.BooleanField(default=False)
    crm = models.CharField(max_length=6, null=True)

    # specialties
    specialties = models.ManyToManyField("specialty.Specialty", related_name="doctors")

    # address
    address = models.OneToOneField(
        "addresses.Address", on_delete=models.CASCADE, related_name="patient", null=True
    )
    # patients_info
    patient_info = models.OneToOneField(
        "patients_info.PatientInfo",
        on_delete=models.CASCADE,
        related_name="patient",
        null=True,
    )
