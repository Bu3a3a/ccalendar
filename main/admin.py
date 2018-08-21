from django import forms
from django.contrib import admin

from main import models


class ShiftInline(admin.StackedInline):
    model = models.ShiftModel
    sortable_field_name = 'type'
    extra = 0


class ShiftAdmin(admin.ModelAdmin):
    list_display = ('day', 'type', 'user',)
    list_filter = ('type', 'day__type', 'day__date',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')

    def get_queryset(self, request):
        queryset = super(ShiftAdmin, self).get_queryset(request)
        queryset = queryset.select_related('user', 'day')
        return queryset


class ShiftDayAdmin(admin.ModelAdmin):
    list_display = ('date', 'type', 'show_datetime',)
    list_filter = ('type', 'date')

    inlines = (ShiftInline,)


admin.site.register(models.ShiftModel, ShiftAdmin)
admin.site.register(models.ShiftDayModel, ShiftDayAdmin)
