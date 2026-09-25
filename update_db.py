
from models.db_config import get_connection
conn=get_connection()

cursor=conn.cursor()
try:

  cursor.execute("ALTER TABLE appointments ADD COLUMN time_slot TEXT")
  print(" column add succesfull")
except:
  print("column already exist")
conn.commit()
conn.close()
