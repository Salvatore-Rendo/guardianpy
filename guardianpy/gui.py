import tkinter as tk
from tkinter import ttk, messagebox
from guardianpy.database import (
    register_user,
    authenticate_user,
    store_password,
    retrieve_password,
)
from guardianpy.encryption import encrypt_password, decrypt_password, set_master_password, get_master_password
import guardianpy.generator as generator

class PasswordEntry(tk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_password = False

    def toggle_password_visibility(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.config(show="")
        else:
            self.config(show="*")

show_password_var = None  # Initialize show_password_var as a global variable

def run_gui():
    def register():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
        else:
            if register_user(username, password):
                messagebox.showinfo("Success", "Registration successful.")
            else:
                messagebox.showerror("Error", "Registration failed. Username already exists.")

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
        else:
            user_id = authenticate_user(username, password)
            if user_id is not None:
                set_master_password(password)  # Set the master password
                logged_in(user_id)
            else:
                messagebox.showerror("Error", "Authentication failed. Please try again.")


    def toggle_password_visibility():
        password_entry.toggle_password_visibility()

    def logged_in(user_id):
        login_window.destroy()
        logged_in_window = tk.Tk()
        logged_in_window.title("Password Manager")

        def store():
            website = website_entry.get()
            email = email_entry.get()
            password = password_entry_logged_in.get()  # Use the logged-in password entry
            master_password = get_master_password()  # Get the master password
            if not website or not email or not password:
                messagebox.showerror("Error", "Please enter website, email, and password.")
            else:
                store_password(user_id, website, email, password, master_password)  # Pass the master_password
                messagebox.showinfo("Success", "Password stored.")

        def retrieve():
            website = website_entry.get()
            master_password = get_master_password()  
            password = retrieve_password(user_id, website, master_password)  # Pass the master_password
            if password:
                messagebox.showinfo("Password", f"Password for {website}: {password}")
            else:
                messagebox.showerror("Error", "Password not found.")


        def generate_password():
            length = int(length_var.get())
            include_numbers = numbers_var.get() == 1
            include_special_chars = special_chars_var.get() == 1

            if length >= 12:
                generated_password = generator.generate_password(length, include_numbers, include_special_chars)
                password_entry_logged_in.delete(0, tk.END)
                password_entry_logged_in.insert(0, generated_password)  # Use the logged-in password entry
            else:
                messagebox.showerror("Error", "Password length must be at least 12 characters.")

        website_label = tk.Label(logged_in_window, text="Website:")
        website_label.pack()
        website_entry = tk.Entry(logged_in_window)
        website_entry.pack()

        email_label = tk.Label(logged_in_window, text="Email:")
        email_label.pack()
        email_entry = tk.Entry(logged_in_window)
        email_entry.pack()

        password_label = tk.Label(logged_in_window, text="Password:")
        password_label.pack()
        password_entry_logged_in = PasswordEntry(logged_in_window, show="*")  # Create a new PasswordEntry widget
        password_entry_logged_in.pack()

        global show_password_var  # Access the global show_password_var
        # Show Password checkbox
        show_password_var = tk.BooleanVar(value=False)
        show_password_checkbox = ttk.Checkbutton(logged_in_window, text="Show Password", variable=show_password_var, command=password_entry_logged_in.toggle_password_visibility)  # Toggle the visibility of the logged-in password entry
        show_password_checkbox.pack()

        store_button = ttk.Button(logged_in_window, text="Store Password", command=store)
        store_button.pack()

        retrieve_button = ttk.Button(logged_in_window, text="Retrieve Password", command=retrieve)
        retrieve_button.pack()

        length_label = tk.Label(logged_in_window, text="Password Length:")
        length_label.pack()
        length_var = tk.StringVar()
        length_var.set(12)
        length_spinbox = tk.Spinbox(logged_in_window, from_=12, to=100, textvariable=length_var)
        length_spinbox.pack()

        numbers_var = tk.IntVar()
        numbers_checkbox = tk.Checkbutton(logged_in_window, text="Include Numbers", variable=numbers_var)
        numbers_checkbox.pack()

        special_chars_var = tk.IntVar()
        special_chars_checkbox = tk.Checkbutton(logged_in_window, text="Include Special Characters", variable=special_chars_var)
        special_chars_checkbox.pack()

        generate_button = ttk.Button(logged_in_window, text="Generate Password", command=generate_password)
        generate_button.pack()

        logged_in_window.mainloop()

    login_window = tk.Tk()
    login_window.title("Login")

    username_label = tk.Label(login_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()
    password_entry = PasswordEntry(login_window, show="*")
    password_entry.pack()

    global show_password_var  # Access the global show_password_var
    # Show Password checkbox
    show_password_var = tk.BooleanVar(value=False)
    show_password_checkbox = ttk.Checkbutton(login_window, text="Show Password", variable=show_password_var, command=toggle_password_visibility)
    show_password_checkbox.pack()

    register_button = ttk.Button(login_window, text="Register", command=register)
    register_button.pack()

    login_button = ttk.Button(login_window, text="Login", command=login)
    login_button.pack()

    login_window.mainloop()
