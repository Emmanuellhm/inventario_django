from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps

def role_required(*allowed_roles):
    """Decorator to restrict a view to users with at least one of the given roles.
    Usage:
        @role_required('admin', 'manager')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(f"{reverse('home')}?next={request.path}")
            user_roles = set(request.user.roles.values_list('name', flat=True))
            if request.user.is_superuser or user_roles.intersection(set(allowed_roles)):
                return view_func(request, *args, **kwargs)
            # If the user lacks the role, redirect to a generic no‑access page
            return redirect('customadmin:no_access')
        return _wrapped_view
    return decorator
