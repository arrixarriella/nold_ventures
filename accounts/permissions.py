from rest_framework.permissions import BasePermission, SAFE_METHODS


# ─────────────────────────────────────────────
# OBJECT OWNERSHIP
# ─────────────────────────────────────────────

class IsOwner(BasePermission):
    """
    Allow access only to the owner of the object.
    Assumes the model has a `user` ForeignKey.
    Used on: UserAddress, FirebaseToken
    """
    message = "You do not have permission to access this resource."

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# ─────────────────────────────────────────────
# READ-ONLY OR OWNER
# ─────────────────────────────────────────────

class IsOwnerOrReadOnly(BasePermission):
    """
    Safe methods (GET, HEAD, OPTIONS) are allowed to any
    authenticated user. Write methods only to the owner.
    Used on: any shared-read but private-write resource.
    """
    message = "You do not have permission to modify this resource."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


# ─────────────────────────────────────────────
# USER TYPE PERMISSIONS
# ─────────────────────────────────────────────

class IsClient(BasePermission):
    """
    Allow access only to users with user_type = CLIENT.
    """
    message = "Only clients can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_type == request.user.CLIENT
        )


class IsFarmer(BasePermission):
    """
    Allow access only to users with user_type = FARMER.
    """
    message = "Only farmers can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_type == request.user.FARMER
        )


class IsAdminUser(BasePermission):
    """
    Allow access only to users with user_type = ADMIN
    or Django's built-in is_staff / is_superuser flag.
    """
    message = "Only admins can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.user_type == request.user.ADMIN
            or request.user.is_staff
            or request.user.is_superuser
        )


class IsStaff(BasePermission):
    """
    Allow access only to users with user_type = STAFF.
    """
    message = "Only staff can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_type == request.user.STAFF
        )


class IsDeliveryGuy(BasePermission):
    """
    Allow access only to users with user_type = DELIVERY.
    """
    message = "Only delivery personnel can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_type == request.user.DELIVERY
        )


class IsStaffOrAdmin(BasePermission):
    """
    Allow access to staff and admins.
    """
    message = "Only staff or admins can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.user_type in (request.user.STAFF, request.user.ADMIN)
            or request.user.is_staff
        )


class IsDeliveryOrAdmin(BasePermission):
    """
    Allow access to delivery guys and admins.
    """
    message = "Only delivery personnel or admins can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.user_type in (request.user.DELIVERY, request.user.ADMIN)
            or request.user.is_staff
        )


class IsClientOrFarmer(BasePermission):
    """
    Allow access to clients and farmers.
    """
    message = "Only clients or farmers can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.user_type in (request.user.CLIENT, request.user.FARMER)
        )


class IsClientOrFarmerOrAdmin(BasePermission):
    """
    Allow access to clients, farmers and admins.
    """
    message = "Only clients, farmers or admins can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.user_type in (request.user.CLIENT, request.user.FARMER, request.user.ADMIN)
            or request.user.is_staff
        )


# ─────────────────────────────────────────────
# ACTIVE ACCOUNT
# ─────────────────────────────────────────────

class IsActiveUser(BasePermission):
    """
    Reject any request from a deactivated account,
    even if their token is still valid.
    """
    message = "Your account has been deactivated. Please contact support."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
        )


# ─────────────────────────────────────────────
# FIRST LOGIN GATE
# ─────────────────────────────────────────────

class HasCompletedOnboarding(BasePermission):
    """
    Block access to endpoints that require a fully
    onboarded user (is_first_login must be False).
    Use this on any view the user shouldn't reach
    before completing profile setup.
    """
    message = "Please complete your profile setup before continuing."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and not request.user.is_first_login
        )