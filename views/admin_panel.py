import tkinter as tk
from tkinter import messagebox, simpledialog
from models.user import register_user, get_all_users, delete_user

def show_admin_panel():
    admin_win = tk.Toplevel()
    admin_win.title("Admin Panel - Manage Users")

    tk.Label(admin_win, text="User Management", font=("Arial", 14, "bold")).pack(pady=10)

    # Entry Form
    form_frame = tk.Frame(admin_win)
    form_frame.pack(pady=5)

    tk.Label(form_frame, text="Username").grid(row=0, column=0, pady=5, padx=5)
    tk.Label(form_frame, text="Password").grid(row=1, column=0, pady=5, padx=5)
    tk.Label(form_frame, text="Role (Admin/Manager/Staff)").grid(row=2, column=0, pady=5, padx=5)

    username_entry = tk.Entry(form_frame)
    password_entry = tk.Entry(form_frame, show="*")
    role_entry = tk.Entry(form_frame)

    username_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)
    role_entry.grid(row=2, column=1)

    def create_new_user():
        uname = username_entry.get().strip()
        pw = password_entry.get().strip()
        r = role_entry.get().strip().capitalize()

        if not uname or not pw or not r:
            messagebox.showerror("Error", "All fields are required.")
            return

        if r not in ["Admin", "Manager", "Staff"]:
            messagebox.showerror("Error", "Role must be Admin, Manager, or Staff")
            return

        success = register_user(uname, pw, r)
        if success:
            messagebox.showinfo("Success", f"User '{uname}' created successfully.")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            role_entry.delete(0, tk.END)
            refresh_user_list()
        else:
            messagebox.showerror("Error", f"User '{uname}' already exists.")

    tk.Button(form_frame, text="Create User", command=create_new_user, bg="green", fg="white").grid(row=3, columnspan=2, pady=10)

    # User List Section
    list_frame = tk.Frame(admin_win)
    list_frame.pack(pady=10)

    def refresh_user_list():
        for widget in list_frame.winfo_children():
            widget.destroy()

        users = get_all_users()
        if not users:
            tk.Label(list_frame, text="No users found.").pack()
            return

        for user in users:
            row = tk.Frame(list_frame)
            row.pack(pady=2, padx=10, fill="x")

            tk.Label(row, text=f"{user['username']} ({user['role']})", anchor='w', width=30).pack(side="left")
            tk.Button(row, text="Delete", fg="white", bg="red",
                      command=lambda u=user['username']: handle_delete_user(u)).pack(side="right")

    def handle_delete_user(username):
        confirm = messagebox.askyesno("Confirm", f"Delete user '{username}'?")
        if confirm:
            if delete_user(username):
                messagebox.showinfo("Deleted", f"User '{username}' deleted.")
                refresh_user_list()
            else:
                messagebox.showerror("Error", "Could not delete user.")

    refresh_user_list()
