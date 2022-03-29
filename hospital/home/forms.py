from dataclasses import field
from django.forms import ModelForm

from .models import Contact
# from invoices.models import Department

class ContactForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['department'].widget.attrs.update({'class': 'form-select form-select-lg'})
        self.fields['msg_type'].widget.attrs.update({'class': 'form-select form-select-lg'})
        self.fields['msg_text'].widget.attrs.update({'class': 'form-control form-control-lg', 'rows': 2})

    class Meta:
        model = Contact
        fields = '__all__'
        # fields = ['name', 'department', 'msg_type', 'msg_text']

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