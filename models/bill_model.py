import sqlite3
from models.db_config import get_connection

# -------- CREATE TABLE --------
def create_bill_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS billing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        doctor_name TEXT,
        date TEXT,
        subtotal REAL,
        tax REAL,
        grand_total REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS billing_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_id INTEGER,
        service_name TEXT,
        qty INTEGER,
        price REAL,
        total REAL,
        FOREIGN KEY (bill_id) REFERENCES billing(id)
    )
    """)

    conn.commit()
    conn.close()


# -------- INSERT BILL --------
def insert_bill(patient, doctor, date, items):
    conn = get_connection()
    cursor = conn.cursor()

    subtotal = sum(item["total"] for item in items)
    tax = subtotal * 0.05
    grand_total = subtotal + tax

    cursor.execute("""
        INSERT INTO billing (patient_name, doctor_name, date, subtotal, tax, grand_total)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (patient, doctor, date, subtotal, tax, grand_total))

    bill_id = cursor.lastrowid

    for item in items:
        cursor.execute("""
            INSERT INTO billing_items (bill_id, service_name, qty, price, total)
            VALUES (?, ?, ?, ?, ?)
        """, (bill_id, item["name"], item["qty"], item["price"], item["total"]))

    conn.commit()
    conn.close()

    return bill_id


# -------- GET ALL BILLS --------
def get_all_bills():
    conn = get_connection()
    bills = conn.execute("SELECT * FROM billing ORDER BY id DESC").fetchall()
    conn.close()
    return bills


# -------- GET SINGLE BILL --------
def get_bill_by_id(bill_id):
    conn = get_connection()

    bill = conn.execute("SELECT * FROM billing WHERE id=?", (bill_id,)).fetchone()
    items = conn.execute("SELECT * FROM billing_items WHERE bill_id=?", (bill_id,)).fetchall()

    conn.close()
    return bill, items