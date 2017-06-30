from rest_framework import permissions

from jobs_app import models


class IsCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.type == models.TYPE_ACCOUNT_COMPANY
