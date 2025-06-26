from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
import os
from django.core.exceptions import ValidationError

class BaseListing(models.Model):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("SOLD", "Sold"),
        ("RESERVED", "Reserved"),
        ("RENTED", "Rented"),
        ("NOT_AVAILABLE", "Not Available"),
    ]
    CONDITION_CHOICES = [
        ("ANY", "Any Condition"),
        ("BRAND_NEW", "Brand New"),
        ("LIKE_NEW", "Like New"),
        ("USED", "Used"),
        ("NOT_WORKING", "Not Working"),
    ]
    COUNTRY_CHOICES = [
        ("NP", "Nepal"),
        ("US", "United States"),
    ]

    # New country field
    country = models.CharField(
        max_length=2, choices=COUNTRY_CHOICES, default='NP'
    )

    title = models.CharField(max_length=200)
    description = CKEditor5Field(config_name="extends")
    real_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="AVAILABLE"
    )
    condition = models.CharField(
        max_length=20, choices=CONDITION_CHOICES, default="ANY"
    )
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)

    listed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_listings"
    )
    listed_date = models.DateField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Auto-calculate discount_percentage if discount_price is set
        if self.discount_price and self.real_price > 0:
            discount_amount = self.real_price - self.discount_price
            self.discount_percentage = (
                discount_amount / self.real_price) * 100
        else:
            self.discount_percentage = 0
        super().save(*args, **kwargs)


def get_upload_path(instance, filename):
    model_name = instance.__class__.__name__.lower()
    return os.path.join("listing_images", model_name, filename)


class ImageMixin(models.Model):
    image1 = models.ImageField(
        upload_to=get_upload_path, blank=True, null=True)
    image2 = models.ImageField(
        upload_to=get_upload_path, blank=True, null=True)
    image3 = models.ImageField(
        upload_to=get_upload_path, blank=True, null=True)
    image4 = models.ImageField(
        upload_to=get_upload_path, blank=True, null=True)
    image5 = models.ImageField(
        upload_to=get_upload_path, blank=True, null=True)
    image6 = models.ImageField(
        upload_to=get_upload_path, blank=True, null=True)
    image7 = models.ImageField(
        upload_to=get_upload_path, blank=True, null=True)
    image8 = models.ImageField(
        upload_to=get_upload_path, blank=True, null=True)
    image9 = models.ImageField(
        upload_to=get_upload_path, blank=True, null=True)
    image10 = models.ImageField(
        upload_to=get_upload_path, blank=True, null=True)

    class Meta:
        abstract = True


class RealEstate(BaseListing, ImageMixin):
    LISTING_TYPE_CHOICES = [
        # For Sale

        # For Sale
        ("SALE_APARTMENT", "Apartment (Sale)"),
        ("SALE_LAND", "Land (Sale)"),
        ("SALE_HOUSE", "House (Sale)"),

        # For Rent
        ("RENT_APARTMENT", "Apartment (Rent)"),
        ("RENT_HOUSE", "House (Rent)"),
        ("RENT_LAND", "Land (Rent)"),
        ("RENT_ROOMMATE", "Room & Roommate (Rent)"),
    ]

    CONDITION_CHOICES = [
        ("NEW", "New"),
        ("EXCELLENT", "Excellent"),
        ("GOOD", "Good"),
        ("FAIR", "Fair"),
        ("NEEDS_RENOVATION", "Needs Renovation"),
    ]

    realestate_condition = models.CharField(
        max_length=20, choices=CONDITION_CHOICES, default="GOOD"
    )
    listing_type = models.CharField(
        max_length=30, choices=LISTING_TYPE_CHOICES, default="SALE_HOUSE"
    )

    def __str__(self):
        return f"{self.title} in {self.city}"


class BooksEducation(BaseListing, ImageMixin):
    author = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    edition = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title



