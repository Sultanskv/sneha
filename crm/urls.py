from django.urls import path , include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
     # Authentication URLs
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Home or root URL
  #  path('', include('your_app.urls')),  # This is where the '/' URL is handled, typically your homepage or dashboard
    

    path('', views.super_admin_login, name='super_admin_login'),
    path('suparadmin-logout/', views.suparadmin_logout, name='suparadmin_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('add_sale/', views.add_sale, name='add_sale'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    

    path('all-leads/', views.all_leads, name='all_leads'),
    path('update-active-status/', views.update_active_status, name='update_active_status'),
    path('export-leads/', views.export_leads_to_excel, name='export_leads_to_excel'),
    # path('webhook/', views.facebook_webhook, name='facebook-webhook'),

    path('login/facebook/', include('social_django.urls', namespace='social')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('all_sale/', views.all_sale, name='all_sale'),
    path('create-lead/', views.create_lead, name='create_lead'),
    # path('select-form/<str:page_id>/', views.select_form, name='select_form'),
    # path('fetch-leads/<str:form_id>/', views.fetch_leads, name='fetch_leads'),


    path('facebook_login/', views.facebook_login, name='facebook_login'),
    path('facebook-pages/', views.facebook_pages, name='facebook_pages'),
    path('select-form/<str:page_id>/', views.select_form, name='select_form'),
    path('fetch-leads/<str:form_id>/', views.fetch_leads, name='fetch_leads'),
    
    path('login/facebook2/', views.facebook_login2, name='facebook_login2'),
    path('complete/facebook/', views.facebook_complete, name='facebook_complete'), # https://crm.joytilingtechnology.com/complete/facebook/


    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/edit/<int:pk>/', views.employee_edit, name='employee_edit'),


    path('upload-customers/', views.upload_customers, name='upload_customers'),
]
 