from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from Transaction.models import Transaction, TransactionValue


class TransactionsBook(models.Model):
    token = models.CharField(max_length=20, null=False)
    verification_code = models.CharField(max_length=4, null=False)
    name = models.CharField(max_length=255, null=False)
    creation_date = models.DateField(default=timezone.now, null=False)
    description = models.TextField(null=True, blank=True)  # allow empty input field (unrequired field)
    author = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='author')
    members = models.ManyToManyField(User)
    transactions = models.ManyToManyField(Transaction)

    def __str__(self):
        return self.name

    def balance(self):
        members = []
        for member in self.members.all():
            total = 0
            for transaction in self.transactions.all():
                if transaction.author == member:
                    total -= transaction.total - TransactionValue.objects.get(transaction=transaction,
                                                                              user=member).value
                else:
                    try:
                        total += TransactionValue.objects.get(transaction=transaction, user=member).value
                    except:
                        pass  # member may have been added to the transactions book after the transaction

            members.append({'member': member, 'total': round(total, 2)})
        return members
