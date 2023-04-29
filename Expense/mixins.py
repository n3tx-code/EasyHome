from django.contrib.auth.mixins import LoginRequiredMixin


class ExpenseMixin(LoginRequiredMixin):
    '''
        check if user is in the expense record of the expense
    '''

    def dispatch(self, request, *args, **kwargs):
        super_result = super().dispatch(request, *args, **kwargs)
        if super_result.status_code == 200:
            expense = self.get_object()
            if request.user.expense_record.get() != expense.expense_record:
                return self.handle_no_permission()
        return super_result
