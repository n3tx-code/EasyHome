from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from User.form import SignInForm


class SignUpView(FormView):
    form_class = SignInForm
    template_name = "User/signUp.html"

    def form_valid(self, form):
        formData = form.cleaned_data
        user = User.objects.create_user(username=formData['email'], first_name=formData['first_name'],
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


'''class ClientLoginView(LoginView):
    template_name = "client/login.html"

    def get_success_url(self):
        try:
            currentClient = Client.objects.get(user=self.request.user)
        except:
            return reverse_lazy('logout')

        if currentClient:
            if currentClient.is_premium:
                return reverse_lazy('offer-choise-after-signIn')

        return reverse_lazy('home')'''
