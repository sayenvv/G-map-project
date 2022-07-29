from django.db import models
from django.contrib.auth.models import Group

# Create your models here.
class Roles_model(models.Model):
    role_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20,choices=(('Active','Active'),('Inactive','Inactive')),default='Active')

    
Group.add_to_class('status', models.CharField(max_length=180,choices=(
    ('Active','Active'),
    ('Inactive','Inactive')
),default='Active'))