from sqlalchemy import or_, and_, desc, asc
from app.models import Product, Category

class ProductService:

    @staticmethod
    def get_filtered_products(
        category_slug=None,
        brand=None,
        gender=None,
        min_price=None,
        max_price=None,
        size=None,
        search_query=None,
        sort_by='newest',
        is_new_release=None,
        is_featured=None,
        page=1,
        per_page=12
    ):
        query = Product.query

        # Filter by Category
        if category_slug:
            category = Category.query.filter_by(slug=category_slug).first()
            if category:
                query = query.filter(Product.category_id == category.id)
            else:
                query = query.filter(False)

        # Filter by Brand
        if brand:
            query = query.filter(Product.brand.ilike(f"%{brand}%"))

        # Filter by Gender (Men, Women, Kids, Unisex)
        if gender:
            g = gender.strip().capitalize()
            if g in ['Men', 'Women', 'Kids']:
                query = query.filter(or_(Product.gender == g, Product.gender == 'Unisex'))

        # New Releases filter
        if is_new_release:
            query = query.filter(Product.is_new_release == True)

        # Featured / Best Sellers filter
        if is_featured:
            query = query.filter(Product.is_featured == True)

        # Filter by Price Range
        if min_price is not None:
            try:
                min_p = float(min_price)
                query = query.filter(Product.price >= min_p)
            except ValueError:
                pass

        if max_price is not None:
            try:
                max_p = float(max_price)
                query = query.filter(Product.price <= max_p)
            except ValueError:
                pass

        # Filter by Size
        if size:
            query = query.filter(Product.available_sizes.ilike(f"%{size}%"))

        # Search Query across Name, Brand, Description, Color
        if search_query:
            term = f"%{search_query.strip()}%"
            query = query.filter(
                or_(
                    Product.name.ilike(term),
                    Product.brand.ilike(term),
                    Product.description.ilike(term),
                    Product.color.ilike(term)
                )
            )

        # Sorting Options
        if sort_by == 'price_low':
            query = query.order_by(asc(Product.price))
        elif sort_by == 'price_high':
            query = query.order_by(desc(Product.price))
        elif sort_by == 'rating':
            query = query.order_by(desc(Product.rating))
        elif sort_by == 'oldest':
            query = query.order_by(asc(Product.created_at))
        else:  # newest
            query = query.order_by(desc(Product.created_at))

        # Pagination
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination

    @staticmethod
    def get_featured_products(limit=8):
        return Product.query.filter_by(is_featured=True).limit(limit).all()

    @staticmethod
    def get_new_arrivals(limit=8):
        return Product.query.filter_by(is_new_release=True).order_by(desc(Product.created_at)).limit(limit).all()

    @staticmethod
    def get_all_brands():
        brands = Product.query.with_entities(Product.brand).distinct().all()
        return [b[0] for b in brands if b[0]]
