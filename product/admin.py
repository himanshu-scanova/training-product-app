from product.api.models import ProductModel
from django.contrib import admin


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "id", )
    list_filter = ['category']
    search_fields = ['name']


admin.site.register(ProductModel, ProductAdmin)
