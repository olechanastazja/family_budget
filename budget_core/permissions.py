from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class IsBudgetOwnerOrReadOnly(IsAuthenticated):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return (
                obj.owner == request.user
                or obj.shared_with.filter(id=request.user.id).exists()
            )
        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
