import math

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from Transaction.models import Transaction


class TransactionCreateForm(forms.ModelForm):
    transactions_book = None
    apply_ratio = forms.BooleanField(label="Appliquer le ratio", required=False)
    particular_sharing = forms.BooleanField(label="Partage particulier", required=False)

    class Meta:
        model = Transaction
        fields = ('author', 'total', 'label')
        labels = {
            'total': 'Total',  # not present in html form ¯\_(ツ)_/¯
        }

    def __init__(self, *args, **kwargs):
        self.transactions_book = kwargs.pop('transactions_book')
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = self.transactions_book.members.all()
        for member in self.transactions_book.members.all():
            input_name_value = 'member_value_' + str(member.id)
            self.fields[input_name_value] = forms.FloatField(min_value=0, required=False,
                                                             initial=0, label=member.first_name)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Ajouter"))

    def clean(self):
        cleaned_data = super().clean()
        if float(cleaned_data.get('total')) < 0.01 or len(str(cleaned_data.get('total')).split('.')[1]) > 2:
            self.add_error('total', "Valeur incorrecte")
        if cleaned_data.get('author') not in self.transactions_book.members.all():
            self.add_error('author', "Personne iconnue")
        if cleaned_data.get('particular_sharing'):
            for member in self.transactions_book.members.all():
                input_name = 'member_value_' + str(member.id)
                if cleaned_data.get(input_name) < 0:
                    self.add_error('particular_sharing', "Le partage n'est pas équilibré")
