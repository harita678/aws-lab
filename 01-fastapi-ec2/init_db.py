from database import get_db_connection

def init_db():
    #get the connection
    conn = get_db_connection()
    print(conn) # Print the connection object to verify it's working
    #we need a cursor to execute SQL commands, because conn doesnt execute the SQL queries
    cursor = conn.cursor()

    print("Creating table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
    """)

    conn.commit()  # Save changes to the database
    cursor.close()  # Close the cursor
    conn.close()    # Close the connection
    print("Table created successfully.")

if __name__ == "__main__":
    init_db()