import customtkinter as ctk
from tkinter import ttk, messagebox
from database import create_connection

class AdminUserPage(ctk.CTkFrame):
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
        
        ctk.CTkLabel(self.create_frame, text="Create Admin User", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.username_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Username")
        self.username_entry.pack(pady=5, padx=10, fill="x")
        
        self.password_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.create_frame, text="Create", command=self.create_admin_user).pack(pady=10)
        
        # Update Form
        self.update_frame = ctk.CTkFrame(self.left_container)
        self.update_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.update_frame, text="Update Admin User", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.update_id_entry = ctk.CTkEntry(self.update_frame, placeholder_text="Admin User ID")
        self.update_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Load Admin User", command=self.load_admin_user).pack(pady=5)
        
        self.update_username_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Username")
        self.update_username_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_password_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Password", show="*")
        self.update_password_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Update", command=self.update_admin_user).pack(pady=10)
        
        # Delete Form
        self.delete_frame = ctk.CTkFrame(self.left_container)
        self.delete_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.delete_frame, text="Delete Admin User", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.delete_id_entry = ctk.CTkEntry(self.delete_frame, placeholder_text="Admin User ID")
        self.delete_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.delete_frame, text="Delete", command=self.delete_admin_user, 
                     fg_color="#FF5252", hover_color="#FF0000").pack(pady=10)

        # Search Form
        self.search_frame = ctk.CTkFrame(self.left_container)
        self.search_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.search_frame, text="Search Admin Users", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search by username...")
        self.search_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.search_frame, text="Search", command=self.search_admin_users).pack(pady=10)
        ctk.CTkButton(self.search_frame, text="Clear Search", command=self.clear_search).pack(pady=5)
        
        # Right side - Table
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        columns = ('ID', 'Username', 'Password')
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
    
    def create_admin_user(self):
        try:
            username = self.username_entry.get()
            password = self.password_entry.get()
            
            if not all([username, password]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO admin_users (username, password)
                VALUES (?, ?)
            """, (username, password))
            
            conn.commit()
            conn.close()
            
            self.clear_create_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Admin User created successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating admin user: {e}")
    
    def load_admin_user(self):
        try:
            admin_user_id = self.update_id_entry.get()
            if not admin_user_id:
                messagebox.showerror("Error", "Please enter a admin user ID")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT username, password
                FROM admin_users
                WHERE id = ?
            """, (int(admin_user_id),))
            
            admin_user = cursor.fetchone()
            conn.close()
            
            if admin_user:
                self.update_username_entry.delete(0, 'end')
                self.update_username_entry.insert(0, admin_user[0])
                self.update_password_entry.delete(0, 'end')
                self.update_password_entry.insert(0, admin_user[1])
            else:
                messagebox.showerror("Error", "Admin User not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading admin user: {e}")
    
    def update_admin_user(self):
        try:
            admin_user_id = self.update_id_entry.get()
            new_username = self.update_username_entry.get()
            new_password = self.update_password_entry.get()
            
            if not all([admin_user_id, new_username, new_password]):
                 messagebox.showerror("Error", "All fields are required")
                 return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE admin_users
                SET username = ?, password = ?
                WHERE id = ?
            """, (new_username, new_password, int(admin_user_id)))
            
            conn.commit()
            conn.close()
            
            self.clear_update_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Admin User updated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error updating admin user: {e}")
    
    def delete_admin_user(self):
        try:
            admin_user_id = self.delete_id_entry.get()
            if not admin_user_id:
                messagebox.showerror("Error", "Please enter a admin user ID")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM admin_users WHERE id = ?
            """, (int(admin_user_id),))
            
            conn.commit()
            conn.close()
            
            self.delete_id_entry.delete(0, 'end')
            self.refresh_table()
            messagebox.showinfo("Success", "Admin User deleted successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting admin user: {e}")
    
    def refresh_table(self):
        # Clear the current table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            # Get admin users
            cursor.execute("""
                SELECT id, username, password
                FROM admin_users
            """)
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing table: {e}")
    
    def clear_create_entries(self):
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
    
    def clear_update_entries(self):
        self.update_id_entry.delete(0, 'end')
        self.update_username_entry.delete(0, 'end')
        self.update_password_entry.delete(0, 'end')

    def search_admin_users(self):
        try:
            search_term = self.search_entry.get().strip().lower()
            
            # Clear the current table
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            conn = create_connection()
            cursor = conn.cursor()
            
            # Get admin users with filters
            query = """
                SELECT id, username, password
                FROM admin_users
                WHERE LOWER(username) LIKE ?
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern,))
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error searching admin users: {e}")
            
    def clear_search(self):
        self.search_entry.delete(0, 'end')
        self.refresh_table()
