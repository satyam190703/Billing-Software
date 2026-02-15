import tkinter as tk
from views.inventory_ui import show_inventory_ui
from views.invoice_ui import show_invoice_ui
from views.report_ui import show_report_ui
from views.admin_panel import show_admin_panel  # Import the admin panel

def show_dashboard(user, login_window):
    root = tk.Toplevel()
    root.title(f"Welcome {user['username']} ({user['role']})")

    tk.Label(root, text="BillingSoft Pro Dashboard", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Button(root, text="Create Invoice", command=show_invoice_ui, width=30).pack(pady=5)
    tk.Button(root, text="Manage Products", command=show_inventory_ui, width=30).pack(pady=5)
    tk.Button(root, text="Reports", command=show_report_ui, width=30).pack(pady=5)

    if user.get('role').lower() == 'admin':
        tk.Button(root, text="Admin Panel", command=show_admin_panel, width=30).pack(pady=5)

    def logout():
        root.destroy()
        login_window.deiconify()

    tk.Button(root, text="Logout", command=logout, width=30).pack(pady=5)
