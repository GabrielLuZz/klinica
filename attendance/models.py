from django.db import models

# Create your models here.
class StatusChoiches(models.TextChoices):

    WAITING="Em espera"
    IN_PROGRESS="Em andamento"
    CANCELED="Cancelado"
    FINISHED="Finalizado"


class Attendance(models.Model):
    
    status=models.CharField(max_length=20, choices=StatusChoiches.choices, default=StatusChoiches.WAITING)
    attendance_type=models.CharField(max_length=50)
    attendance_info=models.TextField()
    created_at=models.DateField(auto_now_add=True)

    users=models.ManyToManyField("users.User", through="AttendanceUsers", related_name="attendances")


class AttendanceUsers(models.Model):

    user=models.ForeignKey("users.User", on_delete=models.CASCADE)
    attendance=models.ForeignKey(Attendance, on_delete=models.CASCADE)
    