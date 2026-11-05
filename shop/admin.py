from django.contrib import admin
from .models import Product, ProductImage, Order, OrderItem

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "discounted_price", "stock", "is_featured", "is_bestseller")
    list_filter = ("category", "is_featured", "is_bestseller")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "quantity", "price_at_purchase", "product_image_url")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "customer_name", "customer_email", "total_amount", "payment_method", "status", "created_at")
    list_filter = ("status", "payment_method", "payment_status", "created_at")
    search_fields = ("customer_name", "customer_email", "customer_phone", "order_id")
    readonly_fields = ("order_id", "created_at")
    inlines = [OrderItemInline]

admin.site.register(ProductImage)
