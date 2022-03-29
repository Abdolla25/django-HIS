from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Team

# Create your views here.

class HomePageView(View):
    def get(self, request):
        team_list = Team.objects.all()
        return HttpResponse(team_list)