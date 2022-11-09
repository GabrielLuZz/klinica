# Generated by Django 4.1.2 on 2022-11-03 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Clinic",
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
                ("clinic_name", models.CharField(max_length=126)),
                ("is_ocuped", models.BooleanField(default=False)),
                ("is_ok", models.BooleanField(default=False)),
            ],
        ),
    ]
