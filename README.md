# Hospital Management System

A comprehensive web-based Hospital Management System built with Flask and SQLAlchemy, designed to streamline hospital operations including patient appointments, doctor schedules, and medical records management.

## Features

- **User Management**: Different roles (Admin, Doctor, Patient) with role-based access
- **Patient Management**: Registration, profile management, and medical history
- **Doctor Management**: Specialization tracking and scheduling
- **Appointment System**: Book, view, and manage appointments
- **Medical Records**: Track diagnoses, prescriptions, and treatment notes

## Screenshots

![Dashboard](/screenshots/dashboard.png)
![Appointments](/screenshots/appointments.png)

## Technologies Used

- **Backend**: Flask, SQLAlchemy, SQLite
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Authentication**: Werkzeug security for password hashing

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/80Chanchal/Hospital-Management-System.git
   cd Hospital-Management-System
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```
   python init_db.py
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Access the application at: `http://localhost:5000`

## Default Credentials

### Admin Account
- **Username**: admin
- **Password**: admin123

### Doctor Accounts
- **Username**: doc_john
- **Password**: doctor123

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Created By

- Chanchal Deore - [GitHub Profile](https://github.com/80Chanchal) 