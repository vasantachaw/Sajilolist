from itertools import chain
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User
from MainApp.models import (
    RealEstate, Automobiles, BooksEducation, HealthBeauty,
    HouseholdAccessories, FurnitureAppliances, PCsPeripherals,
    MusicalInstruments, MobileDevicesAccessories, ElectronicsAppliances,
    FashionwearAddons, ToolsMachinery, CamerasAccessories,
    Wishlist, Ads
)
from RatingReviews.models import Comment
from MainApp.forms import (
    RealEstateForm, BooksEducationForm, HealthBeautyForm, HouseholdAccessoriesForm,
    AutomobilesForm, FurnitureAppliancesForm, PCsPeripheralsForm,
    MusicalInstrumentsForm, MobileDevicesAccessoriesForm, ElectronicsAppliancesForm,
    FashionwearAddonsForm, ToolsMachineryForm, CamerasAccessoriesForm,FoodBeveragesForm,
)
from MainApp.utils import get_location_info
from math import floor
from django.db.models import Avg

def get_form_class(category: str):
    return {
        "realestate": RealEstateForm,
        "books_education": BooksEducationForm,
        "health_beauty": HealthBeautyForm,
        "household_accessories": HouseholdAccessoriesForm,
        "automobiles": AutomobilesForm,
        "furniture_appliances": FurnitureAppliancesForm,
        "pcs_peripherals": PCsPeripheralsForm,
        "musical_instruments": MusicalInstrumentsForm,
        "mobile_devices_accessories": MobileDevicesAccessoriesForm,
        "electronics_appliances": ElectronicsAppliancesForm,
        "fashionwear_addons": FashionwearAddonsForm,
        "tools_machinery": ToolsMachineryForm,
        "cameras_accessories": CamerasAccessoriesForm,
        "food_beverages": FoodBeveragesForm,
    }.get(category)


