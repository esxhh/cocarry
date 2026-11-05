import uuid
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=140)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=80, default="Aesthetic Totes")
    material = models.CharField(max_length=120, default="Cotton canvas")
    dimensions = models.CharField(max_length=120, default="38 ×  P ×  34 cm")
    available_colors = models.CharField(max_length=200, default="Natural, Black")
    features = models.TextField(default="Spacious interior; sturdy handles; reusable")
    stock = models.PositiveIntegerField(default=25)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.7)
    is_featured = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        if self.price and self.price > self.discounted_price:
            return round((self.price - self.discounted_price) * 100 / self.price)
        return 0

    @property
    def cover_image(self):
        first = self.images.first()
        return first.image_url if first else "https://images.unsplash.com/photo-1590874103328-eac38a683ce7"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image_url = models.URLField(max_length=600)
    alt_text = models.CharField(max_length=180, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"{self.product.name} image {self.display_order + 1}"

class Order(models.Model):
    STATUS_CHOICES = [
        ("placed", "Placed"), ("processing", "Processing"),
        ("shipped", "Shipped"), ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    PAYMENT_CHOICES = [("cod", "Cash on Delivery"), ("online", "Online Payment")]
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    customer_name = models.CharField(max_length=160)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    address_line = models.CharField(max_length=250)
    landmark = models.CharField(max_length=180, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=12, choices=PAYMENT_CHOICES, default="cod")
    payment_status = models.CharField(max_length=30, default="Pending")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="placed")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"COCARRY #{str(self.order_id)[:8].upper()}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=140)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=8, decimal_places=2)
    product_image_url = models.URLField(max_length=600, blank=True)

    def line_total(self):
        return self.quantity * self.price_at_purchase

    def __str__(self):
        return f"{self.product_name} × {self.quantity}"
