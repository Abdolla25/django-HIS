from datetime import datetime
from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField

# Create your models here.

# models.DateTimeField(auto_now=True)

class Page(models.Model):
    title = models.CharField(verbose_name='عنوان الصفحة', max_length=120)
    content = HTMLField(verbose_name='محتوى الصفحة')
    pure_html = models.TextField(verbose_name='كود HTML', blank=True)
    url = models.SlugField(verbose_name='رابط الصفحة', unique=True)

    def __str__(self) -> str:
        return '/%s/' % self.url

    class Meta:
        verbose_name = 'صفحة'
        verbose_name_plural = 'صفحات'

class Menu(models.Model):
    page_name = models.CharField(max_length=80, verbose_name='الصفحة')
    page_url = models.ForeignKey(Page, on_delete=models.CASCADE, verbose_name='رابط الصفحة')
    priority = models.PositiveSmallIntegerField(verbose_name='الترتيب', default=0)
    has_sub = models.BooleanField(verbose_name='زر قائمة فرعية؟', default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='توقيت الإنشاء')
    modified = models.DateTimeField(auto_now=True, verbose_name='آخر تعديل')

    def __str__(self) -> str:
        return "الصفحة: '%s'" % (self.page_name)

    class Meta:
        verbose_name = 'قائمة'
        verbose_name_plural = 'قوائم'

class SubMenu(models.Model):
    sub_page_name = models.CharField(max_length=80, verbose_name='الصفحة الفرعية')
    sub_page_url = models.ForeignKey(Page, on_delete=models.CASCADE, verbose_name='رابط الصفحة الفرعية')
    parent = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name='تابع لـ')
    priority = models.PositiveSmallIntegerField(verbose_name='الترتيب الفرعي', default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name='توقيت الإنشاء')
    modified = models.DateTimeField(auto_now=True, verbose_name='آخر تعديل')

    def __str__(self) -> str:
        return "الصفحة الفرعية: '%s'" % (self.sub_page_name)

    class Meta:
        verbose_name = 'قائمة فرعية'
        verbose_name_plural = 'قوائم فرعية'

class Carousel(models.Model):
    caption = models.CharField(max_length=200, verbose_name='عنوان الشريحة')
    text = models.TextField(verbose_name='النص الفرعي')
    img_src = models.CharField(max_length=80, default='home/img/carousel/', verbose_name='رابط الصورة')
    btn_text = models.CharField(max_length=80, default='no-button', verbose_name='زر الضغط')
    btn_url = models.ForeignKey(Page, on_delete=models.CASCADE, verbose_name='رابط زر الضغط')
    priority = models.PositiveSmallIntegerField(verbose_name='الترتيب', default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name='توقيت الإنشاء')
    modified = models.DateTimeField(auto_now=True, verbose_name='آخر تعديل')

    def __str__(self) -> str:
        return "شريحة عرض: '%s' | نص فرعي: '%s'" % (self.caption, self.text)

    class Meta:
        verbose_name = 'شريحة عرض'
        verbose_name_plural = 'شرائح العرض'

class MainIcon(models.Model):
    title = models.CharField(max_length=80, verbose_name='عنوان الأيقونة')
    text = models.TextField(verbose_name='النص الفرعي')
    icon_class = models.CharField(max_length=80, verbose_name='FontAwesome Class')
    btn_text = models.CharField(max_length=80, default='no-button', verbose_name='زر الضغط')
    btn_url = models.ForeignKey(Page, on_delete=models.CASCADE, verbose_name='رابط زر الضغط')
    priority = models.PositiveSmallIntegerField(verbose_name='الترتيب', default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name='توقيت الإنشاء')
    modified = models.DateTimeField(auto_now=True, verbose_name='آخر تعديل')

    def __str__(self) -> str:
        return "أيقونة: '%s'" % (self.title)

    class Meta:
        verbose_name = 'أيقونة'
        verbose_name_plural = 'أيقونات'

class Featurette(models.Model):
    title = models.CharField(max_length=80, verbose_name='عنوان الموضوع')
    muted_title = models.CharField(max_length=80, verbose_name='كلمة مميزة')
    text = models.TextField(verbose_name='النص الفرعي')
    style = models.CharField(verbose_name='تنسيق العرض', max_length=1, choices=(('R', 'يمين'), ('L', 'يسار')))
    img_src = models.CharField(max_length=80, default='home/img/featurette/', verbose_name='رابط الصورة')
    priority = models.PositiveSmallIntegerField(verbose_name='الترتيب', default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name='توقيت الإنشاء')
    modified = models.DateTimeField(auto_now=True, verbose_name='آخر تعديل')

    def __str__(self) -> str:
        return "الموضوع: '%s'" % (self.title)

    class Meta:
        verbose_name = 'موضوع متميز'
        verbose_name_plural = 'موضوعات متميزة'

class Contact(models.Model):
    name = models.CharField(verbose_name='الاسم', blank=True, max_length=80)
    department = models.ForeignKey("invoices.Department", verbose_name="القسم", on_delete=models.CASCADE)
    msg_type = models.CharField(verbose_name='نوع الرسالة', max_length=8, choices=(('suggest', 'مقترح'), ('complain', 'شكوى')))
    msg_text = models.TextField(verbose_name='الرسالة')
    msg_created = models.DateTimeField(auto_now_add=True, verbose_name='توقيت الإنشاء')
    msg_modified = models.DateTimeField(auto_now=True, verbose_name='آخر تعديل')

    def __str__(self) -> str:
        if self.name:
            str_msg = "نموذج باسم: '%s'" % (self.name)
        else:
            str_msg = 'نموذج بدون اسم'
        return str_msg

    class Meta:
        verbose_name = 'نموذج تواصل'
        verbose_name_plural = 'نماذج التواصل'

# class NEW_MODEL(models.Model):
#     name = models.CharField(verbose_name='الاسم', blank=True, max_length=80)

#     def __str__(self) -> str:
#         return 'Something %s bla %s blas' % (arg1, arg2)

#     class Meta:
#         verbose_name = 'نموذج تواصل'
#         verbose_name_plural = 'نماذج التواصل'