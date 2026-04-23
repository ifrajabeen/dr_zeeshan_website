from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from models.models import FAQCategory, FAQQuestion, FAQAnswer
from forms.forms import FAQQuestionForm, FAQAnswerForm
from utils.decorators import admin_required

faq_bp = Blueprint('faq', __name__)


# ========== PUBLIC ROUTES ==========
@faq_bp.route('/faqs')
def faqs():
    """FAQs page - all categories and questions"""
    categories = FAQCategory.query.filter_by(is_active=True).order_by(FAQCategory.order).all()
    
    # Get all answered and approved questions
    questions = FAQQuestion.query.filter_by(is_answered=True, is_approved=True).order_by(
        FAQQuestion.created_at.desc()
    ).all()
    
    return render_template('faqs.html', 
                         categories=categories, 
                         questions=questions,
                         title='FAQs - Dr. Zeeshan Clinic')


@faq_bp.route('/faq/<int:question_id>')
def faq_detail(question_id):
    """Single FAQ detail"""
    question = FAQQuestion.query.get_or_404(question_id)
    question.views += 1
    db.session.commit()
    
    return render_template('faq_detail.html', question=question, title='FAQ Detail')


# ========== PATIENT ROUTES ==========
@faq_bp.route('/faq/ask', methods=['GET', 'POST'])
@login_required
def ask_question():
    """Patient can ask a new question"""
    form = FAQQuestionForm()
    
    if form.validate_on_submit():
        question = FAQQuestion(
            question=form.question.data,
            category_id=form.category.data,
            asked_by_patient_id=current_user.id,
            is_answered=False,
            is_approved=False
        )
        db.session.add(question)
        db.session.commit()
        
        flash('Your question has been submitted. We will answer it soon!', 'success')
        return redirect(url_for('faq.faqs'))
    
    return render_template('ask_question.html', form=form, title='Ask a Question')


# ========== ADMIN ROUTES ==========
@faq_bp.route('/admin/faq/pending')
@login_required
@admin_required
def pending_questions():
    """Admin sees all pending questions"""
    questions = FAQQuestion.query.filter_by(is_answered=False).order_by(
        FAQQuestion.created_at.desc()
    ).all()
    
    return render_template('admin/pending_faqs.html', questions=questions)


@faq_bp.route('/admin/faq/answer/<int:question_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def answer_question(question_id):
    """Admin answers a question"""
    question = FAQQuestion.query.get_or_404(question_id)
    form = FAQAnswerForm()
    
    if form.validate_on_submit():
        answer = FAQAnswer(
            question_id=question.id,
            answer=form.answer.data,
            answered_by_admin_id=current_user.id
        )
        db.session.add(answer)
        
        question.is_answered = True
        question.is_approved = True
        question.answer = form.answer.data
        db.session.commit()
        
        flash('Question answered successfully!', 'success')
        return redirect(url_for('faq.pending_questions'))
    
    return render_template('admin/answer_faq.html', form=form, question=question)


@faq_bp.route('/admin/faq/approve/<int:question_id>')
@login_required
@admin_required
def approve_question(question_id):
    """Approve a question to show publicly"""
    question = FAQQuestion.query.get_or_404(question_id)
    question.is_approved = True
    db.session.commit()
    flash('Question approved and now visible to public!', 'success')
    return redirect(url_for('faq.pending_questions'))


@faq_bp.route('/admin/faq/delete/<int:question_id>')
@login_required
@admin_required
def delete_question(question_id):
    """Delete a question"""
    question = FAQQuestion.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully!', 'success')
    return redirect(url_for('faq.pending_questions'))


@faq_bp.route('/admin/faq/categories')
@login_required
@admin_required
def manage_categories():
    """Manage FAQ categories"""
    categories = FAQCategory.query.order_by(FAQCategory.order).all()
    return render_template('admin/faq_categories.html', categories=categories)


# ========== API ROUTES ==========
@faq_bp.route('/api/faq/ask', methods=['POST'])
def api_ask_question():
    """Real-time answer API - Chatbot style with professional responses"""
    data = request.get_json()
    question = data.get('question', '').lower().strip()
    
    if not question:
        return jsonify({'answer': 'Please type a question to get an answer.'})
    
    # Predefined professional answers
    answers = {
        'therapy': "🧠 Dr. Zeeshan offers:<br><br>• Individual Therapy<br>• Couples Counseling<br>• Anxiety Treatment<br>• Depression Therapy<br>• Stress Management<br><br>Call us to discuss which is right for you!",
        'cost': "💰 Fee Structure:<br><br>• Initial Session: $150 (60-75 min)<br>• Follow-up: $120 (50 min)<br>• Couples: $180 (60 min)<br><br>We accept most insurance plans.",
        'insurance': "✅ We accept major insurance plans including:<br>• Blue Cross Blue Shield<br>• Aetna • Cigna<br>• United Healthcare<br><br>📞 Call to verify your coverage.",
        'appointment': "📅 Book an appointment:<br><br>1. Click 'Book Appointment' button<br>2. Select date & time<br>3. Fill the form<br>4. Submit<br><br>You'll get confirmation email!",
        'cancel': "⚠️ Cancellation Policy:<br><br>• 24+ hours notice: No fee<br>• Less than 24 hours: $50 fee<br>• No-show: Full $150 fee",
        'first': "🌟 First Session (60-75 min):<br><br>• Discuss your concerns<br>• Set therapy goals<br>• Ask questions<br>• Create treatment plan<br><br>Complete intake forms before visit.",
        'online': "💻 Online Therapy Available!<br><br>• Secure video sessions<br>• HIPAA compliant<br>• Same rates as in-person<br>• Flexible scheduling",
        'confidential': "🔒 Confidentiality Guaranteed!<br><br>• All sessions strictly private<br>• HIPAA compliant<br>• Information never shared without consent"
    }
    
    # Match question to answer
    for keyword, answer in answers.items():
        if keyword in question:
            return jsonify({'answer': answer})
    
    # Search database
    all_faqs = FAQQuestion.query.filter_by(is_answered=True, is_approved=True).all()
    best_match = None
    best_score = 0
    
    for faq in all_faqs:
        question_keywords = set(question.split())
        faq_keywords = set(faq.question.lower().split())
        match_score = len(question_keywords.intersection(faq_keywords))
        
        if match_score > best_score:
            best_score = match_score
            best_match = faq
    
    if best_match and best_score > 0:
        return jsonify({'answer': f"📌 {best_match.answer}"})
    
    # Default response
    return jsonify({'answer': "🤔 I want to help! Could you rephrase your question?<br><br>📞 Call us: +1 (555) 123-4567<br>📧 Email: contact@drzeeshanclinic.com"})