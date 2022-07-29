from django.shortcuts import redirect

def has_permission(permission = ""):
    def dec_func(view_func):
        def wrapper_func(request,*args,**kwargs):
            if request.user.has_perm(permission):
                return view_func(request,*args,**kwargs)
            else:
                return redirect(request.META.get('HTTP_REFERER'))
        return wrapper_func
    return dec_func