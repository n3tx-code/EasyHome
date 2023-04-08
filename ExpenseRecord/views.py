from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from ExpenseRecord.forms import ExpenseRecordCreationForm, ExpenseRecordCodeCheckForm
from ExpenseRecord.models import ExpenseRecord


class ExpenseRecordCreationView(LoginRequiredMixin, FormView):
    '''
        This view is used to create a new expense record. It's only accessible if the user is connected and if he doesn't already have an expense record.
    '''
    template_name = 'ExpenseRecord/Creation.html'
    form_class = ExpenseRecordCreationForm
    expense_record = None

    def form_valid(self, form):
        form.save()
        form.instance.users.add(self.request.user)
        form.instance.hash_name(form.data['code'])
        self.expense_record = form.instance
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Création d'un registre des dépenses"
        return context

    def get_success_url(self):
        return reverse_lazy('expense_record_detail')

    def dispatch(self, request, *args, **kwargs):
        super_result = super().dispatch(request, *args, **kwargs)
        if super_result.status_code == 200:
            if request.user.expense_record.exists():
                return redirect(reverse_lazy('expense_record_detail'))
        return super_result


class ExpenseRecordCheckCodeView(LoginRequiredMixin, FormView):
    '''
        This view is used to check the code of the expense record. It's only accessible if the user is connected and if he already have an expense record.
    '''
    template_name = 'ExpenseRecord/CheckCode.html'
    form_class = ExpenseRecordCodeCheckForm
    success_url = reverse_lazy('expense_record_check_code')  # would be change if the code is valid

    # todo : dispatch redirct to expense record creation if no expense record

    def form_valid(self, form):
        code = self.request.POST['code']
        expense_record = self.request.user.expense_record.get()
        if expense_record.check_code(code):
            self.request.session['code'] = code
            return redirect(reverse_lazy('expense_record_detail'))
        messages.add_message(self.request, messages.ERROR, _("Code invalide."))
        return super().form_valid(form)


class ExpenseRecordDetailView(LoginRequiredMixin, TemplateView):
    # todo : expense record mixin
    template_name = 'ExpenseRecord/Detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Registre des dépenses"
        context['expense_record'] = ExpenseRecord.objects.get(users=self.request.user)
        return context
