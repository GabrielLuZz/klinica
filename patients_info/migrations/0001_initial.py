# Generated by Django 4.1.2 on 2022-11-03 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PatientInfo",
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
                ("comorbidities", models.TextField(null=True)),
                ("comments", models.TextField(null=True)),
            ],
        ),
    ]
