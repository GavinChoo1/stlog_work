import psycopg2

try:
    # 1. Connect to the database
    # Since Postgres is in Docker, 'localhost' works for your host
    connection = psycopg2.connect(
        user="admin",
        password="admin123",
        host="127.0.0.1",
        port="5432",
        database="hls_db"
    )

    # 2. Create a cursor (your "pointer" to the data)
    cursor = connection.cursor()

    # 3. Execute a SQL query
    # Note: Using public.test_users because we created it in the public schema
    cursor.execute("SELECT * FROM hls_db.account.users;")

    # 4. Fetch the results
    rows = cursor.fetchall()

    print(f"\n--- Found {len(rows)} Users ---")
    for row in rows:
        print(f"ID: {row[0]} | Username: {row[1]} | Pass: {row[2]}")

except Exception as error:
    print(f"Error connecting to Postgres: {error}")

finally:
    # 5. Close the connection
    if connection:
        cursor.close()
        connection.close()
        print("\nPostgreSQL connection closed.")