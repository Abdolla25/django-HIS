from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', views.contact, name='contact'),
    path('p/<slug:slug>/', views.PageView.as_view(), name='page_details'),
]
