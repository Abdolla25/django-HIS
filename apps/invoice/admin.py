from django.contrib import admin

# Register your models here.

from .models import Company, Category, Department, Invoice, Item

admin.site.register(Company)
admin.site.register(Category)
admin.site.register(Department)
admin.site.register(Item)

# class ChoiceInline(admin.StackedInline):
class ItemInline(admin.TabularInline):
    model = Item
    extra = 1
    
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [ItemInline]

admin.site.register(Invoice, InvoiceAdmin)

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

# class ItemInline(admin.TabularInline):
#     model = Item
#     extra = 1

# class InvoiceAdmin(admin.ModelAdmin):
#     inlines = [ItemInline]
#     list_display = ['number', 'purchase_date', 'current_state', 'company', 'entryPerson']
#     list_filter = ['company', 'entryPerson', 'current_state']
#     search_fields = ['number', 'company', 'entryPerson']

# admin.site.register(Invoice, InvoiceAdmin)
# admin.site.register(Company, list_display=['name', 'commercialRegister'])
# admin.site.register(Department, list_display=['name', 'head'])
# admin.site.register(Item)