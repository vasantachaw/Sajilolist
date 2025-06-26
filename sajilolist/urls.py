"""
URL configuration for sajilolist project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from MainApp import urls as MainApp_urls
from authentication import urls as Auth_urls
from ContactUs import urls as ContactUs_urls
from RatingReviews import urls as RatingReviews_urls
from Blogs import urls as Blogs_urls
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(MainApp_urls)),
    path("authentication/", include(Auth_urls)),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("contact/", include(ContactUs_urls)),
    path("rating/", include(RatingReviews_urls)),
    path("blog/", include(Blogs_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
