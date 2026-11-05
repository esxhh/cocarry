from decimal import Decimal
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Product, Order, OrderItem
from .forms import CheckoutForm
from .email_service import send_order_emails

SHIPPING_FEE = Decimal("49.00")

def home(request):
    products = Product.objects.filter(is_featured=True, stock__gt=0)[:8]
    return render(request, "shop/home.html", {"products": products})

def shop(request):
    products = Product.objects.all()
    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(name__icontains=query)
    category = request.GET.get("category")
    if category:
        products = products.filter(category__icontains=category)
    sort = request.GET.get("sort")
    if sort == "price_low":
        products = products.order_by("discounted_price")
    elif sort == "price_high":
        products = products.order_by("-discounted_price")
    elif sort == "newest":
        products = products.order_by("-created_at")
    return render(request, "shop/shop.html", {"products": products, "query": query})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "shop/product_detail.html", {"product": product})

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})
    key = str(product.id)
    cart[key] = int(cart.get(key, 0)) + 1
    if cart[key] > product.stock:
        cart[key] = product.stock
        messages.warning(request, "We've limited the quantity to available stock.")
    request.session["cart"] = cart
    messages.success(request, f"{product.name} added to your bag.")
    return redirect(request.POST.get("next") or "cart")

def cart(request):
    cart_data = request.session.get("cart", {})
    items, subtotal = [], Decimal("0.00")
    for pid, qty in cart_data.items():
        product = Product.objects.filter(id=pid).first()
        if not product:
            continue
        qty = min(int(qty), product.stock)
        line_total = product.discounted_price * qty
        subtotal += line_total
        items.append({"product": product, "quantity": qty, "line_total": line_total})
    shipping = SHIPPING_FEE if subtotal else Decimal("0.00")
    return render(request, "shop/cart.html", {"items": items, "subtotal": subtotal, "shipping": shipping, "total": subtotal + shipping})

@require_POST
def update_cart(request, product_id):
    cart_data = request.session.get("cart", {})
    product = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get("quantity", 1))
    if qty <= 0:
        cart_data.pop(str(product_id), None)
    else:
        cart_data[str(product_id)] = min(qty, product.stock)
    request.session["cart"] = cart_data
    return redirect("cart")

def checkout(request):
    cart_data = request.session.get("cart", {})
    if not cart_data:
        messages.info(request, "Your bag is empty.")
        return redirect("shop")
    cart_items, subtotal = [], Decimal("0.00")
    for pid, qty in cart_data.items():
        product = Product.objects.filter(id=pid).first()
        if product and product.stock:
            qty = min(int(qty), product.stock)
            cart_items.append((product, qty))
            subtotal += product.discounted_price * qty
    if not cart_items:
        return redirect("cart")
    shipping = SHIPPING_FEE
    total = subtotal + shipping

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.subtotal = subtotal
                order.shipping_fee = shipping
                order.total_amount = total
                order.payment_status = "Pending" if order.payment_method == "cod" else "Awaiting gateway payment"
                order.save()
                for product, qty in cart_items:
                    product.refresh_from_db()
                    if product.stock < qty:
                        messages.error(request, f"Not enough stock for {product.name}. Please update your bag.")
                        order.delete()
                        return redirect("cart")
                    OrderItem.objects.create(
                        order=order, product=product, product_name=product.name,
                        quantity=qty, price_at_purchase=product.discounted_price,
                        product_image_url=product.cover_image,
                    )
                    product.stock -= qty
                    product.save(update_fields=["stock"])
            request.session["cart"] = {}
            send_order_emails(order)
            return render(request, "shop/order_success.html", {"order": order})
    else:
        form = CheckoutForm()
    return render(request, "shop/checkout.html", {"form": form, "cart_items": cart_items, "subtotal": subtotal, "shipping": shipping, "total": total})
