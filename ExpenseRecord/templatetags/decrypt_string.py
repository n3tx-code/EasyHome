from django import template

from ExpenseRecord.utils import decrypt_string as decrypt_string_utils

register = template.Library()


@register.filter
def decrypt_string(string, code):
    return decrypt_string_utils(string, code)
