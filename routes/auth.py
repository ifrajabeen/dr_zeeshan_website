from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from models.models import User
from forms.forms import RegistrationForm, LoginForm, AdminRegistrationForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user exists
        user_exists = User.query.filter(
            (User.email == form.email.data) | (User.username == form.username.data)
        ).first()
        
        if user_exists:
            flash('Email or username already exists.', 'danger')
            return redirect(url_for('auth.signup'))
        
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            role='patient'
        )
        user.password = form.password.data
        
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html', form=form, title='Sign Up')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html', form=form, title='Login')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
@auth_bp.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = AdminRegistrationForm()
    
    if form.validate_on_submit():
        # Verify admin secret code (security ke liye)
        SECRET_ADMIN_CODE = 'ADMIN2026'  # Ye aap change kar sakte hain
        if form.admin_code.data != SECRET_ADMIN_CODE:
            flash('Invalid admin secret code!', 'danger')
            return render_template('admin_signup.html', form=form)
        
        # Check if user exists
        user_exists = User.query.filter(
            (User.email == form.email.data) | (User.username == form.username.data)
        ).first()
        
        if user_exists:
            flash('Email or username already exists.', 'danger')
            return redirect(url_for('auth.admin_signup'))
        
        # Create admin user
        admin = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            role='admin'  # ✅ Role admin set karo
        )
        admin.password = form.password.data
        
        db.session.add(admin)
        db.session.commit()
        
        flash('Admin account created successfully! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('admin_signup.html', form=form, title='Admin Sign Up')