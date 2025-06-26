from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from itertools import chain
from random import shuffle
from MainApp.maps import MODEL_MAP, TEMPLATE_MAP
from MainApp.forms import (
    RealEstateForm, BooksEducationForm, HealthBeautyForm, HouseholdAccessoriesForm,
    AutomobilesForm, FurnitureAppliancesForm, PCsPeripheralsForm, MusicalInstrumentsForm,
    MobileDevicesAccessoriesForm, ElectronicsAppliancesForm, FashionwearAddonsForm,
    ToolsMachineryForm, CamerasAccessoriesForm,FoodBeveragesForm,
)
from MainApp.models import (
    RealEstate, BooksEducation, HealthBeauty, HouseholdAccessories, Automobiles,
    FurnitureAppliances, PCsPeripherals, MusicalInstruments, MobileDevicesAccessories,
    ElectronicsAppliances, FashionwearAddons, ToolsMachinery, CamerasAccessories,
    Wishlist,FoodBeverages,
)
from django.contrib.auth.decorators import login_required

from math import floor

from django.db.models import Avg

from RatingReviews.models import Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import re
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin
from MainApp.maps import MODEL_MAP
from django.http import Http404, HttpResponseBadRequest
from django.apps import apps
from MainApp.utils import get_location_info
from django.db.models import Q
MODEL_MAP = {
    "realestate": ("realestate", "MainApp.RealEstate"),
    "bookseducation": ("books_education", "MainApp.BooksEducation"),
    "healthbeauty": ("health_beauty", "MainApp.HealthBeauty"),
    "householdaccessories": ("household_accessories", "MainApp.HouseholdAccessories"),
    "automobiles": ("automobiles", "MainApp.Automobiles"),
    "furnitureappliances": ("furniture_appliances", "MainApp.FurnitureAppliances"),
    "pcsperipherals": ("pcs_peripherals", "MainApp.PCsPeripherals"),
    "musicalinstruments": ("musical_instruments", "MainApp.MusicalInstruments"),
    "mobiledevicesaccessories": ("mobile_devices_accessories", "MainApp.MobileDevicesAccessories"),
    "electronicsappliances": ("electronics_appliances", "MainApp.ElectronicsAppliances"),
    "fashionwearaddons": ("fashionwear_addons", "MainApp.FashionwearAddons"),
    "toolsmachinery": ("tools_machinery", "MainApp.ToolsMachinery"),
    "camerasaccessories": ("cameras_accessories", "MainApp.CamerasAccessories"),
    "foodbeverages": ("food_beverages", "MainApp.FoodBeverages"),
}


def shop(request):
    
    return render(request, "MainApp/realestate/realestate_details.html")

from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from itertools import chain
from random import shuffle
from django.db.models import Q
from MainApp.models import (
    RealEstate, BooksEducation, HealthBeauty, HouseholdAccessories, Automobiles,
    FurnitureAppliances, PCsPeripherals, MusicalInstruments, MobileDevicesAccessories,
    ElectronicsAppliances, FashionwearAddons, ToolsMachinery, CamerasAccessories,BaseListing
)

from MainApp.utils import get_location_info
from django.conf import settings
import re
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

# Make sure get_location_info is imported or defined somewhere
# from your_module import get_location_info

class RealEstateListView(View):
    def clean_price(self, price_str):
        if not price_str:
            return None
        # Remove all non-digit characters
        cleaned = re.sub(r'\D', '', price_str)  # Keep only digits
        try:
            return int(cleaned)
        except ValueError:
            return None

    def filter_qs(self, qs, user_country, min_price, max_price, condition):
        if user_country:
            qs = qs.filter(country__iexact=user_country)
        if min_price is not None:
            qs = qs.filter(Q(discount_price__gte=min_price) | Q(real_price__gte=min_price))
        if max_price is not None:
            qs = qs.filter(Q(discount_price__lte=max_price) | Q(real_price__lte=max_price))
        if condition and condition != 'Good':
            qs = qs.filter(realestate_condition=condition)  # <-- field name here
        return qs

    def tag(self, qs, name):
        for obj in qs:
            obj.category = name
        return qs

    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        # Accept parameters from both GET and POST
        data = request.GET if request.method == "GET" else request.POST

        raw_min_price = data.get('minamount')
        raw_max_price = data.get('maxamount')
        condition = data.get('condition')
        user_country = data.get('country') or get_location_info().get('country')

        print("Min Price:", raw_min_price)
        print("Max Price:", raw_max_price)
        print("Condition:", condition)
        print("User Country:", user_country)

        min_price = self.clean_price(raw_min_price)
        max_price = self.clean_price(raw_max_price)
        print("Cleaned Min Price:", min_price)
        print("Cleaned Max Price:", max_price)

        # Apply filters
        realestate_qs = self.filter_qs(RealEstate.objects.all(), user_country, min_price, max_price, condition)

        combined = list(chain(
            self.tag(realestate_qs, "Real Estate"),
        ))

        sort_by = request.GET.get('sort_by', 'latest')

        def safe_get(obj, attr, default=None):
            return getattr(obj, attr, default)

        if sort_by == "latest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'), reverse=True)
        elif sort_by == "oldest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'))
        elif sort_by == "price_low_high":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0))
        elif sort_by == "price_high_low":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0), reverse=True)
        elif sort_by == "name_asc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower())
        elif sort_by == "name_desc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower(), reverse=True)
        elif sort_by == "random":
            shuffle(combined)

        paginator = Paginator(combined, 30)
        page_number = request.GET.get('page', 1)

        try:
            combined_page = paginator.page(page_number)
        except PageNotAnInteger:
            combined_page = paginator.page(1)
        except EmptyPage:
            combined_page = paginator.page(paginator.num_pages)

        post_categories = settings.POST_CATEGORIES
        forms = {cat['id']: get_form_class(cat['id'])() for cat in post_categories}

        return render(request, "MainApp/realestate/realestate_list.html", {
            "post_categories": post_categories,
            "forms": forms,
            "all_listings": combined_page,
            "normal": "hero-normal",
            "real_estates": realestate_qs,
            "combined_count": len(combined),
        })





