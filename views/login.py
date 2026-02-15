import tkinter as tk
from tkinter import messagebox
from models.user import authenticate
from views.dashboard import show_dashboard

def show_login():
    root = tk.Tk()
    root.title("BillingSoft Pro - Login")
    root.geometry("300x150")  # Optional: set a fixed size

    tk.Label(root, text="Username").grid(row=0, padx=10, pady=5)
    tk.Label(root, text="Password").grid(row=1, padx=10, pady=5)

    username = tk.Entry(root)
    password = tk.Entry(root, show="*")

    username.grid(row=0, column=1, padx=10, pady=5)
    password.grid(row=1, column=1, padx=10, pady=5)

    def login_action():
        user = authenticate(username.get(), password.get())
        if user:
            root.withdraw()  # ✅ hide login window, don't destroy it
            show_dashboard(user, root)  # ✅ pass login window to dashboard
        else:
            messagebox.showerror("Error", "Invalid credentials")

    tk.Button(root, text="Login", command=login_action).grid(row=3, columnspan=2, pady=10)
    root.mainloop()
