import customtkinter as ctk
from tkinter import ttk, messagebox
from src.database import create_connection

class FeePage(ctk.CTkFrame):
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
        
        ctk.CTkLabel(self.create_frame, text="Create Fee", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.loan_id_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Loan ID")
        self.loan_id_entry.pack(pady=5, padx=10, fill="x")
        
        self.amount_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Amount")
        self.amount_entry.pack(pady=5, padx=10, fill="x")
        
        self.paid_var = ctk.BooleanVar(value=False)
        self.paid_checkbox = ctk.CTkCheckBox(self.create_frame, text="Paid", variable=self.paid_var)
        self.paid_checkbox.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.create_frame, text="Create", command=self.create_fee).pack(pady=10)
        
        # Update Form
        self.update_frame = ctk.CTkFrame(self.left_container)
        self.update_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.update_frame, text="Update Fee", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.update_id_entry = ctk.CTkEntry(self.update_frame, placeholder_text="Fee ID")
        self.update_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Load Fee", command=self.load_fee).pack(pady=5)
        
        self.update_loan_id_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Loan ID")
        self.update_loan_id_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_amount_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Amount")
        self.update_amount_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_paid_var = ctk.BooleanVar()
        self.update_paid_checkbox = ctk.CTkCheckBox(self.update_frame, text="Paid", variable=self.update_paid_var)
        self.update_paid_checkbox.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Update", command=self.update_fee).pack(pady=10)
        
        # Delete Form
        self.delete_frame = ctk.CTkFrame(self.left_container)
        self.delete_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.delete_frame, text="Delete Fee", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.delete_id_entry = ctk.CTkEntry(self.delete_frame, placeholder_text="Fee ID")
        self.delete_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.delete_frame, text="Delete", command=self.delete_fee, 
                     fg_color="#FF5252", hover_color="#FF0000").pack(pady=10)

        # Search Form
        self.search_frame = ctk.CTkFrame(self.left_container)
        self.search_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.search_frame, text="Search Fees", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search by loan ID...")
        self.search_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.search_frame, text="Search", command=self.search_fees).pack(pady=10)
        ctk.CTkButton(self.search_frame, text="Show Unpaid", command=self.search_unpaid_fees).pack(pady=5)
        ctk.CTkButton(self.search_frame, text="Clear Search", command=self.clear_search).pack(pady=5)
        
        self.unpaid_fees_label = ctk.CTkLabel(self.search_frame, text="Total Unpaid Fees: 0", font=("Arial", 12))
        self.unpaid_fees_label.pack(pady=5)
        
        # Right side - Table
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        columns = ('ID', 'Loan ID', 'Amount', 'Paid')
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
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
        self.calculate_unpaid_fees()
        
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
    
    def create_fee(self):
        try:
            loan_id = self.loan_id_entry.get()
            amount = self.amount_entry.get()
            paid = int(self.paid_var.get())
            
            if not all([loan_id, amount]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO fees (loan_id, amount, paid)
                VALUES (?, ?, ?)
            """, (int(loan_id), float(amount), paid))
            
            conn.commit()
            conn.close()
            
            self.clear_create_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Fee created successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating fee: {e}")
    
    def load_fee(self):
        try:
            fee_id = self.update_id_entry.get()
            if not fee_id:
                messagebox.showerror("Error", "Please enter a fee ID")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT loan_id, amount, paid
                FROM fees
                WHERE id = ?
            """, (int(fee_id),))
            
            fee = cursor.fetchone()
            conn.close()
            
            if fee:
                self.update_loan_id_entry.delete(0, 'end')
                self.update_loan_id_entry.insert(0, fee[0])
                self.update_amount_entry.delete(0, 'end')
                self.update_amount_entry.insert(0, fee[1])
                self.update_paid_var.set(bool(fee[2]))
            else:
                messagebox.showerror("Error", "Fee not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading fee: {e}")
    
    def update_fee(self):
        try:
            fee_id = self.update_id_entry.get()
            new_loan_id = self.update_loan_id_entry.get()
            new_amount = self.update_amount_entry.get()
            new_paid = int(self.update_paid_var.get())
            
            if not all([fee_id, new_loan_id, new_amount]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE fees
                SET loan_id = ?, amount = ?, paid = ?
                WHERE id = ?
            """, (int(new_loan_id), float(new_amount), new_paid, int(fee_id)))
            
            conn.commit()
            conn.close()
            
            self.clear_update_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Fee updated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error updating fee: {e}")
    
    def delete_fee(self):
        try:
            fee_id = self.delete_id_entry.get()
            if not fee_id:
                messagebox.showerror("Error", "Please enter a fee ID")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM fees WHERE id = ?
            """, (int(fee_id),))
            
            conn.commit()
            conn.close()
            
            self.clear_delete_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Fee deleted successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting fee: {e}")
    
    def refresh_table(self):
        # Clear the current table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            # Get fees
            cursor.execute("""
                SELECT id, loan_id, amount, paid
                FROM fees
            """)
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing table: {e}")
    
    def clear_create_entries(self):
        self.loan_id_entry.delete(0, 'end')
        self.amount_entry.delete(0, 'end')
        self.paid_var.set(False)
    
    def clear_update_entries(self):
        self.update_id_entry.delete(0, 'end')
        self.update_loan_id_entry.delete(0, 'end')
        self.update_amount_entry.delete(0, 'end')
        self.update_paid_var.set(False)
    
    def clear_delete_entries(self):
        self.delete_id_entry.delete(0, 'end')

    def search_fees(self):
        try:
            search_term = self.search_entry.get().strip().lower()
            
            # Clear the current table
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            conn = create_connection()
            cursor = conn.cursor()
            
            # Get fees with filters
            query = """
                SELECT id, loan_id, amount, paid
                FROM fees
                WHERE CAST(loan_id AS TEXT) LIKE ? OR CAST(amount AS TEXT) LIKE ?
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern))
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error searching fees: {e}")
    
    def search_unpaid_fees(self):
        try:
            # Clear the current table
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            conn = create_connection()
            cursor = conn.cursor()
            
            # Get unpaid fees
            query = """
                SELECT id, loan_id, amount, paid
                FROM fees
                WHERE paid = 0
            """
            
            cursor.execute(query)
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error searching unpaid fees: {e}")
    
    def calculate_unpaid_fees(self):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT SUM(amount) FROM fees WHERE paid = 0")
            total_unpaid = cursor.fetchone()[0]
            
            conn.close()
            
            if total_unpaid is None:
                total_unpaid = 0
            
            self.unpaid_fees_label.configure(text=f"Total Unpaid Fees: {total_unpaid:.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating unpaid fees: {e}")
    
    def clear_search(self):
        self.search_entry.delete(0, 'end')
        self.refresh_table()
        self.calculate_unpaid_fees()
        self.calculate_unpaid_fees()
