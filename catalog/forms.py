from django import forms
from django.forms import ModelForm
import datetime
from .models import *
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RenewBookForm(ModelForm):

    def clean_due_back(self):

        data = self.cleaned_data["due_back"]
        if data < datetime.date.today():
            raise ValidationError (_("Invalid date - renewal in past"))
        if data > datetime.date.today() + datetime.timedelta (weeks= 4):
            raise ValidationError(_("Invalid date - renewal more than 4 weeks ahead"))
        return data
    class Meta:
        model= BookInstance
        fields =["due_back"]
        help_text= {"due_back": _('Enter a date between now and 4 weeks (default 3).')}