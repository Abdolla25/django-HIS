from tokenize import Name
from unicodedata import name
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader

from apps.invoice.forms import AddCategoryForm, AddCompanyForm, AddDepartmentForm, AddInvoiceForm

from django.contrib import messages

from apps.invoice.models import Category, Company, Department

# Create your views here.
def retrieveData(request, model, dataID):
    context = {}
    targetModel = model
    targetID = dataID
    if (targetModel == 'company'):
        context['company_data'] = Company.objects.get(id=targetID)
    elif (targetModel == 'category'):
        context['category_data'] = Category.objects.get(id=targetID)
    elif (targetModel == 'department'):
        context['department_data'] = Department.objects.get(id=targetID)
    html_template = loader.get_template('invoice/edit-{}.html'.format(targetModel))
    return HttpResponse(html_template.render(context, request))

def editData(request, model, dataID):
    targetModel = model
    targetID = dataID
    AddForms = {'company': AddCompanyForm, 'category': AddCategoryForm, 'department': AddDepartmentForm}
    if request.method == 'POST':
        form = AddForms[model](request.POST)
        try:
            if (targetModel == 'company'):
                Company.objects.filter(id=targetID).update(name=form['name'].value())
                Company.objects.filter(id=targetID).update(commercialRegister=form['commercialRegister'].value())
                messages.success(request, 'تم تعديل البيانات بنجاح!')
            elif (targetModel == 'category'):
                Category.objects.filter(id=targetID).update(name=form['name'].value())
                messages.success(request, 'تم تعديل البيانات بنجاح!')
            elif (targetModel == 'department'):
                Department.objects.filter(id=targetID).update(name=form['name'].value())
                messages.success(request, 'تم تعديل البيانات بنجاح!')
        except:
            messages.warning(request, 'لم يتم تعديل البيانات، يرجى مراجعة نوع وقيمة البيانات المدخلة!')
        # if a GET (or any other method) we'll create a blank form
    else:
        messages.warning(request, 'لم يتم تعديل البيانات، يرجى مراجعة نوع وقيمة البيانات المدخلة!')
    return HttpResponseRedirect('/retrieve/{}/{}/'.format(targetModel, targetID))

def addData(request, model):
    AddForms = {'company': AddCompanyForm, 'category': AddCategoryForm, 'department': AddDepartmentForm, 'invoice': AddInvoiceForm}
    if request.method == 'POST':
        form = AddForms[model](request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إضافة البيانات بنجاح!')
        else:
            messages.warning(request, 'لم يتم إضافة البيانات، يرجى مراجعة نوع وقيمة البيانات المدخلة!')
        # if a GET (or any other method) we'll create a blank form
    else:
        messages.warning(request, 'لم يتم إضافة البيانات، يرجى مراجعة نوع وقيمة البيانات المدخلة!')
    return HttpResponseRedirect('/add-{}.html#'.format(model))
