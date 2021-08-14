from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from TransactionsBook.forms import TransactionBookCreateForm
from TransactionsBook.models import TransactionsBook


# TemplateView : mainly for showing data on a html template
class TransactionBookView(LoginRequiredMixin, TemplateView):
    template_name = 'TransactionBook/TransactionBook.html'
    transactions_book = None

    # entry of the view
    def dispatch(self, request, *args, **kwargs):
        try:
            self.transactions_book = TransactionsBook.objects.get(
                members=self.request.user)  # self.request.user is the user of the session
        except:
            return redirect(reverse_lazy('transactions-book-create'))
            # reverse_lazy('<url_name>') generate the path to the url that have the name given in parameter
        return super().dispatch(request)

    def get_context_data(self, **kwargs):
        # context is the data sent to the template
        context = super().get_context_data(**kwargs)
        # will make make the data of self.user.transactionsbook accessible in the template
        # via the variable transactionsBook
        context['transactionsBook'] = self.transactions_book
        context['title'] = 'Transaction Book'
        return context


class TransactionBookCreateView(LoginRequiredMixin, FormView):
    form_class = TransactionBookCreateForm
    template_name = "TransactionBook/create.html"

    def form_valid(self, form):
        formData = form.cleaned_data
        transactions_book = TransactionsBook.objects.create(author=self.request.user, name=formData['name'],
                                                            description=formData['description'])
        transactions_book.members.add(self.request.user)
        transactions_book.save()

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        try:
            TransactionsBook.objects.get(members=self.request.user)
            return redirect(reverse_lazy('transaction-book'))
        except:
            pass
        return super().dispatch(request)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             'Votre livre des comptes a été créé !')
        return reverse_lazy('transaction-book')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Transaction Book Creation"
        return context
