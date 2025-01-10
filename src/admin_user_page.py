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
        
        # Create forms
        self.create_form = self.AdminUserCreateForm(self.left_container, self.controller, self)
        self.update_form = self.AdminUserUpdateForm(self.left_container, self.controller, self)
        self.delete_form = self.AdminUserDeleteForm(self.left_container, self.controller, self)
        self.search_form = self.AdminUserSearchForm(self.left_container, self.controller, self)
        
        # Right side - Table
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        columns = ('ID', 'Username', 'Password', 'Name', 'Role', 'Approved')
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
    
    class AdminUserCreateForm(ctk.CTkFrame):
        def __init__(self, parent, controller, page):
            super().__init__(parent)
            self.controller = controller
            self.page = page
            
            ctk.CTkLabel(self, text="Create Admin User", font=("Arial", 16, "bold")).pack(pady=5)
            
            self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
            self.username_entry.pack(pady=5, padx=10, fill="x")
            
            self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
            self.password_entry.pack(pady=5, padx=10, fill="x")
            
            self.name_entry = ctk.CTkEntry(self, placeholder_text="Name")
            self.name_entry.pack(pady=5, padx=10, fill="x")
            
            self.role_entry = ctk.CTkComboBox(self, values=["admin", "student", "teacher"])
            self.role_entry.pack(pady=5, padx=10, fill="x")
            
            self.approved_var = ctk.BooleanVar(value=False)
            self.approved_checkbox = ctk.CTkCheckBox(self, text="Approved", variable=self.approved_var)
            self.approved_checkbox.pack(pady=5, padx=10, fill="x")
            
            ctk.CTkButton(self, text="Create", command=self.create_admin_user).pack(pady=10)
        
        def create_admin_user(self):
            try:
                username = self.username_entry.get()
                password = self.password_entry.get()
                name = self.name_entry.get()
                role = self.role_entry.get()
                approved = int(self.approved_var.get())
                
                if not all([username, password, name, role]):
                    messagebox.showerror("Error", "All fields are required")
                    return
                
                conn = create_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO users (username, password, name, role, approved)
                    VALUES (?, ?, ?, ?, ?)
                """, (username, password, name, role, approved))
                
                conn.commit()
                conn.close()
                
                self.clear_entries()
                self.page.refresh_table()
                messagebox.showinfo("Success", "Admin user created successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error creating admin user: {e}")
        
        def clear_entries(self):
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
            self.role_entry.delete(0, 'end')
            self.approved_var.set(False)
    
    class AdminUserUpdateForm(ctk.CTkFrame):
        def __init__(self, parent, controller, page):
            super().__init__(parent)
            self.controller = controller
            self.page = page
            
            ctk.CTkLabel(self, text="Update Admin User", font=("Arial", 16, "bold")).pack(pady=5)
            
            self.id_entry = ctk.CTkEntry(self, placeholder_text="Admin User ID")
            self.id_entry.pack(pady=5, padx=10, fill="x")
            
            ctk.CTkButton(self, text="Load User", command=self.load_admin_user).pack(pady=5)
            
            self.username_entry = ctk.CTkEntry(self, placeholder_text="New Username")
            self.username_entry.pack(pady=5, padx=10, fill="x")
            
            self.password_entry = ctk.CTkEntry(self, placeholder_text="New Password", show="*")
            self.password_entry.pack(pady=5, padx=10, fill="x")
            
            self.name_entry = ctk.CTkEntry(self, placeholder_text="New Name")
            self.name_entry.pack(pady=5, padx=10, fill="x")
            
            self.role_entry = ctk.CTkComboBox(self, values=["admin", "student", "teacher"])
            self.role_entry.pack(pady=5, padx=10, fill="x")
            
            self.approved_var = ctk.BooleanVar()
            self.approved_checkbox = ctk.CTkCheckBox(self, text="Approved", variable=self.approved_var)
            self.approved_checkbox.pack(pady=5, padx=10, fill="x")
            
            ctk.CTkButton(self, text="Update", command=self.update_admin_user).pack(pady=10)
        
        def load_admin_user(self):
            try:
                admin_user_id = self.id_entry.get()
                if not admin_user_id:
                    messagebox.showerror("Error", "Please enter a admin user ID")
                    return
                
                conn = create_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT username, password, name, role, approved
                    FROM users
                    WHERE id = ?
                """, (int(admin_user_id),))
                
                admin_user = cursor.fetchone()
                conn.close()
                
                if admin_user:
                    self.username_entry.delete(0, 'end')
                    self.username_entry.insert(0, admin_user[0])
                    self.password_entry.delete(0, 'end')
                    self.password_entry.insert(0, admin_user[1])
                    self.name_entry.delete(0, 'end')
                    self.name_entry.insert(0, admin_user[2])
                    self.role_entry.delete(0, 'end')
                    self.role_entry.insert(0, admin_user[3])
                    self.approved_var.set(bool(admin_user[4]))
                else:
                    messagebox.showerror("Error", "Admin user not found")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error loading admin user: {e}")
        
        def update_admin_user(self):
            try:
                admin_user_id = self.id_entry.get()
                new_username = self.username_entry.get()
                new_password = self.password_entry.get()
                new_name = self.name_entry.get()
                new_role = self.role_entry.get()
                new_approved = int(self.approved_var.get())
                
                if not all([admin_user_id, new_username, new_password, new_name, new_role]):
                    messagebox.showerror("Error", "All fields are required")
                    return
                
                conn = create_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE users
                    SET username = ?, password = ?, name = ?, role = ?, approved = ?
                    WHERE id = ?
                """, (new_username, new_password, new_name, new_role, new_approved, int(admin_user_id)))
                
                conn.commit()
                conn.close()
                
                self.clear_entries()
                self.page.refresh_table()
                messagebox.showinfo("Success", "Admin user updated successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error updating admin user: {e}")
        
        def clear_entries(self):
            self.id_entry.delete(0, 'end')
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
            self.role_entry.delete(0, 'end')
            self.approved_var.set(False)
    
    class AdminUserDeleteForm(ctk.CTkFrame):
        def __init__(self, parent, controller, page):
            super().__init__(parent)
            self.controller = controller
            self.page = page
            
            ctk.CTkLabel(self, text="Delete Admin User", font=("Arial", 16, "bold")).pack(pady=5)
            
            self.id_entry = ctk.CTkEntry(self, placeholder_text="Admin User ID")
            self.id_entry.pack(pady=5, padx=10, fill="x")
            
            ctk.CTkButton(self, text="Delete", command=self.delete_admin_user, 
                         fg_color="#FF5252", hover_color="#FF0000").pack(pady=10)
        
        def delete_admin_user(self):
            try:
                admin_user_id = self.id_entry.get()
                if not admin_user_id:
                    messagebox.showerror("Error", "Please enter a admin user ID")
                    return
                
                conn = create_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    DELETE FROM users WHERE id = ?
                """, (int(admin_user_id),))
                
                conn.commit()
                conn.close()
                
                self.clear_entries()
                self.page.refresh_table()
                messagebox.showinfo("Success", "Admin user deleted successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting admin user: {e}")
        
        def clear_entries(self):
            self.id_entry.delete(0, 'end')
    
    class AdminUserSearchForm(ctk.CTkFrame):
        def __init__(self, parent, controller, page):
            super().__init__(parent)
            self.controller = controller
            self.page = page
            
            ctk.CTkLabel(self, text="Search Admin Users", font=("Arial", 16, "bold")).pack(pady=5)
            
            self.search_entry = ctk.CTkEntry(self, placeholder_text="Search by username...")
            self.search_entry.pack(pady=5, padx=10, fill="x")
            
            ctk.CTkButton(self, text="Search", command=self.search_admin_users).pack(pady=10)
            ctk.CTkButton(self, text="Clear Search", command=self.clear_search).pack(pady=5)
        
        def search_admin_users(self):
            try:
                search_term = self.search_entry.get().strip().lower()
                
                # Clear the current table
                for item in self.page.tree.get_children():
                    self.page.tree.delete(item)
                    
                conn = create_connection()
                cursor = conn.cursor()
                
                # Get admin users with filters
                query = """
                    SELECT id, username, password, name, role, approved
                    FROM users
                    WHERE LOWER(username) LIKE ? OR LOWER(password) LIKE ? OR LOWER(name) LIKE ? OR LOWER(role) LIKE ?
                """
                
                search_pattern = f"%{search_term}%"
                cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
                
                for row in cursor.fetchall():
                    self.page.tree.insert('', 'end', values=row)
                    
                conn.close()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error searching admin users: {e}")
        
        def clear_search(self):
            self.search_entry.delete(0, 'end')
            self.page.refresh_table()
            
    def show_form(self, form_type):
        # Hide all forms first
        self.create_form.grid_remove()
        self.update_form.grid_remove()
        self.delete_form.grid_remove()
        self.search_form.grid_remove()
        
        # Show the selected form
        if form_type == "create":
            self.create_form.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "update":
            self.update_form.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "delete":
            self.delete_form.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "search":
            self.search_form.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
    
    def refresh_table(self):
        # Clear the current table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            # Get admin users
            cursor.execute("""
                SELECT id, username, password, name, role, approved
                FROM users
            """)
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing table: {e}")
