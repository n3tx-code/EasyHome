from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from User.form import SignInForm, LoginForm


class SignUpView(FormView):
    form_class = SignInForm
    template_name = "User/signUp&Login.html"

    def form_valid(self, form):
        formData = form.cleaned_data
        user = User.objects.create_user(username=formData['username'], first_name=formData['first_name'],
                                        last_name=formData['last_name'], email=formData['email'],
                                        password=formData['password'])
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             'Vous pouvez maintenant vous connecter.')
        return reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request)


class LoginView(FormView):
    template_name = "User/signUp&Login.html"
    form_class = LoginForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageTitle'] = "Connexion"
        return context

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request)
