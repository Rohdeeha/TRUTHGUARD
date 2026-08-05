from rest_framework import permissions

class IsFactChecker(permissions.BasePermission):
    """
    Allows access only to users belonging to the 'Fact-Checker' group 
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Superusers always pass
        if request.user.is_superuser:
            return True
            
        return request.user.groups.filter(name='Fact-Checker').exists()


class IsTFGBVLegalExpert(permissions.BasePermission):
    """
    Strict permission class allowing access only to authorized 
    'TFGBV/Legal Expert' group members or superusers.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        if request.user.is_superuser:
            return True
            
        return request.user.groups.filter(name='TFGBV/Legal Expert').exists()