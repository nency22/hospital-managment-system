from flask import Flask,redirect
from models.doctor_model import create_doctor_table 
from models.appointment_model import create_appointment_table
from models.department_model import create_department_table
from models.bill_model import create_bill_tables


import sqlite3
import os
from routes.user_routes import user_bp
from admin_panel.routes import admin_bp



app = Flask(__name__)

UPLOAD_FOLDER="static/images"
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER


# Register Blueprint
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp,url_prefix="/admin")



@app.route("/")
def home():
    return redirect("/user/register")





app.secret_key = "secretkey"

def create_table():
    from models.db_config import get_connection
    conn=get_connection()
    cursor = conn.cursor()
    #user table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE,
                   password TEXT,
                   mobile TEXT,
                   gender TEXT,
                   email TEXT,
                   dob TEXT,
                   address TEXT,
                   role TEXT
                   )
                   """)
    
    
    #admin table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS admins(
                   id INTEGER PRIMARY KEY AUTOINCREMENT , 
                   username  TEXT UNIQUE, 
                   password TEXT)
                   """)
    conn.commit()
    conn.close()

create_table()
create_doctor_table()
create_appointment_table()
create_department_table()
create_bill_tables()

from models.admin_model import insert_admin
insert_admin("admin","1234")






if __name__ == "__main__":

    app.run(debug=True)