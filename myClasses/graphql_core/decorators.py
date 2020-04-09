import inspect

from bkr_core.utils.exceptions import PermissionDenied
from bkr_core.graphql_core.utils import get_id_from_base64_encoded_string
from functools import wraps


def permissions_checker(permission_classes=None):
    permission_classes = permission_classes or []

    def wrapper(func):
        @wraps(func)
        def decorator(self, info, *args, **kwargs):
            user = info.context.user
            pk = kwargs.get("id") or kwargs.get("pk")
            if not pk and args:
                pk = args[0]

            for permission in permission_classes:
                if not permission.has_permission(user):
                    raise PermissionDenied("Permission Denied.")
                if pk and hasattr(permission, "has_object_permission"):
                    obj = permission.model.objects.get(
                        pk=get_id_from_base64_encoded_string(pk)
                    )
                    if not permission.has_object_permission(user, obj):
                        raise PermissionDenied("Permission Denied.")
            if inspect.isclass(self):
                return func(info, *args, **kwargs)
            return func(self, info, *args, **kwargs)

        return decorator

    return wrapper