class HealthBeauty(BaseListing, ImageMixin):
    PRODUCT_TYPE_CHOICES = [
        ('skincare', 'Skincare'),
        ('haircare', 'Haircare'),
        ('makeup', 'Makeup'),
        ('personal_care', 'Personal Care'),
        ('supplements', 'Supplements'),
        ('medical', 'Medical'),
        ('others', 'Others'),
    ]

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('sealed', 'Sealed'),
        ('used', 'Used'),
    ]

    BRAND_CHOICES = [
        ('himalaya', 'Himalaya'),
        ('garnier', 'Garnier'),
        ('loreal', 'L’Oreal'),
        ('olay', 'Olay'),
        ('ponds', 'Pond\'s'),
        ('dove', 'Dove'),
        ('others', 'Others'),
    ]

    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPE_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    brand = models.CharField(max_length=100, choices=BRAND_CHOICES, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    weight = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return self.title

class HouseholdAccessories(BaseListing, ImageMixin):
    material = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title


class Automobiles(BaseListing, ImageMixin):
    VEHICLE_TYPE_CHOICES = [
        ("car", "Car"),
        ("bike", "Bike"),
        ("scooter", "Scooter"),
        ("auto", "Auto Rickshaw"),
        ("truck", "Truck"),
        ("van", "Van"),
        ("jeep", "Jeep"),
        ("bus", "Bus"),
        ("tractor", "Tractor"),
    ]
    BRAND_CHOICES = [
        ("Toyota", "Toyota"),
        ("Honda", "Honda"),
        ("Suzuki", "Suzuki"),
        ("Hyundai", "Hyundai"),
        ("Kia", "Kia"),
        ("Ford", "Ford"),
        ("Nissan", "Nissan"),
        ("Mahindra", "Mahindra"),
        ("Tata", "Tata"),
        ("Volkswagen", "Volkswagen"),
        ("Chevrolet", "Chevrolet"),
        ("BMW", "BMW"),
        ("Mercedes-Benz", "Mercedes-Benz"),
        ("Audi", "Audi"),
        ("Jeep", "Jeep"),
        ("Skoda", "Skoda"),
        ("Renault", "Renault"),
        ("TVS", "TVS"),
        ("Bajaj", "Bajaj"),
        ("Hero", "Hero"),
        ("Royal Enfield", "Royal Enfield"),
        ("Yamaha", "Yamaha"),
        ("Piaggio", "Piaggio"),
        ("Ashok Leyland", "Ashok Leyland"),
        ("Eicher", "Eicher"),
        ("Force Motors", "Force Motors"),
    ]
    FUEL_TYPE_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
        ('CNG', 'CNG'),
        ('LPG', 'LPG'),
        ('Other', 'Other'),
    ]

    vehicle_type = models.CharField(
        max_length=20, choices=VEHICLE_TYPE_CHOICES)
    brand = models.CharField(
        max_length=100, choices=BRAND_CHOICES, default='Toyota')
    model = models.CharField(max_length=100)

    fuel_type = models.CharField(
        max_length=50,
        choices=FUEL_TYPE_CHOICES,
        default='Petrol',
        null=True,
        blank=True,
    )
    year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class FurnitureAppliances(BaseListing, ImageMixin):
    FURNITURE_TYPE_CHOICES = [
        ('sofa', 'Sofa'),
        ('bed', 'Bed'),
        ('table', 'Table'),
        ('chair', 'Chair'),
        ('wardrobe', 'Wardrobe'),
        ('shelf', 'Shelf'),
        ('appliance', 'Appliance'),
        ('other', 'Other'),
    ]

    MATERIAL_CHOICES = [
        ('wood', 'Wood'),
        ('metal', 'Metal'),
        ('plastic', 'Plastic'),
        ('glass', 'Glass'),
        ('leather', 'Leather'),
        ('fabric', 'Fabric'),
        ('mixed', 'Mixed Materials'),
        ('other', 'Other'),
    ]



    COLOR_CHOICES = [
        ('black', 'Black'),
        ('white', 'White'),
        ('brown', 'Brown'),
        ('grey', 'Grey'),
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('multi', 'Multicolor'),
        ('other', 'Other'),
    ]

    furniture_type = models.CharField(max_length=100, choices=FURNITURE_TYPE_CHOICES)
    material = models.CharField(max_length=100, choices=MATERIAL_CHOICES, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, choices=COLOR_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.title


class PCsPeripherals(BaseListing, ImageMixin):
    BRAND_CHOICES = [
        ('HP', 'HP'),
        ('Dell', 'Dell'),
        ('Lenovo', 'Lenovo'),
        ('Asus', 'Asus'),
        ('Acer', 'Acer'),
        ('MSI', 'MSI'),
        ('Apple', 'Apple'),
        ('Other', 'Other'),
    ]
    PC_TYPE_CHOICES = [
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop'),
        ('Monitor', 'Monitor'),
        ('Printer', 'Printer'),
        ('Accessories', 'Accessories'),
        ('Other', 'Other'),
    ]
    pc_type = models.CharField(max_length=30, choices=PC_TYPE_CHOICES, default='Other')


    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, default='Other')
    specs = CKEditor5Field(config_name="extends")

    def __str__(self):
        return self.title



