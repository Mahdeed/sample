import pymysql as sql

DATABASEIP = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DATABASE = "e_commerce"

def connect():
    try:
        db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
        cursor = db.cursor()
        print("DATABASE IS CONNECTED")
    except Exception as e :
        print(e._traceback_)
