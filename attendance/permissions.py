from rest_framework import permissions
from rest_framework.views import Request, View

from .models import Attendance


class isAttendance(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Attendance):
        return request.user.is_attendance


class isDoctor(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Attendance):
        return request.user.is_doctor


class isOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Attendance):

        return request.user in obj.users
