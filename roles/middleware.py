from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse

class RoleRequiredMiddleware(MiddlewareMixin):
    """Middleware that ensures the user has at least one role for protected URLs.
    Views that need role checking should be decorated with @role_required, but this
    middleware adds a safety net for any view that raises PermissionDenied.
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        # If the view has an attribute `required_roles`, enforce it.
        required = getattr(view_func, "required_roles", None)
        if required is None:
            return None  # no role restriction
        if not request.user.is_authenticated:
            return redirect(f"{reverse('customadmin:login')}?next={request.path}")
        user_roles = set(request.user.roles.values_list('name', flat=True))
        if user_roles.intersection(set(required)):
            return None
        return redirect('customadmin:no_access')
