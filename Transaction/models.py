from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class TransactionCategory(models.Model):
    label = models.CharField(max_length=255)
    icon = models.ImageField(upload_to="img/category/", null=False)

    def __str__(self):
        return self.label


class Transaction(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField(MinValueValidator(0.01))
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label + " (" + str(self.total) + "€)"


class TransactionValue(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    value = models.FloatField(MinValueValidator(0))

    def __str__(self):
        return self.transaction.label + " | " + self.user.first_name + " " + self.user.last_name + " | " + self.value
