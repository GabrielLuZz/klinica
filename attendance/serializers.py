from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Attendance
from users.models import User
from utils.helpers import get_object_or_404_with_message
import ipdb



class AttendanceSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()
    receptionist = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()
    doctor_id = serializers.CharField(write_only= True)
    receptionist_id = serializers.CharField(write_only= True)
    patient_id = serializers.CharField(write_only= True)

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
        # extra_kwargs = {
        #     "doctor_id": {"write_only": True},
        #     "receptionist_id": {"write_only": True},
        #     "patient_id": {"write_only": True},
        # }
        read_only_fields = ["created_at"]

    def get_doctor(self, obj):
        attendance = model_to_dict(obj)
        doctor = [user for user in attendance["users"] if user.is_doctor]
        return model_to_dict(doctor[0])

    def get_receptionist(self, obj):
        attendance = model_to_dict(obj)
        receptionist = [user for user in attendance["users"] if user.is_receptionist]
        return model_to_dict(receptionist[0])

    def get_patient(self, obj):
        attendance = model_to_dict(obj)
        patient = [user for user in attendance["users"] if not user.is_doctor and not user.is_receptionist]
        return model_to_dict(patient[0])

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

    def get_doctor(self, obj):
        attendance = model_to_dict(obj)
        users = attendance.users
        return {user for user in users if user.is_doctor}

    def get_receptionist(self, obj):
        attendance = model_to_dict(obj)
        users = attendance.users
        return {user for user in users if user.is_receptionist}

    def get_patient(self, obj):
        attendance = model_to_dict(obj)
        users = attendance.users
        return {
            user for user in users if not user.is_doctor and not user.is_receptionist
        }
