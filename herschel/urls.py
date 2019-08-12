"""herschel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

from .apps.main.views import IndexView, AboutView, GalleryView
from .apps.submissions.views import submission_page, login_view
from .apps.staff import urls as staff_urlconf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('staff/', include(staff_urlconf)),
    path('join/', AboutView.as_view(), name='join'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('submit/', submission_page, name='submit'),
    path('login/', login_view, name='login'),
    re_path('^$', IndexView.as_view(), name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
