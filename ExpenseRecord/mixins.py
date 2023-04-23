from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class ExpenseRecordMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if not request.user.expense_record.exists() and self.request.resolver_match.url_name != 'expense_record_creation':
                return redirect(reverse_lazy('expense_record_creation'))
            elif request.user.expense_record.exists() and self.request.resolver_match.url_name == 'expense_record_creation':
                return redirect(reverse_lazy('expense_record_detail'))
        return super().dispatch(request, *args, **kwargs)
