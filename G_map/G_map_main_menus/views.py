from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.views.generic import View
from .forms import *
from django.utils.decorators import method_decorator
from G_map.decorator import has_permission
from django.contrib import messages
from .utils import Django_messages_Main
from django.views.generic.edit import UpdateView

# Create your views here.
class index_menu(View):
    template_name = 'menus_page.html'

    def get(self,request):
        return render(request,self.template_name)


class dashboard(View):
    template_name = 'dashboard.html'

    def get(self,request):
        return render(request,self.template_name)

class Roles_View(View):
    template_name = 'roles/roles_page.html'
    redirect_url = 'roles_view'
    form_class = RolesForm

    def get(self,request):
        forms = self.form_class()
        data = Group.objects.all()
        return render(request,self.template_name,context={
            'form' : forms,
            'data' : data
            })

    def post(self,request):
        forms = self.form_class(request.POST)
        if(forms.is_valid()):
            forms.save()
            return redirect(self.redirect_url)
        return render(request,self.template_name,context={'form' : forms})

class EditRoles_View(View):
    template_name = 'roles/edit_roles.html'
    redirect_url = 'roles_view'
    form_class = RolesForm

    @method_decorator(has_permission(permission='auth.add_group'))
    def get(self,request,*args,**kwargs):
        form = self.form_class
        pk = kwargs.get('slug')
        return render(request,self.template_name,context={
            'form' : form(initial={
                'name' : Group.objects.filter(slug_field=pk).first().name,
                'status' : Group.objects.filter(slug_field=pk).first().status,
            })
        })

    def post(self,request,**kwargs):
        pk = kwargs.get('slug')
        form_class =self.form_class(request.POST,instance=Group.objects.filter(slug_field=pk).first())
        if(form_class.is_valid()):
            form_class.save()
            return redirect(self.redirect_url)
        return render(request,self.template_name,context={
            'form' : form_class(initial={
                'name' : Group.objects.filter(slug_field=pk).first().name,
                'status' : Group.objects.filter(slug_field=pk).first().status,
            })
        })

class RolesAction_View(View):
    redirect_url = 'roles_view'

    def post(self,request):
        data_id = request.POST.get('disable_data',None)
        Roles_data = Group.objects.filter(id=data_id)
        if(Roles_data.first().status == 'Active'):
            Roles_data.update(status='Inactive')
            messages.success(request,Django_messages_Main['roles_disabled'])
            return redirect(self.redirect_url)
        else:
            Roles_data.update(status='Active')
            messages.success(request,Django_messages_Main['roles_enabled'])
            return redirect(self.redirect_url)

class Service_TypeView(View):
    template_name = 'service_type/service_type.html'
    model_class = Service_Type_Model
    def get(self,request):
        print(self.model_class.objects.filter(id=1).values())
        data = self.model_class.objects.all()
        return render(request,self.template_name,locals())
    

class AddService_TypeView(View):
    template_name = 'service_type/add_servicetype.html'
    form_class = Service_TypeForm
    redirect_url = 'service_type'

    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,locals())

    def post(self,request):
        form = self.form_class(request.POST)
        print(form)
        if(form.is_valid()):
            form.save()
            messages.success(request,Django_messages_Main['service_added'])
            return redirect(self.redirect_url)
        return render(request,self.template_name)

class EditService_TypeView(View):

    template_name = 'service_type/edit_servicetype.html'
    form_class = Service_TypeForm
    redirect_url = 'service_type'
    model_class = Service_Type_Model

    def get(self,request,*args,**kwargs):
        pk = kwargs.get('slug')

        form = self.form_class(initial={
            'service' : self.model_class.objects.filter(slug_field=pk).first().service,
            'status' : self.model_class.objects.filter(slug_field=pk).first().status,
            'scope_of_work' : self.model_class.objects.filter(slug_field=pk).first().scope_of_work,
        })
        return render(request,self.template_name,locals())
    
    def post(self,request,*args,**kwargs):
        pk = kwargs.get('slug')
        form = self.form_class(request.POST,instance=Service_Type_Model.objects.filter(slug_field=pk).first())
        if(form.is_valid()):
            form.save()
            messages.success(request,Django_messages_Main['service_edited'])
            return redirect(self.redirect_url)
        
        return render(request,self.template_name,locals())


