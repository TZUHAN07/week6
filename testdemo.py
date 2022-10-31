import mysql.connector
from mysql.connector import Error

# 連接 MySQL 資料庫
mydb = mysql.connector.connect(
    host="127.0.0.1",    # 主機名稱
    user="root",         # 帳號
    password="j610114*",  # 密碼
    database='website'   # 資料庫名稱
)
mycursor = mydb.cursor()


mycursor.execute("SELECT * FROM MEMBER")
databases = mycursor.fetchall()
for database in databases:
    print(database)
