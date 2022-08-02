from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.shortcuts import redirect, render
from django.views.generic import View
from .forms import *
from django.utils.decorators import method_decorator
from G_map.decorator import has_permission
from django.contrib import messages
from .utils import Django_messages_Main
from django.views.generic.edit import UpdateView
from django.forms.formsets import formset_factory

# Create your views here.
class index_menu(View):
    template_name = 'menus_page.html'

    def get(self,request):
        return render(request,self.template_name)


class dashboard(View):
    template_name = 'dashboard.html'

    def get(self,request):
        is_dashboard = True
        return render(request,self.template_name,locals())

class Roles_View(View):
    template_name = 'roles/roles_page.html'
    redirect_url = 'roles_view'
    form_class = RolesForm
    

    def get(self,request):
        forms = self.form_class()
        data = Group.objects.all()
        is_menu = True
        return render(request,self.template_name,locals())

    @method_decorator(has_permission(permission='auth.add_group'))
    def post(self,request):
        forms = self.form_class(request.POST)
        if(forms.is_valid()):
            forms.save()
            messages.success(request,Django_messages_Main['roles_added'])
            return redirect(self.redirect_url)
        return render(request,self.template_name,context={'form' : forms})

class EditRoles_View(View):
    template_name = 'roles/edit_roles.html'
    redirect_url = 'roles_view'
    form_class = RolesForm

    @method_decorator(has_permission(permission='auth.change_group'))
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('slug')
        is_menu = True
        form = self.form_class(initial={
                'name' : Group.objects.filter(slug_field=pk).first().name,
                'status' : Group.objects.filter(slug_field=pk).first().status,
            })
        return render(request,self.template_name,locals())
    
    @method_decorator(has_permission(permission='auth.change_group'))
    def post(self,request,**kwargs):
        pk = kwargs.get('slug')
        is_menu = True
        form_class =self.form_class(request.POST,instance=Group.objects.filter(slug_field=pk).first())
        if(form_class.is_valid()):
            form_class.save()
            messages.success(request,Django_messages_Main['roles_edited'])
            return redirect(self.redirect_url)
        return render(request,self.template_name,locals())

class RolesAction_View(View):
    redirect_url = 'roles_view'

    def post(self,request):
        data_id = request.POST.get('disable_data',None)
        Roles_data = Group.objects.filter(id=data_id)
        if(Roles_data.first().status == 'Active'):
            Roles_data.update(status='Inactive')
            messages.error(request,Django_messages_Main['roles_disabled'])
            return redirect(self.redirect_url)
        else:
            Roles_data.update(status='Active')
            messages.success(request,Django_messages_Main['roles_enabled'])
            return redirect(self.redirect_url)

class SetPermissions_View(View):
    template_name = 'roles/permissions/set_permission_page.html'
    redirect_url = 'roles_view'

    def get(self,request,*args,**kwargs):
        pk = kwargs.get('slug')
        is_menu = True
        perm = Group.objects.filter(slug_field=pk).first().permissions.all().values_list('id',flat=True)
        data = ContentType.objects.exclude(model__in=['session','logentry','Permission','Contenttype'])
        return render(request,self.template_name,locals())

    def post(self,request,*args,**kwargs):
        pk = kwargs.get('slug')
        permission = request.POST.getlist('permissions')
        if(permission):
            instance = Group.objects.filter(slug_field=pk).first()
            instance.permissions.clear()
            for i in permission:
                instance.permissions.add(Permission.objects.filter(id=i).first())
            messages.success(request,Django_messages_Main['permission_granded'].format(instance.name))
            return redirect(self.redirect_url)
        
        return render(request,self.template_name,locals())

class Service_TypeView(View):
    template_name = 'service_type/service_type.html'
    model_class = Service_Type_Model
    def get(self,request):
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
            messages.error(request,Django_messages_Main['service_disabled'])
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
            messages.error(request,Django_messages_Main['department_disabled'])
            return redirect(self.redirect_url)
        else:
            Service_data.update(status='Active')
            messages.success(request,Django_messages_Main['department_enabled'])
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
    redirect_url = 'designation'

    def get(self,request):
        form =self.form_class()
        return render(request,self.template_name,locals())

    def post(self,request):
        form = self.form_class(request.POST)
        if(form.is_valid()):
            form.save()
            messages.success(request,Django_messages_Main['designation_added'])
            return redirect(self.redirect_url)
        return render(request,self.template_name,locals())

class Edit_DesignationView(View):
    template_name = 'designation/edit_designation_page.html'
    form_class = DesignationForm
    redirect_url = 'designation'
    model_class = Designation_Model

    def get(self,request,**kwargs):
        slug = kwargs.get('slug')
        form =self.form_class(initial={
            'designation' : self.model_class.objects.filter(slug_field=slug).first().designation,
            'department' : self.model_class.objects.filter(slug_field=slug).first().department,
            'status' : self.model_class.objects.filter(slug_field=slug).first().status,
        })
        return render(request,self.template_name,locals())

    def post(self,request,**kwargs):
        slug = kwargs.get('slug')
        form = self.form_class(request.POST,instance=self.model_class.objects.filter(slug_field=slug).first())
        if(form.is_valid()):
            form.save()
            messages.success(request,Django_messages_Main['designation_edited'])
            return redirect(self.redirect_url)
        return render(request,self.template_name)