class MusicalInstruments(BaseListing, ImageMixin):
    INSTRUMENT_TYPE_CHOICES = [
        ('guitar', 'Guitar'),
        ('keyboard', 'Keyboard'),
        ('drums', 'Drums'),
        ('violin', 'Violin'),
        ('flute', 'Flute'),
        ('tabla', 'Tabla'),
        ('microphone', 'Microphone'),
        ('others', 'Others'),
    ]

    BRAND_CHOICES = [
        ('yamaha', 'Yamaha'),
        ('roland', 'Roland'),
        ('fender', 'Fender'),
        ('gibson', 'Gibson'),
        ('korg', 'Korg'),
        ('casio', 'Casio'),
        ('others', 'Others'),
    ]

  
    instrument_type = models.CharField(max_length=50, choices=INSTRUMENT_TYPE_CHOICES)
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, blank=True, null=True)
    features = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title



class MobileDevicesAccessories(BaseListing, ImageMixin):
    BRAND_CHOICES = [
    ('Apple', 'Apple'),
    ('Samsung', 'Samsung'),
    ('Xiaomi', 'Xiaomi'),
    ('OnePlus', 'OnePlus'),
    ('Realme', 'Realme'),
    ('Oppo', 'Oppo'),
    ('Vivo', 'Vivo'),
    ('Nokia', 'Nokia'),
    ('Motorola', 'Motorola'),
    ('Huawei', 'Huawei'),
    ('Honor', 'Honor'),
    ('Asus', 'Asus'),
    ('Lenovo', 'Lenovo'),
    ('Sony', 'Sony'),
    ('HTC', 'HTC'),
    ('Micromax', 'Micromax'),
    ('Infinix', 'Infinix'),
    ('Tecno', 'Tecno'),
    ('ZTE', 'ZTE'),
    ('Lava', 'Lava'),
    ('Gionee', 'Gionee'),
    ('Itel', 'Itel'),
    ('Panasonic', 'Panasonic'),
    ('Meizu', 'Meizu'),
    ('Google Pixel', 'Google Pixel'),
    ('BlackBerry', 'BlackBerry'),
    ('LeEco', 'LeEco'),
    ('Coolpad', 'Coolpad'),
    ('Sharp', 'Sharp'),
    ('Alcatel', 'Alcatel'),
    ('Blu', 'Blu'),
    ('Other', 'Other'),
]

    brand = models.CharField(max_length=100, choices=BRAND_CHOICES)
    model = models.CharField(max_length=100)
    storage_capacity = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.brand} {self.model} - {self.storage_capacity}"


class ElectronicsAppliances(BaseListing, ImageMixin):
    APPLIANCE_TYPE_CHOICES = [
    ('kitchen', 'Kitchen Appliance'),
    ('home', 'Home Appliance'),
    ('personal', 'Personal Gadget'),
    ('other', 'Other'),
]  
    BRAND_CHOICES = [
    ('cg', 'Chaudhary Group (CG)'),
    ('samsung', 'Samsung'),
    ('lg', 'LG'),
    ('sony', 'Sony'),
    ('panasonic', 'Panasonic'),
    ('philips', 'Philips'),
    ('whirlpool', 'Whirlpool'),
    ('bosch', 'Bosch'),
    ('lenovo', 'Lenovo'),
    ('dell', 'Dell'),
    ('other', 'Other'),
]

    brand = models.CharField(max_length=100, choices=BRAND_CHOICES, default='Other')
    appliance_type = models.CharField(max_length=50, choices=APPLIANCE_TYPE_CHOICES, blank=True, null=True)
    warranty = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

