# Generated by Django 4.1.2 on 2022-11-01 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Attendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Em espera", "Waiting"),
                            ("Em andamento", "In Progress"),
                            ("Cancelado", "Canceled"),
                            ("Finalizado", "Finished"),
                        ],
                        default="Em espera",
                        max_length=20,
                    ),
                ),
                ("attendance_type", models.CharField(max_length=50)),
                ("attendance_info", models.TextField()),
                ("created_at", models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="AttendanceUsers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "attendance",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="attendance.attendance",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="attendance",
            name="users",
            field=models.ManyToManyField(
                related_name="attendances",
                through="attendance.AttendanceUsers",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]