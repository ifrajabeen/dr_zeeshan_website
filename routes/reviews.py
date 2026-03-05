from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.models import Review, User, Doctor
from forms.forms import ReviewForm

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/reviews', methods=['GET', 'POST'])
def reviews():
    form = ReviewForm()
    # doctor = Doctor.get_or_create()
    doctor = Doctor.get_doctor()
    approved_reviews = Review.query.filter_by(is_approved=True).order_by(
        Review.created_at.desc()
    ).all()
    
    # Calculate average rating
    avg_rating = 0
    if approved_reviews:
        avg_rating = sum([r.rating for r in approved_reviews]) / len(approved_reviews)
    
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Please login to submit a review.', 'warning')
            return redirect(url_for('auth.login'))
        
        review = Review(
            patient_id=current_user.id,
            rating=form.rating.data,
            comment=form.comment.data,
            is_approved=False
        )
        db.session.add(review)
        db.session.commit()
        
        flash('Thank you for your review! It will be displayed after approval.', 'success')
        return redirect(url_for('reviews.reviews'))
    
    return render_template('reviews.html', form=form, reviews=approved_reviews, 
                         avg_rating=avg_rating, doctor=doctor, title='Patient Reviews')