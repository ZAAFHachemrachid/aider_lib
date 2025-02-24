import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from customtkinter import CTkScrollableFrame
from src.author_page import AuthorPage
from src.database import create_connection
from tkinter import messagebox
from src.category_page import CategoryPage
from src.admin_user_page import AdminUserPage
from src.book_page import BookPage
from src.loan_page import LoanPage
from src.fee_page import FeePage
from src.login_page import LoginPage
from src.signup_page import SignupPage


class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Library Management System")
        self.geometry("800x600")
        self.bg_color = "#000000"

        # Configure grid layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(8, weight=1)

        self.navigation_label = ctk.CTkLabel(self.navigation_frame, text="  Menu  ",
                                                 compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   command=self.show_home_page)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.admin_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Admin",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   command=self.show_admin_page)
        self.admin_button.grid(row=2, column=0, sticky="ew")

        self.author_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Author",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   command=self.show_author_page)
        self.author_button.grid(row=3, column=0, sticky="ew")
        
        self.category_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Category",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   command=self.show_category_page)
        self.category_button.grid(row=4, column=0, sticky="ew")
        
        self.book_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Book",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   command=self.show_book_page)
        self.book_button.grid(row=5, column=0, sticky="ew")
        
        self.loan_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Loan",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   command=self.show_loan_page)
        self.loan_button.grid(row=6, column=0, sticky="ew")
        
        self.fee_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Fee",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   command=self.show_fee_page)
        self.fee_button.grid(row=7, column=0, sticky="ew")
        
        self.exit_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Exit",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   command=self.destroy)
        self.exit_button.grid(row=8, column=0, sticky="ew")

        # Create pages
        self.home_page = CTkScrollableFrame(self)
        self.home_label = ctk.CTkLabel(self.home_page, text="Welcome to the Library Management System", font=("Arial", 20, "bold"))
        self.home_label.grid(row=0, column=0, columnspan=3, pady=20, sticky="ew")
        
        # Labels for counts
        self.active_loans_label = ctk.CTkLabel(self.home_page, text="Active Loans: 0", fg_color=self.bg_color)
        self.active_loans_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.total_books_label = ctk.CTkLabel(self.home_page, text="Total Books: 0", fg_color=self.bg_color)
        self.total_books_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        self.available_books_label = ctk.CTkLabel(self.home_page, text="Available Books: 0", fg_color=self.bg_color)
        self.available_books_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        # Create admin page
        self.admin_page = AdminUserPage(self, self)

        # Create author page
        self.author_page = AuthorPage(self, self)
        
        # Create category page
        self.category_page = CategoryPage(self, self)
        
        # Create book page
        self.book_page = BookPage(self, self)
        
        # Create loan page
        self.loan_page = LoanPage(self, self)
        
        # Create fee page
        self.fee_page = FeePage(self, self)
        
        # Create login frame
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.grid(row=0, column=1, sticky="nsew")
        
        self.login_page = LoginPage(self.login_frame, self)
        self.signup_page = SignupPage(self.login_frame, self)
        self.user = None
        
        self.show_login_page()

    def show_home_page(self):
        # Hide all pages
        self.home_page.grid_remove()
        self.admin_page.grid_remove()
        self.author_page.grid_remove()
        self.category_page.grid_remove()
        self.book_page.grid_remove()
        self.fee_page.grid_remove()
        self.login_frame.grid_remove()
        # Show home page
        if self.user:
            self.home_page.grid(row=0, column=1, sticky="nsew")
            self.update_home_page_labels()
        else:
            self.show_login_page()
            
    def update_home_page_labels(self):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            # Get active loans count
            cursor.execute("SELECT COUNT(*) FROM loans WHERE return_date IS NULL")
            active_loans = cursor.fetchone()[0]
            self.active_loans_label.configure(text=f"Active Loans: {active_loans}")
            
            # Get total books count
            cursor.execute("SELECT COUNT(*) FROM books")
            total_books = cursor.fetchone()[0]
            self.total_books_label.configure(text=f"Total Books: {total_books}")
            
            # Get available books count
            cursor.execute("SELECT SUM(available) FROM books")
            available_books = cursor.fetchone()[0]
            self.available_books_label.configure(text=f"Available Books: {available_books}")
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error updating home page labels: {e}")

    def show_admin_page(self):
        # Hide all pages
        self.home_page.grid_remove()
        self.admin_page.grid_remove()
        self.author_page.grid_remove()
        self.category_page.grid_remove()
        self.book_page.grid_remove()
        self.login_frame.grid_remove()
        # Show admin page
        if self.user and self.user[4] == 'admin':
            self.admin_page.grid(row=0, column=1, sticky="nsew")
        else:
            self.show_login_page()

    def show_author_page(self):
        # Hide all pages
        self.home_page.grid_remove()
        self.admin_page.grid_remove()
        self.author_page.grid_remove()
        self.category_page.grid_remove()
        self.book_page.grid_remove()
        self.login_frame.grid_remove()
        # Show author page
        if self.user:
            self.author_page.grid(row=0, column=1, sticky="nsew")
        else:
            self.show_login_page()
        
    def show_category_page(self):
        # Hide all pages
        self.home_page.grid_remove()
        self.admin_page.grid_remove()
        self.author_page.grid_remove()
        self.category_page.grid_remove()
        self.book_page.grid_remove()
        self.login_frame.grid_remove()
        # Show category page
        if self.user:
            self.category_page.grid(row=0, column=1, sticky="nsew")
        else:
            self.show_login_page()
        
    def show_book_page(self):
        # Hide all pages
        self.home_page.grid_remove()
        self.admin_page.grid_remove()
        self.author_page.grid_remove()
        self.category_page.grid_remove()
        self.book_page.grid_remove()
        self.loan_page.grid_remove()
        self.login_frame.grid_remove()
        self.fee_page.grid_remove()
        # Show book page
        if self.user:
            self.book_page.grid(row=0, column=1, sticky="nsew")
        else:
            self.show_login_page()
        
    def show_loan_page(self):
        # Hide all pages
        self.home_page.grid_remove()
        self.admin_page.grid_remove()
        self.author_page.grid_remove()
        self.category_page.grid_remove()
        self.book_page.grid_remove()
        self.login_frame.grid_remove()
        self.fee_page.grid_remove()
        # Show loan page
        if self.user:
            self.loan_page.grid(row=0, column=1, sticky="nsew")
        else:
            self.show_login_page()
    
    def show_fee_page(self):
        # Hide all pages
        self.home_page.grid_remove()
        self.admin_page.grid_remove()
        self.author_page.grid_remove()
        self.category_page.grid_remove()
        self.book_page.grid_remove()
        self.loan_page.grid_remove()
        self.login_frame.grid_remove()
        # Show fee page
        if self.user:
            self.fee_page.grid(row=0, column=1, sticky="nsew")
        else:
            self.show_login_page()
    
    def show_login_page(self):
        # Hide all pages
        self.home_page.grid_remove()
        self.admin_page.grid_remove()
        self.author_page.grid_remove()
        self.category_page.grid_remove()
        self.book_page.grid_remove()
        self.loan_page.grid_remove()
        self.fee_page.grid_remove()
        # Show login page
        self.login_frame.grid(row=0, column=1, sticky="nsew")
        self.login_page.grid(row=0, column=0, sticky="nsew")
        self.signup_page.grid(row=0, column=0, sticky="nsew")
        self.signup_page.grid_remove()

    def show_signup_page(self):
        self.login_page.grid_remove()
        self.signup_page.grid(row=0, column=0, sticky="nsew")
        
    def show_login_page(self):
        self.signup_page.grid_remove()
        self.login_page.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
