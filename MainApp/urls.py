from django.urls import path
from MainApp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('shop-details/', views.shop, name='shop-details'),
    path('product/<str:model_name>/<int:pk>/',
         views.GenericProductDetailView.as_view(), name='generic_product_detail'),
    path('wishlist/toggle/<str:product_type>/<int:pk>/',
         views.ToggleWishListView.as_view(), name='toggle_wishlist'),

    path('realestate/', views.RealEstateListView.as_view(), name='realestate_list'),
    path('fashion/', views.FashionListView.as_view(), name='fashion_list'),
    path('cameras/', views.CamerasListView.as_view(), name='cameras_list'),
    path('electronics/', views.ElectronicsAppliancesListView.as_view(), name='electronics_list'),
    path('automobiles/', views.AutomobilesListView.as_view(), name='automobiles_list'),
    path('mobiles/', views.MobileDevicesAccessoriesListView.as_view(), name='mobiles_list'),
    path("pcs/", views.PCsPeripheralsListView.as_view(), name="pcs_list"),
    path('furniture/', views.FurnitureAppliancesListView.as_view(), name='furniture_list'),
    path("tools/", views.ToolsMachineryListView.as_view(), name="tools_list"),
    path('musical/', views.MusicalInstrumentsListView.as_view(), name='musical_list'),
     path('health/', views.HealthBeautyListView.as_view(), name='health_list'),
    path('books/', views.BooksEducationListView.as_view(), name='books_list'),
# urls.py
    path("user/<str:username>/", views.UserDetailsView, name="user_details"),
    path('filter/', views.filter_view, name='filter'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('create-listing/<str:category>/',
         views.create_listing, name='create_listing'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
