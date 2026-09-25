from flask import Blueprint, render_template , request, redirect, session, url_for,flash
from models.user_model import insert_user, check_user
from datetime import datetime
from werkzeug.security import generate_password_hash , check_password_hash
from models.appointment_model import insert_appointment, get_user_appointments
from models.department_model import get_all_departments
from models.bill_model import get_bill_by_id



user_bp = Blueprint('user', __name__, template_folder='../templates/user')

#------registration------

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method== 'POST':
        username=request.form['username']
        password= request.form['password']
        confirm_password=request.form['confirm_password']
        mobile=request.form['mobile']
        gender=request.form.get('gender')
        email=request.form['email']
        dob=request.form['dob']
        address=request.form['address']
        role=request.form['role']

        if password != confirm_password:
            flash("password and confirm password do not match")
            return redirect(url_for('user.register'))
        result = insert_user(username, password,mobile,gender, email,dob,address,role)
        if result =="exists":
            flash("username already existing")
            return redirect(url_for('user.register'))
        flash("registration successfull please login")
        return redirect(url_for('user.login'))
    return render_template('user_registration.html')
#----login----
@user_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = check_user(username, password)
        if user:
            session['username'] = user[1]
            session['email']=user[5]
            session['role'] = user[8]
            return redirect(url_for('user.dashboard'))
        else:
            flash("Invalid credential")

    return render_template('user_login.html')

#---dashboard----


@user_bp.route('/dashboard')
def dashboard():
    if 'username' in session:   # remove space ⚠️
        return render_template('user_dashboard.html',
        username=session['username'],
        role=session['role'])
    else:
        return redirect(url_for('user.login'))
    
#---book-appoinment--
@user_bp.route('/book_appointment', methods=["GET","POST"])
def book_appointment():
     if request.method=="POST":
         
         
        
         data=(
             request.form["patient_name"],
             request.form["mobile"],
              request.form["email"],
             request.form["gender"],
             request.form["dob"],
             request.form["department"],
             request.form["doctor"],
             request.form["appointment_date"],
             request.form["time_slot"],
             request.form["problem"],
             request.form["visit_type"],
             request.form["patient_id"],
             request.form["payment_option"],
             None)
         insert_appointment(data)

         return redirect(url_for("user.my_appoinment"))
        


     return render_template('book_appointment.html')



@user_bp.route('/my_appoinment')
def my_appoinment():
     
     email= session.get("email")
     appointments= get_user_appointments(email)
     print(appointments)
     return render_template('my_appoinment.html',appointments=appointments)
 

@user_bp.route('/department')
def department():
     departments= get_all_departments()
     
     return render_template('department.html',departments=departments)

@user_bp.route('/hospital_profile')
def hospital_profile():
     return render_template('hospital_profile.html')

@user_bp.route('/patient')
def patient():
     return render_template('patient.html')

@user_bp.route('/doctor')
def doctor():
     from models.doctor_model import get_all_doctor
     doctors = get_all_doctor()
     return render_template('doctor.html', doctors=doctors)

@user_bp.route('/bill/<int:bill_id>')
def bill(bill_id):
     bill,items= get_bill_by_id(bill_id)
     return render_template('bill.html',bill=bill,items=items)

@user_bp.route('/forgate_password')
def forgate_password():
     return render_template('forgate_password.html')

 
 
 
 
 
    
#---logout---
         
            
@user_bp.route('/logout')
def logout():
    session.clear()
    flash("logout successfull")
    return redirect(url_for('user.login'))
          