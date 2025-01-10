import sqlite3

def create_connection():
    conn = sqlite3.connect('library.db')
    return conn

def seed_data():
    conn = create_connection()
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM categories")
    cursor.execute("DELETE FROM books")
    cursor.execute("DELETE FROM loans")
    cursor.execute("DELETE FROM fees")

    # Seed users
    users = [
        ('r', 'r', 'Admin User', 'admin', 1),
        ('admin', 'admin123', 'Admin User', 'admin', 1),
        ('user1', 'user123', 'Regular User 1', 'user', 1),
        ('user2', 'user123', 'Regular User 2', 'user', 0),
        ('user3', 'user123', 'Regular User 3', 'user', 1),
        ('user4', 'user123', 'Regular User 4', 'user', 0)
    ]
    cursor.executemany("INSERT INTO users (username, password, name, role, approved) VALUES (?, ?, ?, ?, ?)", users)

    # Seed authors
    authors = [
        ('Jane Austen', '123-456-7890', 'jane.austen@example.com', 'A famous novelist'),
        ('Charles Dickens', '987-654-3210', 'charles.dickens@example.com', 'Another famous novelist'),
        ('Agatha Christie', '555-123-4567', 'agatha.christie@example.com', 'A mystery writer'),
        ('Leo Tolstoy', '111-222-3333', 'leo.tolstoy@example.com', 'A Russian writer'),
        ('Virginia Woolf', '444-555-6666', 'virginia.woolf@example.com', 'A modernist writer')
    ]
    cursor.executemany("INSERT INTO authors (name, phone_number, email, description) VALUES (?, ?, ?, ?)", authors)

    # Seed categories
    categories = [
        ('Fiction', 'Fictional stories'),
        ('Mystery', 'Mystery and suspense'),
        ('Classic', 'Classic literature'),
        ('Science Fiction', 'Sci-fi stories'),
        ('Fantasy', 'Fantasy worlds')
    ]
    cursor.executemany("INSERT INTO categories (name, description) VALUES (?, ?)", categories)

    # Seed books
    books = [
        ('Pride and Prejudice', 1, 1, '978-0141439518', 5, 5),
        ('Oliver Twist', 2, 1, '978-0141439648', 3, 3),
        ('The Mysterious Affair at Styles', 3, 2, '978-0062073565', 2, 2),
        ('The ABC Murders', 3, 2, '978-0007119310', 4, 4),
        ('Great Expectations', 2, 3, '978-0141439631', 1, 1),
        ('War and Peace', 4, 3, '978-0140444179', 2, 2),
        ('To the Lighthouse', 5, 1, '978-0156907394', 3, 3),
        ('Dune', 6, 4, '978-0441172719', 4, 4),
        ('The Hobbit', 7, 5, '978-0618260264', 5, 5),
        ('The Lord of the Rings', 7, 5, '978-0618260271', 2, 2)
    ]
    cursor.executemany("INSERT INTO books (title, author_id, category_id, isbn, quantity_book, available) VALUES (?, ?, ?, ?, ?, ?)", books)
    
    # Seed loans
    loans = [
        (3, 1, '2024-01-05', '2024-01-20'),
        (4, 2, '2024-01-10', None),
        (5, 3, '2024-01-15', '2024-01-25'),
        (6, 4, '2024-01-20', None),
        (7, 5, '2024-01-25', '2024-02-05'),
        (8, 1, '2024-02-01', None),
        (9, 2, '2024-02-05', '2024-02-15'),
        (10, 3, '2024-02-10', None),
        (1, 6, '2024-02-15', '2024-02-25'),
        (2, 7, '2024-02-20', None)
    ]
    cursor.executemany("INSERT INTO loans (book_id, user_id, borrow_date, return_date) VALUES (?, ?, ?, ?)", loans)
    
    # Seed fees
    fees = [
        (1, 10.00, 1),
        (2, 5.00, 0),
        (3, 7.50, 1),
        (4, 12.00, 0),
        (5, 2.50, 1),
        (6, 8.00, 0),
        (7, 6.00, 1),
        (8, 9.00, 0),
        (9, 11.00, 1),
        (10, 4.00, 0)
    ]
    cursor.executemany("INSERT INTO fees (loan_id, amount, paid) VALUES (?, ?, ?)", fees)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_data()
    print("Dummy data seeded successfully.")