class ToolsMachineryListView(View):
    def clean_price(self, price_str):
        if not price_str:
            return None
        cleaned = re.sub(r'\D', '', price_str)
        try:
            return int(cleaned)
        except ValueError:
            return None

    def filter_qs(self, qs, user_country, min_price, max_price, condition, power_source, tool_type):
        if user_country:
            qs = qs.filter(country__iexact=user_country)
        if min_price is not None:
            qs = qs.filter(Q(discount_price__gte=min_price) | Q(real_price__gte=min_price))
        if max_price is not None:
            qs = qs.filter(Q(discount_price__lte=max_price) | Q(real_price__lte=max_price))
        if condition and condition != "Good":
            qs = qs.filter(condition=condition)
        if power_source:
            qs = qs.filter(power_source__iexact=power_source)
        if tool_type:
            qs = qs.filter(tool_type__iexact=tool_type)
        return qs

    def tag(self, qs, name):
        for obj in qs:
            obj.category = name
        return qs

    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        data = request.GET if request.method == "GET" else request.POST

        raw_min_price = data.get('minamount')
        raw_max_price = data.get('maxamount')
        condition = data.get('condition')
        power_source = data.get('power_source')
        tool_type = data.get('tool_type')
        user_country = data.get('country') or get_location_info().get('country')

        min_price = self.clean_price(raw_min_price)
        max_price = self.clean_price(raw_max_price)

        tools_qs = self.filter_qs(
            ToolsMachinery.objects.all(),
            user_country,
            min_price,
            max_price,
            condition,
            power_source,
            tool_type
        )

        combined = list(chain(self.tag(tools_qs, "Tools & Machinery")))

        sort_by = request.GET.get('sort_by', 'latest')

        def safe_get(obj, attr, default=None):
            return getattr(obj, attr, default)

        if sort_by == "latest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'), reverse=True)
        elif sort_by == "oldest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'))
        elif sort_by == "price_low_high":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0))
        elif sort_by == "price_high_low":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0), reverse=True)
        elif sort_by == "name_asc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower())
        elif sort_by == "name_desc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower(), reverse=True)
        elif sort_by == "random":
            shuffle(combined)

        paginator = Paginator(combined, 30)
        page_number = request.GET.get('page', 1)

        try:
            combined_page = paginator.page(page_number)
        except PageNotAnInteger:
            combined_page = paginator.page(1)
        except EmptyPage:
            combined_page = paginator.page(paginator.num_pages)

        post_categories = settings.POST_CATEGORIES
        forms = {cat['id']: get_form_class(cat['id'])() for cat in post_categories}

        return render(request, "MainApp/tools/tools_list.html", {
            "post_categories": post_categories,
            "forms": forms,
            "all_listings": combined_page,
            "normal": "hero-normal",
            "tools_list": tools_qs,
            "combined_count": len(combined),
            "power_source_choices": ToolsMachinery.POWER_SOURCE_CHOICES,
            "condition_choices": ToolsMachinery.CONDITION_CHOICES,
            "tool_type_choices": ToolsMachinery.TOOL_TYPE_CHOICES,
        })




class FashionListView(View):
    def filter_qs(self, qs, filters):
        """
        filters: dict with keys like category, size, gender, color, material
        """
        category = filters.get('category')
        size = filters.get('size')
        gender = filters.get('gender')
        color = filters.get('color')
        material = filters.get('material')

        if category:
            qs = qs.filter(category=category)
        if size:
            qs = qs.filter(size=size)
        if gender:
            qs = qs.filter(gender=gender)
        if color:
            qs = qs.filter(color=color)
        if material:
            qs = qs.filter(material=material)

        return qs

    def tag(self, qs, name):
        for obj in qs:
            obj.category_tag = name
        return qs

    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        data = request.GET if request.method == "GET" else request.POST

        # Extract filters
        filters = {
            'category': data.get('category'),
            'size': data.get('size'),
            'gender': data.get('gender'),
            'color': data.get('color'),
            'material': data.get('material'),
        }

        fashion_qs = self.filter_qs(FashionwearAddons.objects.all(), filters)

        combined = list(chain(
            self.tag(fashion_qs, "Fashion"),
        ))

        sort_by = data.get('sort_by', 'latest')

        def safe_get(obj, attr, default=None):
            return getattr(obj, attr, default)

        if sort_by == "latest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'), reverse=True)
        elif sort_by == "oldest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'))
        elif sort_by == "price_low_high":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0))
        elif sort_by == "price_high_low":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0), reverse=True)
        elif sort_by == "name_asc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower())
        elif sort_by == "name_desc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower(), reverse=True)
        elif sort_by == "random":
            shuffle(combined)

        paginator = Paginator(combined, 30)
        page_number = data.get('page', 1)

        try:
            combined_page = paginator.page(page_number)
        except PageNotAnInteger:
            combined_page = paginator.page(1)
        except EmptyPage:
            combined_page = paginator.page(paginator.num_pages)

        post_categories = settings.POST_CATEGORIES
        forms = {cat['id']: get_form_class(cat['id'])() for cat in post_categories}

        return render(request, "MainApp/fashion/fashion_list.html", {
            "post_categories": post_categories,
            "forms": forms,
            "all_listings": combined_page,
            "normal": "hero-normal",
            "fashion_items": fashion_qs,
            "combined_count": len(combined),

            # Pass choice lists for filters (optional, if you want to use in template)
            "category_choices": FashionwearAddons.CategoryChoices.choices,
            "size_choices": FashionwearAddons.SizeChoices.choices,
            "gender_choices": FashionwearAddons.GenderChoices.choices,
            "color_choices": FashionwearAddons.ColorChoices.choices,
            "material_choices": FashionwearAddons.MATERIAL_CHOICES,
        })


class GenericProductDetailView(View):
    def get(self, request, model_name, pk):
        entry = MODEL_MAP.get(model_name.lower())
        template = TEMPLATE_MAP.get(model_name.lower())

        if not entry or not template:
            return render(request, '404.html', status=404)

        field_name, model_path = entry
        try:
            app_label, model_class_name = model_path.split(".")
            model = apps.get_model(app_label, model_class_name)
        except Exception:
            return render(request, '404.html', status=404)

        instance = get_object_or_404(model, pk=pk)
        instance.views += 1
        instance.save()

        return render(request, template, {
            'product': instance,
            'product_type': model_name.lower(),
        })



class CamerasListView(View):
    def filter_qs(self, qs, filters):
        brand = filters.get('brand')
        condition = filters.get('condition')

        if brand:
            qs = qs.filter(brand=brand)
        if condition:
            qs = qs.filter(condition=condition)

        return qs

    def tag(self, qs, name):
        for obj in qs:
            obj.category_tag = name
        return qs

    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        data = request.GET if request.method == "GET" else request.POST

        filters = {
            'brand': data.get('brand'),
            'condition': data.get('condition'),
        }
        print("Applied Filters:", filters)
        cameras_qs = self.filter_qs(CamerasAccessories.objects.all(), filters)

        combined = list(chain(
            self.tag(cameras_qs, "Camera"),
        ))

        sort_by = data.get('sort_by', 'latest')

        def safe_get(obj, attr, default=None):
            return getattr(obj, attr, default)

        if sort_by == "latest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'), reverse=True)
        elif sort_by == "oldest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'))
        elif sort_by == "price_low_high":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0))
        elif sort_by == "price_high_low":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0), reverse=True)
        elif sort_by == "name_asc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower())
        elif sort_by == "name_desc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower(), reverse=True)
        elif sort_by == "random":
            shuffle(combined)

        paginator = Paginator(combined, 30)
        page_number = data.get('page', 1)

        try:
            combined_page = paginator.page(page_number)
        except PageNotAnInteger:
            combined_page = paginator.page(1)
        except EmptyPage:
            combined_page = paginator.page(paginator.num_pages)

        post_categories = settings.POST_CATEGORIES
        forms = {cat['id']: get_form_class(cat['id'])() for cat in post_categories}

        return render(request, "MainApp/cameras/cameras_list.html", {
            "post_categories": post_categories,
            "forms": forms,
            "all_listings": combined_page,
            "normal": "hero-normal",
            "camera_items": cameras_qs,
            "combined_count": len(combined),
            "brand_choices": CamerasAccessories.BRAND_CHOICES,
            "condition_choices": CamerasAccessories.CONDITION_CHOICES,
        })



