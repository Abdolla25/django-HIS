from operator import mod
from tkinter import CASCADE
from uuid import uuid4
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.contrib import admin

# Create your models here.

class Company(models.Model):
    # Basic Fields
    name = models.CharField(null=True, blank=True, max_length=200, verbose_name='اسم الشركة')
    commercialRegister = models.IntegerField(null=True, blank=True, unique=True, verbose_name='رقم السجل التجاري')
    # Utility Fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    def __str__(self) -> str:
        return '%s | رقم السجل التجاري: %s' % (self.name, self.commercialRegister)
    
    def get_absolute_url(self):
        return reverse('company-detail', kwargs={'slug': self.slug})
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {} {}'.format(self.name, self.commercialRegister, self.uniqueId))
        self.slug = slugify('{} {} {}'.format(self.name, self.commercialRegister, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())
        super(Company, self).save(*args, **kwargs)
    class Meta:
        verbose_name = 'شركة'
        verbose_name_plural = 'شركات'


class Category(models.Model):
    # Basic Fields
    name = models.CharField(null=True, blank=True, max_length=200, verbose_name='تصنيف')
    # Utility Fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    def __str__(self) -> str:
        return self.name
    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'slug': self.slug})
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.name, self.uniqueId))
        self.slug = slugify('{} {}'.format(self.name, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())
        super(Category, self).save(*args, **kwargs)
    class Meta:
        verbose_name = 'تصنيف'
        verbose_name_plural = 'تصنيفات'
        

class Department(models.Model):
    # Basic Fields
    name = models.CharField(null=True, blank=True, max_length=200, verbose_name='قسم')
    # Utility Fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    def __str__(self) -> str:
        return self.name
    def get_absolute_url(self):
        return reverse('department-detail', kwargs={'slug': self.slug})
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.name, self.uniqueId))
        self.slug = slugify('{} {}'.format(self.name, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())
        super(Department, self).save(*args, **kwargs)
    class Meta:
        verbose_name = 'قسم'
        verbose_name_plural = 'أقسام'


class Invoice(models.Model):
    STATE = (
        ('A', 'في المشتريات'),
        ('B', 'في الأمن'),
        ('C', 'في الماليات'),
        ('D', 'في الإدارة'),
        ('F', 'منتهية')
    )
    # Basic Fields
    number = models.CharField(null=True, blank=True, max_length=100, verbose_name='رقم الفاتورة')
    entryPerson = models.CharField(null=True, blank=True, max_length=100, verbose_name='إدخال البيانات')
    purchase_date = models.DateField(null=True, blank=True, verbose_name='تاريخ الشراء')
    current_state = models.CharField(null=True, blank=True, verbose_name='حالة الفاتورة الحالية', max_length=1, choices=STATE, default='A')
    # Related Fields
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.PROTECT, verbose_name='اسم الشركة')
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.PROTECT, verbose_name='موجه للقسم')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.PROTECT, verbose_name='تصنيف الفاتورة')
    # Utility Fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100, default=None)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True, default=None)
    last_updated = models.DateTimeField(blank=True, null=True, default=None)
    def __str__(self) -> str:
        return '%s | #فاتورة %s' % (self.company, self.number)
    def get_absolute_url(self):
        return reverse('invoice-detail', kwargs={'slug': self.slug})
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{}'.format(self.uniqueId))
        self.slug = slugify('{}'.format(self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())
        super(Invoice, self).save(*args, **kwargs)
    class Meta:
        unique_together = ['number', 'company']
        permissions = [
            ("it", "نظم المعلومات"),
            ("purchase", "مكتب المشتريات"),
            ("finance", "الماليات"),
            ("director", "المدير"),
            ("security", "الأمن"),
        ]
        verbose_name = 'فاتورة'
        verbose_name_plural = 'فواتير'


class Item(models.Model):
    # Basic Fields
    name = models.CharField(max_length=200, verbose_name='صنف')
    description = models.CharField(null=True, blank=True, max_length=200, verbose_name='وصف')
    quantity = models.FloatField(verbose_name='الكمية')
    price = models.FloatField(verbose_name='سعر الوحدة')
    # Related Fields
    invoice = models.ForeignKey(Invoice, blank=True, null=True, on_delete=models.CASCADE, verbose_name='الفاتورة')
    # Utility Fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True)
    def __str__(self) -> str:
        return self.name
    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'slug': self.slug})
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.name, self.uniqueId))
        self.slug = slugify('{} {}'.format(self.name, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())
        self.total_price = self.quantity * self.price
        super(Item, self).save(*args, **kwargs)
    class Meta:
        verbose_name = 'صنف'
        verbose_name_plural = 'أصناف'


class Comment(models.Model):
    # Basic Fields
    detail = models.CharField(null=True, blank=True, max_length=200, verbose_name='ملاحظة')
    entryPerson = models.CharField(null=True, blank=True, max_length=100, verbose_name='إدخال البيانات')
    # Utility Fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    date_created = models.DateTimeField(blank=True, null=True)
    def __str__(self) -> str:
        return self.name
    def get_absolute_url(self):
        return reverse('comment-detail', kwargs={'id': self.uniqueId})
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
        super(Comment, self).save(*args, **kwargs)
    class Meta:
        verbose_name = 'ملاحظة'
        verbose_name_plural = 'ملاحظات'

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