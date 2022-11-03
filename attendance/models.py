import uuid
from django.db import models

# Create your models here.

class Progress(models.TextChoices):
    # WAITING = "Waiting Attendance"
    DEFAULT = "Waiting Attendance"
    DURING = "During Attendance"
    FINISHED = "Finished Attendance"


class Attendance(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    status = models.CharField(
        max_length=50,
        choices=Progress.choices,
        default=Progress.DEFAULT,
    )
    type = models.CharField(max_length=50)
    information = models.TextField()
    date = models.DateField(auto_now_add=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # doctor = models.ForeignKey(
    #     "doctor.Doctor",
    #     on_delete=models.CASCADE,
    #     related_name="attendances",
    # )
    # receptionist = models.ForeignKey(
    #     "receptionist.Receptionist",
    #     on_delete=models.CASCADE,
    #     related_name="attendances",
    # )
    # patient = models.ForeignKey(
    #     "patient.Patient",
    #     on_delete=models.CASCADE,
    #     related_name="attendances",
    # )

    def __repr__(self) -> str:
        return f"<Attendance {self.type} - {self.status}>"

