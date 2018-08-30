from django.contrib import admin

from app_product.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_id', 'price', 'color', 'size', 'created']
    list_filter = ['created', 'size', 'color']
    search_fields = ['name', 'item_id']


admin.site.register(Product, ProductAdmin)