class FashionwearAddons(BaseListing, ImageMixin):
    class CategoryChoices(models.TextChoices):
        TOPWEAR = 'Topwear', 'Topwear'
        BOTTOMWEAR = 'Bottomwear', 'Bottomwear'
        FOOTWEAR = 'Footwear', 'Footwear'
        ACCESSORIES = 'Accessories', 'Accessories'
        ETHNIC = 'Ethnic', 'Ethnic Wear'
        SPORTS = 'Sportswear', 'Sportswear'
        WINTER = 'Winterwear', 'Winterwear'
        INNERWEAR = 'Innerwear', 'Innerwear'
        SAREE = 'Saree', 'Saree'
        KURTI = 'Kurti', 'Kurti'

    class SizeChoices(models.TextChoices):
        XS = 'XS', 'Extra Small'
        S = 'S', 'Small'
        M = 'M', 'Medium'
        L = 'L', 'Large'
        XL = 'XL', 'Extra Large'
        XXL = 'XXL', '2XL'
        XXXL = 'XXXL', '3XL'
        FREE = 'Free Size', 'Free Size'

    class GenderChoices(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'
        UNISEX = 'Unisex', 'Unisex'
        KIDS = 'Kids', 'Kids'
        OTHER = 'Other', 'Other'

    class ColorChoices(models.TextChoices):
        RED = 'Red', 'Red'
        BLUE = 'Blue', 'Blue'
        BLACK = 'Black', 'Black'
        WHITE = 'White', 'White'
        GREEN = 'Green', 'Green'
        YELLOW = 'Yellow', 'Yellow'
        ORANGE = 'Orange', 'Orange'
        PURPLE = 'Purple', 'Purple'
        PINK = 'Pink', 'Pink'
        GREY = 'Grey', 'Grey'
        BROWN = 'Brown', 'Brown'
        MULTICOLOR = 'Multicolor', 'Multicolor'
        OTHER = 'Other', 'Other'

    MATERIAL_CHOICES = [
        ('Cotton', 'Cotton'),
        ('Polyester', 'Polyester'),
        ('Silk', 'Silk'),
        ('Linen', 'Linen'),
        ('Denim', 'Denim'),
        ('Wool', 'Wool'),
        ('Leather', 'Leather'),
        ('Blended', 'Blended'),
        ('Other', 'Other'),
    ]

    brand = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CategoryChoices.choices)
    size = models.CharField(max_length=20, choices=SizeChoices.choices)
    gender = models.CharField(max_length=20, choices=GenderChoices.choices)
    color = models.CharField(max_length=20, choices=ColorChoices.choices)
    material = models.CharField(max_length=50, choices=MATERIAL_CHOICES, blank=True, null=True)
    occasion = models.CharField(max_length=100, blank=True, null=True, help_text="E.g., Casual, Party, Formal, Festival")

    def __str__(self):
        return f"{self.title} - {self.category} - {self.size} - {self.color} - {self.gender}"


class ToolsMachinery(BaseListing, ImageMixin):
    TOOL_TYPE_CHOICES = [
        ("drill", "Drill"),
        ("grinder", "Grinder"),
        ("saw", "Saw"),
        ("lathe", "Lathe"),
        ("mixer", "Mixer"),
        ("other", "Other"),
    ]

    POWER_SOURCE_CHOICES = [
        ("electric", "Electric"),
        ("gas", "Gas"),
        ("manual", "Manual"),
        ("battery", "Battery Powered"),
        ("hydraulic", "Hydraulic"),
    ]

    tool_type = models.CharField(max_length=100, choices=TOOL_TYPE_CHOICES)
    power_source = models.CharField(max_length=50, choices=POWER_SOURCE_CHOICES)

    def __str__(self):
        return self.title


class CamerasAccessories(BaseListing, ImageMixin):
    BRAND_CHOICES = [
        ("Canon", "Canon"),
        ("Nikon", "Nikon"),
        ("Sony", "Sony"),
        ("Fujifilm", "Fujifilm"),
        ("Panasonic", "Panasonic"),
        ("Olympus", "Olympus"),
        ("GoPro", "GoPro"),
        ("Leica", "Leica"),
        ("Pentax", "Pentax"),
        ("Kodak", "Kodak"),
        ("Sigma", "Sigma"),
        ("Hasselblad", "Hasselblad"),
        ("DJI", "DJI"),
        ("Other", "Other"),
    ]

    brand = models.CharField(
        max_length=100, choices=BRAND_CHOICES, default='Canon')
    model = models.CharField(max_length=100)
    megapixels = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model}"


class Ads(models.Model):
    COUNTRY_CHOICES = [
        ("NP", "Nepal"),
        ("US", "United States"),
    ]

    # New country field
    country = models.CharField(
        max_length=2, choices=COUNTRY_CHOICES, default='NP'
    )
    listed_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_listings"
    )
    banner = models.ImageField(upload_to='ads_banners/')
    link = models.URLField(max_length=500)
    title = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or self.link

    class Meta:
        ordering = ['-created_at']


