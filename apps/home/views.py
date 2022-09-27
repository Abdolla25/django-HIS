# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import datetime
from operator import inv
import os
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
from django.db.models import Sum, F, Q


from apps.invoice.forms import AddCategoryForm, AddCommentForm, AddCompanyForm, AddDepartmentForm, AddInvoiceForm, AddItemForm

from .models import Contact, Menu, Page, SubMenu, Carousel, MainIcon, Featurette
from apps.invoice.models import Category, Comment, Company, Department, Invoice, Item
from .forms import ContactForm

import numpy as np

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
    context = {}
    context['segment'] = 'invoice'
    context['invoice_count'] = Invoice.objects.filter(number__isnull=False).count()
    context['company_count'] = Company.objects.count()
    context['category_count'] = Category.objects.count()
    context['department_count'] = Department.objects.count()
    context['invoice_finished_count'] = Invoice.objects.filter(current_state=5).count()
    invoice_finished = Invoice.objects.filter(current_state=5).values_list('id', flat=True)
    invoice_month = Invoice.objects.filter(Q(purchase_date__month=datetime.date.today().month) & Q(current_state=5)).values_list('id', flat=True)
    context['invoice_total'] = Item.objects.filter(invoice__in=invoice_finished).aggregate(total=Sum('total_price'))['total']
    context['invoice_month_total'] = Item.objects.filter(invoice__in=invoice_month).aggregate(total=Sum('total_price'))['total']
    context['suggest_count'] = Contact.objects.filter(msg_type='suggest').count()
    context['suggest_flag_count'] = Contact.objects.filter(Q(msg_type='suggest') & Q(msg_flag=True)).count()
    context['complain_count'] = Contact.objects.filter(msg_type='complain').count()
    context['complain_flag_count'] = Contact.objects.filter(Q(msg_type='complain') & Q(msg_flag=True)).count()
    context['contact_list'] = Contact.objects.order_by('msg_created').reverse()[:3]
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
        if request.user.has_perm('invoice.it'):
            context['invoice_list'] = Invoice.objects.filter(number__isnull=False).order_by('-last_updated')
        else:
            if request.user.has_perm('invoice.purchase'):
                state = 1
            elif request.user.has_perm('invoice.security'):
                state = 2
            elif request.user.has_perm('invoice.finance'):
                state = 3
            elif request.user.has_perm('invoice.director'):
                state = 4
            context['invoice_list'] = Invoice.objects.filter(number__isnull=False, current_state=state).order_by('-last_updated')
            context['invoice_hold_list'] = Invoice.objects.filter(number__isnull=False).exclude(current_state=state).order_by('-last_updated')
        html_template = loader.get_template('invoice/' + load_template)
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@permission_required('invoice.purchase', login_url="/login/")
def createInvoice(request):
    #clear empty instances
    empty_inv = Invoice.objects.filter(number__isnull=True)
    for x in empty_inv:
        x.delete()
    #create a blank invoice ....
    random = str(uuid4())
    newInvoice = Invoice.objects.create(entryPerson=random)
    newInvoice.save()
    inv = Invoice.objects.get(entryPerson=random)
    return redirect('home:create-build-invoice', slug=inv.slug)

@permission_required('invoice.purchase', login_url="/login/")
def createBuildInvoice(request, slug):
    #fetch that invoice
    try:
        invoice = Invoice.objects.get(slug=slug)
        items = Item.objects.filter(invoice=invoice)
        comments = Comment.objects.filter(invoice=invoice).order_by('-date_created')
    except:
        messages.warning(request, 'توجيه باستخدام رابط غير صحيح، تم إنشاء فاتورة جديدة')
        return redirect('home:create-invoice')
    #fetch all the products - related to this invoice
    context = {}
    context['invoice'] = invoice
    context['items'] = items
    context['comments'] = comments
    context['items_count'] = items.count()
    context['invoice_image'] = (str(invoice.img).split('/', 2))[-1]
    if items.aggregate(total=Sum('total_price'))['total']:
        total = np.round(float(items.aggregate(total=Sum('total_price'))['total']), decimals=4)
        tax = np.round(np.multiply(total, 0.14), decimals=4)
        context['items_total'] = total
        context['items_tax'] = tax
        context['items_inv'] = np.round(np.add(total, tax), decimals=4)
    context['inv_slug'] = slug
    if request.method == 'GET' and invoice.current_state == 1:
        # print()
        item_form  = AddItemForm()
        comment_form  = AddCommentForm(request.POST)
        inv_form = AddInvoiceForm(instance=invoice)
        context['item_form'] = item_form
        context['comment_form'] = comment_form
        context['invoice_form'] = inv_form
        return render(request, 'invoice/add-invoice.html', context)
    elif request.method == 'GET' and invoice.current_state != 1:
        messages.warning(request, 'لا يمكنك تعديل الفاتورة بعد إرسالها للمراجعة!')
        return redirect('home:create-invoice')
    elif request.method == 'POST':
        item_form  = AddItemForm(request.POST)
        comment_form  = AddCommentForm(request.POST)
        # inv_form = AddInvoiceForm(request.POST, request.FILES, instance=invoice)
        inv_form = AddInvoiceForm(request.POST, request.FILES, instance=invoice)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.invoice = invoice
            item.save()
            messages.success(request, "تمت إضافة الصنف بنجاح!")
            return redirect('home:create-build-invoice', slug=slug)
        elif comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.invoice = invoice
            comment.entryPerson = request.user.get_full_name()
            invoice.current_state = 2
            comment.save()
            invoice.save()
            messages.success(request, "تم إرسال الفاتورة للمراجعة بنجاح!")
            return redirect('home:create-invoice')
        elif inv_form.is_valid and 'purchase_date' in request.POST:
            inv_form.save()
            context['item_form'] = item_form
            context['comment_form'] = comment_form
            context['invoice_form'] = inv_form
            context['invoice_image'] = (str(invoice.img).split('/', 2))[-1]
            messages.success(request, "تم حفظ معلومات الفاتورة بنجاح!")
            return render(request, 'invoice/add-invoice.html', context)
        else:
            pass
    else:
        context['item_form'] = item_form
        context['comment_form'] = comment_form
        context['invoice_form'] = inv_form
        messages.warning(request, "لم يتم حفظ الفاتورة، برجاء مراجعة كافة البيانات المدخلة أعلاه!")
        return render(request, 'invoice/add-invoice.html', context)


