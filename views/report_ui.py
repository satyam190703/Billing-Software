import tkinter as tk
from models.invoice import get_all_invoices
import pandas as pd

def show_report_ui():
    win = tk.Toplevel()
    win.title("Reports")

    data = get_all_invoices()
    report = pd.DataFrame(data)

    total_sales = report['total'].sum()
    total_tax = report['tax'].sum()

    tk.Label(win, text=f"Total Sales: ₹{total_sales}").pack()
    tk.Label(win, text=f"Total Tax Collected: ₹{total_tax}").pack()

    def export_excel():
        report.to_excel("sales_report.xlsx", index=False)

    tk.Button(win, text="Export to Excel", command=export_excel).pack()
