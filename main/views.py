# encoding: utf-8
import calendar

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone

from django.views.generic import TemplateView, FormView

from main.models import ShiftModel


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    #
    # def get_success_url(self):
    #     return reverse_lazy('main:index', {'month': self.request.})

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        current_date = timezone.localtime()
        year = int(kwargs.get('year', current_date.year))
        month = int(kwargs.get('month', current_date.month))
        context['year'] = year
        context['month'] = month
        context['month_name'] = calendar.month_name[month]
        context['calendar'] = calendar.HTMLCalendar().monthdatescalendar(year, month)
        context['slots'] = ShiftModel.objects.filter(date__year=year, date__month=month, date_show__lte=current_date)\
            .order_by('date')
        return context

    # def post(self, request, *args, **kwargs):

