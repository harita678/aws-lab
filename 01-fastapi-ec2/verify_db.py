from database import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

# List all tables in the public schema
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public';
""")
tables = cursor.fetchall()
print("Tables in database:")
for t in tables:
    print(f"  - {t[0]}")

# Show columns of users table
cursor.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'users';
""")
columns = cursor.fetchall()
print("\nColumns in 'users' table:")
for col in columns:
    print(f"  - {col[0]}: {col[1]}")

cursor.execute("SELECT id, name, email, password from users;")

row = cursor.fetchall()
print("\nUsers in 'users' table:")
for user in row:
    print(f"  - id: {user[0]}, name: {user[1]}, email: {user[2]}, password: {user[3]}")

cursor.close()
conn.close()