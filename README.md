# 👟 ShoeStore - Full-Stack E-Commerce Platform

A production-style, modern, full-stack e-commerce web application for athletic and lifestyle footwear built with **Python (Flask)**, **SQLAlchemy ORM**, **PostgreSQL / SQLite**, **Flask-Login**, **Flask-Migrate**, and a dynamic, responsive **HTML5/CSS3/Vanilla JS** frontend with **RESTful API** architecture.

---

## 🌟 Key Features

### 🛍 Customer Experience
- **Modern Sneaker Boutique UI**: Vibrant dark mode aesthetic with custom glassmorphism components, micro-animations, and responsive mobile layout.
- **Product Catalogue**: Advanced multi-attribute filtering (category, brand, price slider, size picker), keyword search, sorting (newest, price low/high, rating), and pagination.
- **Product Detail**: Interactive size picker, live quantity toggles, high-resolution product previews, stock indicators, and related product recommendations.
- **Shopping Cart**: Real-time cart badge counter, item quantity modification, size selection, free shipping calculation threshold, and persistent cart storage.
- **Wishlist**: Save favorite kicks, view saved items, and seamlessly move items from wishlist directly to cart.
- **Checkout & Orders**: Multi-step checkout with customer address collection, mock payment flow (Credit Card / PayPal), unique order number generation (`ORD-YYYYMMDD-XXXX`), order history receipts, and real-time status tracking.

### 🛡 Admin Dashboard
- **Executive Analytics**: Live metric stat cards (Total Net Revenue, Orders, Active Shoes, Registered Customers), recent sales table, and low-stock inventory alerts (&le; 10 units).
- **Product Management (CRUD)**: Add new shoes, edit metadata/prices/sizes/colorways, upload/assign image URLs, and delete products.
- **Inventory Management**: Real-time stock unit modifier with stock protection against negative inventory.
- **Order Fulfillment**: Track all customer orders and modify fulfillment status (`Pending`, `Confirmed`, `Processing`, `Shipped`, `Delivered`, `Cancelled`).
- **User Directory**: View registered customer accounts and administrator privileges.

---

## 🛠 Tech Stack

- **Backend**: Python 3.11, Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-WTF, Werkzeug
- **Database**: PostgreSQL (via `DATABASE_URL`) or SQLite (`shoestore.db` fallback)
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design Tokens), Vanilla JavaScript (Fetch API, Toast Notifications), Jinja2 Templates
- **Testing**: Pytest automated test suite
- **Authentication**: Werkzeug pbkdf2:sha256 password hashing, session management, `@admin_required` authorization

---

## 📐 Architecture & Project Structure

```
shoe-store/
├── app/
│   ├── __init__.py           # Application Factory & Error Handlers
│   ├── config.py             # Configs (Dev, Testing, Prod)
│   ├── extensions.py         # SQLAlchemy, Migrate, LoginManager, CSRF
│   ├── models/               # SQLAlchemy ORM Data Models
│   │   ├── __init__.py
│   │   ├── user.py           # User model with role ('customer'/'admin')
│   │   ├── category.py       # Product Category model
│   │   ├── product.py        # Shoe Product model (sizes, stock, price)
│   │   ├── cart.py           # Shopping Cart Item model
│   │   ├── wishlist.py       # Wishlist Item model
│   │   ├── order.py          # Order Header model
│   │   └── order_item.py     # Order Line Item model
│   ├── routes/               # Flask Web & REST API Blueprints
│   │   ├── __init__.py
│   │   ├── auth.py           # Registration, Login, Logout, Profile API
│   │   ├── main.py           # Homepage Blueprint
│   │   ├── products.py       # Product Catalogue & Detail API
│   │   ├── cart.py           # Cart management API
│   │   ├── wishlist.py       # Wishlist API
│   │   ├── orders.py         # Checkout & Order History API
│   │   └── admin.py          # Protected Admin Panel & APIs
│   ├── services/             # Business Logic & DB Transactions
│   │   ├── __init__.py
│   │   ├── product_service.py
│   │   ├── cart_service.py
│   │   ├── order_service.py  # Atomic order creation & inventory check
│   │   └── inventory_service.py
│   ├── templates/            # Jinja2 HTML Templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── products.html
│   │   ├── product.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── orders.html
│   │   ├── wishlist.html
│   │   ├── profile.html
│   │   ├── errors/ (404, 500)
│   │   └── admin/ (dashboard, products, orders, inventory, users)
│   └── static/
│       ├── css/ (main.css, admin.css)
│       ├── js/ (main.js)
│       └── images/ (SVG vector assets)
├── tests/                    # Automated Pytest Test Suite
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_products.py
│   ├── test_cart.py
│   ├── test_orders.py
│   └── test_admin.py
├── seed.py                   # Data Seeding Script (Admin, Customer, 20+ Shoes)
├── .env                      # Environment Variables
├── .env.example
├── requirements.txt          # Python Dependencies
├── run.py                    # Entry Point Server Runner
└── README.md
```

