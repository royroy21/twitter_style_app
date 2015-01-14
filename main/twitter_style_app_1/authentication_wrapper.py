# Django Imports
from django.http import HttpResponseForbidden


def allow_if_authenticated(view):
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden("ERROR: user not authenticated")
        return view(request, *args, **kwargs)
    return new_view