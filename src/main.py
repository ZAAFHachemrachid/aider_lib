import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from src.pages import OtherPage

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
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_label = ctk.CTkLabel(self.navigation_frame, text="  Navigation Menu  ",
                                                 compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   command=self.show_home_page)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.other_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Other Page",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   command=self.show_other_page)
        self.other_button.grid(row=2, column=0, sticky="ew")

        self.exit_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Exit",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   command=self.destroy)
        self.exit_button.grid(row=3, column=0, sticky="ew")

        # Create pages
        self.home_page = ctk.CTkFrame(self)
        self.home_page.grid(row=0, column=1, sticky="nsew")
        self.home_label = ctk.CTkLabel(self.home_page, text="Welcome to the Library Management System")
        self.home_label.pack(pady=20)

        self.other_page = OtherPage(self, self)
        
        self.show_home_page()

    def show_home_page(self):
        self.other_page.grid_forget()
        self.home_page.grid(row=0, column=1, sticky="nsew")

    def show_other_page(self):
        self.home_page.grid_forget()
        self.other_page.grid(row=0, column=1, sticky="nsew")


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
