import customtkinter as ctk

class AuthorPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.label = ctk.CTkLabel(self, text="Author Management Page")
        self.label.pack(pady=20)
