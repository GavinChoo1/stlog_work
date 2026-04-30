from funcs.connections import pg_db
try:
    conn = pg_db()
    cur = conn.cursor()
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'account' AND table_name = 'users';")
    columns = [row[0] for row in cur.fetchall()]
    print("Columns in account.users:", columns)
    conn.close()
except Exception as e:
    print("Error:", e)