@permission_required('invoice.purchase', login_url="/login/")
def deleteItem(request, slug, inv_slug):
    try:
        Item.objects.get(slug=slug).delete()
    except:
        messages.error(request, 'Something went wrong [deleteItem]')
        return redirect('home:create-build-invoice', slug=inv_slug)
    return redirect('home:create-build-invoice', slug=inv_slug)

@permission_required('invoice.purchase', login_url="/login/")
def deleteImage(request, inv_slug):
    try:
        invoice = Invoice.objects.get(slug=inv_slug)
    except:
        messages.error(request, 'Something went wrong clearImage]')
        return redirect('home:create-build-invoice', slug=inv_slug)
    if os.path.exists(str(invoice.img)):
        os.remove(str(invoice.img))
        invoice.img = ''
        invoice.save()
    else:
        messages.error(request, 'Something went wrong [deleteImage]')
        return redirect('home:create-build-invoice', slug=inv_slug)
    return redirect('home:create-build-invoice', slug=inv_slug)


@login_required(login_url="/login/")
def approveInvoice(request, slug):
    if request.user.has_perm('invoice.purchase'):
        state = 1
    elif request.user.has_perm('invoice.security'):
        state = 2
    elif request.user.has_perm('invoice.finance'):
        state = 3
    elif request.user.has_perm('invoice.director'):
        state = 4
    else:
        pass
    try:
        invoice = Invoice.objects.get(slug=slug)
        items = Item.objects.filter(invoice=invoice)
        comments = Comment.objects.filter(invoice=invoice).order_by('-date_created')
        pass
    except:
        messages.warning(request, 'توجيه باستخدام رابط غير صحيح، تواصل مع مطور المنظومة!')
        return render(request, 'invoice/summary-invoice.html', context)
    context = {}
    context['invoice_list'] = Invoice.objects.filter(number__isnull=False, current_state=state).order_by('-last_updated')
    context['invoice_hold_list'] = Invoice.objects.filter(number__isnull=False).exclude(current_state=state).order_by('-last_updated')
    context['invoice'] = invoice
    context['items'] = items
    context['comments'] = comments
    context['items_count'] = items.count()
    if items.aggregate(total=Sum('total_price'))['total']:
        total = np.round(float(items.aggregate(total=Sum('total_price'))['total']), decimals=4)
        tax = np.round(np.multiply(total, 0.14), decimals=4)
        context['items_total'] = total
        context['items_tax'] = tax
        context['items_inv'] = np.round(np.add(total, tax), decimals=4)
    if request.method == 'GET' and invoice.current_state == 2 and request.user.has_perm('invoice.security'):
        comment_form  = AddCommentForm(request.POST)
        context['comment_form'] = comment_form
        return render(request, 'invoice/approve-invoice.html', context)
    elif request.method == 'GET' and invoice.current_state == 3 and request.user.has_perm('invoice.finance'):
        comment_form  = AddCommentForm(request.POST)
        context['comment_form'] = comment_form
        return render(request, 'invoice/approve-invoice.html', context)
    elif request.method == 'GET' and invoice.current_state == 4 and request.user.has_perm('invoice.director'):
        comment_form  = AddCommentForm(request.POST)
        context['comment_form'] = comment_form
        return render(request, 'invoice/approve-invoice.html', context)
    elif request.method == 'POST' and invoice.current_state == 2 and request.user.has_perm('invoice.security'):
        comment_form  = AddCommentForm(request.POST)
        if comment_form.is_valid() and request.POST['decision'] == '1':
            comment = comment_form.save(commit=False)
            comment.invoice = invoice
            comment.entryPerson = request.user.get_full_name()
            invoice.current_state = 1
            comment.save()
            invoice.save()
            messages.success(request, "تم إعادة الفاتورة لقسم المشتريات بنجاح!")
            return render(request, 'invoice/summary-invoice.html', context)
        elif comment_form.is_valid() and request.POST['decision'] == '3':
            comment = comment_form.save(commit=False)
            comment.invoice = invoice
            comment.entryPerson = request.user.get_full_name()
            invoice.current_state = 3
            comment.save()
            invoice.save()
            messages.success(request, "تم اعتماد الفاتورة وإرسالها لقسم الماليات بنجاح!")
            return render(request, 'invoice/summary-invoice.html', context)
    elif request.method == 'POST' and invoice.current_state == 3 and request.user.has_perm('invoice.finance'):
        comment_form  = AddCommentForm(request.POST)
        if comment_form.is_valid() and request.POST['decision'] == '1':
            comment = comment_form.save(commit=False)
            comment.invoice = invoice
            comment.entryPerson = request.user.get_full_name()
            invoice.current_state = 1
            comment.save()
            invoice.save()
            messages.success(request, "تم إعادة الفاتورة لقسم المشتريات بنجاح!")
            return render(request, 'invoice/summary-invoice.html', context)
        elif comment_form.is_valid() and request.POST['decision'] == '4':
            comment = comment_form.save(commit=False)
            comment.invoice = invoice
            comment.entryPerson = request.user.get_full_name()
            invoice.current_state = 4
            comment.save()
            invoice.save()
            messages.success(request, "تم اعتماد الفاتورة وإرسالها لقائد المستشفى بنجاح!")
            return render(request, 'invoice/summary-invoice.html', context)
    elif request.method == 'POST' and invoice.current_state == 4 and request.user.has_perm('invoice.director'):
        comment_form  = AddCommentForm(request.POST)
        if comment_form.is_valid() and request.POST['decision'] == '1':
            comment = comment_form.save(commit=False)
            comment.invoice = invoice
            comment.entryPerson = request.user.get_full_name()
            invoice.current_state = 1
            comment.save()
            invoice.save()
            messages.success(request, "تم إعادة الفاتورة لقسم المشتريات بنجاح!")
            return render(request, 'invoice/summary-invoice.html', context)
        elif comment_form.is_valid() and request.POST['decision'] == '5':
            comment = comment_form.save(commit=False)
            comment.invoice = invoice
            comment.entryPerson = request.user.get_full_name()
            invoice.current_state = 5
            comment.save()
            invoice.save()
            messages.success(request, "تم اعتماد الفاتورة وإرسالها للأرشيف بنجاح!")
            return render(request, 'invoice/summary-invoice.html', context)
        
    return render(request, 'invoice/summary-invoice.html', context)

