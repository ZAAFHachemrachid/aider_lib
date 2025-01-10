import customtkinter as ctk
from tkinter import ttk, messagebox
from src.database import create_connection
from datetime import date

class LoanPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Configure grid
        self.grid_columnconfigure(0, weight=2)  # Left side (forms)
        self.grid_columnconfigure(1, weight=3)  # Right side (tables)
        self.grid_rowconfigure(0, weight=1)  # Top row for loan table
        self.grid_rowconfigure(1, weight=1)  # Bottom row for user/book tables
        
        # Left side container
        self.left_container = ctk.CTkFrame(self)
        self.left_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", rowspan=2)
        self.left_container.grid_rowconfigure(2, weight=1)  # Make forms row expandable
        self.left_container.grid_columnconfigure(0, weight=1)
        
        # Buttons Frame for switching forms
        self.switch_buttons_frame = ctk.CTkFrame(self.left_container)
        self.switch_buttons_frame.grid(row=0, column=0, pady=5, padx=10, sticky="ew")
        self.switch_buttons_frame.grid_columnconfigure((0,1), weight=1)
        
        # Create buttons to switch between forms
        ctk.CTkButton(self.switch_buttons_frame, text="Create Loan", command=lambda: self.show_form("create")).grid(row=0, column=0, padx=2, sticky="ew")
        ctk.CTkButton(self.switch_buttons_frame, text="Return Loan", command=lambda: self.show_form("return")).grid(row=0, column=1, padx=2, sticky="ew")
        ctk.CTkButton(self.switch_buttons_frame, text="Update Loan", command=lambda: self.show_form("update")).grid(row=0, column=2, padx=2, sticky="ew")
        ctk.CTkButton(self.switch_buttons_frame, text="Delete Loan", command=lambda: self.show_form("delete")).grid(row=0, column=3, padx=2, sticky="ew")
        
        # Create Loan Form
        self.create_frame = ctk.CTkFrame(self.left_container)
        self.create_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.create_frame, text="Create Loan", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.user_id_entry = ctk.CTkEntry(self.create_frame, placeholder_text="User ID")
        self.user_id_entry.pack(pady=5, padx=10, fill="x")
        
        self.book_id_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Book ID")
        self.book_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.create_frame, text="Create Loan", command=self.create_loan).pack(pady=10)
        
        # Return Loan Form
        self.return_frame = ctk.CTkFrame(self.left_container)
        self.return_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.return_frame, text="Return Loan", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.loan_id_entry = ctk.CTkEntry(self.return_frame, placeholder_text="Loan ID")
        self.loan_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.return_frame, text="Return Book", command=self.return_loan).pack(pady=10)
        
        # Update Loan Form
        self.update_frame = ctk.CTkFrame(self.left_container)
        self.update_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.update_frame, text="Update Loan", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.loan_id_update_entry = ctk.CTkEntry(self.update_frame, placeholder_text="Loan ID")
        self.loan_id_update_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Load Loan", command=self.load_loan).pack(pady=5)
        
        self.user_id_update_entry = ctk.CTkEntry(self.update_frame, placeholder_text="User ID")
        self.user_id_update_entry.pack(pady=5, padx=10, fill="x")
        
        self.book_id_update_entry = ctk.CTkEntry(self.update_frame, placeholder_text="Book ID")
        self.book_id_update_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Update Loan", command=self.update_loan).pack(pady=10)
        
        # Delete Loan Form
        self.delete_frame = ctk.CTkFrame(self.left_container)
        self.delete_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.delete_frame, text="Delete Loan", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.loan_id_delete_entry = ctk.CTkEntry(self.delete_frame, placeholder_text="Loan ID")
        self.loan_id_delete_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.delete_frame, text="Delete Loan", command=self.delete_loan, 
                     fg_color="#FF5252", hover_color="#FF0000").pack(pady=10)
        
        # Search Forms
        self.search_loan_frame = ctk.CTkFrame(self.left_container)
        self.search_loan_frame.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.search_loan_frame, text="Search Loans", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.search_loan_id_entry = ctk.CTkEntry(self.search_loan_frame, placeholder_text="Loan ID")
        self.search_loan_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.search_loan_frame, text="Search", command=self.search_loans).pack(pady=5)
        ctk.CTkButton(self.search_loan_frame, text="Reset", command=self.reset_loan_search).pack(pady=5)
        
        self.search_user_frame = ctk.CTkFrame(self.left_container)
        self.search_user_frame.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.search_user_frame, text="Search Users", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.search_user_id_entry = ctk.CTkEntry(self.search_user_frame, placeholder_text="User ID")
        self.search_user_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.search_user_frame, text="Search", command=self.search_users).pack(pady=5)
        ctk.CTkButton(self.search_user_frame, text="Reset", command=self.reset_user_search).pack(pady=5)
        
        self.search_book_frame = ctk.CTkFrame(self.left_container)
        self.search_book_frame.grid(row=4, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.search_book_frame, text="Search Books", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.search_book_id_entry = ctk.CTkEntry(self.search_book_frame, placeholder_text="Book ID")
        self.search_book_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.search_book_frame, text="Search", command=self.search_books).pack(pady=5)
        ctk.CTkButton(self.search_book_frame, text="Reset", command=self.reset_book_search).pack(pady=5)
        
        # Right side - Tables
        self.table_container = ctk.CTkFrame(self)
        self.table_container.grid(row=0, column=1, padx=10, pady=10, sticky="nsew", rowspan=2)
        self.table_container.grid_rowconfigure(0, weight=1)
        self.table_container.grid_rowconfigure(1, weight=1)
        self.table_container.grid_columnconfigure(0, weight=1)
        
        # Loan Table
        self.loan_table_frame = ctk.CTkFrame(self.table_container)
        self.loan_table_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.loan_table_frame.grid_rowconfigure(0, weight=1)
        self.loan_table_frame.grid_columnconfigure(0, weight=1)
        
        columns = ('ID', 'User ID', 'Book ID', 'Borrow Date', 'Due Date', 'Return Date', 'Loan Date')
        self.loan_tree = ttk.Treeview(self.loan_table_frame, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            self.loan_tree.heading(col, text=col)
            self.loan_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar_loan = ttk.Scrollbar(self.loan_table_frame, orient="vertical", command=self.loan_tree.yview)
        self.loan_tree.configure(yscrollcommand=scrollbar_loan.set)
        
        # Pack the table and scrollbar
        self.loan_tree.pack(side="left", fill="both", expand=True)
        scrollbar_loan.pack(side="right", fill="y")
        
        # User and Book Info Table
        self.info_table_frame = ctk.CTkFrame(self.table_container)
        self.info_table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.info_table_frame.grid_rowconfigure(0, weight=1)
        self.info_table_frame.grid_columnconfigure(0, weight=1)
        
        # User Table
        self.user_tree = ttk.Treeview(self.info_table_frame, columns=('ID', 'Name'), show='headings')
        self.user_tree.heading('ID', text='User ID')
        self.user_tree.heading('Name', text='User Name')
        self.user_tree.column('ID', width=100)
        self.user_tree.column('Name', width=200)
        
        # Book Table
        self.book_tree = ttk.Treeview(self.info_table_frame, columns=('ID', 'Name'), show='headings')
        self.book_tree.heading('ID', text='Book ID')
        self.book_tree.heading('Name', text='Book Name')
        self.book_tree.column('ID', width=100)
        self.book_tree.column('Name', width=200)
        
        # Pack the tables
        self.user_tree.pack(side="left", fill="both", expand=True)
        self.book_tree.pack(side="right", fill="both", expand=True)
        
        # Show create form by default
        self.show_form("create")
        
        # Load initial data
        self.refresh_table()
        
    def show_form(self, form_type):
        # Hide all forms first
        self.create_frame.grid_remove()
        self.return_frame.grid_remove()
        self.update_frame.grid_remove()
        self.delete_frame.grid_remove()
        
        # Show the selected form
        if form_type == "create":
            self.create_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "return":
            self.return_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "update":
            self.update_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "delete":
            self.delete_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
    
    def create_loan(self):
        try:
            user_id = self.user_id_entry.get()
            book_id = self.book_id_entry.get()
            due_date = self.due_date_entry.get()
            
            if not all([user_id, book_id, due_date]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            borrow_date = date.today().strftime("%Y-%m-%d")
            
            cursor.execute("""
                INSERT INTO loans (user_id, book_id, borrow_date, due_date)
                VALUES (?, ?, ?, ?)
            """, (int(user_id), int(book_id), borrow_date, due_date))
            
            # Update book availability
            cursor.execute("""
                UPDATE books SET available = available - 1 WHERE id = ?
            """, (int(book_id),))
            
            conn.commit()
            conn.close()
            
            self.clear_create_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Loan created successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating loan: {e}")
    
    def return_loan(self):
        try:
            loan_id = self.loan_id_entry.get()
            if not loan_id:
                messagebox.showerror("Error", "Please enter a loan ID")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            return_date = date.today().strftime("%Y-%m-%d")
            
            cursor.execute("""
                UPDATE loans SET return_date = ? WHERE id = ?
            """, (return_date, int(loan_id)))
            
            # Update book availability
            cursor.execute("""
                SELECT book_id FROM loans WHERE id = ?
            """, (int(loan_id),))
            
            book_id = cursor.fetchone()[0]
            
            cursor.execute("""
                UPDATE books SET available = available + 1 WHERE id = ?
            """, (int(book_id),))
            
            conn.commit()
            conn.close()
            
            self.clear_return_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Book returned successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error returning book: {e}")
    
    def load_loan(self):
        try:
            loan_id = self.loan_id_update_entry.get()
            if not loan_id:
                messagebox.showerror("Error", "Please enter a loan ID")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT user_id, book_id
                FROM loans
                WHERE id = ?
            """, (int(loan_id),))
            
            loan = cursor.fetchone()
            conn.close()
            
            if loan:
                self.user_id_update_entry.delete(0, 'end')
                self.user_id_update_entry.insert(0, loan[0])
                self.book_id_update_entry.delete(0, 'end')
                self.book_id_update_entry.insert(0, loan[1])
            else:
                messagebox.showerror("Error", "Loan not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading loan: {e}")
    
    def update_loan(self):
        try:
            loan_id = self.loan_id_update_entry.get()
            user_id = self.user_id_update_entry.get()
            book_id = self.book_id_update_entry.get()
            
            if not all([loan_id, user_id, book_id]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE loans
                SET user_id = ?, book_id = ?
                WHERE id = ?
            """, (int(user_id), int(book_id), int(loan_id)))
            
            conn.commit()
            conn.close()
            
            self.clear_update_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Loan updated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error updating loan: {e}")
    
    def delete_loan(self):
        try:
            loan_id = self.loan_id_delete_entry.get()
            if not loan_id:
                messagebox.showerror("Error", "Please enter a loan ID")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            # Get book_id before deleting
            cursor.execute("""
                SELECT book_id FROM loans WHERE id = ?
            """, (int(loan_id),))
            
            book_id = cursor.fetchone()
            
            if book_id:
                # Update book availability
                cursor.execute("""
                    UPDATE books SET available = available + 1 WHERE id = ?
                """, (int(book_id[0]),))
            
            cursor.execute("""
                DELETE FROM loans WHERE id = ?
            """, (int(loan_id),))
            
            conn.commit()
            conn.close()
            
            self.clear_delete_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Loan deleted successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting loan: {e}")
    
    def refresh_table(self):
        # Clear the current tables
        for item in self.loan_tree.get_children():
            self.loan_tree.delete(item)
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
            
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            # Get loans
            cursor.execute("""
                SELECT id, user_id, book_id, borrow_date, due_date, return_date, loan_date
                FROM loans
            """)
            
            for row in cursor.fetchall():
                self.loan_tree.insert('', 'end', values=row)
            
            # Get users
            cursor.execute("""
                SELECT id, name FROM users
            """)
            
            for row in cursor.fetchall():
                self.user_tree.insert('', 'end', values=row)
            
            # Get books
            cursor.execute("""
                SELECT id, title FROM books
            """)
            
            for row in cursor.fetchall():
                self.book_tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing table: {e}")
    
    def clear_create_entries(self):
        self.user_id_entry.delete(0, 'end')
        self.book_id_entry.delete(0, 'end')
        self.due_date_entry.delete(0, 'end')
    
    def search_loans(self):
        loan_id = self.search_loan_id_entry.get()
        
        # Clear the current table
        for item in self.loan_tree.get_children():
            self.loan_tree.delete(item)
        
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT id, user_id, book_id, borrow_date, due_date, return_date, loan_date
                FROM loans
                WHERE 1=1
            """
            params = []
            
            if loan_id:
                query += " AND id = ?"
                params.append(int(loan_id))
            
            cursor.execute(query, params)
            
            for row in cursor.fetchall():
                self.loan_tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error searching loans: {e}")
    
    def search_users(self):
        user_id = self.search_user_id_entry.get()
        
        # Clear the current table
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT id, name FROM users WHERE 1=1
            """
            params = []
            
            if user_id:
                query += " AND id = ?"
                params.append(int(user_id))
            
            cursor.execute(query, params)
            
            for row in cursor.fetchall():
                self.user_tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error searching users: {e}")
    
    def search_books(self):
        book_id = self.search_book_id_entry.get()
        
        # Clear the current table
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT id, title FROM books WHERE 1=1
            """
            params = []
            
            if book_id:
                query += " AND id = ?"
                params.append(int(book_id))
            
            cursor.execute(query, params)
            
            for row in cursor.fetchall():
                self.book_tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error searching books: {e}")
    
    def reset_loan_search(self):
        self.search_loan_id_entry.delete(0, 'end')
        self.refresh_table()
    
    def reset_user_search(self):
        self.search_user_id_entry.delete(0, 'end')
        self.refresh_table()
    
    def reset_book_search(self):
        self.search_book_id_entry.delete(0, 'end')
        self.refresh_table()
    
    def clear_update_entries(self):
        self.loan_id_update_entry.delete(0, 'end')
        self.user_id_update_entry.delete(0, 'end')
        self.book_id_update_entry.delete(0, 'end')
    
    def clear_delete_entries(self):
        self.loan_id_delete_entry.delete(0, 'end')
    
    def clear_return_entries(self):
        self.loan_id_entry.delete(0, 'end')
