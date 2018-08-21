# encoding: utf-8
import datetime

from django import forms

from main import models


class ShiftTakeForm(forms.Form):
    shift = forms.ModelChoiceField(models.ShiftModel.objects.for_period())


class ShiftTakeByDateForm(forms.Form):
    date = forms.DateField()
    type = forms.ChoiceField(choices=models.ShiftModel.TYPE_CHOICES)

    def clean(self):
        cleaned_data = super().clean()
        ok_dates = models.ShiftDayModel.objects.for_period(only_future=True, only_shown=True, available_for_user=True)\
            .values_list('date', flat=True)
        if cleaned_data['date'] not in ok_dates:
            raise forms.ValidationError('Выбранная дата недоступна для резервирования!')


