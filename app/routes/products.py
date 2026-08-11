from flask import Blueprint, render_template, request, jsonify
from app.extensions import db
from app.models import Product, Category
from app.services.product_service import ProductService

products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
def catalogue():
    category_slug = request.args.get('category', None)
    brand = request.args.get('brand', None)
    gender = request.args.get('gender', None)
    min_price = request.args.get('min_price', None)
    max_price = request.args.get('max_price', None)
    size = request.args.get('size', None)
    search_query = request.args.get('q', None)
    sort_by = request.args.get('sort', 'newest')
    is_new = True if request.args.get('new') == 'true' else None
    collection = request.args.get('collection', None)
    page = request.args.get('page', 1, type=int)

    is_featured = True if collection == 'best-sellers' else None
    if collection == 'new-releases':
        is_new = True

    pagination = ProductService.get_filtered_products(
        category_slug=category_slug,
        brand=brand,
        gender=gender,
        min_price=min_price,
        max_price=max_price,
        size=size,
        search_query=search_query,
        sort_by=sort_by,
        is_new_release=is_new,
        is_featured=is_featured,
        page=page,
        per_page=12
    )

    categories = Category.query.all()
    brands = ProductService.get_all_brands()
    active_category = Category.query.filter_by(slug=category_slug).first() if category_slug else None

    # Title label
    catalog_title = "ALL PRODUCTS"
    if gender:
        catalog_title = f"{gender.upper()}'S FOOTWEAR"
    elif active_category:
        catalog_title = f"{active_category.name.upper()}"
    elif is_new:
        catalog_title = "NEW RELEASES"
    elif collection == 'best-sellers':
        catalog_title = "BEST SELLERS"

    return render_template(
        'products.html',
        pagination=pagination,
        products=pagination.items,
        categories=categories,
        brands=brands,
        active_category=active_category,
        catalog_title=catalog_title,
        current_filters={
            'category': category_slug,
            'brand': brand,
            'gender': gender,
            'min_price': min_price,
            'max_price': max_price,
            'size': size,
            'q': search_query,
            'sort': sort_by,
            'new': request.args.get('new'),
            'collection': collection
        }
    )

@products_bp.route('/products/<int:product_id>')
def product_detail(product_id):
    product = db.get_or_404(Product, product_id)
    # Fetch related products from same category
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id
    ).limit(6).all()

    return render_template('product.html', product=product, related_products=related_products)

# --- REST API ENDPOINTS ---

@products_bp.route('/api/products', methods=['GET'])
def api_get_products():
    category_slug = request.args.get('category', None)
    brand = request.args.get('brand', None)
    gender = request.args.get('gender', None)
    min_price = request.args.get('min_price', None)
    max_price = request.args.get('max_price', None)
    size = request.args.get('size', None)
    search_query = request.args.get('q', None)
    sort_by = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)

    pagination = ProductService.get_filtered_products(
        category_slug=category_slug,
        brand=brand,
        gender=gender,
        min_price=min_price,
        max_price=max_price,
        size=size,
        search_query=search_query,
        sort_by=sort_by,
        page=page,
        per_page=per_page
    )

    return jsonify({
        'products': [p.to_dict() for p in pagination.items],
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }), 200

@products_bp.route('/api/products/<int:product_id>', methods=['GET'])
def api_get_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({'product': product.to_dict()}), 200
