from django.contrib import admin
from .models import Customer, Sale , super_admin , UserProfile

# admin.site.register(Customer)
# admin.site.register(Sale)
# admin.site.register(super_admin)


# admin.py
from django.contrib import admin
from .models import Customer, Sale, super_admin

# Customer Model Admin
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name', 'email', 'phone', 'source', 'date_created', 'active')
    list_display = [field.name for field in Customer._meta.fields] 
    # search_fields = ('name', 'email', 'phone')
  


# Sale Model Admin
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    # list_display = ('id', 'customer', 'amount', 'date')
    list_display = [field.name for field in Sale._meta.fields] 
    # search_fields = ('customer__name',)
    

# Super Admin Model Admin
@admin.register(super_admin)
class SuperAdminAdmin(admin.ModelAdmin):
    # list_display = ('id', 'super_admin_id', 'name', 'email')
    list_display = [field.name for field in super_admin._meta.fields] 
    # search_fields = ('name', 'email', 'super_admin_id')
    

@admin.register(UserProfile)
class SuperAdminAdmin(admin.ModelAdmin):
    # list_display = ('id', 'super_admin_id', 'name', 'email')
    list_display = [field.name for field in UserProfile._meta.fields] 
    # search_fields = ('name', 'email', 'super_admin_id')
        