# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

from apps.invoice.views import addData, editData, retrieveData

app_name = 'home'

urlpatterns = [

    path('invoice/', views.invoice, name='invoice'),

    path('addInvoice/',views.createInvoice, name='create-invoice'),
    path('inv/<slug:slug>',views.createBuildInvoice, name='create-build-invoice'),
    path('deleteInvoice/<slug:slug>',views.deleteInvoice, name='delete-invoice'),
    path('deleteItem/<slug:slug>/<slug:inv_slug>',views.deleteItem, name='delete-item'),
    path('contact/', views.contact, name='contact'),
    path('addData/<str:model>/', addData, name='addData'),
    path('editData/<str:model>/<int:dataID>/', editData, name='editData'),
    path('retrieve/<str:model>/<int:dataID>/', retrieveData, name='retrieveData'),

    path('', views.index, name='home'),

    path('p/<slug:slug>/', views.PageView.as_view(), name='page_details'),

    re_path(r'^.*\.*', views.pages, name='pages'),

]
