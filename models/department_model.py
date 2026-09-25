from models.db_config import get_connection
#-----------create table-------------------

def create_department_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
      CREATE TABLE IF NOT EXISTS departments
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   doctor TEXT,
                   description TEXT,
                   status TEXT,
                   image TEXT)
                   """)
    
    conn.commit()
    conn.close()

    #----------insert department------------

def add_department(data):
    conn=get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO departments
                   (name,doctor,description, status,image)
                   VALUES(?,?,?,?,?)

                    """,data)
    conn.commit()
    conn.close()

    #-------get all------
def get_all_departments():
        conn=get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM departments")

        data = cursor.fetchall()
        conn.close()
        return data
    

    #--------get by ID-----------
def get_department_by_id(id):
        conn= get_connection()
        dept=conn.execute(
            "SELECT * FROM departments WHERE id=?",(id,)).fetchone()
        conn.close()
        return dept
    
    #---------update----------
def update_department(data):
        conn= get_connection()
        conn.execute("""
               UPDATE departments SET name=?,doctor=?,description=?,status=?,image=? WHERE id=?
                     """,data)
        conn.commit()
        conn.close()

    #-------delete---------
def delete_department(id):
        conn = get_connection()
        conn.execute("DELETE FROM departments WHERE id=?",(id,))

        conn.commit()
        conn.close()
        