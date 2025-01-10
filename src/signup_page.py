import customtkinter as ctk
from tkinter import messagebox
from src.database import create_connection

class SignupPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Sign Up", font=("Arial", 24, "bold"))
        self.label.pack(pady=40)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10, padx=20, fill="x")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10, padx=20, fill="x")
        
        self.role_entry = ctk.CTkEntry(self, placeholder_text="Role")
        self.role_entry.pack(pady=10, padx=20, fill="x")

        self.signup_button = ctk.CTkButton(self, text="Sign Up", command=self.signup)
        self.signup_button.pack(pady=20)
        
        self.login_button = ctk.CTkButton(self, text="Login", command=self.show_login_page)
        self.login_button.pack(pady=10)
        
        self.error_label = ctk.CTkLabel(self, text="", fg_color="transparent", text_color="red")
        self.error_label.pack()

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()

        if not username or not password or not role:
            self.error_label.configure(text="Please enter all fields.")
            return
        
        if role not in ['admin', 'user']:
            self.error_label.configure(text="Invalid role. Must be 'admin' or 'user'.")
            return

        conn = create_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "User created successfully.")
            self.controller.show_login_page()
        except Exception as e:
            self.error_label.configure(text=f"Error creating user: {e}")
            conn.close()
            
    def show_login_page(self):
        self.controller.show_login_page()
