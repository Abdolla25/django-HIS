# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.generic import View

from apps.invoice.forms import AddCategoryForm, AddCompanyForm, AddDepartmentForm, AddInvoiceForm, AddPurchaseForm

from .models import Menu, Page, SubMenu, Carousel, MainIcon, Featurette
from apps.invoice.models import Category, Company, Department
from .forms import ContactForm


def index(request):
    context = {}
    context['segment'] = 'index'
    context['menu_items'] = Menu.objects.all().order_by('priority')
    context['submenu_list'] = SubMenu.objects.all().order_by('priority')
    context['carousel_list'] = Carousel.objects.all().order_by('priority')
    context['mainicon_list'] = MainIcon.objects.all().order_by('priority')
    context['featurette_list'] = Featurette.objects.all().order_by('priority')
    context['department_list'] = Department.objects.all()
    context['contact_form'] = ContactForm()
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def invoice(request):
    context = {'segment': 'invoice'}

    html_template = loader.get_template('invoice/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        context['invoice_form'] = AddInvoiceForm
        context['purchase_form'] = AddPurchaseForm
        context['company_form'] = AddCompanyForm
        context['company_list'] = Company.objects.all().order_by('id')
        context['category_form'] = AddCategoryForm
        context['category_list'] = Category.objects.all().order_by('id')
        context['department_form'] = AddDepartmentForm
        context['department_list'] = Department.objects.all().order_by('id')
        # context['test'] = formset_factory(AddInvoiceForm, extra=2)()

        html_template = loader.get_template('invoice/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

def contact(request):
    try:
        ContactForm(request.POST).save()
        messages.success(request, 'تم إرسال النموذج بنجاح!')
        return HttpResponseRedirect('/#contact')
    except:
        messages.warning(request, 'لم يتم إرسال النموذج بسبب خطأ في نوع البيانات المدخل!')
        return redirect('/#contact')

class PageView(View):
    def get(self, request, slug):
        pages = get_object_or_404(Page, url=slug)

        context = {}
        context['pages_list'] = pages
        context['menu_items'] = Menu.objects.all().order_by('priority')
        context['submenu_list'] = SubMenu.objects.all().order_by('priority')
        context['contact_form'] = ContactForm()

        return render(request, 'home/page.html', context)