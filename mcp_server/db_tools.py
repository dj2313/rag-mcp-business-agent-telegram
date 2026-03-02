import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "business_agent.db")

def init_db():
    """Initializes the SQLite database with sample data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        plan TEXT,
        status TEXT
    )
    ''')
    
    # Insert sample data if empty
    cursor.execute('SELECT COUNT(*) FROM customers')
    if cursor.fetchone()[0] == 0:
        sample_customers = [
            (101, 'Alice Smith', 'alice@example.com', 'Premium', 'Active'),
            (102, 'Bob Johnson', 'bob@example.com', 'Free', 'Inactive'),
            (103, 'Charlie Brown', 'charlie@example.com', 'Standard', 'Active'),
        ]
        cursor.executemany('INSERT INTO customers VALUES (?,?,?,?,?)', sample_customers)
        conn.commit()
    
    conn.close()

def search_database(query: str):
    """Searches for customers by name or email."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    search_query = f"%{query}%"
    cursor.execute('SELECT * FROM customers WHERE name LIKE ? OR email LIKE ?', (search_query, search_query))
    rows = cursor.fetchall()
    
    results = [dict(row) for row in rows]
    conn.close()
    return results

def get_record(customer_id: int):
    """Fetches a specific customer record by ID."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
    row = cursor.fetchone()
    
    result = dict(row) if row else None
    conn.close()
    return result

if __name__ == "__main__":
    init_db()
    print("Database initialized with sample records.")
    print("Search 'Alice':", search_database("Alice"))
