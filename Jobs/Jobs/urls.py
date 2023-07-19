"""Jobs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from Jobapp.views import CompanyListAPIView, JobCreateAPIView, UserProfileCreateAPIView

urlpatterns = [
    path('jobs/', JobCreateAPIView.as_view(), name='job-create'),
    path('user-profiles/', UserProfileCreateAPIView.as_view(), name='user-profile-create'),
    path('companies/', CompanyListAPIView.as_view(), name='company-list'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
