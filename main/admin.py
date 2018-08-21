from django.contrib import admin

from main.models import SlotModel


class SlotAdmin(admin.ModelAdmin):
    pass


admin.site.register(SlotModel, SlotAdmin)
