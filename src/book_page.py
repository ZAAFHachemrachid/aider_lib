import customtkinter as ctk

class BookPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.label = ctk.CTkLabel(self, text="Book Management Page")
        self.label.pack(pady=20)
