from django.shortcuts import redirect
from django.contrib import messages
from G_map_main_menus.utils import Django_messages_Main

def has_permission(permission = ""):
    def dec_func(view_func):
        def wrapper_func(request,*args,**kwargs):
            if request.user.has_perm(permission):
                return view_func(request,*args,**kwargs)
            else:
                messages.error(request,Django_messages_Main['no_pernission'])
                return redirect(request.META.get('HTTP_REFERER'))
        return wrapper_func
    return dec_func