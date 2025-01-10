import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk

class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Library Management System")
        self.geometry("800x600")

        # Configure grid layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_label = ctk.CTkLabel(self.navigation_frame, text="  Navigation Menu  ",
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

        self.exit_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Exit",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   command=self.destroy)
        self.exit_button.grid(row=4, column=0, sticky="ew")

        # Create pages
        self.home_page = ctk.CTkFrame(self)
        self.home_page.grid(row=0, column=1, sticky="nsew")
        self.home_label = ctk.CTkLabel(self.home_page, text="Welcome to the Library Management System")
        self.home_label.pack(pady=20)

        # Create admin page
        self.admin_page = ctk.CTkFrame(self)
        self.admin_label = ctk.CTkLabel(self.admin_page, text="Admin Page")
        self.admin_label.pack(pady=20)

        # Create author page
        self.author_page = ctk.CTkFrame(self)
        self.author_label = ctk.CTkLabel(self.author_page, text="Author Page")
        self.author_label.pack(pady=20)
        
        self.show_home_page()

    def show_home_page(self):
        # Hide all pages
        self.home_page.grid_remove()
        self.admin_page.grid_remove()
        self.author_page.grid_remove()
        # Show home page
        self.home_page.grid(row=0, column=1, sticky="nsew")

    def show_admin_page(self):
        # Hide all pages
        self.home_page.grid_remove()
        self.admin_page.grid_remove()
        self.author_page.grid_remove()
        # Show admin page
        self.admin_page.grid(row=0, column=1, sticky="nsew")

    def show_author_page(self):
        # Hide all pages
        self.home_page.grid_remove()
        self.admin_page.grid_remove()
        self.author_page.grid_remove()
        # Show author page
        self.author_page.grid(row=0, column=1, sticky="nsew")

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
