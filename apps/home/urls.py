# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

app_name = 'home'

urlpatterns = [

    path('invoice', views.invoice, name='invoice'),

    path('contact/', views.contact, name='contact'),

    path('', views.index, name='home'),

    path('p/<slug:slug>/', views.PageView.as_view(), name='page_details'),

    re_path(r'^.*\.*', views.pages, name='pages'),

]
