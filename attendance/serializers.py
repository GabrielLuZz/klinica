from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Attendance
from users.models import User
import typing
from utils.helpers import get_object_or_404_with_message
from users.serializers import (
    DoctorSerializer,
    PatientSerializer,
    DoctorAttendanceSerializer,
    ReceptionistAttendanceSerializer,
    PatientAttendanceSerializer,
)
import ipdb


class AttendanceSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()
    receptionist = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()
    doctor_id = serializers.CharField(write_only=True)
    receptionist_id = serializers.CharField(write_only=True)
    patient_id = serializers.CharField(write_only=True)

    class Meta:
        model = Attendance
        fields = [
            "id",
            "status",
            "attendance_type",
            "attendance_info",
            "created_at",
            "doctor_id",
            "receptionist_id",
            "patient_id",
            "doctor",
            "receptionist",
            "patient",
        ]
        read_only_fields = ["created_at", "id"]

    def get_doctor(self, obj) -> typing.Any:
        attendance = model_to_dict(obj)
        doctor = [user for user in attendance["users"] if user.is_doctor][0]
        doctorSerializer = DoctorAttendanceSerializer(doctor)
        return doctorSerializer.data

    def get_receptionist(self, obj) -> typing.Any:
        attendance = model_to_dict(obj)
        receptionist = [user for user in attendance["users"] if user.is_receptionist][0]
        receptionistSerializer = ReceptionistAttendanceSerializer(receptionist)
        return receptionistSerializer.data

    def get_patient(self, obj) -> typing.Any:
        attendance = model_to_dict(obj)
        patient = [
            user
            for user in attendance["users"]
            if not user.is_doctor and not user.is_receptionist
        ][0]
        patientSerializer = PatientAttendanceSerializer(patient)
        return patientSerializer.data

    def create(self, validated_data):
        doctor_id = validated_data.pop("doctor_id")
        receptionist_id = validated_data.pop("receptionist_id")
        patient_id = validated_data.pop("patient_id")

        doctor = get_object_or_404_with_message(
            User,
            id=doctor_id,
            is_doctor=True,
            is_receptionist=False,
            msg="Doctor not Found",
        )
        receptionist = get_object_or_404_with_message(
            User,
            id=receptionist_id,
            is_doctor=False,
            is_receptionist=True,
            msg="Receptionist not Found",
        )
        patient = get_object_or_404_with_message(
            User,
            id=patient_id,
            is_doctor=False,
            is_receptionist=False,
            msg="Patient not Found",
        )

        attendance_obj = Attendance.objects.create(**validated_data)
        attendance_obj.users.set([doctor, receptionist, patient])

        return attendance_obj


class AttendanceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "id",
            "status",
            "attendance_type",
            "attendance_info",
            "created_at",
            "doctor",
            "receptionist",
            "patient",
        ]

    doctor = serializers.SerializerMethodField()
    receptionist = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()

    def get_doctor(self, obj) -> typing.Any:
        attendance = model_to_dict(obj)
        doctor = [user for user in attendance["users"] if user.is_doctor][0]
        doctorSerializer = DoctorAttendanceSerializer(doctor)
        return doctorSerializer.data

    def get_receptionist(self, obj) -> typing.Any:
        attendance = model_to_dict(obj)
        receptionist = [user for user in attendance["users"] if user.is_receptionist][0]
        receptionistSerializer = ReceptionistAttendanceSerializer(receptionist)
        return receptionistSerializer.data

    def get_patient(self, obj) -> typing.Any:
        attendance = model_to_dict(obj)
        patient = [
            user
            for user in attendance["users"]
            if not user.is_doctor and not user.is_receptionist
        ][0]
        patientSerializer = PatientAttendanceSerializer(patient)
        return patientSerializer.data
