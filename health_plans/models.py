from django.db import models

# Create your models here.
class HealthPlan(models.Model):
    
    name=models.CharField(max_length=20)

    patient_info=models.ForeignKey("patients_info.PatientInfo", on_delete=models.CASCADE, related_name="health_plan")
