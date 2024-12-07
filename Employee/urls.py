from django.urls import path , include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.Employee_login, name='employee_login'), 
    path('logout/', views.Employee_logout, name='Employee_logout'), 
    path('dashboard/', views.Dashboard, name='Dashboard'),
    path('leads/', views.employee_leads, name='employee_leads'),
    path('leads/import/', views.export_leads_to_excel_emp, name='export_leads_to_excel_emp'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
]