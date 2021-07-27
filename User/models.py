from django.contrib.auth.models import User as DjangoUser
from django.db import models

from TransactionsBook.models import TransactionsBook


class User(models.Model):
    # link with a Django User Object that is unique (No Django User can be linked with > 1 User and vice versa
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    # classic foreign key link
    transaction_book = models.ForeignKey(TransactionsBook, on_delete=models.SET_NULL, null=True)
