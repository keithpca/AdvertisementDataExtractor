import mysql.connector

print("📡 Attempting connection to MySQL...")

try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='drivpca',
        database='newspaper_ads'
    )
    print("✅ Connected to MySQL successfully!")

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("📋 Tables in the database:", tables)

    cursor.close()
    conn.close()
except mysql.connector.Error as err:
    print("❌ MySQL Error:", err)
except Exception as e:
    print("❌ General Error:", e)