class ElectronicsAppliancesListView(View):
    def filter_qs(self, qs, filters):
        brand = filters.get('brand')
        condition = filters.get('condition')
        appliance_type = filters.get('appliance_type')

        if brand:
            qs = qs.filter(brand=brand)
        if condition:
            qs = qs.filter(condition=condition)
        if appliance_type:
            qs = qs.filter(appliance_type=appliance_type)

        return qs

    def tag(self, qs, name):
        for obj in qs:
            obj.category_tag = name
        return qs

    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        data = request.GET if request.method == "GET" else request.POST

        filters = {
            'brand': data.get('brand'),
            'condition': data.get('condition'),
            'appliance_type': data.get('appliance_type'),
        }
        print("Applied Filters:", filters)
        electronics_qs = self.filter_qs(ElectronicsAppliances.objects.all(), filters)

        combined = list(chain(
            self.tag(electronics_qs, "Electronics"),
        ))

        sort_by = data.get('sort_by', 'latest')

        def safe_get(obj, attr, default=None):
            return getattr(obj, attr, default)

        if sort_by == "latest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'), reverse=True)
        elif sort_by == "oldest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'))
        elif sort_by == "price_low_high":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0))
        elif sort_by == "price_high_low":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0), reverse=True)
        elif sort_by == "name_asc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower())
        elif sort_by == "name_desc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower(), reverse=True)
        elif sort_by == "random":
            shuffle(combined)

        paginator = Paginator(combined, 30)
        page_number = data.get('page', 1)

        try:
            combined_page = paginator.page(page_number)
        except PageNotAnInteger:
            combined_page = paginator.page(1)
        except EmptyPage:
            combined_page = paginator.page(paginator.num_pages)

        post_categories = settings.POST_CATEGORIES
        forms = {cat['id']: get_form_class(cat['id'])() for cat in post_categories}

        return render(request, "MainApp/electronics/electronics_list.html", {
            "post_categories": post_categories,
            "forms": forms,
            "all_listings": combined_page,
            "normal": "hero-normal",
            "electronics_items": electronics_qs,
            "combined_count": len(combined),
            "brand_choices": ElectronicsAppliances.BRAND_CHOICES,
            "condition_choices": ElectronicsAppliances.CONDITION_CHOICES,
            "appliance_type_choices": ElectronicsAppliances.APPLIANCE_TYPE_CHOICES,
        })




class MobileDevicesAccessoriesListView(View):
    def clean_price(self, price_str):
        if not price_str:
            return None
        cleaned = re.sub(r'\D', '', price_str)
        try:
            return int(cleaned)
        except ValueError:
            return None

    def filter_qs(self, qs, filters):
        brand = filters.get('brand')
        condition = filters.get('condition')
        min_price = filters.get('min_price')
        max_price = filters.get('max_price')

        # Print filters applied for debugging
        print(f"Filters applied -> Brand: {brand}, Condition: {condition}, Min Price: {min_price}, Max Price: {max_price}")

        if brand:
            qs = qs.filter(brand=brand)
            print(f"After brand filter count: {qs.count()}")
        if condition:
            qs = qs.filter(condition=condition)
            print(f"After condition filter count: {qs.count()}")
        if min_price is not None:
            qs = qs.filter(discount_price__gte=min_price)
            print(f"After min_price filter count: {qs.count()}")
        if max_price is not None:
            qs = qs.filter(discount_price__lte=max_price)
            print(f"After max_price filter count: {qs.count()}")

        print(f"Final queryset count after all filters: {qs.count()}")
        return qs

    def tag(self, qs, name):
        for obj in qs:
            obj.category_tag = name
        return qs

    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        data = request.GET if request.method == "GET" else request.POST

        filters = {
            'brand': data.get('brand'),
            'condition': data.get('condition'),
            'min_price': self.clean_price(data.get('minamount')),
            'max_price': self.clean_price(data.get('maxamount')),
        }

        mobile_qs = self.filter_qs(MobileDevicesAccessories.objects.all(), filters)
        combined = list(chain(self.tag(mobile_qs, "Mobile Devices")))

        sort_by = data.get('sort_by', 'latest')

        def safe_get(obj, attr, default=None):
            return getattr(obj, attr, default)

        if sort_by == "latest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'), reverse=True)
        elif sort_by == "oldest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'))
        elif sort_by == "price_low_high":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0))
        elif sort_by == "price_high_low":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0), reverse=True)
        elif sort_by == "name_asc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower())
        elif sort_by == "name_desc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower(), reverse=True)
        elif sort_by == "random":
            shuffle(combined)

        paginator = Paginator(combined, 30)
        page_number = data.get('page', 1)

        try:
            combined_page = paginator.page(page_number)
        except PageNotAnInteger:
            combined_page = paginator.page(1)
        except EmptyPage:
            combined_page = paginator.page(paginator.num_pages)

        post_categories = settings.POST_CATEGORIES
        forms = {cat['id']: get_form_class(cat['id'])() for cat in post_categories}

        return render(request, "MainApp/mobiles/mobiles_list.html", {
            "post_categories": post_categories,
            "forms": forms,
            "all_listings": combined_page,
            "normal": "hero-normal",
            "mobile_items": mobile_qs,
            "combined_count": len(combined),
            "brand_choices": MobileDevicesAccessories.BRAND_CHOICES,
            "condition_choices": MobileDevicesAccessories.CONDITION_CHOICES,
        })





