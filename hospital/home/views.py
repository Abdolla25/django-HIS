from datetime import timezone
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import View
from django.contrib import messages

from .models import Menu, SubMenu, Carousel, MainIcon, Featurette, Page

from .forms import ContactForm

from invoices.models import Department

# from .forms import ContactForm

# Create your views here.

class HomeView(View):
    def get(self, request):
        context = {}
        context['menu_items'] = Menu.objects.all().order_by('priority')
        context['submenu_list'] = SubMenu.objects.all().order_by('priority')
        context['carousel_list'] = Carousel.objects.all().order_by('priority')
        context['mainicon_list'] = MainIcon.objects.all().order_by('priority')
        context['featurette_list'] = Featurette.objects.all().order_by('priority')
        context['department_list'] = Department.objects.all()
        context['contact_form'] = ContactForm()

        return render(request, 'home/home.html', context)

def contact(request):
    try:
        ContactForm(request.POST).save()
        messages.success(request, 'تم إرسال النموذج بنجاح!')
        return HttpResponseRedirect('/#contact')
    except:
        messages.warning(request, 'لم يتم إرسال النموذج بسبب خطأ في نوع البيانات المدخل!')
        return redirect('/#contact')

class PageView(View):
    def get(self,request, slug):
        pages = get_object_or_404(Page, url=slug)

        context = {}
        context['pages_list'] = pages
        context['menu_items'] = Menu.objects.all().order_by('priority')
        context['submenu_list'] = SubMenu.objects.all().order_by('priority')
        context['contact_form'] = ContactForm()

        return render(request, 'home/page.html', context)