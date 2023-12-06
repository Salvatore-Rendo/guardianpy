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

def create_centered_window(window, width, height):
    """
    Center the given window on the screen.

    Args:
        window (tk.Tk): The window to be centered.
        width (int): The width of the window.
        height (int): The height of the window.
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

def calculate_min_size(window):
    """
    Set the minimum size of the window based on its content.

    Args:
        window (tk.Tk): The window for which to set the minimum size.
    """
    # Update the window to calculate the required height
    window.update()
    # Add a margin to the minimum size
    min_width = window.winfo_reqwidth() + 50
    min_height = window.winfo_reqheight() + 50
    window.minsize(min_width, min_height)

def run_gui():
    def register():
        """
        Handle the registration process.
        """
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
        """
        Handle the login process.
        """
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
        else:
            user_id = authenticate_user(username, password)
            if user_id is not None:
                set_master_password(password)
                logged_in(user_id)
            else:
                messagebox.showerror("Error", "Authentication failed. Please try again.")

    def toggle_password_visibility():
        """
        Toggle the visibility of the password in the entry.
        """
        password_entry.toggle_password_visibility()

    def logged_in(user_id):
        """
        Handle the main functionality after a successful login.

        Args:
            user_id (int): The user ID associated with the logged-in user.
        """
        login_window.destroy()
        logged_in_window = tk.Tk()
        logged_in_window.title("Password Manager")

        def store():
            """
            Store a password in the database.
            """
            website = website_entry.get()
            email = email_entry.get()
            password = password_entry_logged_in.get()
            master_password = get_master_password()
            if not website or not email or not password:
                messagebox.showerror("Error", "Please enter website, email, and password.")
            else:
                store_password(user_id, website, email, password, master_password)
                messagebox.showinfo("Success", "Password stored.")

        def retrieve():
            """
            Retrieve a password from the database.
            """
            website = website_entry.get()
            master_password = get_master_password()
            password = retrieve_password(user_id, website, master_password)
            if password:
                messagebox.showinfo("Password", f"Password for {website}: {password}")
            else:
                messagebox.showerror("Error", "Password not found.")

        def generate_password():
            """
            Generate a random password.
            """
            length = int(length_var.get())
            include_numbers = numbers_var.get() == 1
            include_special_chars = special_chars_var.get() == 1

            if length >= 12:
                generated_password = generator.generate_password(length, include_numbers, include_special_chars)
                password_entry_logged_in.delete(0, tk.END)
                password_entry_logged_in.insert(0, generated_password)
            else:
                messagebox.showerror("Error", "Password length must be at least 12 characters.")

        website_label = tk.Label(logged_in_window, text="Website:")
        website_label.pack(pady=5)
        website_entry = tk.Entry(logged_in_window)
        website_entry.pack(pady=5)

        email_label = tk.Label(logged_in_window, text="Email:")
        email_label.pack(pady=5)
        email_entry = tk.Entry(logged_in_window)
        email_entry.pack(pady=5)

        password_label = tk.Label(logged_in_window, text="Password:")
        password_label.pack(pady=5)
        password_entry_logged_in = PasswordEntry(logged_in_window, show="*")
        password_entry_logged_in.pack(pady=5)

        global show_password_var
        show_password_var = tk.BooleanVar(value=False)
        show_password_checkbox = ttk.Checkbutton(logged_in_window, text="Show Password", variable=show_password_var, command=password_entry_logged_in.toggle_password_visibility)
        show_password_checkbox.pack(pady=5)

        store_button = ttk.Button(logged_in_window, text="Store Password", command=store)
        store_button.pack(pady=10)

        retrieve_button = ttk.Button(logged_in_window, text="Retrieve Password", command=retrieve)
        retrieve_button.pack(pady=10)

        length_label = tk.Label(logged_in_window, text="Password Length:")
        length_label.pack(pady=5)
        length_var = tk.StringVar()
        length_var.set(12)
        length_spinbox = tk.Spinbox(logged_in_window, from_=12, to=100, textvariable=length_var)
        length_spinbox.pack(pady=5)

        numbers_var = tk.IntVar()
        numbers_checkbox = tk.Checkbutton(logged_in_window, text="Include Numbers", variable=numbers_var)
        numbers_checkbox.pack(pady=5)

        special_chars_var = tk.IntVar()
        special_chars_checkbox = tk.Checkbutton(logged_in_window, text="Include Special Characters", variable=special_chars_var)
        special_chars_checkbox.pack(pady=5)

        generate_button = ttk.Button(logged_in_window, text="Generate Password", command=generate_password)
        generate_button.pack(pady=10)

        # Set minimum size based on the content
        calculate_min_size(logged_in_window)
        create_centered_window(logged_in_window, 400, logged_in_window.winfo_reqheight())

        logged_in_window.mainloop()

    login_window = tk.Tk()
    login_window.title("Login")
    create_centered_window(login_window, 300, 350)

    username_label = tk.Label(login_window, text="Username:")
    username_label.pack(pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack(pady=10)
    password_entry = PasswordEntry(login_window, show="*")
    password_entry.pack(pady=5)

    global show_password_var
    show_password_var = tk.BooleanVar(value=False)
    show_password_checkbox = ttk.Checkbutton(login_window, text="Show Password", variable=show_password_var, command=toggle_password_visibility)
    show_password_checkbox.pack(pady=10)

    register_button = ttk.Button(login_window, text="Register", command=register)
    register_button.pack(pady=10)

    login_button = ttk.Button(login_window, text="Login", command=login)
    login_button.pack(pady=10)

    # Set minimum size based on the content
    calculate_min_size(login_window)

    login_window.mainloop()
    