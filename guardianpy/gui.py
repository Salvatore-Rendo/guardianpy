import tkinter as tk
from tkinter import messagebox
from guardianpy.database import (
    register_user,
    authenticate_user,
    store_password,
    retrieve_password,
)
from guardianpy.encryption import encrypt_password, decrypt_password

def run_gui():
    def register():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
        else:
            register_user(username, password)
            messagebox.showinfo("Success", "Registration successful.")

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
        else:
            user_id = authenticate_user(username, password)
            if user_id is not None:
                logged_in(user_id)
            else:
                messagebox.showerror("Error", "Authentication failed. Please try again.")

    def logged_in(user_id):
        login_window.destroy()
        logged_in_window = tk.Tk()
        logged_in_window.title("Password Manager")

        def store():
            website = website_entry.get()
            password = password_entry.get()
            if not website or not password:
                messagebox.showerror("Error", "Please enter both website and password.")
            else:
                store_password(user_id, website, encrypt_password(password))
                messagebox.showinfo("Success", "Password stored.")

        def retrieve():
            website = website_entry.get()
            password = retrieve_password(user_id, website)
            if password:
                messagebox.showinfo("Password", f"Password for {website}: {decrypt_password(password)}")
            else:
                messagebox.showerror("Error", "Password not found.")

        website_label = tk.Label(logged_in_window, text="Website:")
        website_label.pack()
        website_entry = tk.Entry(logged_in_window)
        website_entry.pack()

        password_label = tk.Label(logged_in_window, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(logged_in_window)
        password_entry.pack()

        store_button = tk.Button(logged_in_window, text="Store Password", command=store)
        store_button.pack()

        retrieve_button = tk.Button(logged_in_window, text="Retrieve Password", command=retrieve)
        retrieve_button.pack()

        logged_in_window.mainloop()

    login_window = tk.Tk()
    login_window.title("Login")

    username_label = tk.Label(login_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    register_button = tk.Button(login_window, text="Register", command=register)
    register_button.pack()

    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.pack()

    login_window.mainloop()
