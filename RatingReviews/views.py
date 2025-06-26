from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404,redirect,render
from MainApp.models import (
    RealEstate, BooksEducation, HealthBeauty, HouseholdAccessories, Automobiles,
    FurnitureAppliances, PCsPeripherals, MusicalInstruments, MobileDevicesAccessories,
    ElectronicsAppliances, FashionwearAddons, ToolsMachinery, CamerasAccessories, FoodBeverages
)
from django.contrib.auth.models import User
from RatingReviews.models import Comment
import json


def _handle_comments(request, product_model, product_id, related_field_name):
    """
    Helper function to GET comments or POST a new comment on a given product model.
    `related_field_name` is the ForeignKey field in Comment model (e.g. 'realestate', 'books_education', etc.)
    """
    product = get_object_or_404(product_model, id=product_id)

    if request.method == "GET":
        # Return comments with no parent (top-level)
        comments = Comment.objects.filter(
            **{related_field_name: product, 'parent': None}).order_by('-created_at')
        # Your template rendering code here or serialize and return JSON
        # For simplicity, just returning JSON (you can customize)
        comments_data = []
        for comment in comments:
            comments_data.append({
                'id': comment.id,
                'user_name': comment.user_name,
                'user_avatar': comment.user_avatar,
                'text': comment.text,
                'created_at': comment.created_at.isoformat(),
                'replies': [{
                    'id': r.id,
                    'user_name': r.user_name,
                    'user_avatar': r.user_avatar,
                    'text': r.text,
                    'created_at': r.created_at.isoformat(),
                } for r in comment.replies.all()]
            })
        return JsonResponse({'success': True, 'comments': comments_data})

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "").strip()
            parent_id = data.get("parent_id", None)

            if not text:
                return JsonResponse({"success": False, "error": "Comment text cannot be empty."})

            comment_kwargs = {
                related_field_name: product,
                'user_name': request.user.get_full_name() or request.user.username,
                'user_avatar': request.user.profile.profile_picture.url if hasattr(request.user, 'profile') else '',
                'text': text
            }

            comment = Comment(**comment_kwargs)

            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment.parent = parent_comment
                except Comment.DoesNotExist:
                    return JsonResponse({"success": False, "error": "Parent comment not found."})

            comment.save()
            return JsonResponse({"success": True, "comment_id": comment.id})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data."})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})


@require_http_methods(["GET", "POST"])
def get_realestate_comments(request, product_id):
    return _handle_comments(request, RealEstate, product_id, 'realestate')


@require_http_methods(["GET", "POST"])
def get_books_education_comments(request, product_id):
    return _handle_comments(request, BooksEducation, product_id, 'books_education')


@require_http_methods(["GET", "POST"])
def get_health_beauty_comments(request, product_id):
    return _handle_comments(request, HealthBeauty, product_id, 'health_beauty')


@require_http_methods(["GET", "POST"])
def get_household_accessories_comments(request, product_id):
    return _handle_comments(request, HouseholdAccessories, product_id, 'household_accessories')


@require_http_methods(["GET", "POST"])
def get_automobiles_comments(request, product_id):
    return _handle_comments(request, Automobiles, product_id, 'automobiles')


@require_http_methods(["GET", "POST"])
def get_furniture_appliances_comments(request, product_id):
    return _handle_comments(request, FurnitureAppliances, product_id, 'furniture_appliances')


@require_http_methods(["GET", "POST"])
def get_pcs_peripherals_comments(request, product_id):
    return _handle_comments(request, PCsPeripherals, product_id, 'pcs_peripherals')


@require_http_methods(["GET", "POST"])
def get_musical_instruments_comments(request, product_id):
    return _handle_comments(request, MusicalInstruments, product_id, 'musical_instruments')


@require_http_methods(["GET", "POST"])
def get_mobile_devices_accessories_comments(request, product_id):
    return _handle_comments(request, MobileDevicesAccessories, product_id, 'mobile_devices_accessories')


@require_http_methods(["GET", "POST"])
def get_electronics_appliances_comments(request, product_id):
    return _handle_comments(request, ElectronicsAppliances, product_id, 'electronics_appliances')


@require_http_methods(["GET", "POST"])
def get_fashionwear_addons_comments(request, product_id):
    return _handle_comments(request, FashionwearAddons, product_id, 'fashionwear_addons')


@require_http_methods(["GET", "POST"])
def get_tools_machinery_comments(request, product_id):
    return _handle_comments(request, ToolsMachinery, product_id, 'tools_machinery')


@require_http_methods(["GET", "POST"])
def get_cameras_accessories_comments(request, product_id):
    return _handle_comments(request, CamerasAccessories, product_id, 'cameras_accessories')


@require_http_methods(["GET", "POST"])
def get_food_beverages_comments(request, product_id):
    return _handle_comments(request, FoodBeverages, product_id, 'food_beverages')
