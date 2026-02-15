import tkinter as tk
from tkinter import messagebox
from models.product import add_product, get_all_products

def show_inventory_ui():
    inv_win = tk.Toplevel()
    inv_win.title("Product Inventory")

    # Labels and Entries
    labels = ['Name', 'SKU', 'Price', 'Quantity', 'GST Rate']
    entries = []

    for i, label in enumerate(labels):
        tk.Label(inv_win, text=label).grid(row=i, column=0)
        e = tk.Entry(inv_win)
        e.grid(row=i, column=1)
        entries.append(e)

    def add_product_ui():
        try:
            name = entries[0].get()
            sku = entries[1].get()
            price = float(entries[2].get())
            qty = int(entries[3].get())
            gst = float(entries[4].get())

            add_product(name, sku, price, qty, gst)
            messagebox.showinfo("Success", "Product added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")

    tk.Button(inv_win, text="Add Product", command=add_product_ui).grid(row=5, columnspan=2, pady=10)

    # Product List
    product_listbox = tk.Listbox(inv_win, width=80)
    product_listbox.grid(row=6, columnspan=2, pady=10)

    def refresh_list():
        product_listbox.delete(0, tk.END)
        for p in get_all_products():
            line = f"{p['sku']} | {p['name']} | ₹{p['price']} | Qty: {p['quantity']} | GST: {p['gst_rate']}%"
            product_listbox.insert(tk.END, line)

    tk.Button(inv_win, text="Refresh", command=refresh_list).grid(row=7, columnspan=2)
