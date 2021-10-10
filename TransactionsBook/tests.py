import random

from django.contrib.auth.models import User
from django.test import TestCase

from Transaction.models import Transaction, TransactionValue
from TransactionsBook.models import TransactionsBook


class BalanceTest(TestCase):
    total = 0
    transactions_book = None

    def setUp(self):
        author = User.objects.create_user('author', 'author@testcom', 'test')
        author.save()
        a_guy = User.objects.create_user('John', 'john@testcom', 'doe')
        a_guy.save()
        self.transactions_book = TransactionsBook.objects.create(author=author, name='test')
        self.transactions_book.members.add(author)
        self.transactions_book.members.add(a_guy)
        self.transactions_book.save()

    def test_with_two_transactions_with_two_authors(self):
        for i in range(0, 2):
            value = round(random.uniform(0.01, 100), 2)
            self.total += value
            transaction = Transaction.objects.create(author=self.transactions_book.author, total=value,
                                                     label='test')
            transaction.save()
            self.transactions_book.transactions.add(transaction)
            for member in self.transactions_book.members.all():
                transaction_value = TransactionValue.objects.create(transaction=transaction, user=member,
                                                                    value=value / 2)
                transaction_value.save()

        balance = self.transactions_book.balance()
        for member in balance:
            if member['member'] == self.transactions_book.author:
                self.assertEqual(member['total'], round(float(0 - self.total / 2), 2))
            else:
                self.assertEqual(member['total'], round(float(self.total / 2), 2))

    def test_with_three_transactions_and_two_others(self):
        value = round(random.uniform(0.01, 100), 2)
        self.total += value
        transaction = Transaction.objects.create(author=self.transactions_book.author, total=value,
                                                 label='test')
        transaction.save()
        self.transactions_book.transactions.add(transaction)
        for member in self.transactions_book.members.all():
            transaction_value = TransactionValue.objects.create(transaction=transaction, user=member,
                                                                value=value / 2)
            transaction_value.save()

        balance = self.transactions_book.balance()
        for member in balance:
            if member['member'] == self.transactions_book.author:
                self.assertEqual(member['total'], round(float(0 - self.total / 2), 2))
            else:
                self.assertEqual(member['total'], round(float(self.total / 2), 2))

    def test_add_member_to_existing_transactions_book(self):
        another_guy = User.objects.create_user('Carl', 'carl@testcom', 'carl')
        another_guy.save()
        self.transactions_book.members.add(another_guy)
        balance = self.transactions_book.balance()
        for member in balance:
            if member['member'] == self.transactions_book.author:
                self.assertEqual(member["total"], round(float(0 - self.total / 2), 2))
            elif member['member'] == another_guy:
                self.assertEqual(member["total"], 0)
            else:
                self.assertEqual(member["total"], round(float(self.total / 2), 2))
        # check balance
        pass

    def test_with_3_authors(self):
        # add a transaction with new member
        # check balance
        pass
