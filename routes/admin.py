from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.models import Appointment, User, Review, Doctor, Setting, Service  
from forms.forms import UpdateAppointmentStatusForm, DoctorProfileForm, AdminProfileForm, SettingForm, ServiceForm 
from utils.email_helper import send_confirmation_email, send_completion_email
from app import db
from utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)


# ========== ADMIN DASHBOARD ==========
@admin_bp.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    # Stats for dashboard
    stats = {
        'total_appointments': Appointment.query.count(),
        'pending_appointments': Appointment.query.filter_by(status='pending').count(),
        'total_patients': User.query.filter_by(role='patient').count(),
        'pending_reviews': Review.query.filter_by(is_approved=False).count(),
        'total_services': Service.query.count(),  # ✅ Added services count
        'total_settings': Setting.query.count()   # ✅ Added settings count
    }
    
    # Recent 5 appointments
    recent_appointments = Appointment.query.order_by(
        Appointment.created_at.desc()
    ).limit(5).all()
    
    return render_template('admin/admin_dashboard.html', 
                         stats=stats, 
                         recent_appointments=recent_appointments)

# ========== MANAGE APPOINTMENTS ==========
@admin_bp.route('/admin/appointments')
@login_required
@admin_required
def manage_appointments():
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    form = UpdateAppointmentStatusForm()
    return render_template('admin/manage_appointments.html', 
                         appointments=appointments, 
                         form=form)


@admin_bp.route('/admin/appointment/<int:appointment_id>/update', methods=['POST'])
@login_required
@admin_required
def update_appointment_status(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    form = UpdateAppointmentStatusForm()
    
    if form.validate_on_submit():
        old_status = appointment.status
        new_status = form.status.data
        appointment.status = new_status
        db.session.commit()
        
        # Patient details
        patient = appointment.patient
        patient_email = patient.email
        patient_name = patient.first_name
        
        # ✅ CONFIRMED - Email bhejo
        if new_status == 'confirmed' and old_status != 'confirmed':
            email_sent = send_confirmation_email(patient_email, patient_name, appointment)
            if email_sent:
                flash(f'✅ Appointment confirmed! Email sent to {patient_email}', 'success')
            else:
                flash(f'⚠️ Appointment confirmed but email failed!', 'warning')
        
        # ✅ COMPLETED - Email bhejo
        elif new_status == 'completed' and old_status != 'completed':
            email_sent = send_completion_email(patient_email, patient_name, appointment)
            if email_sent:
                flash(f'✅ Appointment completed! Thank you email sent', 'success')
            else:
                flash(f'⚠️ Appointment completed but email failed!', 'warning')
        
        # ✅ CANCELLED
        elif new_status == 'cancelled':
            flash(f'❌ Appointment cancelled', 'warning')
        
        else:
            flash(f'Appointment status updated to {new_status}', 'info')
    
    return redirect(url_for('admin.manage_appointments'))

# ========== MANAGE REVIEWS ==========
@admin_bp.route('/admin/reviews')
@login_required
@admin_required
def manage_reviews():
    pending = Review.query.filter_by(is_approved=False).order_by(Review.created_at.desc()).all()
    approved = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).all()
    return render_template('admin/manage_reviews.html', 
                         pending_reviews=pending, 
                         approved_reviews=approved)

@admin_bp.route('/admin/review/<int:review_id>/approve')
@login_required
@admin_required
def approve_review(review_id):
    review = Review.query.get_or_404(review_id)
    review.is_approved = True
    db.session.commit()
    flash('Review approved successfully!', 'success')
    return redirect(url_for('admin.manage_reviews'))

@admin_bp.route('/admin/review/<int:review_id>/disapprove')
@login_required
@admin_required
def disapprove_review(review_id):
    """Approved review ko wapis pending mein kar do"""
    review = Review.query.get_or_404(review_id)
    review.is_approved = False
    db.session.commit()
    flash('Review moved back to pending!', 'warning')
    return redirect(url_for('admin.manage_reviews'))

