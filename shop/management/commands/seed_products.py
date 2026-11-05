from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Product, ProductImage

PRODUCTS = [
    ("The Everyday Muse", "everyday-muse", "A clean, effortless canvas tote made for daily plans, campus days and spontaneous coffee runs.", 799, 599, "Minimalist Totes", "Premium cotton canvas", "38 × 34 × 8 cm", "Natural, Sand", "Minimalist aesthetic; spacious interior; reusable; sturdy shoulder straps", 4.8, True,
     ["photo-1590874103328-eac38a683ce7","photo-1544816155-12df9643f363","photo-1597481499750-3e6b22637e12","photo-1584917865442-de89df76afd3","photo-1591561954557-26941169b49e","photo-1548036328-c9fa89d128fa"]),
    ("Bloom Theory Tote", "bloom-theory", "A floral moodboard in tote form. Light, roomy and ready to brighten everyday outfits.", 899, 699, "Printed Totes", "Durable printed canvas", "38 × 35 × 9 cm", "Cream, Sage", "Floral aesthetic print; lightweight; roomy compartment; reinforced handles", 4.7, True,
     ["photo-1591561954557-26941169b49e","photo-1584917865442-de89df76afd3","photo-1590874103328-eac38a683ce7","photo-1544816155-12df9643f363","photo-1597481499750-3e6b22637e12","photo-1548036328-c9fa89d128fa"]),
    ("Midnight Mood Tote", "midnight-mood", "A sleek black essential with a little edge. Your everyday carry for college, work and city exploring.", 999, 749, "College Essentials", "Heavyweight cotton canvas", "40 × 36 × 10 cm", "Black, Charcoal", "Black minimalist design; unisex; laptop-friendly; reinforced stitching", 4.9, True,
     ["photo-1548036328-c9fa89d128fa","photo-1584917865442-de89df76afd3","photo-1590874103328-eac38a683ce7","photo-1544816155-12df9643f363","photo-1591561954557-26941169b49e","photo-1597481499750-3e6b22637e12"]),
    ("Coquette Dream Tote", "coquette-dream", "Soft pink, sweet details and main-character energy. A cute companion for gifting or daily styling.", 899, 649, "Aesthetic Totes", "Premium cotton", "36 × 33 × 8 cm", "Pastel Pink, Ivory", "Pastel aesthetic; lightweight; durable; spacious; gift-ready style", 4.6, False,
     ["photo-1597481499750-3e6b22637e12","photo-1591561954557-26941169b49e","photo-1544816155-12df9643f363","photo-1590874103328-eac38a683ce7","photo-1584917865442-de89df76afd3","photo-1548036328-c9fa89d128fa"]),
    ("The Art Club Tote", "art-club-tote", "A statement tote for sketchbooks, playlists and creative chaos. Art-inspired style with practical space.", 1099, 799, "Printed Totes", "Premium canvas", "42 × 38 × 10 cm", "Ecru, Multicolor", "Artistic graphic; large storage; statement design; reinforced stitching", 4.8, True,
     ["photo-1544816155-12df9643f363","photo-1590874103328-eac38a683ce7","photo-1597481499750-3e6b22637e12","photo-1548036328-c9fa89d128fa","photo-1591561954557-26941169b49e","photo-1584917865442-de89df76afd3"]),
]
class Command(BaseCommand):
    help = "Seed COCARRY with five demo tote bag products and six image URLs each."
    def handle(self, *args, **kwargs):
        for data in PRODUCTS:
            name, slug, desc, price, sale, category, material, dimensions, colors, features, rating, bestseller, photo_ids = data
            product, _ = Product.objects.update_or_create(slug=slug, defaults={
                "name": name, "description": desc, "price": price, "discounted_price": sale,
                "category": category, "material": material, "dimensions": dimensions,
                "available_colors": colors, "features": features, "stock": 30,
                "rating": rating, "is_featured": True, "is_bestseller": bestseller,
            })
            ProductImage.objects.filter(product=product).delete()
            for idx, photo_id in enumerate(photo_ids):
                url = f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w=900&q=85"
                ProductImage.objects.create(product=product, image_url=url, alt_text=f"{name} product view {idx+1}", display_order=idx)
            self.stdout.write(self.style.SUCCESS(f"Seeded {name}"))
        self.stdout.write(self.style.SUCCESS("COCARRY demo catalog ready."))
