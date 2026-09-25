from models.db_config import get_connection
#-------create table------
def create_appointment_table():
    conn = get_connection()
    cursor=conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments(id INTEGER PRIMARY KEY AUTOINCREMENT,
                   patient_name TEXT,
                   mobile TEXT,
                   email TEXT,
                   gender TEXT,
                   dob TEXT,
                   department TEXT,
                   doctor TEXT,
                   appointment_date TEXT,
                   time_slot TEXT,
                   problem TEXT,
                   visit_type TEXT,
                   patient_id TEXT,
                   payment_option TEXT,
                   report TEXT,
                   status TEXT DEFAULT 'pending'
                   )

                   """)
    
    conn.commit()
    conn.close()
#-------book appoinment------

def insert_appointment(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""

                   INSERT INTO appointments
                   (patient_name, mobile, email, gender,dob, department, doctor , appointment_date, time_slot, problem, visit_type, patient_id , payment_option, report)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                   """,data)
    conn.commit()
    conn.close()

#-------user appoinment-------------
def get_user_appointments(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM appointments 
        WHERE LOWER(email)=LOWER(?) 
        ORDER BY appointment_date DESC
    """, (email,))

    data = cursor.fetchall()
    conn.close()
    return data
#----- admin all appoinment--------

def get_all_appoinmtent():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM appointments")

    data = cursor.fetchall()
    conn.close()

    return data
#-------- update status------

def update_status(id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE appointments SET  status=? WHERE id=?",(status,id))
    
    
    conn.commit()
    conn.close()




