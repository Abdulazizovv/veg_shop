from django.contrib import admin
from .models import CustomUser, Profile, Product, SoldProduct, BuyerInfo


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'description', 'date_posted']
    list_filter = ['category']
    search_fields = ['name', 'category']
    list_per_page = 10


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user__email']
    search_fields = ['user__email']
    list_per_page = 10


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_staff', 'is_active']
    search_fields = ['email']
    list_per_page = 10


class BuyerInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'phone_number']
    search_fields = ['user', 'address', 'phone_number']
    list_per_page = 10


class SoldProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'buyer', 'date_sold', 'status']
    search_fields = ['product', 'buyer']
    list_per_page = 10





admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(SoldProduct, SoldProductAdmin)
admin.site.register(BuyerInfo, BuyerInfoAdmin)

