import sqlite3

def init_db():
    conn = sqlite3.connect("calories.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            intake INTEGER,
            burned INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()

def add_data(date, intake, burned):
    conn = sqlite3.connect("calories.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO calories (date, intake, burned) VALUES (?, ?, ?)", (date, intake, burned))
    conn.commit()
    conn.close()

def fetch_data():
    conn = sqlite3.connect("calories.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT date, intake, burned FROM calories ORDER BY date")
    data = cursor.fetchall()
    
    conn.close()
    return data

# Initialize Database
init_db()
