from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(EmployeeDT)
class CustomerAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name', 'email', 'phone', 'source', 'date_created', 'active')
    list_display = [field.name for field in EmployeeDT._meta.fields] 
    # search_fields = ('name', 'email', 'phone')
  