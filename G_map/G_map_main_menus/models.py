from django.db import models
from django.contrib.auth.models import Group
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_lifecycle import LifecycleModelMixin, hook, AFTER_CREATE,AFTER_UPDATE,AFTER_SAVE

# Create your models here.
# class Company_Model(models.Model):
#     company_name = models.CharField(max_length=100)
#     address = models.TextField()
#     company_registrationNo = models.CharField(max_length=100)
#     company_registrationExpiry = models.DateField()
#     municipality_registration = models.CharField(max_length=100)
#     municipality_licenceExpiry = models.DateField()
#     chamber_of_commerceExpiry = models.DateField()
#     tax_registationExpiry = models.DateField()
#     vat_registationExpiry = models.DateField()
#     rent_for_needsExpiry = models.DateField()
#     professional_indemnityInsurance = models.CharField(max_length=256)
#     workman_compensationInsurance = models.CharField(max_length=256)
#     JSRS = models


class Service_Type_Model(models.Model):
    slug_field = models.SlugField(max_length=256,blank=True)
    service = models.CharField(max_length=100)
    status = models.CharField(max_length=180,choices=(
                ('Active','Active'),
                ('Inactive','Inactive')
            ),default='Active')
    scope_of_work = models.TextField()

    @receiver(post_save, sender='G_map_main_menus.Service_Type_Model')
    def save_slug(sender, *args, **kwargs):
        instance = Service_Type_Model.objects.filter(pk=kwargs['instance'].id)
        value = str(instance.first().service)+" "+str(instance.first().id)
        slug_field = slugify(value, allow_unicode=True)
        instance.update(slug_field=slug_field)

    def __str__(self):
        return self.service
        

    
Group.add_to_class(
    'status', models.CharField(max_length=180,choices=(
        ('Active','Active'),
        ('Inactive','Inactive')
        ),default='Active'),
    
    
    )
Group.add_to_class(
    'slug_field' , models.SlugField(max_length=256,blank=True)
)
@receiver(post_save, sender=Group)
def save_slug(sender, *args, **kwargs):
    instance = Group.objects.filter(pk=kwargs['instance'].id)
    value = str(instance.first().name)+" "+str(instance.first().id)
    slug_field = slugify(value, allow_unicode=True)
    instance.update(slug_field=slug_field)

class Department_Model(LifecycleModelMixin,models.Model):
    slug_field = models.SlugField(max_length=256,blank=True)
    department_name = models.CharField(max_length=100)
    service_type = models.ForeignKey(Service_Type_Model,on_delete=models.CASCADE)
    status = models.CharField(max_length=180,choices=(
                ('Active','Active'),
                ('Inactive','Inactive')
            ),default='Active')

    @receiver(post_save, sender='G_map_main_menus.Department_Model')
    def save_slug(sender, *args, **kwargs):
        instance = Department_Model.objects.filter(pk=kwargs['instance'].id)
        value = str(instance.first().department_name)+" "+str(instance.first().id)
        slug_field = slugify(value, allow_unicode=True)
        instance.update(slug_field=slug_field)

class Designation_Model(models.Model):
    designation = models.CharField(max_length=100)
    department = models.ManyToManyField(Department_Model,blank=True)
    status = models.CharField(max_length=180,choices=(
                ('Active','Active'),
                ('Inactive','Inactive')
            ),default='Active')