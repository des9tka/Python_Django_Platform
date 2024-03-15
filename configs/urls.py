"""
URL configuration for configs project.

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
from django.urls import include, path

from apps.base.views import auth_login, auth_logout, auth_register

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth_login', auth_login, name='auth_login'),
    path('auth_logout', auth_logout, name='auth_logout'),
    path('auth_register', auth_register, name='auth_register'),

    path('rooms', include('apps.base.urls'))
]
