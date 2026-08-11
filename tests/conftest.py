import pytest
from app import create_app
from app.extensions import db
from app.models import User, Category, Product, CartItem, Order

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        
        # Seed basic category
        cat = Category(name="Running", slug="running", description="Running shoes")
        db.session.add(cat)
        db.session.commit()

        # Seed sample product
        prod = Product(
            name="Test Shoe Pro",
            brand="TestBrand",
            description="High quality test shoe",
            price=120.00,
            discount_price=100.00,
            category_id=cat.id,
            color="Red",
            image_url="/static/images/placeholder_shoe.svg",
            stock_quantity=10,
            rating=4.5
        )
        prod.sizes_list = [8, 9, 10]
        db.session.add(prod)

        # Seed Admin & Customer
        admin = User(full_name="Admin User", email="admin@test.com", role="admin")
        admin.set_password("admin123")

        customer = User(full_name="Customer User", email="customer@test.com", role="customer")
        customer.set_password("customer123")

        db.session.add_all([admin, customer])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
