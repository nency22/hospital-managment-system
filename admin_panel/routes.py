from flask import Blueprint, request, redirect, session, url_for, render_template, current_app
from models.admin_model import admin_login, insert_admin
from models.doctor_model import add_doctor, get_all_doctor, delete_doctor, get_doctor_by_id, update_doctor
import os
from werkzeug.utils import secure_filename
from models.db_config import get_connection
from models.appointment_model import get_all_appoinmtent , update_status
from models.department_model import add_department,get_all_departments,delete_department,get_department_by_id,update_department
from models.bill_model import insert_bill,get_all_bills,get_bill_by_id
import json

admin_bp = Blueprint("admin_bp", __name__)


# ------------------ ADMIN LOGIN ------------------
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        print("Entered username:", username)
        print("Entered password:", password)

        admin = admin_login(username, password)
        print("DB Result:", admin)

        if admin:
            session["admin"] = admin[0]
            return redirect(url_for("admin_bp.admin_dashboard"))   # FIXED
        else:
            return "Invalid credential"

    return render_template("admin/admin_login.html")


# ------------------ ADMIN DASHBOARD ------------------
@admin_bp.route("/admin_dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for("admin_bp.login"))

    return render_template("admin/admin_dashboard.html")


# ------------------ ADD DOCTOR ------------------
@admin_bp.route("/add_doctor", methods=["GET", "POST"])
def add_doctor_route():

    if "admin" not in session:
        return redirect(url_for("admin_bp.login"))

    if request.method == "POST":

        image = request.files["doctor_image"]

        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            image.save(image_path)
        else:
            filename = None

        doctor_data = (
            request.form["name"],
            request.form["qualification"],
            request.form["department"],
            request.form["mobile"],
            request.form["email"],
            request.form["experience"],
            request.form["consultant_fee"],
            request.form.get("registration_number"),
            request.form["gender"],
            request.form["available_days"],
            request.form.get("morning_time"),
            request.form.get("evening_time"),
            request.form["about_doctor"],
            filename,
            request.form["status"]
        )

        add_doctor(doctor_data)

        return redirect(url_for("admin_bp.doctor_list"))

    return render_template("admin/add_doctor.html")


# ------------------ EDIT DOCTOR LIST ------------------


@admin_bp.route("/edit_doctor/<int:id>", methods=["GET","POST"])
def edit_doctor(id):

    conn = get_connection()

    if request.method == "POST":

        name = request.form["name"]
        qualification = request.form["qualification"]
        department = request.form["department"]
        mobile = request.form["mobile"]
        email = request.form["email"]
        experience = request.form["experience"]
        fee = request.form["consultant_fee"]
        registration = request.form["registration_number"]
        gender = request.form["gender"]
        request.form.get("morning_time"),
        request.form.get("evening_time"),
            
        about = request.form["about_doctor"]
        status = request.form["status"]

        photo = request.files["doctor_image"]

        if photo and photo.filename != "":
            filename = secure_filename(photo.filename)
            photo.save(os.path.join("static/images", filename))

            conn.execute("""
            UPDATE doctors
            SET name=?, qualification=?, department=?, mobile=?, email=?, experience=?, consultant_fee=?, registration_number=?, gender=?, morning_time=?,evening_time=?, about_doctor=?, status=?, doctor_image=?
            WHERE id=?
            """,(name,qualification,department,mobile,email,experience,fee,registration,gender, about,status,filename,id))

        else:
            conn.execute("""
            UPDATE doctors
            SET name=?, qualification=?, department=?, mobile=?, email=?, experience=?, consultant_fee=?, registration_number=?, gender=?, about_doctor=?, status=?
            WHERE id=?
            """,(name,qualification,department,mobile,email,experience,fee,registration,gender,about,status,id))

        conn.commit()

        return redirect(url_for("admin_bp.doctor_list"))

    doctor = conn.execute("SELECT * FROM doctors WHERE id=?", (id,)).fetchone()

    return render_template("admin/edit_doctor.html", doctor=doctor)
#--------------delete------------

@admin_bp.route("/delete_doctor/<int:id>")
def delete_doctor(id):
    conn=get_connection()
    conn.execute("DELETE FROM doctors WHERE id=?",(id,))
    conn.commit()
    return redirect(url_for("admin_bp.doctor_list"))


# ------------------ DOCTOR LIST ------------------
@admin_bp.route("/doctor_list")
def doctor_list():


    doctors = get_all_doctor()

    return render_template("admin/doctor_list.html", doctors=doctors)


# ------------------ BILL LIST ------------------
@admin_bp.route("/bill_list")
def bill_list():
    bills=get_all_bills()

    return render_template("admin/bill_list.html",bills=bills)
#-------save bill---------------------------------
@admin_bp.route("/save_bill",methods=["POST"])
def save_bill():
    patient= request.form["patient_name"]
    doctor=request.form["doctor_name"]
    date= request.form["date"]
    items=json.loads(request.form["items"])
    insert_bill(patient,doctor, date,items)
    return redirect(url_for("admin_bp.bill_list"))
#------view bill --------
@admin_bp.route("/view_bill/<int:bill_id>")
def view_bill(bill_id):
    bill, items=get_bill_by_id(bill_id)
    return render_template("admin/view_bill.html",bill=bill, items=items)

#-----generate bill----------------------
@admin_bp.route("/generate_bill")    
def generate_bill():
    return render_template("admin/generate_bill.html")
#-----------------manage appoinment--------------
@admin_bp.route("/manage_book")
def manage_book():

    appointments= get_all_appoinmtent()
    
    return render_template("admin/manage_book.html",appointments=appointments)


#-----------approve----------
@admin_bp.route("/approve/<int:id>")
def approve(id):
    update_status(id,"approved")

    return redirect(url_for("admin_bp.manage_book"))
#------------reject---------------------
@admin_bp.route("/reject/<int:id>")
def reject(id):
    update_status(id,"rejected")

    return redirect(url_for("admin_bp.manage_book"))
#---------complete---------------
@admin_bp.route("/complete/<int:id>")
def complete(id):
    update_status(id,"completed")

    return redirect(url_for("admin_bp.manage_book"))


# ------------------ APPOINTMENT DETAIL ------------------
@admin_bp.route("/appointment_details")
def appointment_details():
    return render_template("admin/appointment_details.html")


# ------------------ DEPARTMENT LIST ------------------
@admin_bp.route("/department_list")
def department_list():
    departments= get_all_departments()
    print("department",departments)

    return render_template("admin/department_list.html",departments=departments)

#-----------------add department---------------------
@admin_bp.route("/add_department",methods=["GET","POST"])
def add_department_route():
    if request.method=="POST":
        name= request.form["name"]
        doctor=request.form["doctor"]
        description=request.form["description"]
        status=request.form["status"]
        image= request.files["image"]
        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(os.path.join("static/images",filename))
        else:
             filename=None

        data=(name,doctor,description, status, filename)
        add_department(data)

        return redirect(url_for("admin_bp.department_list"))
        
    return render_template("admin/add_department.html")
    

    #--------delete-----------------
@admin_bp.route("/delete_department/<int:id>")
def delete_department_route(id):
    delete_department(id)
    return redirect(url_for("admin_bp.department_list"))

#------------edit-------------------
@admin_bp.route("/edit_department/<int:id>", methods=["GET","POST"])
def edit_department(id):

    dept = get_department_by_id(id)

    if request.method == "POST":

        name = request.form.get("name")
        doctor = request.form.get("doctor")
        description = request.form.get("description")
        status = request.form.get("status")
        image = request.files.get("image")

        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(os.path.join("static/images", filename))
        else:
            filename = dept["image"]

        data = (name, doctor, description, status, filename, id)
        update_department(data)

        return redirect(url_for("admin_bp.department_list"))

    return render_template("admin/edit_depart.html", dept=dept)


# ------------------ PATIENT LIST ------------------
@admin_bp.route("/patient_list")
def patient_list():
    return render_template("admin/patient_list.html")