from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "seller"


class IsProductOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user
    
    
class IsFavoriteOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user