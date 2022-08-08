# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from operator import inv
from uuid import uuid4
from django import template
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.generic import View
from django.db.models import Sum, F

from apps.invoice.forms import AddCategoryForm, AddCompanyForm, AddDepartmentForm, AddInvoiceForm, AddItemForm

from .models import Menu, Page, SubMenu, Carousel, MainIcon, Featurette
from apps.invoice.models import Category, Company, Department, Invoice, Item
from .forms import ContactForm

inv_slug = ''

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
        context['company_form'] = AddCompanyForm
        context['company_list'] = Company.objects.all().order_by('id')
        context['category_form'] = AddCategoryForm
        context['category_list'] = Category.objects.all().order_by('id')
        context['department_form'] = AddDepartmentForm
        context['department_list'] = Department.objects.all().order_by('id')
        html_template = loader.get_template('invoice/' + load_template)
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@permission_required('invoice.purchase', login_url="/login/")
def listInvP(request):
    pass

@permission_required('invoice.purchase', login_url="/login/")
def createInvoice(request):
    #create a blank invoice ....
    random = str(uuid4())
    newInvoice = Invoice.objects.create(entryPerson=random)
    newInvoice.save()
    inv = Invoice.objects.get(entryPerson=random)
    return redirect('home:create-build-invoice', slug=inv.slug)

@login_required(login_url="/login/")
def createBuildInvoice(request, slug):
    #fetch that invoice
    try:
        invoice = Invoice.objects.get(slug=slug)
        pass
    except:
        messages.warning(request, 'توجيه باستخدام رابط غير صحيح، تم إنشاء فاتورة جديدة')
        return redirect('home:create-invoice')
    #fetch all the products - related to this invoice
    items = Item.objects.filter(invoice=invoice)
    context = {}
    context['invoice'] = invoice
    context['items'] = items
    context['items_count'] = items.count()
    total = items.aggregate(total=Sum(F('price') * F('quantity')))['total']
    context['items_total'] = total
    tax = items.aggregate(total=(Sum(F('price') * F('quantity'))) * 0.14)['total']
    context['items_tax'] = tax
    context['items_inv'] = items.aggregate(total=(Sum(F('price') * F('quantity'))) * 1.14)['total']
    context['inv_slug'] = slug
    if request.method == 'GET':
        item_form  = AddItemForm()
        inv_form = AddInvoiceForm(instance=invoice)
        context['item_form'] = item_form
        context['invoice_form'] = inv_form
        return render(request, 'invoice/add-invoice.html', context)
    if request.method == 'POST':
        item_form  = AddItemForm(request.POST)
        inv_form = AddInvoiceForm(request.POST, instance=invoice)
        if item_form.is_valid():
            obj = item_form.save(commit=False)
            obj.invoice = invoice
            obj.save()
            messages.success(request, "تمت إضافة الصنف بنجاح!")
            return redirect('home:create-build-invoice', slug=slug)
        elif inv_form.is_valid and 'purchase_date' in request.POST:
            inv_form.save()
            context['item_form'] = item_form
            context['invoice_form'] = inv_form
            messages.success(request, "تم تحديث الفاتورة بنجاح")
            return render(request, 'invoice/add-invoice.html', context)
        else:
            context['item_form'] = item_form
            context['invoice_form'] = inv_form
            messages.warning(request,"لم يتم تحديث الفاتورة، برجاء مراجعة كافة البيانات المدخلة أعلاه!")
            return render(request, 'invoice/add-invoice.html', context)
    return render(request, 'invoice/add-invoice.html', context)

@permission_required('invoice.purchase', login_url="/login/")
def deleteInvoice(request, slug):
    try:
        Invoice.objects.get(slug=slug).delete()
    except:
        messages.error(request, 'Something went wrong [deleteInvoice]')
        return redirect('home:create-invoice')
    return redirect('home:create-invoice')

@permission_required('invoice.purchase', login_url="/login/")
def deleteItem(request, slug, inv_slug):
    try:
        Item.objects.get(slug=slug).delete()
    except:
        messages.error(request, 'Something went wrong [deleteItem]')
        return redirect('home:create-build-invoice', slug=inv_slug)
    return redirect('home:create-build-invoice', slug=inv_slug)

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