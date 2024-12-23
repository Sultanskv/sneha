"""
URL configuration for crm_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from crm.views import test_cache
from django.urls import path

urlpatterns = [
    path('django/', admin.site.urls),
    path('crm/', include('crm.urls')),  # CRM sub-admin URLs
    path('head/', include('head.urls')),  # Head admin URLs
    path('', include('Employee.urls')),  # Employee URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
    path('social/', include('social_django.urls', namespace='social')),  # Social auth URLs
    path('test-cache/', test_cache, name='test_cache'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# For development only, serve media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)










# from django.contrib import admin
# from django.urls import path

# from django.contrib import admin
# from django.urls import path, include
# from django.urls import path , include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('crm/', include('crm.urls')),
#     path('', include('head.urls')),
#     path('employee/', include('Employee.urls')),
#     path('accounts/', include('django.contrib.auth.urls')),
#     path('social/', include('social_django.urls', namespace='social')),  # Social auth URLs
# ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# # urls.py

# # For development only. In production, use a web server like Nginx to serve media files.
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Static files serving configuration
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
