# encoding: utf-8
from django import forms
from django.utils import timezone

from main.models import SlotModel


class SlotIndexForm(forms.Form):
    send_month_shift = forms.BooleanField(label='Send shifts for the current month', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_date = timezone.localtime()
        year = int(kwargs.pop('year', current_date.year))
        month = int(kwargs.pop('month', current_date.month))
        empty_slots = SlotModel.objects.filter(date__year=year, date__month=month, date_show__lte=current_date,
                                               user=None)
        for slot in empty_slots:
            self.fields['slot_' + str(slot.pk)] = forms.CheckboxInput()

