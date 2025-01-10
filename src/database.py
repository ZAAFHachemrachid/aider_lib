import sqlite3

def create_connection():
    """ Create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect('library.db')
        print(f"Successfully connected to SQLite version: {sqlite3.version}")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_tables(conn):
    """ Create tables in the database """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                approved INTEGER NOT NULL DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                phone_number TEXT NOT NULL,
                email TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                available INTEGER NOT NULL DEFAULT 1,
                quantity_book INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (author_id) REFERENCES authors(id),
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                borrow_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                loan_date TEXT,
                return_date TEXT,
                fine_amount REAL DEFAULT 0.0,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                loan_id INTEGER,
                amount REAL,
                paid INTEGER,
                FOREIGN KEY (loan_id) REFERENCES loans(id)
            )
        """)
        conn.commit()
        print("Tables created successfully")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

if __name__ == '__main__':
    conn = create_connection()
    if conn:
        create_tables(conn)
        conn.close()
