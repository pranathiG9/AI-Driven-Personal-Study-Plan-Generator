import sqlite3

# Create or update the database schema
conn = sqlite3.connect("users.db")
c = conn.cursor()

# Create users table
c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        role TEXT NOT NULL,
        password TEXT NOT NULL
    )
""")

# Create study_plans table
c.execute("""
    CREATE TABLE IF NOT EXISTS study_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        course_name TEXT NOT NULL,
        start_date TEXT NOT NULL,
        days INTEGER NOT NULL,
        skills TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
""")

conn.commit()
conn.close()

# Functions to manage users and study plans
def add_user(name, email, age, role, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (name, email, age, role, password)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, age, role, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = c.fetchone()
    conn.close()
    return user

def fetch_user(email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    return user

def add_study_plan(user_id, course_name, start_date, days, skills):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO study_plans (user_id, course_name, start_date, days, skills)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, course_name, start_date, days, skills))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()

def get_study_plans(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, course_name, start_date, days, skills FROM study_plans WHERE user_id = ?
        """, (user_id,))
        plans = cursor.fetchall()
        return [
            {
                "id": row[0],
                "course_name": row[1],
                "start_date": row[2],
                "days": row[3],
                "skills": row[4],
            }
            for row in plans
        ]
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

def update_study_plan(plan_id, course_name, start_date, days):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE study_plans
            SET course_name = ?, start_date = ?, days = ?
            WHERE id = ?
        """, (course_name, start_date, days, plan_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()
def delete_study_plan(plan_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM study_plans WHERE id = ?", (plan_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()