class FurnitureAppliancesListView(View):
    def clean_price(self, price_str):
        if not price_str:
            return None
        cleaned = re.sub(r'\D', '', price_str)
        try:
            return int(cleaned)
        except ValueError:
            return None

    def filter_qs(self, qs, filters):
        brand = filters.get('brand')
        condition = filters.get('condition')
        furniture_type = filters.get('furniture_type')
        min_price = filters.get('min_price')
        max_price = filters.get('max_price')

        print(f"Filters applied -> Brand: {brand}, Condition: {condition}, Type: {furniture_type}, Min Price: {min_price}, Max Price: {max_price}")

        if brand:
            qs = qs.filter(brand=brand)
            print(f"After brand filter count: {qs.count()}")
        if condition:
            qs = qs.filter(condition=condition)
            print(f"After condition filter count: {qs.count()}")
        if furniture_type:
            qs = qs.filter(furniture_type=furniture_type)
            print(f"After type filter count: {qs.count()}")
        if min_price is not None:
            qs = qs.filter(discount_price__gte=min_price)
            print(f"After min_price filter count: {qs.count()}")
        if max_price is not None:
            qs = qs.filter(discount_price__lte=max_price)
            print(f"After max_price filter count: {qs.count()}")

        print(f"Final queryset count after all filters: {qs.count()}")
        return qs

    def tag(self, qs, name):
        for obj in qs:
            obj.category_tag = name
        return qs

    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        data = request.GET if request.method == "GET" else request.POST

        filters = {
            'brand': data.get('brand'),
            'condition': data.get('condition'),
            'furniture_type': data.get('furniture_type'),
            'min_price': self.clean_price(data.get('minamount')),
            'max_price': self.clean_price(data.get('maxamount')),
        }

        furniture_qs = self.filter_qs(FurnitureAppliances.objects.all(), filters)
        combined = list(chain(self.tag(furniture_qs, "Furniture & Appliances")))

        sort_by = data.get('sort_by', 'latest')

        def safe_get(obj, attr, default=None):
            return getattr(obj, attr, default)

        if sort_by == "latest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'), reverse=True)
        elif sort_by == "oldest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'))
        elif sort_by == "price_low_high":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0))
        elif sort_by == "price_high_low":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0), reverse=True)
        elif sort_by == "name_asc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower())
        elif sort_by == "name_desc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower(), reverse=True)
        elif sort_by == "random":
            shuffle(combined)

        paginator = Paginator(combined, 30)
        page_number = data.get('page', 1)

        try:
            combined_page = paginator.page(page_number)
        except PageNotAnInteger:
            combined_page = paginator.page(1)
        except EmptyPage:
            combined_page = paginator.page(paginator.num_pages)

        post_categories = settings.POST_CATEGORIES
        forms = {cat['id']: get_form_class(cat['id'])() for cat in post_categories}

        return render(request, "MainApp/furniture/furniture_list.html", {
            "post_categories": post_categories,
            "forms": forms,
            "all_listings": combined_page,
            "normal": "hero-normal",
            "furniture_items": furniture_qs,
            "combined_count": len(combined),
            "condition_choices": FurnitureAppliances.CONDITION_CHOICES,
            "furniture_type_choices": FurnitureAppliances.FURNITURE_TYPE_CHOICES,
        })




class AutomobilesListView(View):
    def filter_qs(self, qs, filters):
        brand = filters.get('brand')
        condition = filters.get('condition')
        vehicle_type = filters.get('vehicle_type')

        if brand:
            qs = qs.filter(brand=brand)
        if condition:
            qs = qs.filter(condition=condition)
        if vehicle_type:
            qs = qs.filter(vehicle_type=vehicle_type)

        return qs

    def tag(self, qs, name):
        for obj in qs:
            obj.category_tag = name
        return qs

    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        data = request.GET if request.method == "GET" else request.POST

        filters = {
            'brand': data.get('brand'),
            'condition': data.get('condition'),
            'vehicle_type': data.get('vehicle_type'),
        }
        print("Applied Filters:", filters)
        automobile_qs = self.filter_qs(Automobiles.objects.all(), filters)

        combined = list(chain(
            self.tag(automobile_qs, "Automobiles"),
        ))

        sort_by = data.get('sort_by', 'latest')

        def safe_get(obj, attr, default=None):
            return getattr(obj, attr, default)

        if sort_by == "latest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'), reverse=True)
        elif sort_by == "oldest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'))
        elif sort_by == "price_low_high":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0))
        elif sort_by == "price_high_low":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0), reverse=True)
        elif sort_by == "name_asc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower())
        elif sort_by == "name_desc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower(), reverse=True)
        elif sort_by == "random":
            shuffle(combined)

        paginator = Paginator(combined, 30)
        page_number = data.get('page', 1)

        try:
            combined_page = paginator.page(page_number)
        except PageNotAnInteger:
            combined_page = paginator.page(1)
        except EmptyPage:
            combined_page = paginator.page(paginator.num_pages)

        post_categories = settings.POST_CATEGORIES
        forms = {cat['id']: get_form_class(cat['id'])() for cat in post_categories}

        return render(request, "MainApp/automobiles/automobiles_list.html", {
            "post_categories": post_categories,
            "forms": forms,
            "all_listings": combined_page,
            "normal": "hero-normal",
            "automobile_items": automobile_qs,
            "combined_count": len(combined),
            "brand_choices": Automobiles.BRAND_CHOICES,
            "condition_choices": Automobiles.CONDITION_CHOICES,
            "vehicle_type_choices": Automobiles.VEHICLE_TYPE_CHOICES,
        })



class MusicalInstrumentsListView(View):
    def filter_qs(self, qs, filters):
        brand = filters.get('brand')
        condition = filters.get('condition')
        instrument_type = filters.get('instrument_type')

        if brand:
            qs = qs.filter(brand=brand)
        if condition:
            qs = qs.filter(condition=condition)
        if instrument_type:
            qs = qs.filter(instrument_type=instrument_type)

        return qs

    def tag(self, qs, name):
        for obj in qs:
            obj.category_tag = name
        return qs

    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        data = request.GET if request.method == "GET" else request.POST

        filters = {
            'brand': data.get('brand'),
            'condition': data.get('condition'),
            'instrument_type': data.get('instrument_type'),
        }

        print("Applied Filters:", filters)

        music_qs = self.filter_qs(MusicalInstruments.objects.all(), filters)

        combined = list(chain(self.tag(music_qs, "Musical Instruments")))

        sort_by = data.get('sort_by', 'latest')

        def safe_get(obj, attr, default=None):
            return getattr(obj, attr, default)

        if sort_by == "latest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'), reverse=True)
        elif sort_by == "oldest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'))
        elif sort_by == "price_low_high":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price') or 0)
        elif sort_by == "price_high_low":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price') or 0, reverse=True)
        elif sort_by == "name_asc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower())
        elif sort_by == "name_desc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower(), reverse=True)
        elif sort_by == "random":
            shuffle(combined)

        paginator = Paginator(combined, 30)
        page_number = data.get('page', 1)

        try:
            combined_page = paginator.page(page_number)
        except PageNotAnInteger:
            combined_page = paginator.page(1)
        except EmptyPage:
            combined_page = paginator.page(paginator.num_pages)

        post_categories = settings.POST_CATEGORIES
        forms = {cat['id']: get_form_class(cat['id'])() for cat in post_categories}

        return render(request, "MainApp/music/music_list.html", {
            "post_categories": post_categories,
            "forms": forms,
            "all_listings": combined_page,
            "normal": "hero-normal",
            "musical_items": music_qs,
            "combined_count": len(combined),
            "brand_choices": getattr(MusicalInstruments, "BRAND_CHOICES", []),
            "condition_choices": getattr(MusicalInstruments, "CONDITION_CHOICES", []),
            "instrument_type_choices": getattr(MusicalInstruments, "INSTRUMENT_TYPE_CHOICES", []),
        })
    



