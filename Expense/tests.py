from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.utils.timezone import now

from Expense.models import Expense
from ExpenseRecord.models import ExpenseRecord
from ExpenseRecord.utils import hash_string


class ExpenseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='test1', password='test')
        self.expense_record1 = ExpenseRecord.objects.create(name='test 1')
        self.expense_record1.users.add(self.user1)
        self.expense_record1.hash_name('1234')
        self.expense_record1.save()
        self.user2 = User.objects.create_user(username='test2', password='test')
        self.expense_record2 = ExpenseRecord.objects.create(name='test 2')
        self.expense_record2.users.add(self.user2)
        self.expense_record2.hash_name('12345')
        self.expense_record2.save()

    def test_ExpenseMixin(self):
        expense = Expense.objects.create(expense_record=self.expense_record1, name=hash_string('test', '1234'), amount=hash_string('100', '1234'),
                                         date=now(), author=self.user1)
        self.client.login(username='test1', password='test')
        session = self.client.session
        session['code'] = '1234'
        session.save()
        response = self.client.get(reverse_lazy('expense_detail', kwargs={'pk': expense.pk}))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        self.client.login(username='test2', password='test')
        session = self.client.session
        session['code'] = '1234'
        session.save()
        response = self.client.get(reverse_lazy('expense_detail', kwargs={'pk': expense.pk}))
        self.assertEqual(response.status_code, 403)
