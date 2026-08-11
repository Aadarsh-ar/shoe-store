from app import create_app
from app.extensions import db
from app.models import User, Category, Product

def seed_database():
    app = create_app('development')
    with app.app_context():
        print("Resetting database tables...")
        db.drop_all()
        db.create_all()

        print("Seeding Users...")
        # 1. Admin Account
        admin = User(
            full_name="Aadarsh (Admin)",
            email="theaaadarsh15@gmail.com",
            role="admin"
        )
        admin.set_password("Aadarsh@15")
        db.session.add(admin)

        # 2. Demo Customer Account
        customer = User(
            full_name="Alex Morgan",
            email="customer@shoestore.com",
            role="customer"
        )
        customer.set_password("customer123")
        db.session.add(customer)

        db.session.commit()

        print("Seeding Categories...")
        categories_data = [
            {"name": "Running", "slug": "running", "description": "High-performance responsive cushion running shoes engineered for speed & endurance."},
            {"name": "Basketball", "slug": "basketball", "description": "High-top dynamic court performance sneakers built for traction & explosive vertical jump."},
            {"name": "Lifestyle", "slug": "lifestyle", "description": "Sleek casual streetwear sneakers for supreme daily comfort and style."},
            {"name": "Skateboard", "slug": "skateboard", "description": "Durable suede skate shoes with vulc soles for ultimate board feel and grip."},
            {"name": "Outdoor & Trail", "slug": "outdoor", "description": "Weather-resistant trail runners and hiking shoes with aggressive lugs for rugged terrain."}
        ]

        categories_map = {}
        for cat in categories_data:
            c = Category(
                name=cat["name"],
                slug=cat["slug"],
                description=cat["description"],
                image_url="/static/images/hero_shoe.svg"
            )
            db.session.add(c)
            db.session.flush()
            categories_map[cat["slug"]] = c.id

        db.session.commit()

        print("Seeding 20+ Shoe Products with Gender & Release attributes...")
        products_data = [
            # Men's Shoes
            {
                "name": "ApexRun Nitro Pro 5",
                "brand": "ApexRun",
                "gender": "Men",
                "category_slug": "running",
                "description": "Engineered carbon-plated long-distance running shoe with ultra-light nitrogen injected foam cushioning.",
                "price": 189.99,
                "discount_price": 159.99,
                "color": "Triple Black / Cyber Cyan",
                "stock_quantity": 25,
                "rating": 4.9,
                "sizes": [8, 9, 9.5, 10, 10.5, 11, 12],
                "is_featured": True,
                "is_new_release": True,
                "image_url": "/static/images/hero_shoe.svg"
            },
            {
                "name": "AirFlex CloudStride X",
                "brand": "AirFlex",
                "gender": "Men",
                "category_slug": "running",
                "description": "Plush daily trainer featuring breathable flyknit mesh upper and responsive dual-density midsole foam.",
                "price": 139.99,
                "discount_price": None,
                "color": "Monochrome White / Silver",
                "stock_quantity": 18,
                "rating": 4.7,
                "sizes": [8, 9, 10, 11, 12],
                "is_featured": True,
                "is_new_release": True,
                "image_url": "/static/images/hero_shoe.svg"
            },
            {
                "name": "StreetPulse Hyper Dunk 99",
                "brand": "StreetPulse",
                "gender": "Men",
                "category_slug": "basketball",
                "description": "High-cut lockdown ankle support basketball shoe with air zoom heel pods for explosive rebounds.",
                "price": 179.99,
                "discount_price": 149.99,
                "color": "Stealth Black / Metallic Gold",
                "stock_quantity": 15,
                "rating": 4.9,
                "sizes": [9, 10, 11, 12, 13],
                "is_featured": True,
                "is_new_release": True,
                "image_url": "/static/images/hero_shoe.svg"
            },
            {
                "name": "StreetPulse Urban Glide 80s",
                "brand": "StreetPulse",
                "gender": "Men",
                "category_slug": "lifestyle",
                "description": "Classic minimalist low-top premium leather sneaker crafted for effortless daily rotation.",
                "price": 109.99,
                "discount_price": 89.99,
                "color": "Crisp White / Gum Sole",
                "stock_quantity": 40,
                "rating": 4.8,
                "sizes": [7, 8, 9, 10, 11, 12],
                "is_featured": True,
                "is_new_release": False,
                "image_url": "/static/images/promo_shoe.svg"
            },
            {
                "name": "TerraTrek Summit Ridge GTX",
                "brand": "TerraTrek",
                "gender": "Men",
                "category_slug": "outdoor",
                "description": "Waterproof Gore-Tex trail runner built with Vibram mega-grip outsole for mud and wet granite.",
                "price": 175.00,
                "discount_price": 149.00,
                "color": "Forest Slate / Amber",
                "stock_quantity": 21,
                "rating": 4.9,
                "sizes": [8, 9, 10, 11, 12],
                "is_featured": True,
                "is_new_release": True,
                "image_url": "/static/images/hero_shoe.svg"
            },

            # Women's Shoes
            {
                "name": "NovaStep AeroFly W 2026",
                "brand": "NovaStep",
                "gender": "Women",
                "category_slug": "running",
                "description": "Maximum cushion marathon trainer designed specifically for women's biomechanics.",
                "price": 169.99,
                "discount_price": None,
                "color": "Pure White / Coral",
                "stock_quantity": 30,
                "rating": 4.8,
                "sizes": [6, 7, 7.5, 8, 8.5, 9],
                "is_featured": True,
                "is_new_release": True,
                "image_url": "/static/images/promo_shoe.svg"
            },
            {
                "name": "AirFlex Flight Master W",
                "brand": "AirFlex",
                "gender": "Women",
                "category_slug": "basketball",
                "description": "Retro-inspired high top silhouette blended with modern performance court materials.",
                "price": 199.99,
                "discount_price": None,
                "color": "Obsidian / Rose Gold",
                "stock_quantity": 8,
                "rating": 5.0,
                "sizes": [6, 7, 8, 9],
                "is_featured": True,
                "is_new_release": False,
                "image_url": "/static/images/hero_shoe.svg"
            },
            {
                "name": "ApexRun Future Craft W",
                "brand": "ApexRun",
                "gender": "Women",
                "category_slug": "lifestyle",
                "description": "Futuristic 3D-printed lattice midsole lifestyle shoe with metallic iridescent heel tab.",
                "price": 220.00,
                "discount_price": 185.00,
                "color": "Iridescent Pearl White",
                "stock_quantity": 12,
                "rating": 4.9,
                "sizes": [6.5, 7.5, 8.5, 9.5],
                "is_featured": True,
                "is_new_release": True,
                "image_url": "/static/images/hero_shoe.svg"
            },
            {
                "name": "VoltMotion Velocity W",
                "brand": "VoltMotion",
                "gender": "Women",
                "category_slug": "running",
                "description": "Ultra-lightweight sprint flat designed for 5K to 10K racing with aggressive forefoot traction.",
                "price": 119.99,
                "discount_price": 99.99,
                "color": "Electric Mauve",
                "stock_quantity": 14,
                "rating": 4.6,
                "sizes": [6, 7, 8, 9],
                "is_featured": False,
                "is_new_release": True,
                "image_url": "/static/images/promo_shoe.svg"
            },
            {
                "name": "TerraTrek Canyon Hiker W",
                "brand": "TerraTrek",
                "gender": "Women",
                "category_slug": "outdoor",
                "description": "Breathable mountain approach trail shoe with rock protection plate and reinforced bumper.",
                "price": 145.00,
                "discount_price": None,
                "color": "Sandstone / Sage",
                "stock_quantity": 16,
                "rating": 4.7,
                "sizes": [6, 7, 8, 9],
                "is_featured": False,
                "is_new_release": False,
                "image_url": "/static/images/placeholder_shoe.svg"
            },

            # Kids' Shoes
            {
                "name": "StreetPulse Junior Runner",
                "brand": "StreetPulse",
                "gender": "Kids",
                "category_slug": "running",
                "description": "Durable easy-strap athletic sneaker built for active kids and playground performance.",
                "price": 69.99,
                "discount_price": 54.99,
                "color": "Black / Neon Yellow",
                "stock_quantity": 25,
                "rating": 4.7,
                "sizes": [3.5, 4.5, 5.5, 6.5],
                "is_featured": True,
                "is_new_release": True,
                "image_url": "/static/images/promo_shoe.svg"
            },
            {
                "name": "VoltMotion Young Dunk",
                "brand": "VoltMotion",
                "gender": "Kids",
                "category_slug": "basketball",
                "description": "Padded ankle support youth basketball sneaker built with non-marking traction outsole.",
                "price": 79.99,
                "discount_price": None,
                "color": "Red / Black",
                "stock_quantity": 18,
                "rating": 4.8,
                "sizes": [4, 5, 6],
                "is_featured": True,
                "is_new_release": True,
                "image_url": "/static/images/hero_shoe.svg"
            },

            # Unisex / Lifestyle & Skate
            {
                "name": "StreetPulse Boarder Pro Vulc",
                "brand": "StreetPulse",
                "gender": "Unisex",
                "category_slug": "skateboard",
                "description": "Reinforced heavy-duty suede skate shoe with rubber toe cap and sticky gum tread for maximum flick.",
                "price": 84.99,
                "discount_price": None,
                "color": "Black Suede / White Sole",
                "stock_quantity": 28,
                "rating": 4.7,
                "sizes": [7, 8, 9, 10, 11],
                "is_featured": False,
                "is_new_release": False,
                "image_url": "/static/images/promo_shoe.svg"
            },
            {
                "name": "VoltMotion Kickflip Hi",
                "brand": "VoltMotion",
                "gender": "Unisex",
                "category_slug": "skateboard",
                "description": "High-top canvas and suede skate sneaker with padded collar to protect ankles during big drops.",
                "price": 89.99,
                "discount_price": 74.99,
                "color": "Checkerboard Black / Red",
                "stock_quantity": 16,
                "rating": 4.6,
                "sizes": [8, 9, 10, 11, 12],
                "is_featured": False,
                "is_new_release": True,
                "image_url": "/static/images/hero_shoe.svg"
            },
            {
                "name": "NovaStep Grindhouse Low",
                "brand": "NovaStep",
                "gender": "Unisex",
                "category_slug": "skateboard",
                "description": "Impact absorbing heel gel pad skate shoe designed for rail grinds and stair sets.",
                "price": 95.00,
                "discount_price": None,
                "color": "Raw Ochre / Gum",
                "stock_quantity": 14,
                "rating": 4.5,
                "sizes": [7, 8, 9, 10],
                "is_featured": False,
                "is_new_release": False,
                "image_url": "/static/images/placeholder_shoe.svg"
            },
            {
                "name": "ApexRun All-Weather MudClaw",
                "brand": "ApexRun",
                "gender": "Men",
                "category_slug": "outdoor",
                "description": "Extreme 6mm lugged trail racing shoe designed for alpine ascents and obstacle course races.",
                "price": 160.00,
                "discount_price": 135.00,
                "color": "Hazard Yellow / Black",
                "stock_quantity": 3,
                "rating": 4.8,
                "sizes": [8, 9, 10, 11, 12],
                "is_featured": False,
                "is_new_release": True,
                "image_url": "/static/images/hero_shoe.svg"
            },
            {
                "name": "AirFlex Nomad Trail Sandal",
                "brand": "AirFlex",
                "gender": "Unisex",
                "category_slug": "outdoor",
                "description": "High-traction hybrid trail sport sandal with quick-drying straps and anatomic footbed.",
                "price": 79.99,
                "discount_price": 64.99,
                "color": "Earth Charcoal",
                "stock_quantity": 25,
                "rating": 4.6,
                "sizes": [7, 8, 9, 10, 11],
                "is_featured": False,
                "is_new_release": False,
                "image_url": "/static/images/placeholder_shoe.svg"
            },
            {
                "name": "VoltMotion Alpine Shield X",
                "brand": "VoltMotion",
                "gender": "Men",
                "category_slug": "outdoor",
                "description": "Insulated winter trail running shoe with zip gaiter upper and carbide tip ice studs.",
                "price": 195.00,
                "discount_price": None,
                "color": "Stealth Black / Cobalt",
                "stock_quantity": 11,
                "rating": 4.9,
                "sizes": [8, 9, 10, 11, 12],
                "is_featured": True,
                "is_new_release": True,
                "image_url": "/static/images/hero_shoe.svg"
            }
        ]

        for p_data in products_data:
            cat_id = categories_map[p_data["category_slug"]]
            product = Product(
                name=p_data["name"],
                brand=p_data["brand"],
                gender=p_data["gender"],
                category_id=cat_id,
                description=p_data["description"],
                price=p_data["price"],
                discount_price=p_data["discount_price"],
                color=p_data["color"],
                stock_quantity=p_data["stock_quantity"],
                rating=p_data["rating"],
                is_featured=p_data["is_featured"],
                is_new_release=p_data["is_new_release"],
                image_url=p_data["image_url"]
            )
            product.sizes_list = p_data["sizes"]
            db.session.add(product)

        db.session.commit()
        print("Database seeded successfully with updated gender & release attributes!")

if __name__ == '__main__':
    seed_database()