def get_contact(request, slug, req):
    context = {}
    context['department_list'] = Department.objects.all()
    context['contact_req'] = req
    num = ''.join(filter(lambda i: i.isdigit(), req))
    star = (request.path).rsplit('/')[3]
    if req[0] == 's':
        form = Contact.objects.filter(id=num)
        if form[0].msg_flag:
            form.update(msg_flag=False)
        else:
            form.update(msg_flag=True)
        return HttpResponseRedirect('all')
    if slug == 'suggest':
        context['contact_type'] = "المقترحات"
        context['contact_slug'] = "suggest"
        if req[0] == 'd':
            context['contact_department'] = "آخر {} يوم".format(num)
            context['contact_list'] = Contact.objects.filter(msg_type='suggest', msg_created__gte=datetime.datetime.now()-datetime.timedelta(days=int(num)))
        elif num and req[0] != 's':
            context['contact_list'] = Contact.objects.filter(msg_type='suggest', department=num)
            context['contact_department'] = Department.objects.get(id=num)
        else:
            context['contact_list'] = Contact.objects.filter(msg_type='suggest')
    elif slug == 'complain':
        context['contact_type'] = "الشكاوى"
        context['contact_slug'] = "complain"
        context['contact_list'] = Contact.objects.filter(msg_type='complain')
        if req[0] == 'd':
            context['contact_department'] = "آخر {} يوم".format(num)
            context['contact_list'] = Contact.objects.filter(msg_type='complain', msg_created__gte=datetime.datetime.now()-datetime.timedelta(days=int(num)))
        elif num:
            context['contact_list'] = Contact.objects.filter(msg_type='complain', department=num)
            context['contact_department'] = Department.objects.get(id=num)
        else:
            context['contact_list'] = Contact.objects.filter(msg_type='complain')
    elif slug == 'star':
        context['contact_type'] = "النماذج المميزة"
        context['contact_slug'] = "star"
        context['contact_list'] = Contact.objects.order_by('msg_created').reverse().filter(msg_flag=True)
    return render(request, 'invoice/list-contact.html', context)

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