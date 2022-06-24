from django.contrib import admin
from .models import Payment, Order, OrderProduct

# Register your models here.

class OrderProductInline(admin.TabularInline):
  # this will create a table of instance of type "OrderProdcut" that are connected to
  # the "Order" Instance
  model = OrderProduct
  extra = 0 # number of extra rows
  readonly_fields = ["payment", "user", "product", "quantity", "product_price", "ordered", "value"]

class OrderAdmin(admin.ModelAdmin):
  list_display = ['full_name', 'order_total', 'order_number', 'is_ordered', 'phone', 'email']
  list_filter = ["status", "is_ordered"]
  search_fields = ["order_number", 'first_name', "last_name", "phone", "email"]
  list_per_page = 20
  inlines = [OrderProductInline]

class OrderProductAdmin(admin.ModelAdmin):
  list_display = ['product', 'values']

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)