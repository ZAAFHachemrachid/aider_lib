import sqlite3
from datetime import datetime, timedelta
import hashlib

class DatabaseSeeder:
    def __init__(self, db_name='library.db'):
        """Initialize the seeder with database connection"""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    def _hash_password(self, password):
        """Simple password hashing"""
        return password
    
    def seed_users(self):
        """Seed users table with initial data"""
        users = [
            ('admin', self._hash_password('admin'), 'r', 'admin', 1),
            ('admin', self._hash_password('admin123'), 'Admin User', 'admin', 1),
            ('librarian', self._hash_password('lib123'), 'Head Librarian', 'librarian', 1),
            ('john_doe', self._hash_password('user123'), 'John Doe', 'user', 1),
            ('jane_smith', self._hash_password('user123'), 'Jane Smith', 'user', 1)
        ]
        self.cursor.executemany('''
            INSERT OR IGNORE INTO users (username, password, name, role, approved)
            VALUES (?, ?, ?, ?, ?)
        ''', users)
        
    def seed_authors(self):
        """Seed authors table with initial data"""
        authors = [
            ('J.K. Rowling', '+44 20 7123 4567', 'jk@example.com', 'British author known for Harry Potter series'),
            ('George Orwell', '+44 20 7123 4568', 'george@example.com', 'English novelist and essayist'),
            ('Jane Austen', '+44 20 7123 4569', 'jane@example.com', 'English novelist known for Pride and Prejudice'),
            ('Stephen King', '+1 207 555 0123', 'stephen@example.com', 'American author of horror and fantasy novels')
        ]
        self.cursor.executemany('''
            INSERT OR IGNORE INTO authors (name, phone_number, email, description)
            VALUES (?, ?, ?, ?)
        ''', authors)
    
    def seed_categories(self):
        """Seed categories table with initial data"""
        categories = [
            ('Fiction', 'Novels and made-up stories'),
            ('Non-Fiction', 'Factual books and biographies'),
            ('Science Fiction', 'Future and science-based fiction'),
            ('Mystery', 'Crime and detective stories'),
            ('Fantasy', 'Magic and supernatural stories')
        ]
        self.cursor.executemany('''
            INSERT OR IGNORE INTO categories (name, description)
            VALUES (?, ?)
        ''', categories)
    
    def seed_books(self):
        """Seed books table with initial data"""
        books = [
            ('Harry Potter and the Philosopher\'s Stone', 1, 5, '9780747532699', 1, 5),
            ('1984', 2, 3, '9780451524935', 1, 3),
            ('Pride and Prejudice', 3, 1, '9780141439518', 1, 4),
            ('The Shining', 4, 1, '9780307743657', 1, 2),
            ('Animal Farm', 2, 1, '9780452284241', 1, 3)
        ]
        self.cursor.executemany('''
            INSERT OR IGNORE INTO books (title, author_id, category_id, isbn, available, quantity_book)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', books)
    
    def seed_loans(self):
        """Seed loans table with initial data"""
        current_date = datetime.now()
        loans = [
            (3, 1, (current_date - timedelta(days=15)).strftime('%Y-%m-%d'),
             (current_date + timedelta(days=15)).strftime('%Y-%m-%d'),
             (current_date - timedelta(days=15)).strftime('%Y-%m-%d'), None, 0.0),
            (4, 2, (current_date - timedelta(days=15)).strftime('%Y-%m-%d'),
             (current_date - timedelta(days=15)).strftime('%Y-%m-%d'),
             (current_date - timedelta(days=15)).strftime('%Y-%m-%d'), None, 5.0)
        ]
        self.cursor.executemany('''
            INSERT OR IGNORE INTO loans (user_id, book_id, borrow_date, due_date, loan_date, return_date, fine_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', loans)
    
    def seed_fees(self):
        """Seed fees table with initial data"""
        fees = [
            (2, 5.0, 0),  # Unpaid fee for the overdue book
        ]
        self.cursor.executemany('''
            INSERT OR IGNORE INTO fees (loan_id, amount, paid)
            VALUES (?, ?, ?)
        ''', fees)
    
    def seed_all(self):
        """Seed all tables with initial data"""
        try:
            self.seed_users()
            self.seed_authors()
            self.seed_categories()
            self.seed_books()
            self.seed_loans()
            self.seed_fees()
            self.conn.commit()
            print("Database seeded successfully!")
        except sqlite3.Error as e:
            print(f"Error seeding database: {e}")
            self.conn.rollback()
        finally:
            self.conn.close()

if __name__ == '__main__':
    seeder = DatabaseSeeder()
    seeder.seed_all()