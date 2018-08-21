# encoding: utf-8
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from main.views import IndexView, ShiftTakeView

urlpatterns = [
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # path(r'account/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', IndexView.as_view(), name='index'),
    re_path(r'(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/', IndexView.as_view(), name='index_full'),

    path('take/', ShiftTakeView.as_view(), name='take_shift'),
]