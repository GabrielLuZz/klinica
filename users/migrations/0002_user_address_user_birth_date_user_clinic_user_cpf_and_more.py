# Generated by Django 4.1.2 on 2022-11-01 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("addresses", "0001_initial"),
        ("clinic", "0001_initial"),
        ("patients_info", "0001_initial"),
        ("specialty", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="address",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="patient",
                to="addresses.address",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="birth_date",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="clinic",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="doctor",
                to="clinic.clinic",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="cpf",
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="crm",
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="is_doctor",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="is_recepcionist",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="patient_info",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="patient",
                to="patients_info.patientinfo",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="specialties",
            field=models.ManyToManyField(
                related_name="doctors", to="specialty.specialty"
            ),
        ),
    ]