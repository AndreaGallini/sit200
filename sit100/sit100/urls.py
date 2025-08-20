"""
URL configuration for sit100 project.

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
from django.contrib.auth import views as auth_views
from apps.core.views import CustomLoginView
from apps.project.views import *
from apps.project_result.views import *
from apps.documentation.views import *
from apps.project_setup.save_views import *
from apps.user_profile.views import *
from apps.project_setup.views import *
from apps.project_archive.views import *
from apps.api_integrations.views import *
from apps.project_pipeline.views import *
from apps.core.views import FirstPasswordSetView
from django.contrib.auth.decorators import login_required
from decorator_include import decorator_include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
urlpatterns = [
    path('', lambda request: redirect('login/')),
    path('404/', TemplateView.as_view(template_name='404.html'), name='404'),
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('', decorator_include(login_required, 'apps.project_pipeline.urls')),
    path('documentazione/', decorator_include(login_required, 'apps.documentation.urls')),
    path('', decorator_include(login_required, 'apps.project_setup.save_urls')),
    path('dashboard/', decorator_include(login_required, 'apps.frontend.urls')),
    path('dashboard_result/<int:project_code>/',
         dashboard_result, name='dashboard_result'),
    path('project/', decorator_include(login_required, 'apps.project_setup.urls')),
    path('project/', decorator_include(login_required, 'apps.project_pipeline.urls')),
    path('project/', decorator_include(login_required, 'apps.project_result.urls')),
    path('project/', decorator_include(login_required, 'apps.project_archive.urls')),
    path('legal/', include('apps.legal.urls')),
    path('user/', decorator_include(login_required, 'apps.user_profile.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        email_template_name='emails/reset_email.html',
        html_email_template_name='emails/reset_email.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('password_insert/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_insert'),
    path('download-word/<int:project_code>/',
         download_word, name='download_word'),
    path('download-pdf/<int:project_code>/',
         download_pdf, name='download_pdf'),
    path('delete_project/<int:project_code>/',
         delete_project, name='delete_project'),
    path('set_first_password/<uidb64>/<token>/',
         FirstPasswordSetView.as_view(), name='set_first_password'),
    path('operation-not-allowed/', TemplateView.as_view(
        template_name='operation_not_allowed.html'), name='operation_not_allowed'),
]

urlpatterns += static(settings.PROJECT_URL,
                      document_root=settings.PROJECT_ROOT)
urlpatterns += static(settings.USER_URL, document_root=settings.USER_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
