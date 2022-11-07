from rest_framework import permissions
from rest_framework.views import Request, View

from .models import Attendance


class IsReceptionist(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.is_receptionist


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.is_doctor


class IsOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        user_id = request.path.split("/")[-3]
        return request.user.id == int(user_id)
