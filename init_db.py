from app import app, db
from models import User, Patient, Doctor, Appointment, MedicalRecord
from werkzeug.security import generate_password_hash
from datetime import datetime

with app.app_context():
    # Create all tables
    db.create_all()
    
    # Check if admin user already exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@hospital.com',
            password=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully!")
    else:
        print("Admin user already exists.")
    
    # Add default doctors if they don't exist
    if not Doctor.query.first():
        # Create some doctor users first
        doctors_data = [
            {
                'username': 'doc_john',
                'email': 'john@hospital.com',
                'password': generate_password_hash('doctor123'),
                'first_name': 'John',
                'last_name': 'Smith',
                'specialization': 'Cardiology',
                'phone': '555-123-4567'
            },
            {
                'username': 'doc_sarah',
                'email': 'sarah@hospital.com',
                'password': generate_password_hash('doctor123'),
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'specialization': 'Neurology',
                'phone': '555-321-7654'
            },
            {
                'username': 'doc_mike',
                'email': 'mike@hospital.com',
                'password': generate_password_hash('doctor123'),
                'first_name': 'Michael',
                'last_name': 'Williams',
                'specialization': 'Pediatrics',
                'phone': '555-789-0123'
            },
            {
                'username': 'doc_emily',
                'email': 'emily@hospital.com',
                'password': generate_password_hash('doctor123'),
                'first_name': 'Emily',
                'last_name': 'Davis',
                'specialization': 'Dermatology',
                'phone': '555-456-7890'
            },
            {
                'username': 'doc_david',
                'email': 'david@hospital.com',
                'password': generate_password_hash('doctor123'),
                'first_name': 'David',
                'last_name': 'Wilson',
                'specialization': 'Orthopedics',
                'phone': '555-234-5678'
            },
            {
                'username': 'doc_lisa',
                'email': 'lisa@hospital.com',
                'password': generate_password_hash('doctor123'),
                'first_name': 'Lisa',
                'last_name': 'Brown',
                'specialization': 'Ophthalmology',
                'phone': '555-345-6789'
            },
            {
                'username': 'doc_robert',
                'email': 'robert@hospital.com',
                'password': generate_password_hash('doctor123'),
                'first_name': 'Robert',
                'last_name': 'Miller',
                'specialization': 'ENT',
                'phone': '555-567-8901'
            }
        ]
        
        for doc_data in doctors_data:
            # Create user account
            doctor_user = User(
                username=doc_data['username'],
                email=doc_data['email'],
                password=doc_data['password'],
                role='doctor'
            )
            db.session.add(doctor_user)
            db.session.commit()
            
            # Create doctor profile
            doctor = Doctor(
                user_id=doctor_user.id,
                first_name=doc_data['first_name'],
                last_name=doc_data['last_name'],
                specialization=doc_data['specialization'],
                phone=doc_data['phone']
            )
            db.session.add(doctor)
            db.session.commit()
        
        print("Default doctors added successfully!")
    
    print("Database initialized successfully!")