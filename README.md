# OLX.UZ Marketplace Backend

## Loyiha haqida

Bu loyiha **OLX.UZ ga o‘xshash marketplace platformasining backend qismi** hisoblanadi. Loyiha Django va Django REST Framework yordamida ishlab chiqilgan bo‘lib, foydalanuvchilar mahsulotlarni ko‘rishi, sevimlilarga qo‘shishi, buyurtma berishi va sotuvchilar bilan savdo qilishi mumkin.

Platformada ikki xil foydalanuvchi roli mavjud:

* **Customer (xaridor)** – mahsulotlarni ko‘rish, qidirish, sevimlilarga qo‘shish, buyurtma berish va sotuvchilarga fikr qoldirish.
* **Seller (sotuvchi)** – mahsulot qo‘shish, tahrirlash, o‘chirish, buyurtmalarni boshqarish va sotuvlarni amalga oshirish.

### Asosiy texnologiyalar

* Python
* Django
* Django REST Framework
* PostgreSQL
* Simple JWT (autentifikatsiya)
* drf-spectacular (Swagger API dokumentatsiyasi)
* python-telegram-bot
* Git

---

# O‘rnatish va ishga tushirish

Quyidagi bosqichlar orqali loyihani lokal kompyuteringizda ishga tushirishingiz mumkin.

## 1. Repository ni klonlash

```bash
git clone https://github.com/mukhammadrizo2009/olx.uz.git
cd olx-marketplace-backend
```

## 2. Virtual environment yaratish

```bash
python -m venv venv
```

Faollashtirish:

Windows:

```bash
venv\Scripts\activate
```

Linux / MacOS:

```bash
source venv/bin/activate
```

## 3. Kerakli kutubxonalarni o‘rnatish

```bash
pip install -r requirements.txt
```

## 4. .env fayl yaratish

`.env.example` fayldan nusxa olib `.env` fayl yarating.

```bash
cp .env.example .env
```

## 5. Migratsiyalarni bajarish

```bash
python manage.py migrate
```

## 6. Superuser yaratish (ixtiyoriy)

```bash
python manage.py createsuperuser
```

## 7. Serverni ishga tushirish

```bash
python manage.py runserver
```

Server ishga tushgandan keyin:

```
http://127.0.0.1:8000
```

---

# .env fayl namunasi (.env.example)

```
DEBUG=True

SECRET_KEY=django-secret-key

POSTGRES_DB=olx_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=2009

ALLOWED_HOSTS=127.0.0.1,localhost
```

---

# API Dokumentatsiyasi (Swagger)

Loyihada **drf-spectacular** yordamida avtomatik API hujjatlari yaratilgan.

Swagger UI orqali barcha endpointlarni test qilish mumkin.

Swagger manzili:

```
http://127.0.0.1:8000/api/schema/swagger-ui/
```

Redoc hujjatlari:

```
http://127.0.0.1:8000/api/schema/redoc/
```

Bu sahifalarda barcha API endpointlar, request va response formatlari ko‘rsatilgan.

---

# Asosiy API endpointlar

### Autentifikatsiya

```
POST /api/v1/auth/telegram-login/
POST /api/v1/auth/refresh/
POST /api/v1/auth/logout/
```

### Mahsulotlar

```
GET    /api/v1/products/
GET    /api/v1/products/{id}/
POST   /api/v1/products/
PATCH  /api/v1/products/{id}/
DELETE /api/v1/products/{id}/
```

### Sevimlilar

```
GET    /api/v1/favorites/
POST   /api/v1/favorites/
DELETE /api/v1/favorites/{id}/
```

### Buyurtmalar

```
GET    /api/v1/orders/
POST   /api/v1/orders/
PATCH  /api/v1/orders/{id}/
```

### Fikrlar (Reviews)

```
GET  /api/v1/reviews/
POST /api/v1/reviews/
```

---

# Muallif

**Muhammad Rizo**

Najot Ta'lim backend dasturlash kursi uchun yakuniy loyiha.