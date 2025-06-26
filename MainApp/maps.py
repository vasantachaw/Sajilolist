# MainApp/maps.py

from MainApp.models import (
    RealEstate, BooksEducation, HealthBeauty, HouseholdAccessories, Automobiles,
    FurnitureAppliances, PCsPeripherals, MusicalInstruments, MobileDevicesAccessories,
    ElectronicsAppliances, FashionwearAddons, ToolsMachinery, CamerasAccessories,FoodBeverages
)

MODEL_MAP = {
    'realestate': RealEstate,
    'bookseducation': BooksEducation,
    'healthbeauty': HealthBeauty,
    'household': HouseholdAccessories,
    'automobiles': Automobiles,
    'furnitureappliances': FurnitureAppliances,
    'pcsperipherals': PCsPeripherals,
    'musicalinstruments': MusicalInstruments,
    'mobiledevicesaccessories': MobileDevicesAccessories,
    'toolsmachinery': ElectronicsAppliances,
    'fashion': FashionwearAddons,
    'tools': ToolsMachinery,
    'camerasaccessories': CamerasAccessories,
    'foodbeverages': FoodBeverages,
}

TEMPLATE_MAP = {
    'realestate': 'MainApp/realestate/real-estate_details.html',
    'bookseducation': 'MainApp/books/book_details.html',
    'healthbeauty': 'MainApp/health/health_details.html',
    'household': 'MainApp/household/household_details.html',
    'automobiles': 'MainApp/automobiles/automobiles_details.html',
    'furnitureappliances': 'MainApp/furniture/furniture_details.html',
    'pcsperipherals': 'MainApp/PcsAccessories/pc_details.html',
    'musicalinstruments': 'MainApp/music/music_details.html',
    'mobiledevicesaccessories': 'MainApp/mobiles/mobiles_details.html',
    'electronicsappliances': 'MainApp/electronics/electronics_details.html',
    'fashionwearaddons': 'MainApp/fashion/fashion_details.html',
    'toolsmachinery': 'MainApp/tools/tools_details.html',
    'camerasaccessories': 'MainApp/cameras/cameras_details.html',
    'foodbeverages': 'MainApp/food/food_details.html',

}

