"""charity_lab URL Configuration

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
from django.contrib import admin
from django.urls import path

import charity_donation_app.views as Charity_Views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Charity_Views.LandingPage.as_view(), name='main'),
    path('form/', Charity_Views.AddDonation.as_view(), name='form'),
    path('login/', Charity_Views.Login.as_view(), name='login'),
    path('register/', Charity_Views.Register.as_view(), name='register'),
]
