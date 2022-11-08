from django.shortcuts import get_object_or_404
from users.models import User
from utils.helpers import get_object_or_404_with_message
from clinic.models import Clinic
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError


# class DoctorSave:
#     def perform_create(self, serializer):
#         if self.request.data["doctor"]:
#             user = get_object_or_404_with_message(
#                 User, pk=self.request.data["doctor"], msg="Doctor not found"
#             )
#             serializer.save(doctor=user)
