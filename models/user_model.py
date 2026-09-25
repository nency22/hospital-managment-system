from models.db_config import get_connection


def insert_user(username,password,mobile,gender,email,dob, address, role):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?",(username,))
    if cursor.fetchone():
        conn.close()
        return "exists"
    cursor.execute("""
      INSERT INTO users(
                   username,
                   password,
                   mobile,
                   gender,
                   email,
                   dob, 
                   address, 
                   role)
                   VALUES(?,?,?,?,?,?,?,?)
                  


                   """,(username, password, mobile, gender, email, dob, address, role))
    conn.commit()
    conn.close()
    return "success"
def check_user(username,password):
    conn=get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",(username,password))
    
    user=cursor.fetchone()
    conn.close()
    return user
    
