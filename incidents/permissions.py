from rest_framework import permissions

class IsTFGBVSpecialist(permissions.BasePermission):
    """
    Custom permission to only allow TFGBV specialists or superusers.
    """
    def has_permission(self, request, view):
        # 1. Block anyone who isn't logged in
        if not request.user or not request.user.is_authenticated:
            return False
            
        # 2. Allow superusers (you, the admin)
        if request.user.is_superuser:
            return True
            
        # 3. Allow regular users only if they are in the 'tfgbv_specialist' group
        return request.user.groups.filter(name='tfgbv_specialist').exists()