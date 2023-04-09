from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse_lazy

from ExpenseRecord.models import ExpenseRecord


class ExpenseRecordTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='test')

    def test_check_code(self):
        expense_record = ExpenseRecord.objects.create(name='test')
        expense_record.users.add(self.user)
        expense_record.hash_name('1234')
        expense_record.save()

        self.assertTrue(expense_record.check_code('1234'))

    def test_login_success_url(self):
        self.client.login(username='test', password='test')
        self.assertURLEqual(self.client.get(reverse_lazy('expense_record_creation')).resolver_match.url_name, 'expense_record_creation')

        expense_record = ExpenseRecord.objects.create(name='test')
        expense_record.users.add(self.user)
        expense_record.hash_name('1234')
        expense_record.save()

        self.assertRedirects(self.client.post(reverse_lazy('expense_record_creation')), reverse_lazy('expense_record_detail'))

    def test_ExpenseRecordCheckCodeView_form_valid(self):
        self.client.login(username='test', password='test')
        expense_record = ExpenseRecord.objects.create(name='test')
        expense_record.users.add(self.user)
        expense_record.hash_name('1234')
        expense_record.save()

        # wrong code
        self.assertEqual(self.client.post(reverse_lazy('expense_record_check_code'), {'code': '0000'}).resolver_match.url_name,
                         'expense_record_check_code')

        # correct code
        self.assertRedirects(self.client.post(reverse_lazy('expense_record_check_code'), {'code': '1234'}), reverse_lazy('expense_record_detail'))
        self.assertEqual(self.client.session['code'], '1234')

    def test_ExpenseRecordMixin(self):
        self.client.login(username='test', password='test')
        self.assertRedirects(self.client.get(reverse_lazy('expense_record_detail')), reverse_lazy('expense_record_creation'))

        expense_record = ExpenseRecord.objects.create(name='test')
        expense_record.users.add(self.user)
        expense_record.hash_name('1234')
        expense_record.save()

        self.assertRedirects(self.client.get(reverse_lazy('expense_record_creation')), reverse_lazy('expense_record_detail'))
