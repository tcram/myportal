"""
URL configuration for myportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from gsearch import views as gsearch_views

from globus_portal_framework.urls import register_custom_index
register_custom_index('dssearch', ['dataset-search'])

urlpatterns = [
    path('admin/', admin.site.urls),
    # Override the default search view
    path('<dssearch:index>/', gsearch_views.dataset_search, name='search'),
    # Provides the basic search portal
    path('', include('globus_portal_framework.urls')),
    # Provides Login urls for Globus Auth
    path('', include('social_django.urls', namespace='social')),
]