class ViewService_TypeView(View):
    model_class = Service_Type_Model
    template_name = 'service_type/view_servicetype.html'

    def get(self,request,*args,**kwargs):
        pk = kwargs.get('slug')
        service = self.model_class.objects.filter(slug_field=pk).first().service
        status = self.model_class.objects.filter(slug_field=pk).first().status
        scope_of_work = self.model_class.objects.filter(slug_field=pk).first().scope_of_work
        return render(request,self.template_name,locals())

  

class ServiceTypeAction_View(View):

    model_class = Service_Type_Model
    redirect_url = 'service_type'

    def post(self,request):
        data_id = request.POST.get('disable_data',None)
        Service_data = self.model_class.objects.filter(id=data_id)
        if(Service_data.first().status == 'Active'):
            Service_data.update(status='Inactive')
            messages.success(request,Django_messages_Main['service_disabled'])
            return redirect(self.redirect_url)
        else:
            Service_data.update(status='Active')
            messages.success(request,Django_messages_Main['service_enabled'])
            return redirect(self.redirect_url)

class DepartmentView(View):

    template_name = 'department/department_page.html'
    model_class = Department_Model
    def get(self,request):
        data = self.model_class.objects.all()
        return render(request,self.template_name,locals())

class Add_DepartmentView(View):
    template_name = 'department/add_departmentpage.html'
    form_class = DepartmentForm
    redirect_url = 'department'

    def get(self,request):
        form =self.form_class()
        return render(request,self.template_name,locals())

    def post(self,request):
        form = self.form_class(request.POST)
        if(form.is_valid()):
            form.save()
            messages.success(request,Django_messages_Main['department_added'])
            return redirect(self.redirect_url)
        return render(request,self.template_name,locals())

class Edit_DepartmentView(View):
    template_name = 'department/edit_departmentpage.html'
    form_class = DepartmentForm
    redirect_url = 'department'
    model_class = Department_Model

    def get(self,request,**kwargs):
        slug = kwargs.get('slug')
        form =self.form_class(initial={
            'department_name' : self.model_class.objects.filter(slug_field=slug).first().department_name,
            'service_type' : self.model_class.objects.filter(slug_field=slug).first().service_type,
            'status' : self.model_class.objects.filter(slug_field=slug).first().status,
        })
        return render(request,self.template_name,locals())

    def post(self,request,**kwargs):
        slug = kwargs.get('slug')
        form = self.form_class(request.POST,instance=self.model_class.objects.filter(slug_field=slug).first())
        if(form.is_valid()):
            form.save()
            messages.success(request,Django_messages_Main['department_edited'])
            return redirect(self.redirect_url)
        return render(request,self.template_name)

class DepartmentAction_View(View):

    model_class = Department_Model
    redirect_url = 'department'

    def post(self,request):
        data_id = request.POST.get('disable_data',None)
        Service_data = self.model_class.objects.filter(id=data_id)
        if(Service_data.first().status == 'Active'):
            Service_data.update(status='Inactive')
            messages.success(request,Django_messages_Main['service_disabled'])
            return redirect(self.redirect_url)
        else:
            Service_data.update(status='Active')
            messages.success(request,Django_messages_Main['service_enabled'])
            return redirect(self.redirect_url)

class DesignationView(View):

    template_name = 'designation/designation_page.html'
    model_class = Designation_Model

    def get(self,request):
        data = self.model_class.objects.all()
        return render(request,self.template_name,locals())

class Add_DesignationView(View):

    template_name = 'designation/add_designation_page.html'
    form_class = DesignationForm
    redirect_url = 'department'

    def get(self,request):
        form =self.form_class()
        return render(request,self.template_name,locals())

    def post(self,request):
        form = self.form_class(request.POST)
        if(form.is_valid()):
            form.save()
            messages.success(request,Django_messages_Main['department_added'])
            return redirect(self.redirect_url)
        return render(request,self.template_name,locals())