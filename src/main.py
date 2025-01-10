import tkinter as tk
import customtkinter as ctk

class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Library Management System")
        self.geometry("800x600")

        self.label = ctk.CTkLabel(self, text="Welcome to the Library Management System")
        self.label.pack(pady=20)

        self.button = ctk.CTkButton(self, text="Exit", command=self.destroy)
        self.button.pack(pady=20)


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
