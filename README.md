# COCARRY Django Tote Bag Store

A responsive Gen-Z tote bag storefront using Django, SQLite, session cart, guest checkout, Django admin, and SMTP order notifications.

## Included
- COCARRY editorial-inspired storefront and responsive mobile layouts
- Five seeded tote bag products, each with six distinct image URL slots
- Product listing/detail gallery, search, sort, cart and checkout
- Cash on Delivery order placement with database persistence
- Order email notification to **cocarrytotes@gmail.com** plus customer confirmation
- Admin product, image, inventory, and order management

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `.env`. For Gmail SMTP, create a Google App Password and put it in `EMAIL_HOST_PASSWORD`. Never use your ordinary account password or commit `.env`.

Then:
```powershell
python manage.py migrate
python manage.py seed_products
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/ and admin at http://127.0.0.1:8000/admin/.

## Deploy to Render

The repository includes a Render Blueprint in `render.yaml`. It creates the
Singapore web service on Render's free plan, with no paid database or other
paid resources. The demo uses SQLite on the service's temporary filesystem.
Render can spin the service down and discard its filesystem on a restart or
deploy, so products and orders may reset or be lost. Do not use this deployment
for reliable order storage.

Push this repository to GitHub, then create a new Blueprint from it in the
Render dashboard. Render generates the `SECRET_KEY`; `DEBUG` is disabled. The
service runs migrations and seeds the catalog when it starts.
Configure `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and related SMTP variables
in the Render dashboard if checkout emails should be delivered. Do not put
production secrets in Git.

For a custom domain, set `ALLOWED_HOSTS` to include its hostname and
`CSRF_TRUSTED_ORIGINS` to its full HTTPS origin in the Render dashboard.

## Email
The official recipient is configured by default as `COCARRY_BRAND_EMAIL=cocarrytotes@gmail.com`. Successful checkout saves the order first and then attempts brand and customer email. Failures are logged and do not roll back the order. SMTP must be configured for messages to actually be delivered.

## Notes
- Product images are loaded from remote Unsplash URLs; internet access is needed to display them. Admin can edit image URL entries.
- Online payment is not active. COD is functional; Razorpay requires merchant credentials and server-side payment verification before enabling.
- Local development uses SQLite. Production requires `SECRET_KEY` and `DATABASE_URL`; PostgreSQL and HTTPS security settings are enabled automatically when `DEBUG=False`.