class HealthBeautyListView(View):
    def filter_qs(self, qs, filters):
        condition = filters.get('condition')
        product_type = filters.get('product_type')
        brand = filters.get('brand')

        if condition:
            qs = qs.filter(condition=condition)
        if product_type:
            qs = qs.filter(product_type=product_type)
        if brand:
            qs = qs.filter(brand=brand)

        return qs

    def tag(self, qs, name):
        for obj in qs:
            obj.category_tag = name
        return qs

    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        data = request.GET if request.method == "GET" else request.POST

        filters = {
            'condition': data.get('condition'),
            'product_type': data.get('product_type'),
            'brand': data.get('brand'),
        }

        print("Applied Filters:", filters)

        qs = HealthBeauty.objects.all()
        health_qs = self.filter_qs(qs, filters)
        combined = list(chain(self.tag(health_qs, "Health & Beauty")))

        sort_by = data.get('sort_by', 'latest')

        def safe_get(obj, attr, default=None):
            return getattr(obj, attr, default)

        if sort_by == "latest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'), reverse=True)
        elif sort_by == "oldest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'))
        elif sort_by == "price_low_high":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0))
        elif sort_by == "price_high_low":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0), reverse=True)
        elif sort_by == "name_asc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower())
        elif sort_by == "name_desc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower(), reverse=True)
        elif sort_by == "random":
            shuffle(combined)

        paginator = Paginator(combined, 30)
        page_number = data.get('page', 1)

        try:
            combined_page = paginator.page(page_number)
        except PageNotAnInteger:
            combined_page = paginator.page(1)
        except EmptyPage:
            combined_page = paginator.page(paginator.num_pages)

        post_categories = settings.POST_CATEGORIES
        forms = {cat['id']: get_form_class(cat['id'])() for cat in post_categories}

        return render(request, "MainApp/health/health_list.html", {
            "post_categories": post_categories,
            "forms": forms,
            "all_listings": combined_page,
            "normal": "hero-normal",
            "health_items": health_qs,
            "combined_count": len(combined),
            "condition_choices": HealthBeauty.CONDITION_CHOICES,
            "product_type_choices": HealthBeauty.PRODUCT_TYPE_CHOICES,
            "brand_choices": HealthBeauty.BRAND_CHOICES,
        })



    
class PCsPeripheralsListView(View):
    def filter_qs(self, qs, filters):
        brand = filters.get('brand')
        condition = filters.get('condition')
        pc_type = filters.get('pc_type')

        if brand:
            qs = qs.filter(brand=brand)
        if condition:
            qs = qs.filter(condition=condition)
        if pc_type:
            qs = qs.filter(pc_type=pc_type)

        return qs

    def tag(self, qs, name):
        for obj in qs:
            obj.category_tag = name
        return qs

    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        data = request.GET if request.method == "GET" else request.POST

        filters = {
            'brand': data.get('brand'),
            'condition': data.get('condition'),
            'pc_type': data.get('pc_type'),
        }

        print("Applied Filters:", filters)

        pc_qs = self.filter_qs(PCsPeripherals.objects.all(), filters)

        combined = list(chain(self.tag(pc_qs, "PCs & Peripherals")))

        sort_by = data.get('sort_by', 'latest')

        def safe_get(obj, attr, default=None):
            return getattr(obj, attr, default)

        if sort_by == "latest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'), reverse=True)
        elif sort_by == "oldest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'))
        elif sort_by == "price_low_high":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0))
        elif sort_by == "price_high_low":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0), reverse=True)
        elif sort_by == "name_asc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower())
        elif sort_by == "name_desc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower(), reverse=True)
        elif sort_by == "random":
            shuffle(combined)

        paginator = Paginator(combined, 30)
        page_number = data.get('page', 1)

        try:
            combined_page = paginator.page(page_number)
        except PageNotAnInteger:
            combined_page = paginator.page(1)
        except EmptyPage:
            combined_page = paginator.page(paginator.num_pages)

        post_categories = settings.POST_CATEGORIES
        forms = {cat['id']: get_form_class(cat['id'])() for cat in post_categories}

        return render(request, "MainApp/PcsAccessories/pc_list.html", {
            "post_categories": post_categories,
            "forms": forms,
            "all_listings": combined_page,
            "normal": "hero-normal",
            "pc_items": pc_qs,
            "combined_count": len(combined),
            "brand_choices": PCsPeripherals.BRAND_CHOICES,
            "condition_choices": PCsPeripherals.CONDITION_CHOICES,
            "pc_type_choices": PCsPeripherals.PC_TYPE_CHOICES,
        })

class BooksEducationListView(View):
    def filter_qs(self, qs, filters):
        condition = filters.get('condition')
        if condition:
            qs = qs.filter(condition=condition)
        return qs

    def tag(self, qs, name):
        for obj in qs:
            obj.category_tag = name
        return qs

    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        data = request.GET if request.method == "GET" else request.POST

        filters = {
            'condition': data.get('condition'),
        }

        print("Applied Filters:", filters)

        book_qs = self.filter_qs(BooksEducation.objects.all(), filters)
        combined = list(chain(self.tag(book_qs, "Books & Education")))

        sort_by = data.get('sort_by', 'latest')

        def safe_get(obj, attr, default=None):
            return getattr(obj, attr, default)

        if sort_by == "latest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'), reverse=True)
        elif sort_by == "oldest":
            combined.sort(key=lambda x: safe_get(x, 'listed_date'))
        elif sort_by == "price_low_high":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0))
        elif sort_by == "price_high_low":
            combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price', 0), reverse=True)
        elif sort_by == "name_asc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower())
        elif sort_by == "name_desc":
            combined.sort(key=lambda x: safe_get(x, 'title', '').lower(), reverse=True)
        elif sort_by == "random":
            shuffle(combined)

        paginator = Paginator(combined, 30)
        page_number = data.get('page', 1)

        try:
            combined_page = paginator.page(page_number)
        except PageNotAnInteger:
            combined_page = paginator.page(1)
        except EmptyPage:
            combined_page = paginator.page(paginator.num_pages)

        post_categories = settings.POST_CATEGORIES
        forms = {cat['id']: get_form_class(cat['id'])() for cat in post_categories}

        return render(request, "MainApp/Books/book_list.html", {
            "post_categories": post_categories,
            "forms": forms,
            "all_listings": combined_page,
            "normal": "hero-normal",
            "book_items": book_qs,
            "combined_count": len(combined),
            "condition_choices": BooksEducation.CONDITION_CHOICES,
        })

