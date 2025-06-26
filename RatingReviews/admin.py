from django.contrib import admin
from RatingReviews.models import Comment,Chats

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'get_product_name', 'created_at', 'is_reply')
    list_filter = ('created_at',)
    search_fields = ('user_name', 'text')

    def get_product_name(self, obj):
        product = (
            obj.realestate or obj.books_education or obj.health_beauty or
            obj.household_accessories or obj.automobiles or obj.furniture_appliances or
            obj.pcs_peripherals or obj.musical_instruments or obj.mobile_devices_accessories or
            obj.electronics_appliances or obj.fashionwear_addons or obj.tools_machinery or
            obj.cameras_accessories or obj.food_beverages
        )
        return getattr(product, 'title', str(product)) if product else "No Product"
    get_product_name.short_description = 'Product'

    def is_reply(self, obj):
        return obj.parent is not None
    is_reply.boolean = True





@admin.register(Chats)
class ChatsAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')