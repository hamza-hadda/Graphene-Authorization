from graphene_django import DjangoObjectType
from graphene import ObjectType

from .decorators import permissions_checker


class IsAuthenticated:
    """
    Allows access only to authenticated users
    """

    @staticmethod
    def has_permission(user):
        return (
            user
            and user.is_authenticated
            and user.is_active
            and not user.is_disabled_employee
        )


class IsBookrStaff:
    """
    Allow access only to Bookr Staff
    """

    @staticmethod
    def has_permission(user):
        return user and user.is_authenticated and user.is_active and user.is_staff


class PermissionDjangoObjectType(DjangoObjectType):
    """
    Check if the object
    """

    class Meta:
        abstract = True

    @classmethod
    def get_node(cls, info, id):
        return permissions_checker(cls.permission_classes())(super().get_node)(
            cls, info, id
        )

    @staticmethod
    def permission_classes():
        return []


class PermissionObjectType(ObjectType):
    """
    Check if the object
    """

    class Meta:
        abstract = True

    @classmethod
    def get_node(cls, info, id):
        return permissions_checker(cls.permission_classes())(super().get_node)(
            cls, info, id
        )

    @staticmethod
    def permission_classes():
        return []