@admin_bp.route('/admin/review/<int:review_id>/delete')
@login_required
@admin_required
def delete_review(review_id):
    """Review ko permanently delete kar do"""
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted successfully!', 'success')
    return redirect(url_for('admin.manage_reviews'))

# ========== EDIT DOCTOR PROFILE ==========
@admin_bp.route('/admin/doctor/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_doctor():
    doctor = Doctor.get_doctor()
    form = DoctorProfileForm()
    
    if form.validate_on_submit():
        doctor.name = form.name.data
        doctor.title = form.title.data
        doctor.qualifications = form.qualifications.data
        doctor.experience = form.experience.data
        doctor.biography = form.biography.data
        doctor.specializations = form.specializations.data
        doctor.email = form.email.data
        doctor.phone = form.phone.data
        
        db.session.commit()
        flash('Doctor profile updated successfully!', 'success')
        return redirect(url_for('admin.edit_doctor'))
    
    if request.method == 'GET':
        form.name.data = doctor.name
        form.title.data = doctor.title
        form.qualifications.data = doctor.qualifications
        form.experience.data = doctor.experience
        form.biography.data = doctor.biography
        form.specializations.data = doctor.specializations
        form.email.data = doctor.email
        form.phone.data = doctor.phone
    
    return render_template('admin/edit_doctor.html', form=form, doctor=doctor)

# ========== ADMIN PROFILE ==========
@admin_bp.route('/admin/profile', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_profile():
    """Admin apni profile update karne ka page"""
    form = AdminProfileForm()
    
    if form.validate_on_submit():
        # Current password verify karo agar change kar raha hai
        if form.current_password.data:
            if not current_user.verify_password(form.current_password.data):
                flash('Current password is incorrect!', 'danger')
                return redirect(url_for('admin.admin_profile'))
            
            # New password set karo
            if form.new_password.data:
                current_user.password = form.new_password.data
        
        # Update basic info
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin.admin_profile'))
    
    # GET request - form mein existing data bharo
    if request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    
    return render_template('admin/profile.html', form=form, title='Admin Profile')

# ========== NEW: WEBSITE SETTINGS MANAGEMENT ==========
@admin_bp.route('/admin/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def settings():
    """Website settings manage karne ka page"""
    # Get all settings as a dictionary
    settings_dict = Setting.get_all_dict()
    
    if request.method == 'POST':
        # Update each setting from form data
        for key in settings_dict.keys():
            if key in request.form:
                Setting.set(key, request.form[key])
        
        # Also check for any new settings that might be in form but not in dict
        for key in request.form:
            if key != 'csrf_token' and key not in settings_dict:
                Setting.set(key, request.form[key])
                
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('admin.settings'))
    
    return render_template('admin/settings.html', settings=settings_dict)

# ========== NEW: SERVICES MANAGEMENT ==========
@admin_bp.route('/admin/services')
@login_required
@admin_required
def manage_services():
    """All services ki list"""
    services = Service.query.order_by(Service.order).all()
    return render_template('admin/services.html', services=services)

@admin_bp.route('/admin/services/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_service():
    """Naya service add karo"""
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            title=form.title.data,
            description=form.description.data,
            icon=form.icon.data,
            order=form.order.data,
            is_active=form.is_active.data
        )
        db.session.add(service)
        db.session.commit()
        flash('Service added successfully!', 'success')
        return redirect(url_for('admin.manage_services'))
    
    return render_template('admin/add_service.html', form=form)

@admin_bp.route('/admin/services/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_service(id):
    """Service edit karo"""
    service = Service.query.get_or_404(id)
    form = ServiceForm(obj=service)
    
    if form.validate_on_submit():
        service.title = form.title.data
        service.description = form.description.data
        service.icon = form.icon.data
        service.order = form.order.data
        service.is_active = form.is_active.data
        db.session.commit()
        flash('Service updated successfully!', 'success')
        return redirect(url_for('admin.manage_services'))
    
    return render_template('admin/edit_service.html', form=form, service=service)

@admin_bp.route('/admin/services/delete/<int:id>')
@login_required
@admin_required
def delete_service(id):
    """Service delete karo"""
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted successfully!', 'success')
    return redirect(url_for('admin.manage_services'))

