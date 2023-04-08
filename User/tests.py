from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse_lazy


class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='test')

    def test_login_success_url(self):
        response = self.client.post(reverse_lazy('login'), {'username': 'test', 'password': 'test'})
        self.assertRedirects(response, reverse_lazy('expense_record_creation'))