def categories_context(request):
    location_info = get_location_info()
    country_filter = location_info.get('country')
    currency_symbol = location_info.get('currency_symbol', '$')

    discount_filter = Q(discount_percentage__gt=0)

    def filter_by_country(qs):
        return qs.filter(country__iexact=country_filter) if country_filter else qs

    # Get discounted listings for each category filtered by country
    realestate = filter_by_country(RealEstate.objects.filter(discount_filter))
    books = filter_by_country(BooksEducation.objects.filter(discount_filter))
    health = filter_by_country(HealthBeauty.objects.filter(discount_filter))
    household = filter_by_country(HouseholdAccessories.objects.filter(discount_filter))
    autos = filter_by_country(Automobiles.objects.filter(discount_filter))
    furniture = filter_by_country(FurnitureAppliances.objects.filter(discount_filter))
    pcs = filter_by_country(PCsPeripherals.objects.filter(discount_filter))
    musical = filter_by_country(MusicalInstruments.objects.filter(discount_filter))
    mobiles = filter_by_country(MobileDevicesAccessories.objects.filter(discount_filter))
    electronics = filter_by_country(ElectronicsAppliances.objects.filter(discount_filter))
    fashion = filter_by_country(FashionwearAddons.objects.filter(discount_filter))
    tools = filter_by_country(ToolsMachinery.objects.filter(discount_filter))
    cameras = filter_by_country(CamerasAccessories.objects.filter(discount_filter))
    

    def tag(qs, name):
        # Add a category attribute for each object for template use
        for obj in qs:
            obj.category = name
        return qs

    # Combine all discounted listings and tag with category
    combined = list(chain(
        tag(realestate, "Real Estate"),
        tag(books, "Books"),
        tag(health, "Health & Beauty"),
        tag(household, "Household"),
        tag(autos, "Automobiles"),
        tag(furniture, "Furniture"),
        tag(pcs, "PCs"),
        tag(musical, "Musical Instruments"),
        tag(mobiles, "Mobile Devices"),
        tag(electronics, "Electronics"),
        tag(fashion, "Fashionwear"),
        tag(tools, "Tools & Machinery"),
        tag(cameras, "Cameras & Accessories"),
    ))

    # Sort combined list by discount percentage descending and by listed_date descending
    combined_discounted = sorted(combined, key=lambda x: getattr(x, 'discount_percentage', 0), reverse=True)
    newly_posted = sorted(combined, key=lambda x: getattr(x, 'listed_date', None), reverse=True)

    post_categories = settings.POST_CATEGORIES or []

    # Instantiate forms for each category for use in templates
    forms = {cat['id']: get_form_class(cat['id'])() for cat in post_categories if get_form_class(cat['id'])}

    def count_and_order(model):
        qs = filter_by_country(model.objects.all())
        return qs.order_by('-listed_date'), qs.count()

    # Querysets and counts for each category
    real_estate_qs, real_estate_count = count_and_order(RealEstate)
    autos_qs, autos_count = count_and_order(Automobiles)
    books_qs, books_count = count_and_order(BooksEducation)
    health_qs, health_count = count_and_order(HealthBeauty)
    household_qs, household_count = count_and_order(HouseholdAccessories)
    furniture_qs, furniture_count = count_and_order(FurnitureAppliances)
    pcs_qs, pcs_count = count_and_order(PCsPeripherals)
    musical_qs, musical_count = count_and_order(MusicalInstruments)
    mobiles_qs, mobiles_count = count_and_order(MobileDevicesAccessories)
    electronics_qs, electronics_count = count_and_order(ElectronicsAppliances)
    fashion_qs, fashion_count = count_and_order(FashionwearAddons)
    tools_qs, tools_count = count_and_order(ToolsMachinery)
    cameras_qs, cameras_count = count_and_order(CamerasAccessories)

    # Active users (non-superuser)
    active_users = User.objects.filter(is_active=True, is_superuser=False)

    # Wishlist count for authenticated user
    wishlist_count = Wishlist.objects.filter(user=request.user).count() if request.user.is_authenticated else 0

    # Active Ads filtered by country, newest first
    ads = filter_by_country(Ads.objects.filter(is_active=True)).order_by('-created_at')
    user_reviews_top = user_reviews_top = Comment.objects.filter(rating__isnull=False,parent__isnull=True).select_related('user_profile').order_by('-rating')[:5]
    average_rating = user_reviews_top.aggregate(avg=Avg('rating'))['avg'] or 0
    total_reviews = user_reviews_top.count()

    full_stars = int(floor(average_rating))
    half_star = 1 if (average_rating - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star

    return {
        # Querysets for listings
        'real_estate': real_estate_qs.order_by('?'),  # Random order
        'real_estate_discounted': real_estate_qs.order_by('-discount_percentage')[:6],
        'real_estates_count': real_estate_count,
        'real_estate_listed_date': real_estate_qs.filter(is_available=True).order_by('-listed_date')[:6],

        'automobiles': autos_qs,
        'automobiles_count': autos_count,

        'books_education': books_qs,
        'books_education_count': books_count,

        'health_beauty': health_qs,
        'health_beauty_count': health_count,

        'household_accessories': household_qs,
        'household_accessories_count': household_count,

        'furniture_appliances': furniture_qs,
        'furniture_appliances_count': furniture_count,

        'pcs_peripherals': pcs_qs,
        'pcs_peripherals_count': pcs_count,

        'musical_instruments': musical_qs,
        'musical_instruments_count': musical_count,

        'mobile_devices': mobiles_qs,
        'mobile_devices_count': mobiles_count,

        'electronics_appliances': electronics_qs,
        'electronics_appliances_count': electronics_count,

        'fashion_wear': fashion_qs.filter(is_available=True).order_by('-listed_date')[:6],
        'fashion_wear_discounted': fashion_qs.order_by('-discount_percentage')[:6],
        'fashion_wear_count': fashion_count,

        'tools_machinery': tools_qs,
        'tools_machinery_count': tools_count,

        'cameras_accessories': cameras_qs,
        'cameras_accessories_count': cameras_count,

        # Combined listings
        'combined_discount': combined_discounted,
        'newly_posted': newly_posted,

        # User and wishlist info
        'user_profile': active_users,
        'wishlist_count': wishlist_count,

        # Post category forms and settings
        'listing_types': list(forms.keys()),
        'post_categories': post_categories,
        'forms': forms,

        # Ads and location info
        'Ads': ads,
        'country_code': country_filter,
        'country_currency': currency_symbol,
        'user_reviews_toped': user_reviews_top,
        'average_rating': average_rating,
        'total_reviews': total_reviews,
        'full_stars': full_stars,
        'half_star': half_star,
        'empty_stars': empty_stars,
    }
