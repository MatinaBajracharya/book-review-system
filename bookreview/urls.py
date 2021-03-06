"""bookreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from user import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from book.views import *
from allauth.account.views import LoginView

class MyLoginView(LoginView):
    template_name = 'user/login.html'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    url(r'^accounts/login', MyLoginView.as_view(), name='account_login'),
    url(r'^accounts/signup', user_views.register, name='account_signup'),
    path('register/', user_views.register, name='register'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='user/changepassword.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='user/passwordchanged.html'), name='password_change_done'),
    path('profile/<int:pk>', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', user_views.user_logout, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'), 
    path('', include('forum.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('admin/upload-csv/', book_detail_upload, name="book_detail_upload"),
    path('', include('book.urls')),
    path('delete-user/<int:pk>', user_views.DeleteProfile, name='delete_user'),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 