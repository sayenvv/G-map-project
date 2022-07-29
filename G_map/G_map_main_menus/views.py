from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.views.generic import View
from .forms import *
from django.utils.decorators import method_decorator
from G_map.decorator import has_permission

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
    template_name = 'roles_page.html'
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
        print(forms)
        if(forms.is_valid()):
            forms.save()
            return redirect(self.redirect_url)
        return render(request,self.template_name,context={'form' : forms})

class EditRoles_View(View):
    template_name = 'edit_roles.html'
    redirect_url = 'roles_view'
    form_class = RolesForm

    @method_decorator(has_permission(permission='auth.add_group'))
    def get(self,request,*args,**kwargs):
        form = self.form_class
        pk = kwargs.get('pk')
        return render(request,self.template_name,context={
            'form' : form(initial={
                'name' : Group.objects.filter(id=pk).first().name,
                'status' : Group.objects.filter(id=pk).first().status,
            })
        })

    def post(self,request,**kwargs):
        pk = kwargs.get('pk')
        form_class =self.form_class(request.POST,instance=Group.objects.filter(id=pk).first())
        if(form_class.is_valid()):
            form_class.save()
            return redirect(self.redirect_url)
        return render(request,self.template_name,context={
            'form' : form_class(initial={
                'name' : Group.objects.filter(id=pk).first().name,
                'status' : Group.objects.filter(id=pk).first().status,
            })
        })