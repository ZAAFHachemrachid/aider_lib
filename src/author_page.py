import customtkinter as ctk
from tkinter import ttk, messagebox
from database import create_connection
from database import create_connection

class AuthorPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Configure grid
        self.grid_columnconfigure(0, weight=2)  # Left side (forms)
        self.grid_columnconfigure(1, weight=3)  # Right side (table)
        self.grid_rowconfigure(0, weight=1)  # Make row expandable
        
        # Left side container
        self.left_container = ctk.CTkFrame(self)
        self.left_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.left_container.grid_rowconfigure(1, weight=1)  # Make forms row expandable
        self.left_container.grid_columnconfigure(0, weight=1)
        
        # Buttons Frame for switching forms
        self.switch_buttons_frame = ctk.CTkFrame(self.left_container)
        self.switch_buttons_frame.grid(row=0, column=0, pady=5, padx=10, sticky="ew")
        self.switch_buttons_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        # Create buttons to switch between forms
        ctk.CTkButton(self.switch_buttons_frame, text="Create Form", command=lambda: self.show_form("create")).grid(row=0, column=0, padx=2, sticky="ew")
        ctk.CTkButton(self.switch_buttons_frame, text="Update Form", command=lambda: self.show_form("update")).grid(row=0, column=1, padx=2, sticky="ew")
        ctk.CTkButton(self.switch_buttons_frame, text="Delete Form", command=lambda: self.show_form("delete")).grid(row=0, column=2, padx=2, sticky="ew")
        ctk.CTkButton(self.switch_buttons_frame, text="Search Form", command=lambda: self.show_form("search")).grid(row=0, column=3, padx=2, sticky="ew")
        
        # Create Form
        self.create_frame = ctk.CTkFrame(self.left_container)
        self.create_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.create_frame, text="Create Author", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.name_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Name")
        self.name_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.create_frame, text="Create", command=self.create_author).pack(pady=10)
        
        # Update Form
        self.update_frame = ctk.CTkFrame(self.left_container)
        self.update_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.update_frame, text="Update Author", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.update_id_entry = ctk.CTkEntry(self.update_frame, placeholder_text="Author ID")
        self.update_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Load Author", command=self.load_author).pack(pady=5)
        
        self.update_name_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Name")
        self.update_name_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Update", command=self.update_author).pack(pady=10)
        
        # Delete Form
        self.delete_frame = ctk.CTkFrame(self.left_container)
        self.delete_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.delete_frame, text="Delete Author", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.delete_id_entry = ctk.CTkEntry(self.delete_frame, placeholder_text="Author ID")
        self.delete_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.delete_frame, text="Delete", command=self.delete_author, 
                     fg_color="#FF5252", hover_color="#FF0000").pack(pady=10)

        # Search Form
        self.search_frame = ctk.CTkFrame(self.left_container)
        self.search_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.search_frame, text="Search Authors", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search by name...")
        self.search_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.search_frame, text="Search", command=self.search_authors).pack(pady=10)
        ctk.CTkButton(self.search_frame, text="Clear Search", command=self.clear_search).pack(pady=5)
        
        # Right side - Table
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        columns = ('ID', 'Name')
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the table and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Show create form by default
        self.show_form("create")
        
        # Load initial data
        self.refresh_table()
        
    def show_form(self, form_type):
        # Hide all forms first
        self.create_frame.grid_remove()
        self.update_frame.grid_remove()
        self.delete_frame.grid_remove()
        self.search_frame.grid_remove()
        
        # Show the selected form
        if form_type == "create":
            self.create_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "update":
            self.update_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "delete":
            self.delete_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "search":
            self.search_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
    
    def create_author(self):
        try:
            name = self.name_entry.get()
            
            if not name:
                messagebox.showerror("Error", "All fields are required")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO authors (name)
                VALUES (?)
            """, (name,))
            
            conn.commit()
            conn.close()
            
            self.clear_create_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Author created successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating author: {e}")
    
    def load_author(self):
        try:
            author_id = self.update_id_entry.get()
            if not author_id:
                messagebox.showerror("Error", "Please enter a author ID")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name
                FROM authors
                WHERE id = ?
            """, (int(author_id),))
            
            author = cursor.fetchone()
            conn.close()
            
            if author:
                self.update_name_entry.delete(0, 'end')
                self.update_name_entry.insert(0, author[0])
            else:
                messagebox.showerror("Error", "Author not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading author: {e}")
    
    def update_author(self):
        try:
            author_id = self.update_id_entry.get()
            new_name = self.update_name_entry.get()
            
            if not all([author_id, new_name]):
                 messagebox.showerror("Error", "All fields are required")
                 return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE authors
                SET name = ?
                WHERE id = ?
            """, (new_name, int(author_id)))
            
            conn.commit()
            conn.close()
            
            self.clear_update_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Author updated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error updating author: {e}")
    
    def delete_author(self):
        try:
            author_id = self.delete_id_entry.get()
            if not author_id:
                messagebox.showerror("Error", "Please enter a author ID")
                return
            
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM authors WHERE id = ?
            """, (int(author_id),))
            
            conn.commit()
            conn.close()
            
            self.delete_id_entry.delete(0, 'end')
            self.refresh_table()
            messagebox.showinfo("Success", "Author deleted successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting author: {e}")
    
    def refresh_table(self):
        # Clear the current table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            # Get authors
            cursor.execute("""
                SELECT id, name
                FROM authors
            """)
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing table: {e}")
    
    def clear_create_entries(self):
        self.name_entry.delete(0, 'end')
    
    def clear_update_entries(self):
        self.update_id_entry.delete(0, 'end')
        self.update_name_entry.delete(0, 'end')

    def search_authors(self):
        try:
            search_term = self.search_entry.get().strip().lower()
            
            # Clear the current table
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            conn = create_connection()
            cursor = conn.cursor()
            
            # Get authors with filters
            query = """
                SELECT id, name
                FROM authors
                WHERE LOWER(name) LIKE ?
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern,))
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error searching authors: {e}")
            
    def clear_search(self):
        self.search_entry.delete(0, 'end')
        self.refresh_table()
