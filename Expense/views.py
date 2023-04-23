from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from Expense.forms import ExpenseCreationForm
from ExpenseRecord.mixins import ExpenseRecordMixin
from ExpenseRecord.utils import hash_string


class ExpenseCreationView(ExpenseRecordMixin, FormView):
    template_name = 'Expense/Creation.html'
    success_url = reverse_lazy('expense_record_detail')
    form_class = ExpenseCreationForm

    def form_valid(self, form):
        form.instance.expense_record = self.request.user.expense_record.get()
        form.instance.name = hash_string(form.instance.name, self.request.session['code'])
        form.instance.amount = hash_string(form.instance.amount, self.request.session['code'])
        form.save()
        messages.add_message(self.request, messages.SUCCESS, _("Dépense ajoutée."))
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['expense-record'] = self.request.user.expense_record.get()
        return kwargs
