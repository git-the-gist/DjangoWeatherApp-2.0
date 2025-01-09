"""weathersource URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from weatherAppModule import views

urlpatterns = [
    path('weathersource/home/', views.home, name='home'),
    path('weathersource/api/search', views.cities_api, name='api'),
    path('weathersource/search', views.search_city, name='search_city'),
    path('weathersource/page-not-found', views.error_404_view, name='error_404'),
    path('weathersource/location-not-found', views.error_location_view, name='error_location'),
    path("__debug__/", include("debug_toolbar.urls")),
]
