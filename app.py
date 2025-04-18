from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
from models import db, User, Patient, Doctor, Appointment, MedicalRecord
db.init_app(app)

# Routes will be added here

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Check if username or email already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'danger')
            return render_template('register.html')
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already exists', 'danger')
            return render_template('register.html')
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    
    # Fetch user-specific data based on role
    if session['role'] == 'patient':
        patient = Patient.query.filter_by(user_id=session['user_id']).first()
        appointments = []
        if patient:
            # Get upcoming appointments for patient
            appointments = Appointment.query.filter_by(patient_id=patient.id).all()
        return render_template('dashboard.html', patient=patient, appointments=appointments)
    elif session['role'] == 'doctor':
        doctor = Doctor.query.filter_by(user_id=session['user_id']).first()
        appointments = []
        if doctor:
            # Get upcoming appointments for doctor
            appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
        return render_template('dashboard.html', doctor=doctor, appointments=appointments)
    
    return render_template('dashboard.html')

@app.route('/patient/appointments')
def patient_appointments():
    if 'user_id' not in session or session['role'] != 'patient':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    patient = Patient.query.filter_by(user_id=session['user_id']).first()
    if not patient:
        flash('Patient profile not found. Please complete your profile first.', 'warning')
        return redirect(url_for('dashboard'))
        
    appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    today = datetime.now().date()
    
    return render_template('patient_appointments.html', appointments=appointments, today=today)

@app.route('/view_appointment/<int:appointment_id>')
def view_appointment(appointment_id):
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Check if the user has permission to view this appointment
    if session['role'] == 'patient':
        patient = Patient.query.filter_by(user_id=session['user_id']).first()
        if appointment.patient_id != patient.id:
            flash('Unauthorized access', 'danger')
            return redirect(url_for('patient_appointments'))
    elif session['role'] == 'doctor':
        doctor = Doctor.query.filter_by(user_id=session['user_id']).first()
        if appointment.doctor_id != doctor.id:
            flash('Unauthorized access', 'danger')
            return redirect(url_for('doctor_appointments'))
    elif session['role'] != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get related medical record if appointment is completed
    medical_record = None
    if appointment.status == 'completed':
        medical_record = MedicalRecord.query.filter_by(
            patient_id=appointment.patient_id,
            doctor_id=appointment.doctor_id,
            date=appointment.date
        ).first()
    
    return render_template('view_appointment.html', appointment=appointment, medical_record=medical_record)

@app.route('/doctor/appointments')
def doctor_appointments():
    if 'user_id' not in session or session['role'] != 'doctor':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    doctor = Doctor.query.filter_by(user_id=session['user_id']).first()
    if not doctor:
        flash('Doctor profile not found. Please complete your profile first.', 'warning')
        return redirect(url_for('dashboard'))
        
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    today = datetime.now().date()
    
    return render_template('doctor_appointments.html', appointments=appointments, today=today)

@app.route('/book-appointment', methods=['GET', 'POST'])
def book_appointment():
    if 'user_id' not in session or session['role'] != 'patient':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    patient = Patient.query.filter_by(user_id=session['user_id']).first()
    if not patient:
        flash('Please complete your profile before booking an appointment', 'warning')
        return redirect(url_for('create_patient_profile'))
    
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        notes = request.form.get('notes')
        
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H:%M').time()
        
        new_appointment = Appointment(
            patient_id=patient.id,
            doctor_id=doctor_id,
            date=date,
            time=time,
            notes=notes,
            status='scheduled'
        )
        
        db.session.add(new_appointment)
        db.session.commit()
        
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('patient_appointments'))
    
    doctors = Doctor.query.all()
    return render_template('book_appointment.html', doctors=doctors)

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/complete_appointment/<int:appointment_id>')
def complete_appointment(appointment_id):
    if 'user_id' not in session or session['role'] != 'doctor':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    doctor = Doctor.query.filter_by(user_id=session['user_id']).first()
    
    if appointment.doctor_id != doctor.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('doctor_appointments'))
    
    appointment.status = 'completed'
    db.session.commit()
    
    flash('Appointment marked as completed', 'success')
    return redirect(url_for('doctor_appointments'))

@app.route('/create-patient-profile', methods=['GET', 'POST'])
def create_patient_profile():
    if 'user_id' not in session or session['role'] != 'patient':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    # Check if profile already exists
    existing_profile = Patient.query.filter_by(user_id=session['user_id']).first()
    if existing_profile:
        flash('You already have a patient profile', 'info')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        gender = request.form.get('gender')
        date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d').date()
        blood_group = request.form.get('blood_group')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        
        # Create patient profile
        new_patient = Patient(
            user_id=session['user_id'],
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            blood_group=blood_group,
            phone=phone,
            email=email,
            address=address
        )
        
        db.session.add(new_patient)
        db.session.commit()
        
        flash('Patient profile created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    # Get user email for pre-filling the form
    user = User.query.get(session['user_id'])
    return render_template('create_patient_profile.html', user=user)

@app.route('/cancel_appointment/<int:appointment_id>')
def cancel_appointment(appointment_id):
    if 'user_id' not in session or session['role'] != 'patient':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    patient = Patient.query.filter_by(user_id=session['user_id']).first()
    
    if appointment.patient_id != patient.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('patient_appointments'))
    
    appointment.status = 'cancelled'
    db.session.commit()
    
    flash('Appointment cancelled successfully', 'success')
    return redirect(url_for('patient_appointments'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)