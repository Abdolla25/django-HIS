from dataclasses import field
from django.forms import ModelForm

from .models import Category, Company, Department, Invoice, Item

class AddCompanyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddCompanyForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['commercialRegister'].widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = Company
        fields = '__all__'

class AddCategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddCategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = Category
        fields = '__all__'

class AddDepartmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddDepartmentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = Department
        fields = '__all__'

class AddInvoiceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddInvoiceForm, self).__init__(*args, **kwargs)
        self.fields['company'].widget.attrs.update({'class': 'form-control', 'required': ''})
        self.fields['number'].widget.attrs.update({'class': 'form-control', 'required': ''})
        self.fields['purchase_date'].widget.attrs.update({'class': 'form-control w-75 vDateField', 'onkeydown': 'event.preventDefault()', 'placeholder': 'اضغط رمز التقويم لإدخال التاريخ...', 'required': '', 'style': 'pointer-events: none;'})
        self.fields['category'].widget.attrs.update({'class': 'form-control', 'required': ''})
        self.fields['department'].widget.attrs.update({'class': 'form-control', 'required': ''})
        self.fields['entryPerson'].widget.attrs.update({'class': 'form-control', 'readonly': '', 'required': ''})
    
    class Meta:
        model = Invoice
        fields = '__all__'

class AddItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddItemForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = Item
        fields = '__all__'

# class ContactForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super(ContactForm, self).__init__(*args, **kwargs)
#         self.fields['name'].widget.attrs.update({'class': 'form-control form-control-lg'})
#         self.fields['department'].widget.attrs.update({'class': 'form-select form-select-lg'})
#         self.fields['form_type'].widget.attrs.update({'class': 'form-select form-select-lg'})
#         self.fields['details'].widget.attrs.update({'class': 'form-control form-control-lg'})

#     name = forms.CharField(label='الاسم', max_length=80, required=False)
#     department = forms.ModelChoiceField(label='القسم', queryset=Department.objects.all())
#     form_type = forms.ChoiceField(label='نوع الرسالة', choices=(('suggest', 'مقترح'), ('complian', 'شكوى')))
#     details = forms.CharField(label='تفاصيل', widget=forms.Textarea)