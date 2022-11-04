from rest_framework import permissions
from rest_framework.views import Request, View

from .models import Attendance


class isReceptionist(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.is_receptionist


class isDoctor(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.is_doctor


class isOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Attendance):
        return request.user in obj.users
