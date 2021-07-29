from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import TransactionsBook


class TransactionBookCreateForm(forms.ModelForm):
    class Meta:
        model = TransactionsBook
        fields = ('name', 'description')
        labels = {
            'name': "Nom",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Créer"))
