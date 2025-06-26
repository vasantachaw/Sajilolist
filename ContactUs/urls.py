from django.urls import path
from ContactUs import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
path('contact/',views.contact_us_view, name='contact'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
