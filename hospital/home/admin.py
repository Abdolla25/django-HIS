from re import search
from django.contrib import admin

# Register your models here.

from .models import Menu, SubMenu, Carousel, MainIcon, Featurette, Contact, Page

# list_display = [field.name for field in Page._meta.get_fields()]

class SubInline(admin.TabularInline):
    model = SubMenu
    extra = 1

class MenuAdmin(admin.ModelAdmin):
    inlines = [SubInline]
    list_display = ['page_name', 'page_url', 'priority', 'has_sub', 'created', 'modified']
    search_fields = ['page_name', 'page_url']

class CarouselAdmin(admin.ModelAdmin):
    list_display = ['caption', 'text', 'img_src', 'btn_text', 'btn_url', 'priority', 'created', 'modified']
    search_fields = ['caption']

class MainIconAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'icon_class', 'btn_text', 'btn_url', 'priority', 'created', 'modified']
    search_fields = ['title']

class FeaturetteAdmin(admin.ModelAdmin):
    list_display = ['title', 'muted_title', 'text', 'style', 'img_src', 'priority', 'created', 'modified']
    search_fields = ['title']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'msg_type', 'msg_text', 'msg_created', 'msg_modified']
    list_filter = ['department', 'msg_type']
    search_fields = ['name', 'msg_text']

class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']
    search_fields = ['title', 'url']

admin.site.register(Menu, MenuAdmin)
admin.site.register(Carousel, CarouselAdmin)
admin.site.register(MainIcon, MainIconAdmin)
admin.site.register(Featurette, FeaturetteAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Page, PageAdmin)