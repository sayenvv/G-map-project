from pyexpat import model
from django.contrib.auth.models import Group
from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget
from django.forms import inlineformset_factory



class RolesForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("__all__")

    def __init__(self, *args, **kwargs):
        super(RolesForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control form-control-sm'})
    
    

    @receiver(post_save, sender=Group)
    def save_slug(sender, *args, **kwargs):
        print(sender,"ssss")
        instance = Group.objects.filter(pk=kwargs['instance'].id)
        value = str(instance.first().name)+" "+str(instance.first().id)
        slug_field = slugify(value, allow_unicode=True)
        instance.update(slug_field=slug_field)

class Service_TypeForm(forms.ModelForm):
    class Meta:
        model = Service_Type_Model
        fields = ("__all__")

    def __init__(self, *args, **kwargs):
        super(Service_TypeForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control form-control-sm'})
        self.fields['scope_of_work'].widget = CKEditorWidget() 

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department_Model
        fields = ("__all__")

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control form-control-sm'})

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation_Model
        fields = ("__all__")

    def __init__(self, *args, **kwargs):
        super(DesignationForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control form-control-sm'})

class AssignDepartmentForm(forms.ModelForm):
    class Meta:
        model = Designation_Model
        fields = ("designation","department")

    def __init__(self, *args, **kwargs):
        super(AssignDepartmentForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control form-control-sm'})

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor_Model
        fields = ("__all__")

    def __init__(self, *args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control form-control-sm'})


class QuestionnairForm(forms.ModelForm):
    class Meta:
        model = Questionnair_Model
        fields = ("__all__")

    def __init__(self, *args, **kwargs):
        super(QuestionnairForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control form-control-sm'})

class DionamicQuestionForm(forms.ModelForm):
    class Meta:
        model = Questionnair_Model
        fields = ("question",)

    def __init__(self, *args, **kwargs):
        super(DionamicQuestionForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control form-control-sm'})

