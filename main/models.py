from django.contrib.auth.models import User
from django.db import models


class SlotModel(models.Model):
    TYPE_CHOICES = (
        (0, 'normal'),
        (1, 'beeper'),
        (2, 'special'),
    )
    TYPE_CHOICES_DICT = {item[0]: item[1] for item in TYPE_CHOICES}

    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.IntegerField(choices=TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    date_show = models.DateTimeField()

    @property
    def type_str(self):
        return self.TYPE_CHOICES_DICT.get(self.type)

