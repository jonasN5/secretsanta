from rest_framework import permissions


class OwnerOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        # Instance must have an attribute named `owner`.
        return obj.owner_id == request.user.id
