from django.contrib import admin
from .models import Product, Variation, Value, Price, Stock, ReviewRating, Gallery
import admin_thumbnails

# Register your models here.

@admin_thumbnails.thumbnail("image")
class GalleryInline(admin.TabularInline):
  model = Gallery
  extra = 1

class ProductAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug" : ["name",]}
  list_display = ["name", "category", "price", "last_modified", "is_available",]
  inlines = [GalleryInline,]

class VariationAdmin(admin.ModelAdmin):
  list_filter = ["category", "product",]


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Value)
admin.site.register(Price)
admin.site.register(Stock)
admin.site.register(ReviewRating)
admin.site.register(Gallery)