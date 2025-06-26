from django.urls import path
from RatingReviews import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('comments/realestate/<int:product_id>/', views.get_realestate_comments, name='realestate_comments'),
    path('comments/bookseducation/<int:product_id>/', views.get_books_education_comments, name='books_education_comments'),
    path('comments/healthbeauty/<int:product_id>/', views.get_health_beauty_comments, name='health_beauty_comments'),
    path('comments/householdaccessories/<int:product_id>/', views.get_household_accessories_comments, name='household_accessories_comments'),
    path('comments/automobiles/<int:product_id>/', views.get_automobiles_comments, name='automobiles_comments'),
    path('comments/furnitureappliances/<int:product_id>/', views.get_furniture_appliances_comments, name='furniture_appliances_comments'),
    path('comments/pcsperipherals/<int:product_id>/', views.get_pcs_peripherals_comments, name='pcs_peripherals_comments'),
    path('comments/musicalinstruments/<int:product_id>/', views.get_musical_instruments_comments, name='musical_instruments_comments'),
    path('comments/mobiledevicesaccessories/<int:product_id>/', views.get_mobile_devices_accessories_comments, name='mobile_devices_accessories_comments'),
    path('comments/electronicsappliances/<int:product_id>/', views.get_electronics_appliances_comments, name='electronics_appliances_comments'),
    path('comments/fashionwearaddons/<int:product_id>/', views.get_fashionwear_addons_comments, name='fashionwear_addons_comments'),
    path('comments/toolsmachinery/<int:product_id>/', views.get_tools_machinery_comments, name='tools_machinery_comments'),
    path('comments/camerasaccessories/<int:product_id>/', views.get_cameras_accessories_comments, name='cameras_accessories_comments'),
    path('comments/foodbeverages/<int:product_id>/', views.get_food_beverages_comments, name='food_beverages_comments'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
