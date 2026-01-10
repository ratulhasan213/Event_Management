"""
URL configuration for event_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
from events.views import Home
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.conf import settings
from users.views import PasswordResetConfirm,ResetPassword
from django.contrib.auth.views import PasswordResetDoneView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",Home.as_view(),name= "home"),
    path("events/",include("events.urls")),
    path("users/",include("users.urls")),
    path("users/password_reset/",ResetPassword.as_view(),name="password_reset"),
    path("users/password_reset_confirm/<uidb64>/<token>/",PasswordResetConfirm.as_view(),name = 'password_reset_confirm'),
    path("password_reset_done/", PasswordResetDoneView.as_view(),name="password_reset_done"),
]+debug_toolbar_urls()



urlpatterns+=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

""" 

from debug_toolbar.toolbar import debug_toolbar_urls

 """