class FoodBeverages(BaseListing, ImageMixin):
    CATEGORY_CHOICES = [
        ("FOOD", "Food"),
        ("BEVERAGE", "Beverage"),
        ("SNACK", "Snack"),
        ("ALCOHOL", "Alcoholic Beverage"),
        ("NON_ALCOHOL", "Non-Alcoholic Beverage"),
    ]

    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="FOOD")
    expiration_date = models.DateField(blank=True, null=True)
    packaging = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Bottle, Box, Can")
    quantity = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 500ml, 1kg, 12-pack")
    allergen_info = models.TextField(blank=True, null=True, help_text="Allergen or dietary info if applicable")

    def __str__(self):
        return f"{self.title} ({self.brand})"

class Wishlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="wishlists")

    realestate = models.ForeignKey(
        RealEstate, null=True, blank=True, on_delete=models.CASCADE)
    books_education = models.ForeignKey(
        BooksEducation, null=True, blank=True, on_delete=models.CASCADE)
    health_beauty = models.ForeignKey(
        HealthBeauty, null=True, blank=True, on_delete=models.CASCADE)
    household_accessories = models.ForeignKey(
        HouseholdAccessories, null=True, blank=True, on_delete=models.CASCADE)
    automobiles = models.ForeignKey(
        Automobiles, null=True, blank=True, on_delete=models.CASCADE)
    furniture_appliances = models.ForeignKey(
        FurnitureAppliances, null=True, blank=True, on_delete=models.CASCADE)
    pcs_peripherals = models.ForeignKey(
        PCsPeripherals, null=True, blank=True, on_delete=models.CASCADE)
    musical_instruments = models.ForeignKey(
        MusicalInstruments, null=True, blank=True, on_delete=models.CASCADE)
    mobile_devices_accessories = models.ForeignKey(
        MobileDevicesAccessories, null=True, blank=True, on_delete=models.CASCADE)
    electronics_appliances = models.ForeignKey(
        ElectronicsAppliances, null=True, blank=True, on_delete=models.CASCADE)
    fashionwear_addons = models.ForeignKey(
        FashionwearAddons, null=True, blank=True, on_delete=models.CASCADE)
    tools_machinery = models.ForeignKey(
        ToolsMachinery, null=True, blank=True, on_delete=models.CASCADE)
    cameras_accessories = models.ForeignKey(
        CamerasAccessories, null=True, blank=True, on_delete=models.CASCADE)
    food_beverages = models.ForeignKey(
        FoodBeverages, null=True, blank=True, on_delete=models.CASCADE)

    added_at = models.DateTimeField(auto_now_add=True)

    def validate_unique(self, exclude=None):
        super().validate_unique(exclude=exclude)
        fields = [
            self.realestate,
            self.books_education,
            self.health_beauty,
            self.household_accessories,
            self.automobiles,
            self.furniture_appliances,
            self.pcs_peripherals,
            self.musical_instruments,
            self.mobile_devices_accessories,
            self.electronics_appliances,
            self.fashionwear_addons,
            self.tools_machinery,
            self.cameras_accessories,
            self.food_beverages,
        ]
        set_count = sum(1 for f in fields if f is not None)
        if set_count == 0:
            raise ValidationError("One product field must be set.")
        if set_count > 1:
            raise ValidationError("Only one product field can be set.")

        for field_name in [
            "realestate",
            "books_education",
            "health_beauty",
            "household_accessories",
            "automobiles",
            "furniture_appliances",
            "pcs_peripherals",
            "musical_instruments",
            "mobile_devices_accessories",
            "electronics_appliances",
            "fashionwear_addons",
            "tools_machinery",
            "cameras_accessories",
            "food_beverages",
        ]:
            product = getattr(self, field_name)
            if product:
                qs = Wishlist.objects.filter(
                    user=self.user, **{field_name: product})
                if self.pk:
                    qs = qs.exclude(pk=self.pk)
                if qs.exists():
                    raise ValidationError(
                        f"Wishlist entry for this {field_name.replace('_', ' ')} already exists.")

    def save(self, *args, **kwargs):
        self.full_clean()  # calls validate_unique and clean
        super().save(*args, **kwargs)

    def __str__(self):
        product = (
            self.realestate
            or self.books_education
            or self.health_beauty
            or self.household_accessories
            or self.automobiles
            or self.furniture_appliances
            or self.pcs_peripherals
            or self.musical_instruments
            or self.mobile_devices_accessories
            or self.electronics_appliances
            or self.fashionwear_addons
            or self.tools_machinery
            or self.cameras_accessories
            or self.food_beverages
        )
        name = getattr(product, 'title', None) or str(product) or "Unknown"
        return f"Wishlist - {self.user.username}: {name}"
