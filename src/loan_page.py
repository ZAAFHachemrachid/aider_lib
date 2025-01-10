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
        self.switch_buttons_frame.grid_columnconfigure((0,1), weight=1)
        
        # Create buttons to switch between forms
        ctk.CTkButton(self.switch_buttons_frame, text="Create Loan", command=lambda: self.show_form("create")).grid(row=0, column=0, padx=2, sticky="ew")
        ctk.CTkButton(self.switch_buttons_frame, text="Return Loan", command=lambda: self.show_form("return")).grid(row=0, column=1, padx=2, sticky="ew")
        
        # Create Loan Form
        self.create_frame = ctk.CTkFrame(self.left_container)
        self.create_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.create_frame, text="Create Loan", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.user_id_entry = ctk.CTkEntry(self.create_frame, placeholder_text="User ID")
        self.user_id_entry.pack(pady=5, padx=10, fill="x")
        
        self.book_id_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Book ID")
        self.book_id_entry.pack(pady=5, padx=10, fill="x")
        
        self.due_date_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Due Date (YYYY-MM-DD)")
        self.due_date_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.create_frame, text="Create Loan", command=self.create_loan).pack(pady=10)
        
        # Return Loan Form
        self.return_frame = ctk.CTkFrame(self.left_container)
        self.return_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.return_frame, text="Return Loan", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.loan_id_entry = ctk.CTkEntry(self.return_frame, placeholder_text="Loan ID")
        self.loan_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.return_frame, text="Return Book", command=self.return_loan).pack(pady=10)
        
        # Right side - Table
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        columns = ('ID', 'User ID', 'Book ID', 'Loan Date', 'Due Date', 'Return Date')
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
        self.return_frame.grid_remove()
        
        # Show the selected form
        if form_type == "create":
            self.create_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "return":
            self.return_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
    
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
            
            loan_date = date.today().strftime("%Y-%m-%d")
            
            cursor.execute("""
                INSERT INTO loans (user_id, book_id, loan_date, due_date)
                VALUES (?, ?, ?, ?)
            """, (int(user_id), int(book_id), loan_date, due_date))
            
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
    
    def refresh_table(self):
        # Clear the current table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            # Get loans
            cursor.execute("""
                SELECT id, user_id, book_id, loan_date, due_date, return_date
                FROM loans
            """)
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing table: {e}")
    
    def clear_create_entries(self):
        self.user_id_entry.delete(0, 'end')
        self.book_id_entry.delete(0, 'end')
        self.due_date_entry.delete(0, 'end')
    
    def clear_return_entries(self):
        self.loan_id_entry.delete(0, 'end')
