import math

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from Transaction.forms import TransactionCreateForm
from Transaction.models import Transaction, TransactionValue
from TransactionsBook.models import TransactionsBook


class TransactionAddView(LoginRequiredMixin, FormView):
    form_class = TransactionCreateForm
    template_name = "Transaction/create.html"
    transactions_book = None
    success_url = reverse_lazy('transactions-book')

    def dispatch(self, request, *args, **kwargs):
        try:
            self.transactions_book = TransactionsBook.objects.get(members=self.request.user)
        except:
            return redirect(reverse_lazy('transactions-book-create'))
        return super().dispatch(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Transaction Creation"
        return context

    def get_form_kwargs(self):
        kwargs = super(TransactionAddView, self).get_form_kwargs()
        kwargs['transactions_book'] = self.transactions_book
        return kwargs

    def form_valid(self, form):
        form_data = form.cleaned_data
        transaction = Transaction.objects.create(author=form_data['author'], total=form_data['total'],
                                                 label=form_data['label'])
        transaction.save()
        self.transactions_book.transactions.add(transaction)
        transaction_values = []
        try:
            if form_data['apply_ratio']:
                # get ratio
                for member in self.transactions_book.members.all():
                    # apply ratio
                    pass
            if form_data['particular_sharing']:
                for member in self.transactions_book.members.all():
                    pass
            else:
                for member in self.transactions_book.members.all():
                    transaction_value = TransactionValue.objects.create(transaction=transaction, user=member,
                                                                        value=form_data['total'] / len(
                                                                            self.transactions_book.members.all()))
                    transaction_value.save()
                    transaction_values.append(transaction_value)
        except:
            transaction.delete()
            for transaction_value in transaction_values:
                transaction_value.delete()
            messages.add_message(self.request, messages.ERROR,
                                 "Une erreur est survenue lors de l'enregistrement de votre transaction")
            self.transactions_book.transactions.remove(transaction)
            self.success_url = reverse_lazy('transaction-add')
        return super().form_valid(form)