class Assign_DepartmentView(View):

    template_name = 'designation/assign_department_page.html'
    form_class = AssignDepartmentForm
    redirect_url = 'designation'
    model_class = Designation_Model

    def get(self,request,**kwargs):
        slug = kwargs.get('slug')
        form =self.form_class(initial={
            'designation' : self.model_class.objects.filter(slug_field=slug).first().designation,
            'department' : self.model_class.objects.filter(slug_field=slug).first().department.all(),
        })
        return render(request,self.template_name,locals())

    def post(self,request,**kwargs):
        slug = kwargs.get('slug')
        form = self.form_class(request.POST,instance=self.model_class.objects.filter(slug_field=slug).first())
        if(form.is_valid()):
            form.save()
            messages.success(request,Django_messages_Main['department_assigned'])
            return redirect(self.redirect_url)
        return render(request,self.template_name,locals())

class DesignationAction_View(View):
    model_class = Designation_Model
    redirect_url = 'designation'

    def post(self,request):
        data_id = request.POST.get('disable_data',None)
        Service_data = self.model_class.objects.filter(id=data_id)
        if(Service_data.first().status == 'Active'):
            Service_data.update(status='Inactive')
            messages.success(request,Django_messages_Main['designation_disabled'])
            return redirect(self.redirect_url)
        else:
            Service_data.update(status='Active')
            messages.success(request,Django_messages_Main['designation_enabled'])
            return redirect(self.redirect_url)

class VendorView(View):

    template_name = 'vendor/vendor_page.html'
    model_class = Vendor_Model

    def get(self,request):
        data = self.model_class.objects.all()
        return render(request,self.template_name,locals())

class Add_VendorView(View):

    template_name = 'vendor/add_vendor_page.html'
    form_class = VendorForm
    redirect_url = 'vendor'

    def get(self,request):
        form =self.form_class()
        return render(request,self.template_name,locals())

    def post(self,request):
        form = self.form_class(request.POST)
        if(form.is_valid()):
            form.save()
            messages.success(request,Django_messages_Main['vendor_added'])
            return redirect(self.redirect_url)
        return render(request,self.template_name,locals())

class Edit_VendorView(View):

    template_name = 'vendor/edit_vendor_page.html'
    form_class = VendorForm
    redirect_url = 'vendor'
    model_class = Vendor_Model

    def get(self,request,**kwargs):
        slug = kwargs.get('slug')
        form =self.form_class(initial={
            'name' : self.model_class.objects.filter(slug_field=slug).first().name,
            'email' : self.model_class.objects.filter(slug_field=slug).first().email,
            'phone' : self.model_class.objects.filter(slug_field=slug).first().phone,
            'status' : self.model_class.objects.filter(slug_field=slug).first().status,
        })
        return render(request,self.template_name,locals())

    def post(self,request,**kwargs):
        slug = kwargs.get('slug')
        form = self.form_class(request.POST,instance=self.model_class.objects.filter(slug_field=slug).first())
        if(form.is_valid()):
            form.save()
            messages.success(request,Django_messages_Main['vendor_edited'])
            return redirect(self.redirect_url)
        return render(request,self.template_name)

class VendorAction_View(View):
    model_class = Vendor_Model
    redirect_url = 'vendor'

    def post(self,request):
        data_id = request.POST.get('disable_data',None)
        Service_data = self.model_class.objects.filter(id=data_id)
        if(Service_data.first().status == 'Active'):
            Service_data.update(status='Inactive')
            messages.error(request,Django_messages_Main['vendor_disabled'])
            return redirect(self.redirect_url)
        else:
            Service_data.update(status='Active')
            messages.success(request,Django_messages_Main['vendor_enabled'])
            return redirect(self.redirect_url)


class QuestionnairView(View):
    template_name = 'questionnair/questionnair_page.html'
    model_class = Questionnair_Model

    def get(self,request):
        data = self.model_class.objects.all()
        return render(request,self.template_name,locals())

class Add_QuestionnairView(View):
    template_name = 'questionnair/add_questionnair_page.html'
    form_class = QuestionnairForm
    dionamic_formclass = DionamicQuestionForm
    redirect_url = 'questionnair'

    def get(self,request):
        form = formset_factory(self.form_class,self.dionamic_formclass,extra=2)
        return render(request,self.template_name,locals())

    def post(self,request):
        form = self.form_class(request.POST)
        if(form.is_valid()):
            form.save()
            messages.success(request,Django_messages_Main['vendor_added'])
            return redirect(self.redirect_url)
        return render(request,self.template_name,locals())