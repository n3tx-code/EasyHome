from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from ExpenseRecord.utils import hash_string, decrypt_string


class ExpenseRecord(models.Model):
    name = models.CharField(_("Nom"), max_length=255)
    users = models.ManyToManyField(User, related_name="expense_record")
    hashed_name = models.CharField(_("Nom chiffré"), max_length=255)  # representation of the name hashed with the unique code of the expense record

    def hash_name(self, code):
        '''
            Hash the name of the expense record with the code
        '''
        self.hashed_name = hash_string(self.name, code)
        self.save()

    def check_code(self, code):
        '''
            Check if the code is the good one
        '''
        try:
            return decrypt_string(self.hashed_name, code) == self.name
        except ValueError:
            return False

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Expense record"
        verbose_name_plural = "Expense ecords"
