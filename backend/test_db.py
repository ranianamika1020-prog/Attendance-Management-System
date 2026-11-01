from db import get_db_connection

try:
    conn = get_db_connection()
    print("MySQL connected successfully!")
    print("Connected database:", conn.database)

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")

    print("\nTables in database:")
    for table in cursor.fetchall():
        print(table[0])

    cursor.close()
    conn.close()

except Exception as e:
    print("Error:", e)