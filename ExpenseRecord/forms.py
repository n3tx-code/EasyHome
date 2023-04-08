from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.utils.translation import gettext_lazy as _

from EasyHome import settings
from ExpenseRecord.models import ExpenseRecord


class ExpenseRecordCreationForm(forms.ModelForm):
    code = forms.CharField(label=_("Code du compte partagée"), max_length=255, required=True,
                           help_text=_(
                               "Le code du compte partagé est un code unique à partager avec les autres utilisateurs du compte uniquement !"
                               "Il n'est pas stocké dans notre base de données et ne peut être récupéré en cas de perte. "
                               "Il est utilisé pour chiffrer les données du compte partagé."
                               "Faites bien attention à l'enregistrer/l'écrire quelque part. Il sera demandé à chaque connexion."))

    class Meta:
        model = ExpenseRecord
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _("Créer un compte partagé"), css_class="btn-block btn-success px-4 py-2"))


class ExpenseRecordCodeCheckForm(forms.Form):
    code = forms.CharField(label=_("Code du compte partagé"), max_length=255, required=True,
                           help_text=_("Entrez le code du compte partagé pour vous connecter."))

    if not settings.DEBUG:
        # todo :
        # captcha = ReCaptchaField(widget=ReCaptchaV3, label=False)
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _("Valider le code"), css_class="btn-block btn-success px-4 py-2"))
