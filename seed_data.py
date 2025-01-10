import sqlite3

def create_connection():
    conn = sqlite3.connect('library.db')
    return conn

def seed_data():
    conn = create_connection()
    cursor = conn.cursor()

    # Seed users
    users = [
        ('admin', 'admin123', 'Admin User', 'admin', 1),
        ('user1', 'user123', 'Regular User 1', 'user', 1),
        ('user2', 'user123', 'Regular User 2', 'user', 0)
    ]
    cursor.executemany("INSERT INTO users (username, password, name, role, approved) VALUES (?, ?, ?, ?, ?)", users)

    # Seed authors
    authors = [
        ('Jane Austen', '123-456-7890', 'jane.austen@example.com', 'A famous novelist'),
        ('Charles Dickens', '987-654-3210', 'charles.dickens@example.com', 'Another famous novelist'),
        ('Agatha Christie', '555-123-4567', 'agatha.christie@example.com', 'A mystery writer')
    ]
    cursor.executemany("INSERT INTO authors (name, phone_number, email, description) VALUES (?, ?, ?, ?)", authors)

    # Seed categories
    categories = [
        ('Fiction', 'Fictional stories'),
        ('Mystery', 'Mystery and suspense'),
        ('Classic', 'Classic literature')
    ]
    cursor.executemany("INSERT INTO categories (name, description) VALUES (?, ?)", categories)

    # Seed books
    books = [
        ('Pride and Prejudice', 1, 1, '978-0141439518', 5, 5),
        ('Oliver Twist', 2, 1, '978-0141439648', 3, 3),
        ('The Mysterious Affair at Styles', 3, 2, '978-0062073565', 2, 2),
        ('The ABC Murders', 3, 2, '978-0007119310', 4, 4),
        ('Great Expectations', 2, 3, '978-0141439631', 1, 1)
    ]
    cursor.executemany("INSERT INTO books (title, author_id, category_id, isbn, quantity_book, available) VALUES (?, ?, ?, ?, ?, ?)", books)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_data()
    print("Dummy data seeded successfully.")
