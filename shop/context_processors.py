def cart_context(request):
    cart = request.session.get("cart", {})
    count = sum(int(q) for q in cart.values())
    return {"cart_count": count}
