from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAccountOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsChargeOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.account.user == request.user


class IsHimself(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
