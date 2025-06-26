from authentication.views import login_view,register_view,otp_view,logout_view,forget_password_view, otp,profile_view
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # Authentication URLs
    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
    path('logout/',logout_view, name='logout'),
    path('otp-verify/<uuid:uid>', otp_view, name='otp-verify'),
    path('otp-verify', otp, name='otp'),
    path('forgot-password',forget_password_view, name='forgot-password'),
    path('profile', profile_view, name='profile'),  # Assuming profile view is same as login for now
   
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
