
# from .models import Customer,  UserProfile
from django.contrib import admin
from .models import  super_admin
# from django.urls import reverse
# from django.utils.html import format_html
from .models import  Customer, super_admin, Page, Lead, Form





@admin.register(super_admin)
class SuperAdminAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')
    filter_horizontal = ('allowed_pages',)
    
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('page_id', 'name', 'category')
    search_fields = ('name', 'page_id')

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'city', 'created_time', 'assigned_to', 'active')
    search_fields = ('full_name', 'email', 'phone_number', 'city')
    list_filter = ('active', 'assigned_to', 'created_time')  # Add filters for Active status and Assigned user
    list_editable = ('assigned_to', 'active')  # Editable fields directly in the list display
    autocomplete_fields = ('assigned_to',)  # Enable user dropdown with search functionality

    def formatted_created_time(self, obj):
        return obj.created_time.strftime('%Y-%m-%d %H:%M:%S')
    formatted_created_time.short_description = 'Created Time' 
    
    def display_city(self, obj):
        return obj.city or "Not Provided"
    display_city.short_description = "City"

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'source', 'active', 'status')
    search_fields = ('name', 'email', 'phone')

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('form_id', 'name', 'status')
    search_fields = ('form_id', 'name')






















# @admin.register(UserProfile)
# class SuperAdminAdmin(admin.ModelAdmin):
#     # list_display = ('id', 'super_admin_id', 'name', 'email')
#     list_display = [field.name for field in UserProfile._meta.fields] 
#     # search_fields = ('name', 'email', 'super_admin_id')
        

# admin.site.register(Customer)
# admin.site.register(Sale)
# admin.site.register(super_admin)


# admin.py
# Customer Model Admin
# @admin.register(Customer)
# class CustomerAdmin(admin.ModelAdmin):
#     # list_display = ('id', 'name', 'email', 'phone', 'source', 'date_created', 'active')
#     list_display = [field.name for field in Customer._meta.fields] 
#     # search_fields = ('name', 'email', 'phone')
  


# Sale Model Admin

    