class ToggleWishListView(View):
    def get_model_and_field(self, product_type):
        if product_type not in MODEL_MAP:
            raise Http404("Invalid product type.")
        field_name, model_path = MODEL_MAP[product_type]
        model = apps.get_model(*model_path.split("."))
        return field_name, model

    def post(self, request, product_type, pk):
        field_name, model = self.get_model_and_field(product_type)
        product = get_object_or_404(model, pk=pk)

        filter_kwargs = {
            "user": request.user,
            field_name: product
        }

        wishlist_item = Wishlist.objects.filter(**filter_kwargs).first()

        if wishlist_item:
            wishlist_item.delete()
            in_wishlist = False
        else:
            Wishlist.objects.create(user=request.user, **{field_name: product})
            in_wishlist = True

        return render(request, "MainApp/partials/wishList.html", {
            "product": product,
            "product_type": product_type,
            "in_wishlist": in_wishlist,
        })

    def get(self, request, product_type, pk):
        field_name, model = self.get_model_and_field(product_type)
        product = get_object_or_404(model, pk=pk)

        filter_kwargs = {
            "user": request.user,
            field_name: product
        }

        in_wishlist = Wishlist.objects.filter(**filter_kwargs).exists()

        return render(request, "MainApp/partials/wishList.html", {
            "product": product,
            "product_type": product_type,
            "in_wishlist": in_wishlist,
        })




def home(request):
    country_filter = get_location_info()['country']

    def filter_by_country(qs):
        if country_filter:
            return qs.filter(country__iexact=country_filter)
        return qs

    # Filter all category querysets by country if filter provided
    realestate = filter_by_country(RealEstate.objects.all())
    books = filter_by_country(BooksEducation.objects.all())
    health = filter_by_country(HealthBeauty.objects.all())
    household = filter_by_country(HouseholdAccessories.objects.all())
    autos = filter_by_country(Automobiles.objects.all())
    furniture = filter_by_country(FurnitureAppliances.objects.all())
    pcs = filter_by_country(PCsPeripherals.objects.all())
    musical = filter_by_country(MusicalInstruments.objects.all())
    mobiles = filter_by_country(MobileDevicesAccessories.objects.all())
    electronics = filter_by_country(ElectronicsAppliances.objects.all())
    fashion = filter_by_country(FashionwearAddons.objects.all())
    tools = filter_by_country(ToolsMachinery.objects.all())
    cameras = filter_by_country(CamerasAccessories.objects.all())

    def tag(qs, name):
        for obj in qs:
            obj.category = name
        return qs

    combined = list(chain(
        tag(realestate, "Real Estate"),
        tag(books, "Books"),
        tag(health, "Health & Beauty"),
        tag(household, "Household"),
        tag(autos, "Automobiles"),
        tag(furniture, "Furniture"),
        tag(pcs, "PCs"),
        tag(musical, "Instruments"),
        tag(mobiles, "Mobiles"),
        tag(electronics, "Electronics"),
        tag(fashion, "Fashion"),
        tag(tools, "Tools"),
        tag(cameras, "Cameras"),
    ))

    sort_by = request.GET.get('sort_by', 'latest')

    def safe_get(obj, attr, default=None):
        return getattr(obj, attr, default)

    if sort_by == "latest":
        combined.sort(key=lambda x: safe_get(x, 'listed_date'), reverse=True)
    elif sort_by == "oldest":
        combined.sort(key=lambda x: safe_get(x, 'listed_date'))
    elif sort_by == "price_low_high":
        combined.sort(key=lambda x: safe_get(x, 'discount_price')
                      or safe_get(x, 'real_price', 0))
    elif sort_by == "price_high_low":
        combined.sort(key=lambda x: safe_get(x, 'discount_price')
                      or safe_get(x, 'real_price', 0), reverse=True)
    elif sort_by == "name_asc":
        combined.sort(key=lambda x: safe_get(x, 'title', '').lower())
    elif sort_by == "name_desc":
        combined.sort(key=lambda x: safe_get(
            x, 'title', '').lower(), reverse=True)
    elif sort_by == "random":
        shuffle(combined)

    paginator = Paginator(combined, 20)
    page_number = request.GET.get('page', 1)
    try:
        combined_page = paginator.page(page_number)
    except PageNotAnInteger:
        combined_page = paginator.page(1)
    except EmptyPage:
        combined_page = paginator.page(paginator.num_pages)

    post_categories = settings.POST_CATEGORIES
    forms = {cat['id']: get_form_class(cat['id'])() for cat in post_categories}

    return render(request, "MainApp/home.html", {
        "post_categories": post_categories,
        "forms": forms,
        "All_listening": combined_page,
        "normal": "hero-normal",
        "real_estates": realestate,
        "combined_count": len(combined),

    })


def tag(qs, name):
    for obj in qs:
        obj.category = name
    return qs

def is_in_wishlist(user, obj):
    model_name = obj.__class__.__name__.lower()
    filters = {"user": user}
    
    if model_name == "realestate":
        filters["realestate_id"] = obj.id
    elif model_name == "automobiles":
        filters["automobiles_id"] = obj.id
    elif model_name == "bookseducation":
        filters["books_education_id"] = obj.id
    elif model_name == "healthbeauty":
        filters["health_beauty_id"] = obj.id
    elif model_name == "householdaccessories":
        filters["household_accessories_id"] = obj.id
    elif model_name == "furnitureappliances":
        filters["furniture_appliances_id"] = obj.id
    elif model_name == "pcsperipherals":
        filters["pcs_peripherals_id"] = obj.id
    elif model_name == "musicalinstruments":
        filters["musical_instruments_id"] = obj.id
    elif model_name == "mobiledevicesaccessories":
        filters["mobile_devices_accessories_id"] = obj.id
    elif model_name == "electronicsappliances":
        filters["electronics_appliances_id"] = obj.id
    elif model_name == "fashionwearaddons":
        filters["fashionwear_addons_id"] = obj.id
    elif model_name == "toolsmachinery":
        filters["tools_machinery_id"] = obj.id
    elif model_name == "camerasaccessories":
        filters["cameras_accessories_id"] = obj.id
    else:
        # Model not in wishlist mapping, return False
        return False

    return Wishlist.objects.filter(**filters).exists()

