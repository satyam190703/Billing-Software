import tkinter as tk
from tkinter import messagebox, simpledialog
from models.invoice import create_invoice
from utils.pdf_generator import generate_invoice_pdf
from utils.emailer import send_invoice_pdf
import os
import re

def show_invoice_ui():
    win = tk.Toplevel()
    win.title("Create Invoice")

    tk.Label(win, text="Customer Name").grid(row=0, column=0)
    customer_entry = tk.Entry(win)
    customer_entry.grid(row=0, column=1)

    items = []

    def add_item():
        try:
            name = item_name.get().strip()
            price = float(item_price.get())
            qty = int(item_qty.get())
            gst = float(item_gst.get())

            if not name:
                raise ValueError("Item name required.")

            items.append({
                "name": name,
                "price": price,
                "quantity": qty,
                "gst": gst
            })
            listbox.insert(tk.END, f"{name} x {qty} @ ₹{price:.2f} + GST {gst}%")
            item_name.delete(0, tk.END)
            item_price.delete(0, tk.END)
            item_qty.delete(0, tk.END)
            item_gst.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid item entry: {e}")

    # Item input fields
    tk.Label(win, text="Item Name").grid(row=1, column=0)
    tk.Label(win, text="Price").grid(row=2, column=0)
    tk.Label(win, text="Quantity").grid(row=3, column=0)
    tk.Label(win, text="GST %").grid(row=4, column=0)

    item_name = tk.Entry(win)
    item_price = tk.Entry(win)
    item_qty = tk.Entry(win)
    item_gst = tk.Entry(win)

    item_name.grid(row=1, column=1)
    item_price.grid(row=2, column=1)
    item_qty.grid(row=3, column=1)
    item_gst.grid(row=4, column=1)

    tk.Button(win, text="Add Item", command=add_item).grid(row=5, columnspan=2)

    listbox = tk.Listbox(win, width=60)
    listbox.grid(row=6, columnspan=2, pady=5)

    # Payment + discount fields
    tk.Label(win, text="Payment Mode").grid(row=7, column=0)
    payment_entry = tk.Entry(win)
    payment_entry.grid(row=7, column=1)

    tk.Label(win, text="Discount (₹)").grid(row=8, column=0)
    discount_entry = tk.Entry(win)
    discount_entry.insert(0, "0")
    discount_entry.grid(row=8, column=1)

    # Email format check
    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def create_inv():
        try:
            if not customer_entry.get().strip():
                raise ValueError("Customer name is required.")
            if not payment_entry.get().strip():
                raise ValueError("Payment mode is required.")
            if not items:
                raise ValueError("No items added.")

            discount = float(discount_entry.get())
            invoice = create_invoice(
                customer_name=customer_entry.get().strip(),
                items=items,
                payment_mode=payment_entry.get().strip(),
                discount=discount
            )

            # Create invoices folder if it doesn't exist
            os.makedirs("invoices", exist_ok=True)
            filename = f"invoices/{invoice['invoice_no']}.pdf"
            generate_invoice_pdf(invoice, filename)

            messagebox.showinfo("Success", f"Invoice saved as {filename}")

            # Ask if user wants to email it
            send = messagebox.askyesno("Email", "Do you want to email this invoice?")
            if send:
                recipient = simpledialog.askstring("Send Email", "Enter customer email:")
                if recipient:
                    if is_valid_email(recipient):
                        send_invoice_pdf(recipient, filename)
                        messagebox.showinfo("Email Sent", f"Invoice sent to {recipient}")
                    else:
                        messagebox.showerror("Invalid Email", "Please enter a valid email address.")

            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Invoice creation failed: {e}")

    tk.Button(win, text="Generate Invoice", command=create_inv).grid(row=9, columnspan=2, pady=10)
