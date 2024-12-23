


from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login', views.head_login, name='head_login'),
    path('logout/', views.head_logout, name='head_logout'),
    path('head_dashboard/', views.head_dashboard, name='head_dashboard'),
    path('head_add_customer/', views.head_add_customer, name='head_add_customer'),
    path('head_privacy-policy/', views.head_privacy_policy, name='head_privacy_policy'),
    path('head_terms-of-service/', views.head_terms_of_service, name='head_terms_of_service'),
    path('head_update_active_status', views.head_update_active_status, name='head_update_active_status'),
    path('head_export-leads/', views.head_export_leads_to_excel, name='head_export_leads_to_excel'),
    path('head_employees/', views.head_employee_list, name='head_employee_list'),
    path('head_employees/add/', views.head_employee_add, name='head_employee_add'),
    path('head_employees/edit/<int:pk>/', views.head_employee_edit, name='head_employee_edit'),
    path('head_all-leads/', views.head_all_leads, name='head_all_leads'),
    path('head/head_pages/', views.head_fetch_pages, name='head_fetch_pages'),
    # path('head_pages/<str:page_id>/leads/', views.head_fetch_forms_for_page, name='head_fetch_leads_for_page'),
    path('head_forms/<str:form_id>/leads/', views.fetch_all_leads_from_api, name='head_fetch_leads_for_form'),
    path('head/forms/<str:page_id>/', views.head_fetch_forms_for_page, name='head_fetch_forms_for_page'),
    #  path('assign-lead/', views.assign_lead_to_user, name='assign_lead_to_user'),
    # path('auto-assign-leads/', views.auto_assign_leads_task, name='auto_assign_leads'),
]













# from django.urls import path , include
# from django.contrib.auth import views as auth_views
# from . import views
# # from .views import fetch_pages, fetch_all_page_leads

# urlpatterns = [
#      # Authentication URLs
#     path('login/', auth_views.LoginView.as_view(), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
#     # Home or root URL
#   #  path('', include('your_app.urls')),  # This is where the '/' URL is handled, typically your homepage or dashboard
    

#     path('', views.head_login, name='super_admin_login'),
#     path('suparadmin-logout/', views.head_logout, name='suparadmin_logout'),
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('add_customer/', views.add_customer, name='add_customer'),
   
#     path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
#     path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    

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
    
#     path('all-leads/', views.all_leads, name='all_leads'),


#     path('employees/', views.employee_list, name='employee_list'),
#     path('employees/add/', views.employee_add, name='employee_add'),
#     path('employees/edit/<int:pk>/', views.employee_edit, name='employee_edit'),

#     # path('leads/changelist/', views.calls_lead_changelist, name='calls_lead_changelist'),

#    path("pages/", views.fetch_pages, name="fetch_pages"),
#    path("pages/<str:page_id>/leads/", views.fetch_leads_for_page, name="fetch_leads_for_page"),
#     path("forms/<str:form_id>/leads/", views.fetch_leads_for_form, name="fetch_leads_for_form"),
# ]


    
 