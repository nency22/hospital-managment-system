# Hospital Management System

A web-based Hospital Management System developed using Python and Flask.
The system provides role-based access for managing hospital operations such as
users, doctors, departments, appointments, billing, and dashboards.

## Features

- User Registration and Login
- Role-Based Authentication
- Admin Dashboard
- User Dashboard
- Doctor Management
- Department Management
- Appointment Management
- Billing Management
- Hospital Profile Management
- Password Management
- Dynamic Web Pages
- Database Integration

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- HTML5
- CSS3
- JavaScript
- SQLite
- Jinja2
- Git
- GitHub

## Project Structure

```text
hospital_management_system/
│
├── admin/
├── admin_panel/
├── database/
├── models/
├── routes/
├── static/
├── templates/
├── user/
├── utils/
│
├── app.py
├── extension.py
├── update_db.py
├── requirements.txt
├── README.md
└── .gitignore

Installation
1. Clone the Repository
git clone https://github.com/nency22/hospital-managment-system.git
2. Navigate to the Project
cd hospital-managment-system
3. Create a Virtual Environment
python -m venv venv
4. Activate Virtual Environment

Windows PowerShell:

.\venv\Scripts\Activate.ps1
5. Install Dependencies
pip install -r requirements.txt
6. Run the Application
python app.py

The application will run locally on:

http://127.0.0.1:5000/
Authentication and Roles

The system uses authentication and role-based access control.

Admin
Manage doctors
Manage departments
Manage users
Manage appointments
Manage billing
Access admin dashboard
User
Register/Login
View profile
View doctors and departments
Book appointments
View appointments
View billing information
Access user dashboard
Database

The application uses SQLite for local development and database management.

Database-related models are organized inside the models/ directory.

Future Improvements
Online Payment Integration
Email Notifications
REST API
PostgreSQL Database
Cloud Deployment
Advanced Analytics
Automated Testing
Author

Nency

Python Backend Developer

GitHub:
https://github.com/nency22


 
