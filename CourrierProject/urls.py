"""
URL configuration for CourrierProject project.

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
from courrier.views_auth import index
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='connexion'),
    path('auth/', include(('courrier.urls.urls_auth', 'auth'), namespace='auth')),
    path('user/', include(('courrier.urls.urls_user', 'user'), namespace='user')),
    path('service/', include(('courrier.urls.urls_service', 'service'), namespace='service')),
    path('mission/', include(('courrier.urls.urls_mission', 'mission'), namespace='mission')),
    path('courrier/', include(('courrier.urls.urls_courrier', 'courriers'), namespace='courriers')),
    path('permission/', include(('courrier.urls.urls_permission', 'permission'), namespace='permission')),
]