def UserDetailsView(request, username):
    profile_user = get_object_or_404(User, username=username)
    country_filter = get_location_info().get('country')

    # ✅ Handle Review Submission
    if request.method == 'POST':
        text = request.POST.get('review_text')
        rating = request.POST.get('rating')

        # Print values to console
        print(f"Submitted review text: {text}")
        print(f"Submitted rating: {rating}")

        if text and rating:
            Comment.objects.create(
                user_profile=profile_user,
                user_name=request.user.get_full_name() or request.user.username,
                user_avatar=(
                    request.user.profile.profile_picture.url
                    if hasattr(request.user, 'profile') and request.user.profile.profile_picture
                    else ''
                ),
                text=text,
                rating=int(rating)
            )
            return redirect('user_details', username=profile_user.username)


    # Fetch existing reviews
    comments = Comment.objects.filter(user_profile=profile_user).order_by('-id')

    def filter_by_user_and_country(qs):
        qs = qs.filter(listed_by=profile_user)
        if country_filter:
            qs = qs.filter(country__iexact=country_filter)
        return qs

    listings = {
        "Real Estate": filter_by_user_and_country(RealEstate.objects.all()),
        "Books": filter_by_user_and_country(BooksEducation.objects.all()),
        "Health & Beauty": filter_by_user_and_country(HealthBeauty.objects.all()),
        "Household": filter_by_user_and_country(HouseholdAccessories.objects.all()),
        "Automobiles": filter_by_user_and_country(Automobiles.objects.all()),
        "Furniture": filter_by_user_and_country(FurnitureAppliances.objects.all()),
        "PCs": filter_by_user_and_country(PCsPeripherals.objects.all()),
        "Instruments": filter_by_user_and_country(MusicalInstruments.objects.all()),
        "Mobiles": filter_by_user_and_country(MobileDevicesAccessories.objects.all()),
        "Electronics": filter_by_user_and_country(ElectronicsAppliances.objects.all()),
        "Fashion": filter_by_user_and_country(FashionwearAddons.objects.all()),
        "Tools": filter_by_user_and_country(ToolsMachinery.objects.all()),
        "Cameras": filter_by_user_and_country(CamerasAccessories.objects.all()),
    }

    combined = list(chain.from_iterable(tag(qs, name) for name, qs in listings.items()))

    if request.user.is_authenticated:
        for item in combined:
            item.in_wishlist = is_in_wishlist(request.user, item)
    else:
        for item in combined:
            item.in_wishlist = False

    sort_by = request.GET.get('sort_by', 'latest')

    def safe_get(obj, attr, default=None):
        return getattr(obj, attr, default)

    if sort_by == "latest":
        combined.sort(key=lambda x: safe_get(x, 'listed_date'), reverse=True)
    elif sort_by == "oldest":
        combined.sort(key=lambda x: safe_get(x, 'listed_date'))
    elif sort_by == "price_low_high":
        combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price') or 0)
    elif sort_by == "price_high_low":
        combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price') or 0, reverse=True)
    elif sort_by == "name_asc":
        combined.sort(key=lambda x: safe_get(x, 'title', '').lower())
    elif sort_by == "name_desc":
        combined.sort(key=lambda x: safe_get(x, 'title', '').lower(), reverse=True)
    elif sort_by == "random":
        shuffle(combined)

    paginator = Paginator(combined, 20)
    page_number = request.GET.get('page', 1)
    try:
        combined_page = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        combined_page = paginator.page(1)

    post_categories = settings.POST_CATEGORIES
    forms = {cat['id']: get_form_class(cat['id'])() for cat in post_categories}
    average_rating = comments.aggregate(avg=Avg('rating'))['avg'] or 0
    total_reviews = comments.count()
    full_stars = int(floor(average_rating))
    half_star = 1 if (average_rating - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star

    return render(request, "MainApp/user/user_details.html", {
    "post_categories": post_categories,
    "forms": forms,
    "all_listings": combined_page,
    "normal": "hero-normal",
    "real_estates": listings["Real Estate"],
    "profile_user": profile_user,
    "combined_count": len(combined),
    "comments": comments,
    "average_rating": round(average_rating, 1),
    "total_reviews": total_reviews,
    "full_stars": full_stars,
    "half_star": half_star,
    "empty_stars": empty_stars,
})


@login_required
def wishlist_view(request):
    user = request.user
    user_wishlist = Wishlist.objects.filter(user=user)

    def fetch(model_name, model_cls, field_name, label):
        ids = user_wishlist.exclude(**{f"{field_name}__isnull": True}).values_list(f"{field_name}_id", flat=True)
        qs = model_cls.objects.filter(id__in=ids)
        for obj in qs:
            obj.category = label
        return qs

    combined = list(chain(
        fetch("realestate", RealEstate, "realestate", "Real Estate"),
        fetch("books_education", BooksEducation, "books_education", "Books"),
        fetch("health_beauty", HealthBeauty, "health_beauty", "Health & Beauty"),
        fetch("household_accessories", HouseholdAccessories, "household_accessories", "Household"),
        fetch("automobiles", Automobiles, "automobiles", "Automobiles"),
        fetch("furniture_appliances", FurnitureAppliances, "furniture_appliances", "Furniture"),
        fetch("pcs_peripherals", PCsPeripherals, "pcs_peripherals", "PCs"),
        fetch("musical_instruments", MusicalInstruments, "musical_instruments", "Instruments"),
        fetch("mobile_devices_accessories", MobileDevicesAccessories, "mobile_devices_accessories", "Mobiles"),
        fetch("electronics_appliances", ElectronicsAppliances, "electronics_appliances", "Electronics"),
        fetch("fashionwear_addons", FashionwearAddons, "fashionwear_addons", "Fashion"),
        fetch("tools_machinery", ToolsMachinery, "tools_machinery", "Tools"),
        fetch("cameras_accessories", CamerasAccessories, "cameras_accessories", "Cameras"),
        fetch("food_beverages", FoodBeverages, "food_beverages", "Food"),
    ))

    for item in combined:
        item.in_wishlist = True if user.is_authenticated else False

    # -------------------------
    # ✅ Filter Logic
    # -------------------------
    raw_min_price = request.GET.get('minamount')
    raw_max_price = request.GET.get('maxamount')
    condition = request.GET.get('condition')
    user_country = request.GET.get('country') or get_location_info()['country']

    minamount = clean_price(raw_min_price)
    maxamount = clean_price(raw_max_price)

    def matches_condition(item):
        return not condition or getattr(item, "condition", None) == condition

    def matches_price(item):
        price = getattr(item, "discount_price", None) or getattr(item, "real_price", None)
        try:
            if minamount is not None and price < minamount:
                return False
            if maxamount is not None and price > maxamount:
                return False
        except:
            return False
        return True

    combined = [item for item in combined if matches_condition(item) and matches_price(item)]

    # -------------------------
    # ✅ Sorting
    # -------------------------
    sort_by = request.GET.get('sort_by', 'latest')

    def safe_get(obj, attr, default=None):
        return getattr(obj, attr, default)

    if sort_by == "latest":
        combined.sort(key=lambda x: safe_get(x, 'listed_date') or 0, reverse=True)
    elif sort_by == "oldest":
        combined.sort(key=lambda x: safe_get(x, 'listed_date') or 0)
    elif sort_by == "price_low_high":
        combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price') or 0)
    elif sort_by == "price_high_low":
        combined.sort(key=lambda x: safe_get(x, 'discount_price') or safe_get(x, 'real_price') or 0, reverse=True)
    elif sort_by == "name_asc":
        combined.sort(key=lambda x: (safe_get(x, 'title') or '').lower())
    elif sort_by == "name_desc":
        combined.sort(key=lambda x: (safe_get(x, 'title') or '').lower(), reverse=True)
    elif sort_by == "random":
        shuffle(combined)

    # -------------------------
    # ✅ Pagination
    # -------------------------
    paginator = Paginator(combined, 20)
    page_number = request.GET.get('page', 1)
    try:
        combined_page = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        combined_page = paginator.page(1)

    return render(request, "MainApp/wishlist/wishlist.html", {
        "wishlist_items": combined_page,
        "combined_count": len(combined),
        "condition_choices": BaseListing.CONDITION_CHOICES,
        "sort_by": sort_by,
        "minamount": raw_min_price,
        "maxamount": raw_max_price,
        "selected_condition": condition,
        "country_filter": user_country,
    })


def clean_price(price_str):
    if not price_str:
        return None
    # Remove all non-digit characters including dot, then convert to int
    cleaned = re.sub(r'\D', '', price_str)  # Keep only digits
    try:
        return int(cleaned)
    except ValueError:
        return None


def filter_view(request):
    # Extract filters from GET
    raw_min_price = request.GET.get('minamount')
    raw_max_price = request.GET.get('maxamount')
    condition = request.GET.get('condition')
    user_country = request.GET.get('country') or get_location_info()['country']
    min_price = clean_price(raw_min_price)
    max_price = clean_price(raw_max_price)
    print("Min Price:", min_price)
    print("Max Price:", max_price)
    print("Condition:", condition)
    print("User Country:", user_country)

    def filter_qs(qs):
        if user_country:
            qs = qs.filter(country__iexact=user_country)

        if min_price:
            qs = qs.filter(
                Q(discount_price__gte=min_price) | Q(real_price__gte=min_price)
            )
        if max_price:
            qs = qs.filter(
                Q(discount_price__lte=max_price) | Q(real_price__lte=max_price)
            )
        if condition and condition != 'ANY_CONDITION':
            qs = qs.filter(condition=condition)
        return qs

    # Filter all models
    realestate = filter_qs(RealEstate.objects.all())
    books = filter_qs(BooksEducation.objects.all())
    health = filter_qs(HealthBeauty.objects.all())
    household = filter_qs(HouseholdAccessories.objects.all())
    autos = filter_qs(Automobiles.objects.all())
    furniture = filter_qs(FurnitureAppliances.objects.all())
    pcs = filter_qs(PCsPeripherals.objects.all())
    musical = filter_qs(MusicalInstruments.objects.all())
    mobiles = filter_qs(MobileDevicesAccessories.objects.all())
    electronics = filter_qs(ElectronicsAppliances.objects.all())
    fashion = filter_qs(FashionwearAddons.objects.all())
    tools = filter_qs(ToolsMachinery.objects.all())
    cameras = filter_qs(CamerasAccessories.objects.all())

    def tag(qs, name):
        for obj in qs:
            obj.category = name
        return qs

    combined = list(chain(
        tag(realestate, "Real Estate"),
        tag(books, "Books"),
        tag(health, "Health & Beauty"),
        tag(household, "Household"),
        tag(autos, "Automobiles"),
        tag(furniture, "Furniture"),
        tag(pcs, "PCs"),
        tag(musical, "Instruments"),
        tag(mobiles, "Mobiles"),
        tag(electronics, "Electronics"),
        tag(fashion, "Fashion"),
        tag(tools, "Tools"),
        tag(cameras, "Cameras"),
    ))

    sort_by = request.GET.get('sort_by', 'latest')

    def safe_get(obj, attr, default=None):
        return getattr(obj, attr, default)

    if sort_by == "latest":
        combined.sort(key=lambda x: safe_get(x, 'listed_date'), reverse=True)
    elif sort_by == "oldest":
        combined.sort(key=lambda x: safe_get(x, 'listed_date'))
    elif sort_by == "price_low_high":
        combined.sort(key=lambda x: safe_get(x, 'discount_price')
                      or safe_get(x, 'real_price', 0))
    elif sort_by == "price_high_low":
        combined.sort(key=lambda x: safe_get(x, 'discount_price')
                      or safe_get(x, 'real_price', 0), reverse=True)
    elif sort_by == "name_asc":
        combined.sort(key=lambda x: safe_get(x, 'title', '').lower())
    elif sort_by == "name_desc":
        combined.sort(key=lambda x: safe_get(
            x, 'title', '').lower(), reverse=True)
    elif sort_by == "random":
        shuffle(combined)

    paginator = Paginator(combined, 30)
    page_number = request.GET.get('page', 1)

    try:
        combined_page = paginator.page(page_number)
    except PageNotAnInteger:
        combined_page = paginator.page(1)
    except EmptyPage:
        combined_page = paginator.page(paginator.num_pages)

    post_categories = settings.POST_CATEGORIES
    forms = {cat['id']: get_form_class(cat['id'])() for cat in post_categories}

    return render(request, "MainApp/home.html", {
        "post_categories": post_categories,
        "forms": forms,
        "All_listening": combined_page,
        "normal": "hero-normal",
        "real_estates": realestate,
        "combined_count": len(combined),
    })

@login_required
def create_listing(request, category):
    form_class = get_form_class(category)
    if form_class is None:
        return render(request, "404.html", status=404)

    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.listed_by = request.user

            # Get location info
            location = get_location_info()
            if location:
                listing.country = location.get("country", "")
                listing.state = location.get("region", "")
                listing.city = location.get("city", "")

            listing.save()

            # Handle image uploads
            images = request.FILES.getlist('images')
            image_fields = [f'image{i+1}' for i in range(10)]
            for i, image in enumerate(images[:10]):
                setattr(listing, image_fields[i], image)
            listing.save()

            messages.success(
                request, f"{category.replace('_', ' ').title()} listing created!")
            return redirect("home")
    else:
        form = form_class()

    category_name = next(
        (c["name"] for c in settings.POST_CATEGORIES if c["id"] == category),
        category.replace('_', ' ').title()
    )

    return render(request, "MainApp/partials/create_listing.html", {
        "form": form,
        "category": category,
        "category_name": category_name,
    })

