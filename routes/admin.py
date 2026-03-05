from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.models import Appointment, User, Review, Doctor
from forms.forms import UpdateAppointmentStatusForm, DoctorProfileForm, AdminProfileForm
from utils.email_helper import send_appointment_confirmation_email
# from utils.email_helper import send_appointment_confirmation_email, send_appointment_cancellation_email
from app import db
from utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

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

# @admin_bp.route('/admin/appointment/<int:appointment_id>/update', methods=['POST'])
# @login_required
# @admin_required
# def update_appointment_status(appointment_id):
#     appointment = Appointment.query.get_or_404(appointment_id)
#     form = UpdateAppointmentStatusForm()
    
#     if form.validate_on_submit():
#         appointment.status = form.status.data
#         db.session.commit()
#         flash(f'Appointment status updated to {form.status.data}.', 'success')
    
#     return redirect(url_for('admin.manage_appointments'))
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
        
        print(f"🔍 DEBUG: Appointment {appointment_id} status changed to {new_status}")
        
        # ✅ Email send karo jab status confirm ho
        if new_status == 'confirmed' and old_status != 'confirmed':
            # Patient ki details lo
            # patient = appointment.patient
            # patient_email = patient.email  #✅ Ye patient ka email hai!
            # patient_name = f"{patient.first_name} {patient.last_name}"
            send_appointment_confirmation_email(
                patient_email=appointment.patient.email,
                patient_name=appointment.patient.first_name,
                appointment=appointment
            )
            print(f"🔍 DEBUG: Confirmation email will be sent to PATIENT: {patient_email}")
            
            # Patient ko email bhejo
            result = send_appointment_confirmation_email(
                patient_email=patient_email, # ✅ Patient ka email
                patient_name=patient_name,
                appointment=appointment
            )
            
            if result:
                flash(f'Appointment confirmed! Email sent to patient: {patient_email}', 'success')
            else:
                flash(f'Appointment confirmed but EMAIL FAILED to send to {patient_email}!', 'danger')
        
        # ✅ Email send karo jab status cancel ho
        elif new_status == 'cancelled' and old_status != 'cancelled':
            patient = appointment.patient
            patient_email = patient.email # ✅ Patient ka email!
            patient_name = f"{patient.first_name} {patient.last_name}"
            
            print(f"🔍 DEBUG: Cancellation email will be sent to PATIENT: {patient_email}")
            
            result = send_appointment_cancellation_email(
                patient_email=patient_email, # ✅ Patient ka email
                patient_name=patient_name,
                appointment=appointment
            )
            
            if result:
                flash(f'Appointment cancelled. Email sent to patient: {patient_email}', 'warning')
            else:
                flash(f'Appointment cancelled but EMAIL FAILED to send to {patient_email}!', 'danger')
        
        else:
            flash(f'Appointment status updated to {new_status}.', 'success')
    
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

# ========== ADMIN DASHBOARD (Optional) ==========
@admin_bp.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    # Stats for dashboard
    stats = {
        'total_appointments': Appointment.query.count(),
        'pending_appointments': Appointment.query.filter_by(status='pending').count(),
        'total_patients': User.query.filter_by(role='patient').count(),
        'pending_reviews': Review.query.filter_by(is_approved=False).count()
    }
    
    # Recent 5 appointments
    recent_appointments = Appointment.query.order_by(
        Appointment.created_at.desc()
    ).limit(5).all()
    
    return render_template('admin/admin_dashboard.html', 
                         stats=stats, 
                         recent_appointments=recent_appointments)
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