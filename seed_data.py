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
            ('admin', self._hash_password('admin123'), 'Admin User', 'admin', 1),
            ('librarian', self._hash_password('lib123'), 'Head Librarian', 'librarian', 1),
            ('john_doe', self._hash_password('user123'), 'John Doe', 'user', 1),
            ('jane_smith', self._hash_password('user123'), 'Jane Smith', 'user', 1),
            ('mike_wilson', self._hash_password('user123'), 'Mike Wilson', 'user', 1),
            ('sarah_jones', self._hash_password('user123'), 'Sarah Jones', 'user', 1)
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
            ('Stephen King', '+1 207 555 0123', 'stephen@example.com', 'American author of horror and fantasy novels'),
            ('Agatha Christie', '+44 20 7123 4570', 'agatha@example.com', 'Queen of Mystery'),
            ('Neil Gaiman', '+44 20 7123 4571', 'neil@example.com', 'Fantasy and comic book author'),
            ('Terry Pratchett', '+44 20 7123 4572', 'terry@example.com', 'Creator of Discworld series'),
            ('Isaac Asimov', '+1 212 555 0124', 'isaac@example.com', 'Science fiction grandmaster'),
            ('Margaret Atwood', '+1 416 555 0125', 'margaret@example.com', 'Canadian author and poet'),
            ('Charles Dickens', '+44 20 7123 4573', 'charles@example.com', 'Victorian era novelist'),
            ('Ernest Hemingway', '+1 305 555 0126', 'ernest@example.com', 'American novelist'),
            ('Virginia Woolf', '+44 20 7123 4574', 'virginia@example.com', 'Modernist author'),
            ('Ray Bradbury', '+1 310 555 0127', 'ray@example.com', 'Science fiction author'),
            ('Haruki Murakami', '+81 3 5555 0128', 'haruki@example.com', 'Japanese contemporary author')
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
            ('Fantasy', 'Magic and supernatural stories'),
            ('Classic Literature', 'Time-tested literary works'),
            ('Horror', 'Scary and supernatural stories'),
            ('Contemporary Fiction', 'Modern literary works'),
            ('Historical Fiction', 'Fiction set in past times'),
            ('Dystopian', 'Stories about troubled futures')
        ]
        self.cursor.executemany('''
            INSERT OR IGNORE INTO categories (name, description)
            VALUES (?, ?)
        ''', categories)
    
    def seed_books(self):
        """Seed books table with initial data"""
        books = [
            # J.K. Rowling - Fantasy (5)
            ('Harry Potter and the Philosopher\'s Stone', 1, 5, '9780747532699', 1, 5),
            ('Harry Potter and the Chamber of Secrets', 1, 5, '9780747538486', 1, 4),
            ('Harry Potter and the Prisoner of Azkaban', 1, 5, '9780747542155', 1, 3),
            ('Harry Potter and the Goblet of Fire', 1, 5, '9780747591054', 1, 4),
            ('Harry Potter and the Order of Phoenix', 1, 5, '9780747551003', 1, 3),

            # George Orwell - Dystopian (10)
            ('1984', 2, 10, '9780451524935', 1, 3),
            ('Animal Farm', 2, 10, '9780452284241', 1, 3),

            # Jane Austen - Classic Literature (6)
            ('Pride and Prejudice', 3, 6, '9780141439518', 1, 4),
            ('Emma', 3, 6, '9780141439587', 1, 3),
            ('Sense and Sensibility', 3, 6, '9780141439662', 1, 3),

            # Stephen King - Horror (7)
            ('The Shining', 4, 7, '9780307743657', 1, 2),
            ('It', 4, 7, '9781501142970', 1, 3),
            ('Pet Sematary', 4, 7, '9781501156700', 1, 2),
            ('Salem\'s Lot', 4, 7, '9780385007510', 1, 2),
            ('The Stand', 4, 7, '9780307743680', 1, 2),

            # Agatha Christie - Mystery (4)
            ('Murder on the Orient Express', 5, 4, '9780062693662', 1, 3),
            ('And Then There Were None', 5, 4, '9780062490371', 1, 3),
            ('Death on the Nile', 5, 4, '9780062490360', 1, 3),

            # Neil Gaiman - Fantasy (5)
            ('American Gods', 6, 5, '9780380789030', 1, 3),
            ('Neverwhere', 6, 5, '9780380789031', 1, 2),
            ('Good Omens', 6, 5, '9780380789032', 1, 2),

            # Terry Pratchett - Fantasy (5)
            ('The Color of Magic', 7, 5, '9780062225672', 1, 3),
            ('Guards! Guards!', 7, 5, '9780062225673', 1, 2),
            ('Small Gods', 7, 5, '9780062225674', 1, 2),

            # Isaac Asimov - Science Fiction (3)
            ('Foundation', 8, 3, '9780553293357', 1, 3),
            ('I, Robot', 8, 3, '9780553294385', 1, 3),
            ('The Caves of Steel', 8, 3, '9780553293400', 1, 2),

            # Margaret Atwood - Contemporary Fiction (8)
            ('The Handmaid\'s Tale', 9, 8, '9780385490818', 1, 4),
            ('Oryx and Crake', 9, 8, '9780385721677', 1, 3),
            ('The Blind Assassin', 9, 8, '9780385720953', 1, 2),

            # Charles Dickens - Classic Literature (6)
            ('Great Expectations', 10, 6, '9780141439563', 1, 3),
            ('A Tale of Two Cities', 10, 6, '9780141439600', 1, 3),
            ('Oliver Twist', 10, 6, '9780141439747', 1, 2),

            # Ernest Hemingway - Classic Literature (6)
            ('The Old Man and the Sea', 11, 6, '9780684801223', 1, 3),
            ('For Whom the Bell Tolls', 11, 6, '9780684803356', 1, 2),
            ('A Farewell to Arms', 11, 6, '9780684801469', 1, 2),

            # Virginia Woolf - Classic Literature (6)
            ('Mrs Dalloway', 12, 6, '9780156628709', 1, 2),
            ('To the Lighthouse', 12, 6, '9780156907392', 1, 2),

            # Ray Bradbury - Science Fiction (3)
            ('Fahrenheit 451', 13, 3, '9781451673319', 1, 4),
            ('The Martian Chronicles', 13, 3, '9781451678192', 1, 3),

            # Haruki Murakami - Contemporary Fiction (8)
            ('Norwegian Wood', 14, 8, '9780375704024', 1, 3),
            ('Kafka on the Shore', 14, 8, '9781400079278', 1, 2),
            ('1Q84', 14, 8, '9780307593313', 1, 2)
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
            (4, 2, (current_date - timedelta(days=25)).strftime('%Y-%m-%d'),
             (current_date - timedelta(days=5)).strftime('%Y-%m-%d'),
             (current_date - timedelta(days=25)).strftime('%Y-%m-%d'), None, 5.0),
            (5, 15, (current_date - timedelta(days=10)).strftime('%Y-%m-%d'),
             (current_date + timedelta(days=20)).strftime('%Y-%m-%d'),
             (current_date - timedelta(days=10)).strftime('%Y-%m-%d'), None, 0.0),
            (6, 22, (current_date - timedelta(days=5)).strftime('%Y-%m-%d'),
             (current_date + timedelta(days=25)).strftime('%Y-%m-%d'),
             (current_date - timedelta(days=5)).strftime('%Y-%m-%d'), None, 0.0)
        ]
        self.cursor.executemany('''
            INSERT OR IGNORE INTO loans (user_id, book_id, borrow_date, due_date, loan_date, return_date, fine_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', loans)
    
    def seed_fees(self):
        """Seed fees table with initial data"""
        fees = [
            (2, 5.0, 0),  # Unpaid fee for the overdue book
            (3, 2.5, 1),  # Paid fee
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