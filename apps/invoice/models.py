from operator import mod
from tkinter import CASCADE
from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name='اسم الشركة')
    commercialRegister = models.IntegerField(unique=True, verbose_name='رقم السجل التجاري')

    def __str__(self) -> str:
        return '%s | رقم السجل التجاري: %s' % (self.name, self.commercialRegister)

    class Meta:
        verbose_name = 'شركة'
        verbose_name_plural = 'شركات'

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='تصنيف')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'تصنيف'
        verbose_name_plural = 'تصنيفات'
        
class Department(models.Model):
    name = models.CharField(max_length=200, verbose_name='قسم')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'قسم'
        verbose_name_plural = 'أقسام'

class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name='صنف')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='تصنيف الصنف')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'صنف'
        verbose_name_plural = 'أصناف'

class Invoice(models.Model):
    number = models.IntegerField(verbose_name='رقم الفاتورة')
    purchase_date = models.DateField(verbose_name='تاريخ الشراء')
    STATE = (
        ('A', 'في المشتريات'),
        ('B', 'في الأمن'),
        ('C', 'في الماليات'),
        ('D', 'في الإدارة')
    )
    current_state = models.CharField(verbose_name='حالة الفاتورة الحالية', max_length=1, choices=STATE, default='A')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='اسم الشركة')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name='موجه للقسم')
    entryPerson = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='إدخال البيانات')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='تصنيف الفاتورة')

    def __str__(self) -> str:
        return '%s | #فاتورة %s' % (self.company, self.number)

    class Meta:
        verbose_name = 'فاتورة'
        verbose_name_plural = 'فواتير'

class Purchase(models.Model):
    quantity = models.SmallIntegerField(verbose_name='الكمية المضافة')
    price = models.FloatField(verbose_name='سعر الوحدة')
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, verbose_name='صنف')
    invoice = models.ForeignKey(Invoice, on_delete=models.DO_NOTHING, verbose_name='فاتورة')

    def __str__(self) -> str:
        return '{} | عدد: {}'.format(self.item, self.quantity)

    class Meta:
        verbose_name = 'عملية شراء'
        verbose_name_plural = 'عمليات شراء'


# # For Reference ...
# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date =  models.DateTimeField('date published')
    
#     def __str__(self) -> str:
#         return self.question_text

#     @admin.display(
#         boolean=True,
#         ordering='pub_date',
#         description='Published recently?',
#     )
#     def was_published_recently(self):
#         return timezone.now() - datetime.timedelta(days=1) <= self.pub_date <= timezone.now()
        
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)

#     def __str__(self) -> str:
#         return self.choice_text