from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class TransactionsBook(models.Model):
    token = models.CharField(max_length=20, null=False)
    verification_code = models.CharField(max_length=4, null=False)
    name = models.CharField(max_length=255, null=False)
    creation_date = models.DateField(default=timezone.now, null=False)
    description = models.TextField(null=True)
    author = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
