import customtkinter as ctk
from tkinter import messagebox
from database import create_connection

class AdminUserDeleteForm(ctk.CTkFrame):
    def __init__(self, parent, controller, master_page):
        super().__init__(parent)
        self.controller = controller
        self.master_page = master_page
        
        ctk.CTkLabel(self, text="Delete Admin User", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.delete_id_entry = ctk.CTkEntry(self, placeholder_text="Admin User ID")
        self.delete_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self, text="Delete", command=self.delete_admin_user, 
                     fg_color="#FF5252", hover_color="#FF0000").pack(pady=10)
    
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
            
            self.clear_entries()
            self.master_page.refresh_table()
            messagebox.showinfo("Success", "Admin User deleted successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting admin user: {e}")
            
    def clear_entries(self):
        self.delete_id_entry.delete(0, 'end')
```

src\admin_user_search_form.py
```python
<<<<<<< SEARCH
