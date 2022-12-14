"""learnyn URL Configuration

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
from django.contrib import admin
from django.urls import include, path

from .views import HomeView
from .api.views import HomeAPIView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),
    path('class-admins/', include('classadmins.urls')),
    path('schools/', include('school.urls')),
    path('results/', include('results.urls')),
    path('students/', include('students.urls')),
    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('api', HomeAPIView.as_view(), name='api_home'),
    path('api/accounts/', include('accounts.api.urls')),
    path('api/class-admins/', include('classadmins.api.urls')),
    path("api/school/", include("school.api.urls")),
    path('api/students/', include('students.api.urls')),
    path('api/results/', include('results.api.urls')),
]