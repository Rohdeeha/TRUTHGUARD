from rest_framework import permissions

class IsFactChecker(permissions.BasePermission):
    """
    Custom permission to allow fact-checkers and superusers to edit/triage reports.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.is_superuser or request.user.groups.filter(name='fact_checker').exists()


class IsTFGBVLegalExpert(permissions.BasePermission):
    """
    Custom permission to strictly allow legal experts and superusers to view sensitive TFGBV cases.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.is_superuser or request.user.groups.filter(name='tfgbv_expert').exists()