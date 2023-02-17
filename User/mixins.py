from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.base import ContextMixin


class UnknownUserMixin(ContextMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("login"))
        return super().dispatch(request, *args, **kwargs)
