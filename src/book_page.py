import customtkinter as ctk

class BookPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.label = ctk.CTkLabel(self, text="Book Management Page")
        self.label.pack(pady=20)
import customtkinter as ctk
from tkinter import ttk, messagebox
from database import create_connection

class BookPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Configure grid
        self.grid_columnconfigure(0, weight=2)  # Left side (forms)
        self.grid_columnconfigure(1, weight=3)  # Right side (table)
        self.grid_rowconfigure(0, weight=1)  # Make row expandable
        
        # Left side container
        self.left_container = ctk.CTkFrame(self)
        self.left_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.left_container.grid_rowconfigure(1, weight=1)  # Make forms row expandable
        self.left_container.grid_columnconfigure(0, weight=1)
        
        # Buttons Frame for switching forms
        self.switch_buttons_frame = ctk.CTkFrame(self.left_container)
        self.switch_buttons_frame.grid(row=0, column=0, pady=5, padx=10, sticky="ew")
        self.switch_buttons_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        # Create buttons to switch between forms
        ctk.CTkButton(self.switch_buttons_frame, text="Create Form", command=lambda: self.show_form("create")).grid(row=0, column=0, padx=2, sticky="ew")
        ctk.CTkButton(self.switch_buttons_frame, text="Update Form", command=lambda: self.show_form("update")).grid(row=0, column=1, padx=2, sticky="ew")
        ctk.CTkButton(self.switch_buttons_frame, text="Delete Form", command=lambda: self.show_form("delete")).grid(row=0, column=2, padx=2, sticky="ew")
        ctk.CTkButton(self.switch_buttons_frame, text="Search Form", command=lambda: self.show_form("search")).grid(row=0, column=3, padx=2, sticky="ew")
        
        # Create Form
        self.create_frame = ctk.CTkFrame(self.left_container)
        self.create_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.create_frame, text="Create Book", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.title_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Title")
        self.title_entry.pack(pady=5, padx=10, fill="x")
        
        self.author_id_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Author ID")
        self.author_id_entry.pack(pady=5, padx=10, fill="x")
        
        self.category_id_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Category ID")
        self.category_id_entry.pack(pady=5, padx=10, fill="x")
        
        self.isbn_entry = ctk.CTkEntry(self.create_frame, placeholder_text="ISBN")
        self.isbn_entry.pack(pady=5, padx=10, fill="x")
        
        self.quantity_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Quantity")
        self.quantity_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.create_frame, text="Create", command=self.create_book).pack(pady=10)
        
        # Update Form
        self.update_frame = ctk.CTkFrame(self.left_container)
        self.update_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.update_frame, text="Update Book", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.update_id_entry = ctk.CTkEntry(self.update_frame, placeholder_text="Book ID")
        self.update_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Load Book", command=self.load_book).pack(pady=5)
        
        self.update_title_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Title")
        self.update_title_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_author_id_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Author ID")
        self.update_author_id_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_category_id_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Category ID")
        self.update_category_id_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_isbn_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New ISBN")
        self.update_isbn_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_quantity_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Quantity")
        self.update_quantity_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Update", command=self.update_book).pack(pady=10)
        
        # Delete Form
        self.delete_frame = ctk.CTkFrame(self.left_container)
        self.delete_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.delete_frame, text="Delete Book", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.delete_id_entry = ctk.CTkEntry(self.delete_frame, placeholder_text="Book ID")
        self.delete_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.delete_frame, text="Delete", command=self.delete_book, 
                     fg_color="#FF5252", hover_color="#FF0000").pack(pady=10)

        # Search Form
        self.search_frame = ctk.CTkFrame(self.left_container)
        self.search_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.search_frame, text="Search Books", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search by title, author, or ISBN...")
        self.search_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.search_frame, text="Search", command=self.search_books).pack(pady=10)
        ctk.CTkButton(self.search_frame, text="Clear Search", command=self.clear_search).pack(pady=5)
        
        # Right side - Table
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        columns = ('ID', 'Title', 'Author ID', 'Category ID', 'ISBN', 'Available', 'Quantity')
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the table and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Show create form by default
        self.show_form("create")
        
        # Load initial data
        self.refresh_table()
        
    def show_form(self, form_type):
        # Hide all forms first
        self.create_frame.grid_remove()
        self.update_frame.grid_remove()
        self.delete_frame.grid_remove()
        self.search_frame.grid_remove()
        
        # Show the selected form
        if form_type == "create":
            self.create_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "update":
            self.update_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "delete":
            self.delete_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "search":
            self.search_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
    
    def create_book(self):
        try:
            title = self.title_entry.get()
            author_id = self.author_id_entry.get()
            category_id = self.category_id_entry.get()
            isbn = self.isbn_entry.get()
            quantity = self.quantity_entry.get()
            
            if not all([title, author_id, category_id, isbn, quantity]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO books (title, author_id, category_id, isbn, quantity_book)
                VALUES (?, ?, ?, ?, ?)
            """, (title, int(author_id), int(category_id), isbn, int(quantity)))
            
            conn.commit()
            conn.close()
            
            self.clear_create_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Book created successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating book: {e}")
    
    def load_book(self):
        try:
            book_id = self.update_id_entry.get()
            if not book_id:
                messagebox.showerror("Error", "Please enter a book ID")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT title, author_id, category_id, isbn, quantity_book
                FROM books
                WHERE id = ?
            """, (int(book_id),))
            
            book = cursor.fetchone()
            conn.close()
            
            if book:
                self.update_title_entry.delete(0, 'end')
                self.update_title_entry.insert(0, book[0])
                self.update_author_id_entry.delete(0, 'end')
                self.update_author_id_entry.insert(0, book[1])
                self.update_category_id_entry.delete(0, 'end')
                self.update_category_id_entry.insert(0, book[2])
                self.update_isbn_entry.delete(0, 'end')
                self.update_isbn_entry.insert(0, book[3])
                self.update_quantity_entry.delete(0, 'end')
                self.update_quantity_entry.insert(0, book[4])
            else:
                messagebox.showerror("Error", "Book not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading book: {e}")
    
    def update_book(self):
        try:
            book_id = self.update_id_entry.get()
            new_title = self.update_title_entry.get()
            new_author_id = self.update_author_id_entry.get()
            new_category_id = self.update_category_id_entry.get()
            new_isbn = self.update_isbn_entry.get()
            new_quantity = self.update_quantity_entry.get()
            
            if not all([book_id, new_title, new_author_id, new_category_id, new_isbn, new_quantity]):
                 messagebox.showerror("Error", "All fields are required")
                 return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE books
                SET title = ?, author_id = ?, category_id = ?, isbn = ?, quantity_book = ?
                WHERE id = ?
            """, (new_title, int(new_author_id), int(new_category_id), new_isbn, int(new_quantity), int(book_id)))
            
            conn.commit()
            conn.close()
            
            self.clear_update_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Book updated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error updating book: {e}")
    
    def delete_book(self):
        try:
            book_id = self.delete_id_entry.get()
            if not book_id:
                messagebox.showerror("Error", "Please enter a book ID")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM books WHERE id = ?
            """, (int(book_id),))
            
            conn.commit()
            conn.close()
            
            self.delete_id_entry.delete(0, 'end')
            self.refresh_table()
            messagebox.showinfo("Success", "Book deleted successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting book: {e}")
    
    def refresh_table(self):
        # Clear the current table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            # Get books
            cursor.execute("""
                SELECT id, title, author_id, category_id, isbn, available, quantity_book
                FROM books
            """)
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing table: {e}")
    
    def clear_create_entries(self):
        self.title_entry.delete(0, 'end')
        self.author_id_entry.delete(0, 'end')
        self.category_id_entry.delete(0, 'end')
        self.isbn_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
    
    def clear_update_entries(self):
        self.update_id_entry.delete(0, 'end')
        self.update_title_entry.delete(0, 'end')
        self.update_author_id_entry.delete(0, 'end')
        self.update_category_id_entry.delete(0, 'end')
        self.update_isbn_entry.delete(0, 'end')
        self.update_quantity_entry.delete(0, 'end')

    def search_books(self):
        try:
            search_term = self.search_entry.get().strip().lower()
            
            # Clear the current table
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            conn = create_connection()
            cursor = conn.cursor()
            
            # Get books with filters
            query = """
                SELECT id, title, author_id, category_id, isbn, available, quantity_book
                FROM books
                WHERE LOWER(title) LIKE ? OR LOWER(isbn) LIKE ?
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern))
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error searching books: {e}")
            
    def clear_search(self):
        self.search_entry.delete(0, 'end')
        self.refresh_table()
