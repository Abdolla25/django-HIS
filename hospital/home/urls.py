from django.urls import include, path, re_path
from django.contrib import admin

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path("search/", views.SearchResultsView.as_view(), name="search_results"),
    path('contact/', views.contact, name='contact'),
    path("account/", include("django.contrib.auth.urls")),
    path('invoice/', views.invoice, name='invoice'),
    path('<slug:slug>/', views.PageView.as_view(), name='page_details'),
]
