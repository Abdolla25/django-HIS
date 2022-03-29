from django.contrib import admin

# Register your models here.

from .models import Person, Company, Invoice, Item, Department

# class ChoiceInline(admin.StackedInline):
# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 1
    

# class QuestionAdmin(admin.ModelAdmin):
#     # fields = ['pub_date', 'question_text']
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date']}),
#     ]
#     inlines = [ChoiceInline]
#     list_display = ('question_text', 'pub_date', 'was_published_recently')
#     list_filter = ['pub_date', 'question_text']
#     search_fields = ['question_text']

class ItemInline(admin.TabularInline):
    model = Item
    extra = 1

class InvoiceAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
    list_display = ['number', 'purchase_date', 'isFinanceAuth', 'isDirectorAuth', 'company', 'entryPerson']
    list_filter = ['company', 'entryPerson', 'isFinanceAuth', 'isDirectorAuth']
    search_fields = ['number', 'company', 'entryPerson']

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Person, list_display=['name', 'militaryNumber'])
admin.site.register(Company, list_display=['name', 'commercialRegister'])
admin.site.register(Department, list_display=['name', 'head'])