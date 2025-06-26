from MainApp.models import (
    RealEstate, BooksEducation, HealthBeauty, HouseholdAccessories, Automobiles,
    FurnitureAppliances, PCsPeripherals, MusicalInstruments, MobileDevicesAccessories,
    ElectronicsAppliances, FashionwearAddons, ToolsMachinery, CamerasAccessories,FoodBeverages,
)
from django import forms


excludes = [
    "listed_by", "listed_date", "views", "is_available",'country','city','state',
]


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            classes = (existing_classes + ' form-control').strip()
            field.widget.attrs.update({
                'class': classes,
                'style': 'width:100%; padding:8px 10px; border:1px solid #ccc; border-radius:4px;'
            })


class RealEstateForm(StyledModelForm):
    class Meta:
        model = RealEstate
        exclude =[
    "listed_by", "listed_date", "views", "is_available",'country','city','state','condition',
]
        labels = {
            "title": "Listing Title",
            "description": "Description",
            "real_price": "Original Price",
            "discount_price": "Discounted Price",
            "condition": "Condition",
            "address": "Address",
            "realestate_condition": "Condition",
            "listing_type": "Listing Type",
            "discount_percentage": "Discount Percentage (optional)",
        }


class BooksEducationForm(StyledModelForm):
    class Meta:
        model = BooksEducation
        exclude = excludes
        labels = {
            "title": "Book Title",
            "author": "Author",
            "publisher": "Publisher",
            "edition": "Edition",
            "description": "Description",
            "real_price": "Original Price",
            "discount_price": "Discounted Price",
            "condition": "Condition",
            "address": "Address",
        }


class HealthBeautyForm(StyledModelForm):
    class Meta:
        model = HealthBeauty
        exclude = excludes
        labels = {
            "title": "Product Name",
            "brand": "Brand",
            "expiry_date": "Expiry Date",
            "description": "Description",
            "real_price": "Original Price",
            "discount_price": "Discounted Price",
            "condition": "Condition",
            "address": "Address",
        }


class HouseholdAccessoriesForm(StyledModelForm):
    class Meta:
        model = HouseholdAccessories
        exclude = excludes
        labels = {
            "title": "Product Name",
            "material": "Material",
            "description": "Description",
            "real_price": "Original Price",
            "discount_price": "Discounted Price",
            "condition": "Condition",
            "address": "Address",
        }


class AutomobilesForm(StyledModelForm):
    class Meta:
        model = Automobiles
        exclude = excludes
        labels = {
            "vehicle_type": "Vehicle Type",
            "brand": "Brand",
            "model": "Model",
            "year": "Year",
            "mileage": "Mileage",
            "condition": "Condition",
            "description": "Description",
            "real_price": "Original Price",
            "discount_price": "Discounted Price",
            "address": "Address",
        }


class FurnitureAppliancesForm(StyledModelForm):
    class Meta:
        model = FurnitureAppliances
        exclude = excludes
        labels = {
            "title": "Item Name",
            "furniture_type": "Furniture Type",
            "description": "Description",
            "real_price": "Original Price",
            "discount_price": "Discounted Price",
            "condition": "Condition",
            "address": "Address",
        }


class PCsPeripheralsForm(StyledModelForm):
    class Meta:
        model = PCsPeripherals
        exclude = excludes
        labels = {
            "title": "Product Name",
            "specs": "Specifications",
            "description": "Description",
            "real_price": "Original Price",
            "discount_price": "Discounted Price",
            "condition": "Condition",
            "address": "Address",
        }


class MusicalInstrumentsForm(StyledModelForm):
    class Meta:
        model = MusicalInstruments
        exclude = excludes
        labels = {
            "title": "Instrument Name",
            "instrument_type": "Instrument Type",
            "description": "Description",
            "real_price": "Original Price",
            "discount_price": "Discounted Price",
            "condition": "Condition",
            "address": "Address",
        }


class MobileDevicesAccessoriesForm(StyledModelForm):
    class Meta:
        model = MobileDevicesAccessories
        exclude = excludes
        labels = {
            "brand": "Brand",
            "model": "Model",
            "storage_capacity": "Storage Capacity",
            "description": "Description",
            "real_price": "Original Price",
            "discount_price": "Discounted Price",
            "condition": "Condition",
            "address": "Address",
        }


class ElectronicsAppliancesForm(StyledModelForm):
    class Meta:
        model = ElectronicsAppliances
        exclude = excludes
        labels = {
            "title": "Product Name",
            "brand": "Brand",
            "warranty": "Warranty",
            "description": "Description",
            "real_price": "Original Price",
            "discount_price": "Discounted Price",
            "condition": "Condition",
            "address": "Address",
        }


class FashionwearAddonsForm(StyledModelForm):
    class Meta:
        model = FashionwearAddons
        exclude = excludes
        labels = {
            "title": "Item Name",
            "size": "Size",
            "gender": "Gender",
            "description": "Description",
            "real_price": "Original Price",
            "discount_price": "Discounted Price",
            "condition": "Condition",
            "address": "Address",
        }


class ToolsMachineryForm(StyledModelForm):
    class Meta:
        model = ToolsMachinery
        exclude = excludes
        labels = {
            "title": "Tool Name",
            "tool_type": "Tool Type",
            "power_source": "Power Source",
            "description": "Description",
            "real_price": "Original Price",
            "discount_price": "Discounted Price",
            "condition": "Condition",
            "address": "Address",
        }


class CamerasAccessoriesForm(StyledModelForm):
    class Meta:
        model = CamerasAccessories
        exclude = excludes
        labels = {
            "brand": "Brand",
            "model": "Model",
            "megapixels": "Megapixels",
            "description": "Description",
            "real_price": "Original Price",
            "discount_price": "Discounted Price",
            "condition": "Condition",
            "address": "Address",
        }

class FoodBeveragesForm(StyledModelForm):
    class Meta:
        model = FoodBeverages
        exclude = excludes
        labels = {
            "brand": "Brand",
            "category": "Category",
            "expiration_date": "Expiration Date",
            "packaging": "Packaging Type",
            "quantity": "Quantity (e.g., 500ml, 1kg)",
            "description": "Product Description",
            "real_price": "Original Price",
            "discount_price": "Discounted Price",
            "condition": "Condition",
            "address": "Address",
        }
