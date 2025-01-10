import customtkinter as ctk

class OtherPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="This is the Other Page")
        label.pack(pady=20)
