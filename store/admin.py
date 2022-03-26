from django.contrib import admin
from .models import Product, Variation, Value, Price

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug" : ["name",]}
  list_display = ["name", "category", "price", "stock", "last_modified", "is_available",]

class VariationAdmin(admin.ModelAdmin):
  list_filter = ["category", "product",]


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Value)
admin.site.register(Price)