from database import get_db_connection

def create_user(name: str, email: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id;",(name, email, password))
    user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return {
        "id": user_id,
        "name": name,
        "email": email,
        "password": password
    }

def get_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, password from users where id = %s;", (user_id,))

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None:
        return None
    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "password": row[3]
    }
def update_user(user_id: int, name: str = None, email: str = None, password: str = None):
    """Update fields of an existing user. Returns updated user dict or None if not found."""
    # Build dynamic UPDATE based on which fields were provided
    updates = []
    values = []
    
    if name is not None:
        updates.append("name = %s")
        values.append(name)
    if email is not None:
        updates.append("email = %s")
        values.append(email)
    if password is not None:
        updates.append("password = %s")
        values.append(password)
    
    if not updates:
        # Nothing to update — just return current user
        return get_user(user_id)
    
    # Build the final SQL
    sql = f"UPDATE users SET {', '.join(updates)} WHERE id = %s RETURNING id, name, email, password;"
    values.append(user_id)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, tuple(values))
    row = cursor.fetchone()
    
    conn.commit()
    cursor.close()
    conn.close()
    
    if row is None:
        return None
    
    return {
        "id": row[0],
        "name": row[1],
        "email": row[2]
    }

def delete_user(user_id: int):
    """Delete a user by id. Returns True if deleted, False if not found."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    deleted = cursor.rowcount > 0
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return deleted