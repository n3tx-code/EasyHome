from django.db import models
from django.utils.translation import gettext_lazy as _


class Expense(models.Model):
    name = models.CharField(_('Nom de la dépense'), max_length=255)
    amount = models.CharField(_('Montant de la dépense'), max_length=255)
    date = models.CharField(_('Date de la dépense'), max_length=255)
    author = models.ForeignKey('auth.User', related_name='expenses', on_delete=models.CASCADE, verbose_name=_('Auteur de la dépense'))
    expense_record = models.ForeignKey('ExpenseRecord.ExpenseRecord', related_name='expenses', on_delete=models.CASCADE)
