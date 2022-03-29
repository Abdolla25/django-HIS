from operator import mod
from tkinter import CASCADE
from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name='اسم الشركة')
    commercialRegister = models.IntegerField(unique=True, verbose_name='رقم السجل التجاري')

    def __str__(self) -> str:
        return 'شركة %s مسجلة برقم: %s' % (self.name, self.commercialRegister)

    class Meta:
        verbose_name = 'شركة'
        verbose_name_plural = 'شركات'

class Person(models.Model):
    name = models.CharField(max_length=200, verbose_name='الاسم')
    militaryNumber = models.IntegerField(unique=True, verbose_name='الرقم العسكري')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'فرد'
        verbose_name_plural = 'أفراد'

class Invoice(models.Model):
    number = models.IntegerField(verbose_name='رقم الفاتورة')
    purchase_date = models.DateField(verbose_name='تاريخ الشراء')
    AUTHORIZATION = (
        ('H', 'HOLD'),
        ('A', 'ACCEPTED'),
        ('R', 'REJECTED')
    )
    isFinanceAuth = models.CharField(verbose_name='تصديق الماليات؟', max_length=1, choices=AUTHORIZATION, default='H')
    isDirectorAuth = models.CharField(verbose_name='تصديق المدير؟', max_length=1, choices=AUTHORIZATION, default='H')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='اسم الشركة')
    entryPerson = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='إدخال البيانات')

    def __str__(self) -> str:
        return '%s | #فاتورة %s' % (self.company, self.number)

    class Meta:
        verbose_name = 'فاتورة'
        verbose_name_plural = 'فواتير'

class Department(models.Model):
    name = models.CharField(max_length=200, verbose_name='اسم القسم')
    head = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='رئيس القسم')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'قسم'
        verbose_name_plural = 'أقسام'

class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name='اسم العنصر')
    quantity = models.SmallIntegerField(verbose_name='الكمية المضافة')
    price = models.FloatField(verbose_name='سعر الوحدة')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='القسم التابع له')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name='مضاف للفاتورة')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'عنصر'
        verbose_name_plural = 'عناصر'





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