import os
import pymysql
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()

charset = os.getenv('DB_CHARSET')
connect_timeout = int(os.getenv('DB_CONNECT_TIMEOUT', 10))
db = os.getenv('DB_NAME')
host = os.getenv('DB_HOST')
password = os.getenv('DB_PASSWORD')
read_timeout = int(os.getenv('DB_READ_TIMEOUT', 10))
port = int(os.getenv('DB_PORT', 3306))
user = os.getenv('DB_USER')
write_timeout = int(os.getenv('DB_WRITE_TIMEOUT', 10))

connection = pymysql.connect(
    charset=charset,
    connect_timeout=connect_timeout,
    cursorclass=getattr(pymysql.cursors, os.getenv('DB_CURSORCLASS', 'DictCursor')),
    db=db,
    host=host,
    password=password,
    read_timeout=read_timeout,
    port=port,
    user=user,
    write_timeout=write_timeout
)
  
try:
    cursor = connection.cursor()

    # Select all users from the `users` table
    cursor.execute("SELECT * FROM users")

    # Fetch all rows from the last executed statement
    rows = cursor.fetchall()

    # Check if rows exist
    if rows:
        # Print column names
        print([column[0] for column in cursor.description])
        # Print each row
        for row in rows:
            print(row)
    else:
        print("No data found.")

finally:
    connection.close()