---

## ⚡ Quick Start & Installation

### 1. Clone & Setup Environment

```bash
cd "c:\Users\theaa\Desktop\SHOE STORE"
python -m venv venv
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Configuration

Create a `.env` file (or copy `.env.example`):

```env
SECRET_KEY=shoestore-super-secret-key-2026-production-grad-key
DATABASE_URL=sqlite:///shoestore.db
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
```

> **Note**: To use PostgreSQL, set `DATABASE_URL=postgresql://username:password@localhost:5432/shoestore_db`.

### 4. Seed the Database

Run the database seed script to populate sample categories, admin user, customer user, and 20+ realistic shoes:

```bash
python seed.py
```

### 5. Run the Application

```bash
python run.py
```

Open your browser and navigate to **`http://127.0.0.1:5000`**.

---

## 🔑 Demo Login Credentials

- **Admin Account**:
  - Email: `admin@shoestore.com`
  - Password: `admin123`
  - Access: Full Admin Dashboard (`/admin/dashboard`)

- **Customer Account**:
  - Email: `customer@shoestore.com`
  - Password: `customer123`

---

## 🧪 Running Automated Tests

Run the test suite using `pytest`:

```bash
pytest
```

---

## 🔌 RESTful API Documentation

| Endpoint | Method | Description | Auth Required |
|---|---|---|---|
| `POST /api/auth/register` | `POST` | Register new customer account | No |
| `POST /api/auth/login` | `POST` | Authenticate user & start session | No |
| `POST /api/auth/logout` | `POST` | Terminate session | Yes |
| `GET /api/auth/me` | `GET` | Get authenticated user info | No |
| `GET /api/products` | `GET` | Get filtered, sorted, paginated shoes | No |
| `GET /api/products/<id>` | `GET` | Get detailed product by ID | No |
| `GET /api/cart` | `GET` | Fetch active user/session cart summary | No |
| `POST /api/cart` | `POST` | Add product item to cart | No |
| `PUT /api/cart/<item_id>` | `PUT` | Update cart item quantity | No |
| `DELETE /api/cart/<item_id>`| `DELETE` | Remove item from cart | No |
| `GET /api/wishlist` | `GET` | Fetch saved wishlist items | Yes |
| `POST /api/wishlist` | `POST` | Add product to wishlist | Yes |
| `DELETE /api/wishlist/<id>`| `DELETE` | Remove item from wishlist | Yes |
| `POST /api/orders` | `POST` | Submit cart & place order | Yes |
| `GET /api/orders` | `GET` | Fetch user order history | Yes |
| `GET /api/orders/<id>` | `GET` | Get single order details | Yes |
| `POST /admin/api/products` | `POST` | Create new product | Admin |
| `PUT /admin/api/products/<id>`| `PUT` | Update product details | Admin |
| `DELETE /admin/api/products/<id>`| `DELETE` | Delete product | Admin |
| `PUT /admin/api/products/<id>/stock`| `PUT` | Update product stock | Admin |
| `PUT /admin/api/orders/<id>/status`| `PUT` | Update order status | Admin |

---

## 🚀 Deployment Instructions

1. **Environment**: Set `FLASK_ENV=production` and specify a strong `SECRET_KEY` in environment variables.
2. **Database**: Provide a managed PostgreSQL connection string in `DATABASE_URL`.
3. **WSGI Server**: Serve the app using Gunicorn or Waitress:
   ```bash
   pip install gunicorn
   gunicorn "app:create_app()" -w 4 -b 0.0.0.0:8000
   ```
