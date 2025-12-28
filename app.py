import os
import json
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///exam_platform.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Configure Google Generative AI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# ==================== DATABASE MODELS ====================

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    role = db.Column(db.String(20), default='student')  # student, instructor, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    exams = db.relationship('Exam', backref='creator', lazy=True, foreign_keys='Exam.creator_id')
    attempts = db.relationship('ExamAttempt', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }


class Exam(db.Model):
    """Exam/Test model"""
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(120))
    duration_minutes = db.Column(db.Integer, default=60)
    total_questions = db.Column(db.Integer)
    passing_score = db.Column(db.Float, default=60.0)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    questions = db.relationship('Question', backref='exam', lazy=True, cascade='all, delete-orphan')
    attempts = db.relationship('ExamAttempt', backref='exam', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_questions=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'creator_id': self.creator_id,
            'subject': self.subject,
            'duration_minutes': self.duration_minutes,
            'total_questions': self.total_questions,
            'passing_score': self.passing_score,
            'is_published': self.is_published,
            'created_at': self.created_at.isoformat()
        }
        if include_questions:
            data['questions'] = [q.to_dict() for q in self.questions]
        return data


class Question(db.Model):
    """Question model"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), default='multiple_choice')  # multiple_choice, essay, true_false
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    points = db.Column(db.Float, default=1.0)
    order = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    options = db.relationship('QuestionOption', backref='question', lazy=True, cascade='all, delete-orphan')
    answers = db.relationship('Answer', backref='question', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_options=True):
        data = {
            'id': self.id,
            'exam_id': self.exam_id,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'difficulty': self.difficulty,
            'points': self.points,
            'order': self.order
        }
        if include_options:
            data['options'] = [o.to_dict() for o in self.options]
        return data


class QuestionOption(db.Model):
    """Multiple choice options for questions"""
    __tablename__ = 'question_options'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    option_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer)
    
    def to_dict(self):
        return {
            'id': self.id,
            'option_text': self.option_text,
            'order': self.order
            # Note: is_correct is hidden from students until exam is submitted
        }


class ExamAttempt(db.Model):
    """Student exam attempt/submission"""
    __tablename__ = 'exam_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    score = db.Column(db.Float)
    percentage = db.Column(db.Float)
    status = db.Column(db.String(20), default='in_progress')  # in_progress, submitted, graded
    is_passed = db.Column(db.Boolean)
    
    answers = db.relationship('Answer', backref='attempt', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'exam_id': self.exam_id,
            'user_id': self.user_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'score': self.score,
            'percentage': self.percentage,
            'status': self.status,
            'is_passed': self.is_passed
        }


class Answer(db.Model):
    """Student answers to questions"""
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('exam_attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answer_text = db.Column(db.Text)  # For essay/text answers
    selected_option_id = db.Column(db.Integer, db.ForeignKey('question_options.id'))  # For multiple choice
    is_correct = db.Column(db.Boolean)
    points_earned = db.Column(db.Float)
    ai_feedback = db.Column(db.Text)  # AI-generated feedback
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'attempt_id': self.attempt_id,
            'question_id': self.question_id,
            'answer_text': self.answer_text,
            'selected_option_id': self.selected_option_id,
            'is_correct': self.is_correct,
            'points_earned': self.points_earned,
            'ai_feedback': self.ai_feedback
        }


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 409
        
        user = User(
            username=data['username'],
            email=data['email'],
            full_name=data.get('full_name', ''),
            role=data.get('role', 'student')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Missing username or password'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== EXAM ROUTES ====================

@app.route('/api/exams', methods=['GET'])
@jwt_required()
def get_exams():
    """Get all published exams"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        exams = Exam.query.filter_by(is_published=True).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'exams': [exam.to_dict() for exam in exams.items],
            'total': exams.total,
            'pages': exams.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/exams/<int:exam_id>', methods=['GET'])
