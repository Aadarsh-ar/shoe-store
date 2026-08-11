from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User
from app.services.cart_service import CartService

auth_bp = Blueprint('auth', __name__)

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Admin authorization required'}), 403
            flash('Access denied. Administrator privileges required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# --- WEB PAGE ROUTES ---

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            
            # Merge any guest cart into user cart
            session_id = session.get('session_id')
            if session_id:
                CartService.merge_guest_cart_to_user(session_id, user.id)

            flash(f'Welcome back, {user.full_name}!', 'success')
            next_page = request.args.get('next')
            if user.is_admin():
                return redirect(next_page or url_for('admin.dashboard'))
            return redirect(next_page or url_for('main.index'))

        flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not full_name or not email or not password:
            flash('Please fill in all required fields.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email address already exists.', 'warning')
            return render_template('register.html')

        user = User(
            full_name=full_name,
            email=email,
            role='customer'
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        
        # Merge guest cart
        session_id = session.get('session_id')
        if session_id:
            CartService.merge_guest_cart_to_user(session_id, user.id)

        flash('Account created successfully! Welcome to ShoeStore.', 'success')
        return redirect(url_for('main.index'))

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        new_password = request.form.get('new_password', '')
        
        if full_name:
            current_user.full_name = full_name
        
        if new_password:
            if len(new_password) < 6:
                flash('New password must be at least 6 characters.', 'danger')
                return render_template('profile.html')
            current_user.set_password(new_password)

        db.session.commit()
        flash('Profile updated successfully!', 'success')

    return render_template('profile.html')


# --- REST API ENDPOINTS ---

@auth_bp.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}
    full_name = data.get('full_name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not full_name or not email or not password:
        return jsonify({'error': 'Missing required fields: full_name, email, password'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email address is already registered'}), 409

    user = User(full_name=full_name, email=email, role='customer')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return jsonify({
        'message': 'Registration successful',
        'user': user.to_dict()
    }), 201

@auth_bp.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        session_id = session.get('session_id')
        if session_id:
            CartService.merge_guest_cart_to_user(session_id, user.id)

        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200

    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/api/auth/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/api/auth/me', methods=['GET'])
def api_me():
    if current_user.is_authenticated:
        return jsonify({'user': current_user.to_dict()}), 200
    return jsonify({'user': None}), 200
