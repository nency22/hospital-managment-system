from models.db_config import get_connection

# create doctor table
def create_doctor_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT,
        qualification TEXT,
        mobile TEXT,
        email TEXT,
        experience INTEGER,
        consultant_fee INTEGER,
        registration_number TEXT,
        gender TEXT,
        available_days TEXT,
        morning_time TEXT,
        evening_time TEXT,
        about_doctor TEXT,
        doctor_image TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


# add doctor
def add_doctor(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO doctors(
        name, qualification, department, mobile, email, experience,
        consultant_fee, registration_number, gender, available_days,
        morning_time, evening_time, about_doctor, doctor_image, status
    )
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, data)

    conn.commit()
    conn.close()


# get all doctors
def get_all_doctor():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM doctors")

    rows = cursor.fetchall()

    doctors = []

    for row in rows:

        doctors.append({
            "id":row[0],
            "name":row[1],
            "qualification":row[2],
            "department":row[3],
            "mobile":row[4],
            "email":row[5],
            "experience":row[6],
            "fee":row[7],
            "registration":row[8],
            "gender":row[9],
            "available_days":row[10],
            "morning_time":row[11],
            "evening_time":row[12],
            "about":row[13],
            "image":row[14],
            "status":row[15]
        })

    conn.close()

    return doctors

# get single doctor
def get_doctor_by_id(doctor_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM doctors WHERE id=?", (doctor_id,))
    doctor = cursor.fetchone()

    conn.close()
    return doctor


# update doctor
def update_doctor(doctor_id, data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE doctors SET
        name=?,
        qualification=?,
        department=?,
        mobile=?,
        email=?,
        experience=?,
        consultant_fee=?,
        registration_number=?,
        gender=?,
        available_days=?,
        morning_time=?,
        evening_time=?,
        about_doctor=?,
        doctor_image=?,
        status=?
    WHERE id=?
    """, (*data, doctor_id))

    conn.commit()
    conn.close()


# delete doctor
def delete_doctor(doctor_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM doctors WHERE id=?", (doctor_id,))
    conn.commit()
    conn.close()