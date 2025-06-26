from django.db import models
from MainApp.models import (
    RealEstate, BooksEducation, HealthBeauty, HouseholdAccessories, Automobiles,
    FurnitureAppliances, PCsPeripherals, MusicalInstruments, MobileDevicesAccessories,
    ElectronicsAppliances, FashionwearAddons, ToolsMachinery, CamerasAccessories, FoodBeverages,
)
from django.contrib.auth.models import User
from authentication.models import Profile
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Comment(models.Model):
    # User who wrote the comment
    user_profile = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='profiles_reviews')

    # ForeignKeys for various product models, exactly one should be set
    realestate = models.ForeignKey('MainApp.RealEstate', null=True, blank=True, on_delete=models.CASCADE, related_name='comments_realestate')
    books_education = models.ForeignKey('MainApp.BooksEducation', null=True, blank=True, on_delete=models.CASCADE, related_name='comments_books_education')
    health_beauty = models.ForeignKey('MainApp.HealthBeauty', null=True, blank=True, on_delete=models.CASCADE, related_name='comments_health_beauty')
    household_accessories = models.ForeignKey('MainApp.HouseholdAccessories', null=True, blank=True, on_delete=models.CASCADE, related_name='comments_household_accessories')
    automobiles = models.ForeignKey('MainApp.Automobiles', null=True, blank=True, on_delete=models.CASCADE, related_name='comments_automobiles')
    furniture_appliances = models.ForeignKey('MainApp.FurnitureAppliances', null=True, blank=True, on_delete=models.CASCADE, related_name='comments_furniture_appliances')
    pcs_peripherals = models.ForeignKey('MainApp.PCsPeripherals', null=True, blank=True, on_delete=models.CASCADE, related_name='comments_pcs_peripherals')
    musical_instruments = models.ForeignKey('MainApp.MusicalInstruments', null=True, blank=True, on_delete=models.CASCADE, related_name='comments_musical_instruments')
    mobile_devices_accessories = models.ForeignKey('MainApp.MobileDevicesAccessories', null=True, blank=True, on_delete=models.CASCADE, related_name='comments_mobile_devices_accessories')
    electronics_appliances = models.ForeignKey('MainApp.ElectronicsAppliances', null=True, blank=True, on_delete=models.CASCADE, related_name='comments_electronics_appliances')
    fashionwear_addons = models.ForeignKey('MainApp.FashionwearAddons', null=True, blank=True, on_delete=models.CASCADE, related_name='comments_fashionwear_addons')
    tools_machinery = models.ForeignKey('MainApp.ToolsMachinery', null=True, blank=True, on_delete=models.CASCADE, related_name='comments_tools_machinery')
    cameras_accessories = models.ForeignKey('MainApp.CamerasAccessories', null=True, blank=True, on_delete=models.CASCADE, related_name='comments_cameras_accessories')
    food_beverages = models.ForeignKey('MainApp.FoodBeverages', null=True, blank=True, on_delete=models.CASCADE, related_name='comments_food_beverages')

    # User info at comment time
    user_name = models.CharField(max_length=100)
    user_avatar = models.URLField(blank=True, null=True)

    # Review content
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)  # Optional for replies

    # Nested replies support
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        # Validate exactly one product FK is set
        product_fks = [
            self.realestate, self.books_education, self.health_beauty,
            self.household_accessories, self.automobiles, self.furniture_appliances,
            self.pcs_peripherals, self.musical_instruments, self.mobile_devices_accessories,
            self.electronics_appliances, self.fashionwear_addons, self.tools_machinery,
            self.cameras_accessories, self.food_beverages,
        ]
        filled = [fk for fk in product_fks if fk is not None]
        if len(filled) != 1:
            raise ValidationError("Exactly one product ForeignKey must be set.")

    def __str__(self):
        product = (
            self.realestate or self.books_education or self.health_beauty or
            self.household_accessories or self.automobiles or self.furniture_appliances or
            self.pcs_peripherals or self.musical_instruments or self.mobile_devices_accessories or
            self.electronics_appliances or self.fashionwear_addons or self.tools_machinery or
            self.cameras_accessories or self.food_beverages
        )
        name = getattr(product, 'title', None) or str(product) or "Unknown"
        return f"{self.user_name} - {name}: {self.text[:30]}"

    def is_reply(self):
        return self.parent is not None

    def is_review(self):
        return self.rating is not None and not self.is_reply()


class Chats(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_chats')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    content = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Each product category (multiple FK style)
    realestate = models.ForeignKey(RealEstate, null=True, blank=True, on_delete=models.CASCADE, related_name='chats_realestate')
    books_education = models.ForeignKey(BooksEducation, null=True, blank=True, on_delete=models.CASCADE, related_name='chats_books_education')
    health_beauty = models.ForeignKey(HealthBeauty, null=True, blank=True, on_delete=models.CASCADE, related_name='chats_health_beauty')
    household_accessories = models.ForeignKey(HouseholdAccessories, null=True, blank=True, on_delete=models.CASCADE, related_name='chats_household_accessories')
    automobiles = models.ForeignKey(Automobiles, null=True, blank=True, on_delete=models.CASCADE, related_name='chats_automobiles')
    furniture_appliances = models.ForeignKey(FurnitureAppliances, null=True, blank=True, on_delete=models.CASCADE, related_name='chats_furniture_appliances')
    pcs_peripherals = models.ForeignKey(PCsPeripherals, null=True, blank=True, on_delete=models.CASCADE, related_name='chats_pcs_peripherals')
    musical_instruments = models.ForeignKey(MusicalInstruments, null=True, blank=True, on_delete=models.CASCADE, related_name='chats_musical_instruments')
    mobile_devices_accessories = models.ForeignKey(MobileDevicesAccessories, null=True, blank=True, on_delete=models.CASCADE, related_name='chats_mobile_devices_accessories')
    electronics_appliances = models.ForeignKey(ElectronicsAppliances, null=True, blank=True, on_delete=models.CASCADE, related_name='chats_electronics_appliances')
    fashionwear_addons = models.ForeignKey(FashionwearAddons, null=True, blank=True, on_delete=models.CASCADE, related_name='chats_fashionwear_addons')
    tools_machinery = models.ForeignKey(ToolsMachinery, null=True, blank=True, on_delete=models.CASCADE, related_name='chats_tools_machinery')
    cameras_accessories = models.ForeignKey(CamerasAccessories, null=True, blank=True, on_delete=models.CASCADE, related_name='chats_cameras_accessories')
    food_beverages = models.ForeignKey(FoodBeverages, null=True, blank=True, on_delete=models.CASCADE, related_name='chats_food_beverages')

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.content[:30]}"

    def get_product(self):
        return (
            self.realestate or self.books_education or self.health_beauty or
            self.household_accessories or self.automobiles or self.furniture_appliances or
            self.pcs_peripherals or self.musical_instruments or self.mobile_devices_accessories or
            self.electronics_appliances or self.fashionwear_addons or self.tools_machinery or
            self.cameras_accessories or self.food_beverages
        )

    def get_product_url(self):
        product = self.get_product()
        return product.get_absolute_url() if product else "#"

    def get_product_image(self):
        product = self.get_product()
        return getattr(product, "image1", None).url if product and getattr(product, "image1", None) else ""