@jwt_required()
def get_exam(exam_id):
    """Get exam details with questions"""
    try:
        user_id = get_jwt_identity()
        exam = Exam.query.get(exam_id)
        
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        if not exam.is_published and exam.creator_id != user_id:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        return jsonify(exam.to_dict(include_questions=True)), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/exams', methods=['POST'])
@jwt_required()
def create_exam():
    """Create a new exam (instructor only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user.role not in ['instructor', 'admin']:
            return jsonify({'error': 'Only instructors can create exams'}), 403
        
        data = request.get_json()
        
        if not data or not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
        
        exam = Exam(
            title=data['title'],
            description=data.get('description', ''),
            creator_id=user_id,
            subject=data.get('subject', ''),
            duration_minutes=data.get('duration_minutes', 60),
            passing_score=data.get('passing_score', 60.0)
        )
        
        db.session.add(exam)
        db.session.commit()
        
        return jsonify({
            'message': 'Exam created successfully',
            'exam': exam.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/exams/<int:exam_id>', methods=['PUT'])
@jwt_required()
def update_exam(exam_id):
    """Update exam (instructor only)"""
    try:
        user_id = get_jwt_identity()
        exam = Exam.query.get(exam_id)
        
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        if exam.creator_id != user_id and User.query.get(user_id).role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        exam.title = data.get('title', exam.title)
        exam.description = data.get('description', exam.description)
        exam.subject = data.get('subject', exam.subject)
        exam.duration_minutes = data.get('duration_minutes', exam.duration_minutes)
        exam.passing_score = data.get('passing_score', exam.passing_score)
        exam.is_published = data.get('is_published', exam.is_published)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Exam updated successfully',
            'exam': exam.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== QUESTION ROUTES ====================

@app.route('/api/exams/<int:exam_id>/questions', methods=['POST'])
@jwt_required()
def add_question(exam_id):
    """Add a question to exam"""
    try:
        user_id = get_jwt_identity()
        exam = Exam.query.get(exam_id)
        
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        if exam.creator_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        if not data or not data.get('question_text'):
            return jsonify({'error': 'Question text is required'}), 400
        
        question = Question(
            exam_id=exam_id,
            question_text=data['question_text'],
            question_type=data.get('question_type', 'multiple_choice'),
            difficulty=data.get('difficulty', 'medium'),
            points=data.get('points', 1.0),
            order=data.get('order', 0)
        )
        
        db.session.add(question)
        db.session.flush()
        
        # Add options if provided
        if data.get('options'):
            for idx, option in enumerate(data['options']):
                q_option = QuestionOption(
                    question_id=question.id,
                    option_text=option['text'],
                    is_correct=option.get('is_correct', False),
                    order=idx
                )
                db.session.add(q_option)
        
        db.session.commit()
        exam.total_questions = len(exam.questions)
        db.session.commit()
        
        return jsonify({
            'message': 'Question added successfully',
            'question': question.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== EXAM ATTEMPT ROUTES ====================

@app.route('/api/exams/<int:exam_id>/start', methods=['POST'])
@jwt_required()
def start_exam(exam_id):
    """Start an exam attempt"""
    try:
        user_id = get_jwt_identity()
        exam = Exam.query.get(exam_id)
        
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        if not exam.is_published:
            return jsonify({'error': 'Exam is not published'}), 403
        
        # Check for existing in-progress attempt
        existing_attempt = ExamAttempt.query.filter_by(
            exam_id=exam_id,
            user_id=user_id,
            status='in_progress'
        ).first()
        
        if existing_attempt:
            return jsonify({
                'message': 'Resuming existing exam attempt',
                'attempt': existing_attempt.to_dict()
            }), 200
        
        attempt = ExamAttempt(
            exam_id=exam_id,
            user_id=user_id,
            status='in_progress'
        )
        
        db.session.add(attempt)
        db.session.commit()
        
        return jsonify({
            'message': 'Exam started successfully',
            'attempt': attempt.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/attempts/<int:attempt_id>/submit-answer', methods=['POST'])
@jwt_required()
def submit_answer(attempt_id):
    """Submit answer to a question"""
    try:
        user_id = get_jwt_identity()
        attempt = ExamAttempt.query.get(attempt_id)
        
        if not attempt:
            return jsonify({'error': 'Attempt not found'}), 404
        
        if attempt.user_id != user_id or attempt.status != 'in_progress':
            return jsonify({'error': 'Invalid or completed attempt'}), 403
        
        data = request.get_json()
        question_id = data.get('question_id')
        
        # Check if answer already exists
        existing_answer = Answer.query.filter_by(
            attempt_id=attempt_id,
            question_id=question_id
        ).first()
        
        if existing_answer:
            # Update existing answer
            existing_answer.answer_text = data.get('answer_text')
            existing_answer.selected_option_id = data.get('selected_option_id')
        else:
            # Create new answer
            answer = Answer(
                attempt_id=attempt_id,
                question_id=question_id,
                answer_text=data.get('answer_text'),
                selected_option_id=data.get('selected_option_id')
            )
            db.session.add(answer)
        
        db.session.commit()
        
        return jsonify({'message': 'Answer submitted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/attempts/<int:attempt_id>/submit', methods=['POST'])
@jwt_required()
def submit_exam(attempt_id):
    """Submit exam for grading"""
    try:
        user_id = get_jwt_identity()
        attempt = ExamAttempt.query.get(attempt_id)
        
        if not attempt:
            return jsonify({'error': 'Attempt not found'}), 404
        
        if attempt.user_id != user_id or attempt.status != 'in_progress':
            return jsonify({'error': 'Invalid or already submitted attempt'}), 403
        
        attempt.end_time = datetime.utcnow()
        attempt.status = 'submitted'
        
        # Calculate score
        total_points = 0
        earned_points = 0
        
        for answer in attempt.answers:
            question = answer.question
            total_points += question.points
            
            if question.question_type == 'multiple_choice':
                if answer.selected_option_id:
                    option = QuestionOption.query.get(answer.selected_option_id)
                    if option and option.is_correct:
                        answer.is_correct = True
                        answer.points_earned = question.points
                        earned_points += question.points
                    else:
                        answer.is_correct = False
                        answer.points_earned = 0
            
            elif question.question_type == 'true_false':
                # Similar logic for true/false
                if answer.answer_text:
                    option = question.options[0]
                    if answer.answer_text.lower() == str(option.is_correct).lower():
                        answer.is_correct = True
                        answer.points_earned = question.points
                        earned_points += question.points
                    else:
                        answer.is_correct = False
                        answer.points_earned = 0
        
        attempt.score = earned_points
        attempt.percentage = (earned_points / total_points * 100) if total_points > 0 else 0
        attempt.is_passed = attempt.percentage >= attempt.exam.passing_score
        attempt.status = 'graded'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Exam submitted successfully',
            'attempt': attempt.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/attempts/<int:attempt_id>', methods=['GET'])
@jwt_required()
def get_attempt(attempt_id):
    """Get exam attempt details"""
    try:
        user_id = get_jwt_identity()
        attempt = ExamAttempt.query.get(attempt_id)
        
        if not attempt:
            return jsonify({'error': 'Attempt not found'}), 404
        
        if attempt.user_id != user_id and User.query.get(user_id).role != 'instructor':
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({
            'attempt': attempt.to_dict(),
            'answers': [a.to_dict() for a in attempt.answers]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== AI INTEGRATION ROUTES ====================

@app.route('/api/ai/generate-questions', methods=['POST'])
@jwt_required()
def generate_questions():
    """Generate questions using Google AI"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user.role not in ['instructor', 'admin']:
            return jsonify({'error': 'Only instructors can generate questions'}), 403
        
        if not GOOGLE_API_KEY:
            return jsonify({'error': 'Google AI not configured'}), 500
        
        data = request.get_json()
        topic = data.get('topic')
        num_questions = data.get('num_questions', 5)
        difficulty = data.get('difficulty', 'medium')
        question_type = data.get('question_type', 'multiple_choice')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        prompt = f"""Generate {num_questions} {question_type} questions about "{topic}" with {difficulty} difficulty level.
        
        Format the response as a JSON array with this structure:
        [
            {{
                "question_text": "Question here?",
                "options": [
                    {{"text": "Option A", "is_correct": false}},
                    {{"text": "Option B", "is_correct": true}},
                    {{"text": "Option C", "is_correct": false}},
                    {{"text": "Option D", "is_correct": false}}
                ],
                "difficulty": "{difficulty}"
            }}
        ]
        
        Return ONLY the JSON array, no other text."""
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        # Parse AI response
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        questions = json.loads(response_text)
        
        return jsonify({
            'message': 'Questions generated successfully',
            'questions': questions
        }), 200
    
    except json.JSONDecodeError:
        return jsonify({'error': 'Failed to parse AI response'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ai/evaluate-answer', methods=['POST'])
@jwt_required()
def evaluate_answer():
    """Evaluate essay answers using Google AI"""
    try:
        user_id = get_jwt_identity()
        
        if not GOOGLE_API_KEY:
            return jsonify({'error': 'Google AI not configured'}), 500
        
        data = request.get_json()
        question_text = data.get('question_text')
        answer_text = data.get('answer_text')
        rubric = data.get('rubric', 'Evaluate the accuracy, completeness, and clarity of the answer.')
        
        if not question_text or not answer_text:
            return jsonify({'error': 'Question and answer text are required'}), 400
        
        prompt = f"""Evaluate the following student answer to an exam question.
        
        Question: {question_text}
        
        Student's Answer: {answer_text}
        
        Evaluation Criteria: {rubric}
        
        Provide feedback in JSON format:
        {{
            "score": 0-100,
            "feedback": "Detailed feedback",
            "strengths": ["strength1", "strength2"],
            "improvements": ["improvement1", "improvement2"]
        }}
        
        Return ONLY the JSON, no other text."""
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        evaluation = json.loads(response_text)
        
        return jsonify({
            'message': 'Answer evaluated successfully',
            'evaluation': evaluation
        }), 200
    
    except json.JSONDecodeError:
        return jsonify({'error': 'Failed to parse AI response'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ai/explain-concept', methods=['POST'])
@jwt_required()
def explain_concept():
    """Get AI explanation for a concept"""
    try:
        if not GOOGLE_API_KEY:
            return jsonify({'error': 'Google AI not configured'}), 500
        
        data = request.get_json()
        concept = data.get('concept')
        level = data.get('level', 'intermediate')  # beginner, intermediate, advanced
        
        if not concept:
            return jsonify({'error': 'Concept is required'}), 400
        
        prompt = f"""Explain the concept of '{concept}' at a {level} level.
        
        Provide a clear, concise explanation with:
        1. Definition
        2. Key points
        3. Real-world examples
        4. Related concepts
        
        Keep the explanation suitable for a student learning this for the first time."""
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        return jsonify({
            'message': 'Explanation generated successfully',
            'concept': concept,
            'explanation': response.text
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== STATISTICS AND REPORTING ====================

@app.route('/api/exams/<int:exam_id>/statistics', methods=['GET'])
@jwt_required()
def get_exam_statistics(exam_id):
    """Get exam statistics (instructor only)"""
    try:
        user_id = get_jwt_identity()
        exam = Exam.query.get(exam_id)
        
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        if exam.creator_id != user_id and User.query.get(user_id).role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        attempts = ExamAttempt.query.filter_by(exam_id=exam_id, status='graded').all()
        
        if not attempts:
            return jsonify({
                'exam_id': exam_id,
                'total_attempts': 0,
                'average_score': 0,
                'pass_rate': 0,
                'statistics': {}
            }), 200
        
        scores = [a.percentage for a in attempts]
        passed = sum(1 for a in attempts if a.is_passed)
        
        return jsonify({
            'exam_id': exam_id,
            'total_attempts': len(attempts),
            'average_score': sum(scores) / len(scores),
            'highest_score': max(scores),
            'lowest_score': min(scores),
            'pass_rate': (passed / len(attempts)) * 100,
            'statistics': {
                'total_questions': exam.total_questions,
                'duration_minutes': exam.duration_minutes,
                'passing_score': exam.passing_score
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/attempts', methods=['GET'])
@jwt_required()
def get_user_attempts():
    """Get user's exam attempts"""
    try:
        user_id = get_jwt_identity()
        
        attempts = ExamAttempt.query.filter_by(user_id=user_id).order_by(
            ExamAttempt.start_time.desc()
        ).all()
        
        return jsonify({
            'attempts': [
                {
                    **a.to_dict(),
                    'exam_title': a.exam.title
                } for a in attempts
            ]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized access'}), 401


# ==================== APPLICATION INITIALIZATION ====================

@app.before_first_request
def create_tables():
    """Create database tables"""
    db.create_all()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


if __name__ == '__main__':
    # Development server
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_ENV', 'development') == 'development'
    )
