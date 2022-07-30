"""G_map URL Configuration

The `urlpatterns` list routes URLs to  For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('',index_menu.as_view(),name='menus' ),
    path('dashboard',dashboard.as_view(),name='dashboard' ),

# Roles path
    path('roles-view/',include([
        path('',Roles_View.as_view(),name='roles_view' ),
        path('edit-roles/<str:slug>',EditRoles_View.as_view(),name='edit_roles' ),
        path('actions-roles',RolesAction_View.as_view(),name='actions_roles' ),
    ])),

# service path
    path('service-type/',include([
        path('',Service_TypeView.as_view(),name='service_type' ),
        path('add-service-type',AddService_TypeView.as_view(),name='add_service_type' ),
        path('edit-service-type/<str:slug>',EditService_TypeView.as_view(),name='edit_service_type' ),
        path('view-service-type/<str:slug>',ViewService_TypeView.as_view(),name='view_service_type' ),
        path('actions-service-type',ServiceTypeAction_View.as_view(),name='actions_servicetype' ),
    ])),

# department path
    path('Department/',include([
        path('',DepartmentView.as_view(),name='department' ),
        path('add-department',Add_DepartmentView.as_view(),name='add_department' ),
        path('edit-department/<str:slug>',Edit_DepartmentView.as_view(),name='edit_department' ),
        # path('view-department/<int:pk>',ViewService_TypeView.as_view(),name='view_department' ),
        path('actions-department',DepartmentAction_View.as_view(),name='actions_department' ),
    ])),

# designation path
    path('Designation/',include([
        path('',DesignationView.as_view(),name='designation' ),
        path('add-designation',Add_DesignationView.as_view(),name='add_designation' ),
        
    ])),
]
