# Library Management System

This is a Library Management System built with Python and Tkinter. It uses a SQLite database to store information about users, authors, categories, books, and loans.

## Project Structure

-   `library.db`: SQLite database file.
-   `seed_data.py`: Script to seed the database with initial data.
-   `src/`: Source code directory.
    -   `__init__.py`: Makes the `src` directory a Python package.
    -   `admin_user_page.py`: Manages admin user functionalities.
    -   `author_page.py`: Manages author functionalities.
    -   `book_page.py`: Manages book functionalities.
    -   `category_page.py`: Manages category functionalities.
    -   `database.py`: Manages database connections and table creation.
    -   `fee_page.py`: Manages fee functionalities.
    -   `loan_page.py`: Manages loan functionalities.
    -   `login_page.py`: Manages user login.
    -   `main.py`: Main application file.

## How to Run

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Seed the database:**
    ```bash
    python seed_data.py
    ```
3.  **Run the application:**
    ```bash
    python src/main.py
    ```

## Code Explanation

### `database.py`

-   `create_connection()`: Establishes a connection to the SQLite database (`library.db`).
-   `create_tables(conn)`: Creates the necessary tables in the database if they don't exist.

### `seed_data.py`

-   `DatabaseSeeder`: Class to seed the database with initial data for users, authors, categories, books, loans, and fees.
-   `seed_all()`: Seeds all tables.

### `src/main.py`

-   `LibraryApp`: Main application class that sets up the GUI using `customtkinter`.
-   Manages navigation between different pages (Home, Admin, Author, Category, Book, Loan, Fee).
-   Includes a login system to authenticate users.
-   Displays a book chart on the home page.

### `src/admin_user_page.py`

-   `AdminUserPage`: Manages the creation, updating, deletion, and searching of admin users.

### `src/author_page.py`

-   `AuthorPage`: Manages the creation, updating, deletion, and searching of authors.

### `src/category_page.py`

-   `CategoryPage`: Manages the creation, updating, deletion, and searching of categories.

### `src/book_page.py`

-   `BookPage`: Manages the creation, updating, deletion, and searching of books.

### `src/loan_page.py`

-   `LoanPage`: Manages the creation, returning, updating, deletion, and searching of loans.

### `src/fee_page.py`

-   `FeePage`: Manages the creation, updating, deletion, and searching of fees.

### `src/login_page.py`

-   `LoginPage`: Handles user login and authentication.

## Requirements

-   Python 3.6+
-   `customtkinter`
-   `matplotlib`
-   `sqlite3` (included with Python)
```
