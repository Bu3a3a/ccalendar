from django.contrib.auth.models import User
from django.db import models


class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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


class ShiftDayModel(CommonModel):
    TYPE_CHOICES = (
        (0, 'weekend'),
        (1, 'holiday'),
        (2, 'special'),
    )
    TYPE_CHOICES_DICT = {item[0]: item[1] for item in TYPE_CHOICES}

    type = models.IntegerField(choices=TYPE_CHOICES)
    date = models.DateField()
    show_datetime = models.DateTimeField()

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



