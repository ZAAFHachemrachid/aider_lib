import customtkinter as ctk
from tkinter import messagebox
from database import create_connection

class AdminUserCreateForm(ctk.CTkFrame):
    def __init__(self, parent, controller, master_page):
        super().__init__(parent)
        self.controller = controller
        self.master_page = master_page
        
        ctk.CTkLabel(self, text="Create Admin User", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=5, padx=10, fill="x")
        
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self, text="Create", command=self.create_admin_user).pack(pady=10)
    
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
            
            self.clear_entries()
            self.master_page.refresh_table()
            messagebox.showinfo("Success", "Admin User created successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating admin user: {e}")
            
    def clear_entries(self):
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
```

src\admin_user_update_form.py
```python
<<<<<<< SEARCH
