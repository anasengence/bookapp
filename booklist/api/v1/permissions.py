from rest_framework import permissions
# from booklist.models import Blocklist


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff and request.user.is_superuser


class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsRegularUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and not request.user.is_staff
        )


# class BlocklistPermission(permissions.BasePermission):

#     def has_permission(self, request, view):
#         ip_addr = request.META["REMOTE_ADDR"]
#         blocked = Blocklist.objects.filter(ip_addr=ip_addr).exists()
#         return not blocked