from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import FloatField
from django.utils.translation import gettext_lazy as _

from Expense.models import Expense


class ExpenseCreationForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'date', 'author']

    def __init__(self, *args, **kwargs):
        expense_record = kwargs.pop('expense-record')
        super().__init__(*args, **kwargs)
        self.fields['amount'] = FloatField(min_value=0.01, step_size=0.01, label=_('Montant de la dépense'))
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['author'].queryset = expense_record.users.all()
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _("Ajouter une dépense"), css_class="btn-block btn-success px-4 py-2"))
