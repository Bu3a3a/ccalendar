# encoding: utf-8
import calendar

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone

from django.views.generic import TemplateView, FormView

from main.models import ShiftModel, ShiftDayModel
from main.forms import ShiftTakeForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        current_date = timezone.localtime()
        year = int(kwargs.get('year', current_date.year))
        month = int(kwargs.get('month', current_date.month))
        context['year'] = year
        context['month'] = month
        context['month_name'] = calendar.month_name[month]
        month_calendar = calendar.HTMLCalendar().monthdatescalendar(year, month)
        context['calendar'] = month_calendar.copy()
        shifts = ShiftModel.objects.for_period(month=month, year=year)
        context['shifts'] = shifts
        shiftdays = ShiftDayModel.objects.for_period(month=month, year=year, available_for_user=self.request.user)
        context['shiftdays'] = shiftdays
        context['shiftdays_dict'] = {date.date.day: date for date in shiftdays}
        context['shifts_dict'] = {date.date.day: date.shiftmodel_set.all() for date in shiftdays}
        return context


class ShiftTakeView(LoginRequiredMixin, FormView):
    template_name = 'take_shift.html'
    form_class = ShiftTakeForm

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)

        shift = form.cleaned_data['shift']
        shift.user = self.request.user
        shift.save()

        if self.request.is_ajax():
            data = {
                'success': True,
            }
            return JsonResponse(data)
        else:
            return response


class ShiftTakeByDateView(LoginRequiredMixin, FormView):
    template_name = 'take_shift_by_date.html'
    form_class = ShiftTakeForm

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)

        shift = form.cleaned_data['shift']
        shift.user = self.request.user
        shift.save()

        if self.request.is_ajax():
            data = {
                'success': True,
            }
            return JsonResponse(data)
        else:
            return response