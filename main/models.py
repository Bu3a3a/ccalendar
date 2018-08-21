# encoding: utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ShiftModelManager(models.Manager):

    def for_user(self, user=None):
        return self.get_queryset().filter(user=user).select_related('user', 'day')

    def for_period(self, day=None, month=None, year=None, user=None, only_shown=True):

        queryset = self.for_user(user)

        if day:
            queryset = queryset.filter(day__date__day=day)

        if month:
            queryset = queryset.filter(day__date__month=month)

        if year:
            queryset = queryset.filter(day__date__year=year)

        if only_shown:
            current_datetime = timezone.now()
            queryset = queryset.filter(day__show_datetime__lte=current_datetime)

        return queryset


class ShiftModel(CommonModel):
    TYPE_CHOICES = (
        (0, 'normal'),
        (1, 'beeper'),
        (2, 'special'),
    )
    TYPE_CHOICES_DICT = {item[0]: item[1] for item in TYPE_CHOICES}

    type = models.IntegerField(choices=TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    day = models.ForeignKey('ShiftDayModel', on_delete=models.CASCADE)

    objects = ShiftModelManager()

    @property
    def type_str(self):
        return self.TYPE_CHOICES_DICT.get(self.type)

    def __str__(self):
        return u'{}: {}: {}'.format(self.user, self.day, self.type)

    class Meta:
        verbose_name = 'Дежурство'
        verbose_name_plural = 'Дежурства'
        db_table = 'main_shift'
        ordering = ('day__date', 'user')
        unique_together = ('user', 'day')


class ShiftDayModelManager(models.Manager):

    def for_period(self, day=None, month=None, year=None, available_for_user=None, only_shown=True, only_future=False):

        queryset = self.get_queryset()

        if day:
            queryset = queryset.filter(date__day=day)

        if month:
            queryset = queryset.filter(date__month=month)

        if year:
            queryset = queryset.filter(date__year=year)

        if only_shown:
            current_datetime = timezone.now()
            queryset = queryset.filter(show_datetime__lte=current_datetime)

        if only_future:
            current_datetime = timezone.now()
            queryset = queryset.filter(date__gte=current_datetime)

        if available_for_user:
            queryset = queryset.exclude(shiftmodel__user__exact=available_for_user)

        return queryset



class ShiftDayModel(CommonModel):
    TYPE_CHOICES = (
        (0, 'weekend'),
        (1, 'holiday'),
        (2, 'special'),
    )
    TYPE_CHOICES_DICT = {item[0]: item[1] for item in TYPE_CHOICES}

    type = models.IntegerField(choices=TYPE_CHOICES)
    date = models.DateField(unique=True)
    show_datetime = models.DateTimeField()

    objects = ShiftDayModelManager()

    @property
    def type_str(self):
        return self.TYPE_CHOICES_DICT.get(self.type)

    def __str__(self):
        return u'{}: {}: {}'.format(self.date, self.type_str, self.show_datetime)

    class Meta:
        verbose_name = 'День с дежурствами'
        verbose_name_plural = 'Дни с дежурствами'
        db_table = 'main_shiftday'
        ordering = ['date', 'type']



