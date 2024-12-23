from django.urls import path
from django.contrib.auth import views as auth_views
from crm import views

urlpatterns = [
    path('', views.super_admin_login, name='super_admin_login'),
    path('logout/', views.suparadmin_logout, name='suparadmin_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('update-active-status/', views.update_active_status, name='update_active_status'),
    path('export-leads/', views.export_leads_to_excel, name='export_leads_to_excel'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/edit/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('leads/', views.all_leads, name='all_leads'),
    path('pages/', views.fetch_pages, name='fetch_pages'),
    path('old-leads/', views.old_leads, name='old_leads'),
 
    path('forms/<str:form_id>/leads/', views.fetch_leads_for_form, name='fetch_leads_for_form'),
    path('pages/<int:page_id>/forms/', views.fetch_forms_for_page, name='fetch_forms_for_page'),
    path('get-latest-lead/', views.get_latest_lead, name='get_latest_lead'),
    path('test-cache/', views.test_cache, name='test_cache'),
    path('clear_session_flag/', views.clear_session_flag, name='clear_session_flag'),
    path('api/fetch-new-leads/', views.fetch_new_leads, name='fetch_new_leads'),
    path('leads/<str:form_id>/', views.fetch_leads_from_db, name='fetch_leads_from_db'),
   path('fetch-leads/', views.manual_fetch_leads, name='fetch_leads'),
 
]












# from django.urls import path , include
# from django.contrib.auth import views as auth_views
# from . import views
# # from .views import fetch_pages, fetch_all_page_leads

# urlpatterns = [
#      # Authentication URLs
#     path('crm/login/', auth_views.LoginView.as_view(), name='login'),
#     path('crm/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
#     # Home or root URL
#   #  path('', include('your_app.urls')),  # This is where the '/' URL is handled, typically your homepage or dashboard
    

#     path('', views.super_admin_login, name='super_admin_login'),
#     path('crm/suparadmin-logout/', views.suparadmin_logout, name='suparadmin_logout'),
#     path('crm/dashboard/', views.dashboard, name='dashboard'),
#     path('crm/add_customer/', views.add_customer, name='add_customer'),
   
#     path('crm/privacy-policy/', views.privacy_policy, name='privacy_policy'),
#     path('crm/terms-of-service/', views.terms_of_service, name='terms_of_service'),
    

#     # path('all-leads/', views.all_leads, name='all_leads'),
#     path('update-active-status/', views.update_active_status, name='update_active_status'),
#     path('export-leads/', views.export_leads_to_excel, name='export_leads_to_excel'),
#     # path('webhook/', views.facebook_webhook, name='facebook-webhook'),

#     path('login/facebook/', include('social_django.urls', namespace='social')),
#     path('auth/', include('social_django.urls', namespace='social')),
    
#     path('create-lead/', views.create_lead, name='create_lead'),
#     # path('select-form/<str:page_id>/', views.select_form, name='select_form'),
#     # path('fetch-leads/<str:form_id>/', views.fetch_leads, name='fetch_leads'),

#     # path('fetch-leads/<str:form_id>/', views.fetch_leads, name='fetch_leads'),
    
#     # path('all-leads/', views.all_leads, name='all_leads'),


#     path('employees/', views.employee_list, name='employee_list'),
#     path('employees/add/', views.employee_add, name='employee_add'),
#     path('employees/edit/<int:pk>/', views.employee_edit, name='employee_edit'),

#     # path('leads/changelist/', views.calls_lead_changelist, name='calls_lead_changelist'),
#     path('leads/', views.all_leads, name='all_leads'),

#    path("pages/", views.fetch_pages, name="fetch_pages"),
#     path("pages/<str:page_id>/forms/", views.fetch_forms_for_page, name="fetch_forms_for_page"),
#     path("forms/<str:form_id>/leads/", views.fetch_leads_for_form, name="fetch_leads_for_form"),
    
# ]


    
 