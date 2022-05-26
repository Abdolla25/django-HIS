from django.urls import path, re_path
from django.contrib import admin

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path("search/", views.SearchResultsView.as_view(), name="search_results"),
    path('contact/', views.contact, name='contact'),
    re_path(r'^admin/', admin.site.urls, name='admin'),
    path('<slug:slug>/', views.PageView.as_view(), name='page_details'),
]
