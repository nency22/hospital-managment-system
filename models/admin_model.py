from models.db_config import get_connection
import sqlite3

#insert admin
def insert_admin(username,password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO  admins (username, password) VALUES(?,?)",(username,password))
        conn.commit()
        print("admin inserted successfull")

    except sqlite3.IntegrityError:
     print("admin already exists")
    conn.close()

    # check admin login

def admin_login(username,password):
       conn = get_connection()
       cursor = conn.cursor()

       cursor.execute("SELECT * FROM admins WHERE username=? AND password=?",(username,password))

       admin = cursor.fetchone()

       conn.close()

       return admin


    
            
        