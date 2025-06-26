from django.contrib import admin
from MainApp.models import (
    BooksEducation,
    HealthBeauty,
    HouseholdAccessories,
    Automobiles,
    FurnitureAppliances,
    PCsPeripherals,
    MusicalInstruments,
    MobileDevicesAccessories,
    ElectronicsAppliances,
    FashionwearAddons,
    ToolsMachinery,
    CamerasAccessories,
    Wishlist,
    RealEstate,
    Ads,
    FoodBeverages,
)


@admin.register(RealEstate)
class RealEstateAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "city",
        "listing_type",
        "status",
        "real_price",
        "listed_by",
        "listed_date",
    )
    search_fields = ("title", "city", "address", "listed_by__username")
    list_filter = ("listing_type", "status", "city", "realestate_condition")
    readonly_fields = ("listed_date", "views")
    autocomplete_fields = ["listed_by"]
    list_per_page = 25
    ordering = ['-listed_date']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "product_name", "added_at")
    list_filter = ("added_at",)
    search_fields = ("user__username",)

    def product_name(self, obj):
        product = (
            obj.realestate
            or obj.books_education
            or obj.health_beauty
            or obj.household_accessories
            or obj.automobiles
            or obj.furniture_appliances
            or obj.pcs_peripherals
            or obj.musical_instruments
            or obj.mobile_devices_accessories
            or obj.electronics_appliances
            or obj.fashionwear_addons
            or obj.tools_machinery
            or obj.cameras_accessories
            or obj.food_beverages
        )
        if product:
            return str(product)
        return "-"
    product_name.short_description = "Product"

@admin.register(BooksEducation)
class BooksEducationAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publisher", "edition")
    search_fields = ("title", "author", "publisher")


@admin.register(HealthBeauty)
class HealthBeautyAdmin(admin.ModelAdmin):
    list_display = ("title", "brand", "expiry_date")
    search_fields = ("title", "brand")


@admin.register(HouseholdAccessories)
class HouseholdAccessoriesAdmin(admin.ModelAdmin):
    list_display = ("title", "material")
    search_fields = ("title", "material")


@admin.register(Automobiles)
class AutomobilesAdmin(admin.ModelAdmin):
    list_display = ("vehicle_type", "brand", "model", "year", "mileage", "condition")
    search_fields = ("brand", "model")
    list_filter = ("vehicle_type", "condition", "year")


@admin.register(FurnitureAppliances)
class FurnitureAppliancesAdmin(admin.ModelAdmin):
    list_display = ("title", "furniture_type")
    search_fields = ("title", "furniture_type")


@admin.register(PCsPeripherals)
class PCsPeripheralsAdmin(admin.ModelAdmin):
    list_display = ("title", "brand", "real_price", "discount_price", "listed_date", "is_available")
    search_fields = ("title", "brand")
    list_filter = ("brand", "listed_date", "is_available", "status", "condition", "country")
    ordering = ("-listed_date",)


@admin.register(MusicalInstruments)
class MusicalInstrumentsAdmin(admin.ModelAdmin):
    list_display = ("title", "instrument_type")
    search_fields = ("title", "instrument_type")


@admin.register(MobileDevicesAccessories)
class MobileDevicesAccessoriesAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "storage_capacity")
    search_fields = ("brand", "model")


@admin.register(ElectronicsAppliances)
class ElectronicsAppliancesAdmin(admin.ModelAdmin):
    list_display = ("title", "brand", "warranty")
    search_fields = ("title", "brand")


@admin.register(FashionwearAddons)
class FashionwearAddonsAdmin(admin.ModelAdmin):
    list_display = ("title", "size", "gender")
    search_fields = ("title",)


@admin.register(ToolsMachinery)
class ToolsMachineryAdmin(admin.ModelAdmin):
    list_display = ("title", "tool_type", "power_source")
    search_fields = ("title", "tool_type", "power_source")


@admin.register(CamerasAccessories)
class CamerasAccessoriesAdmin(admin.ModelAdmin):
    list_display = ("title", "brand", "model", "megapixels")
    search_fields = ("title", "brand", "model")


@admin.register(Ads)
class AdsAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'listed_by', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'link', 'listed_by__username']
    readonly_fields = ['created_at']
    autocomplete_fields = ['listed_by']


@admin.register(FoodBeverages)
class FoodBeveragesAdmin(admin.ModelAdmin):
    list_display = ("title", "brand", "category", "expiration_date", "listed_by", "listed_date", "is_available")
    list_filter = ("category", "expiration_date", "is_available")
    search_fields = ("title", "brand")
    readonly_fields = ("listed_date",)
    autocomplete_fields = ["listed_by"]
    ordering = ['-listed_date']
    list_per_page = 25