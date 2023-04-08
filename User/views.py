from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from User.form import LoginForm, SignInForm
from User.mixins import UnknownUserMixin


class SignInView(FormView, UnknownUserMixin):
    template_name = 'User/SignIn.html'
    form_class = SignInForm
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Inscription")
        return context

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, _("Compte créé."))
        return super().form_valid(form)


class LoginView(UnknownUserMixin, FormView):
    template_name = "User/signUp&Login.html"
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Connexion")
        return context

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def get_success_url(self):
        # check user has an expense record
        if self.request.user.expense_record.exists():
            return reverse_lazy('expense_record_check_code')
        else:
            return reverse_lazy('expense_record_creation')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('expense_record_detail'))
        return super().dispatch(request)

# todo : mixin that check code in session, other wise redirect to check code
