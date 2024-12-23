from django.contrib import admin

# Register your models here.
from crm.admin import Lead,LeadAdmin,PageAdmin

from .models import Customer,  head

@admin.register(head)
class SuperAdminAdmin(admin.ModelAdmin):
    # list_display = ('id', 'super_admin_id', 'name', 'email')
    list_display = [field.name for field in head._meta.fields] 
    # search_fields = ('name', 'email', 'super_admin_id')
    




