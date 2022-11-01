from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Attendance
from users.models import User


class AttendanceSerializer(serializers.ModelSerializer):
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
        read_only_fields = ["created_at"]

    doctor = serializers.CharField()
    receptionist = serializers.CharField()
    patient = serializers.CharField()

    def create(self, validated_data):
        doctor_id = validated_data.pop("doctor")
        receptionist_id = validated_data.pop("receptionist")
        patient_id = validated_data.pop("patient")

        doctor = get_object_or_404(
            User, id=doctor_id, is_doctor=True, is_receptionist=False
        )
        receptionist = get_object_or_404(
            User, id=receptionist_id, is_doctor=False, is_receptionist=True
        )
        patient = get_object_or_404(
            User, id=patient_id, is_doctor=False, is_receptionist=False
        )

        attendance_obj = Attendance.objects.create(**validated_data)
        attendance_obj.users.set([doctor, receptionist, patient])


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
        return {user for user in users if not user.is_doctor and not user.is_receptionist}
