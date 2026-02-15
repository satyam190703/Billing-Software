# Invoice schema & operations
from config import invoices_collection
from datetime import datetime

def get_next_invoice_number():
    last_invoice = invoices_collection.find_one(sort=[("_id", -1)])
    if last_invoice and "invoice_no" in last_invoice:
        last_number = int(last_invoice["invoice_no"].split("-")[1])
        new_number = f"INV-{last_number + 1:03d}"
    else:
        new_number = "INV-001"
    return new_number

def create_invoice(customer_name, items, payment_mode, discount=0):
    subtotal = sum(i['price'] * i['quantity'] for i in items)
    tax = sum((i['price'] * i['gst'] / 100) * i['quantity'] for i in items)
    total = subtotal + tax - discount

    invoice_no = get_next_invoice_number()
    
    invoice = {
        "invoice_no": invoice_no,
        "customer_name": customer_name,
        "items": items,
        "subtotal": round(subtotal, 2),
        "tax": round(tax, 2),
        "discount": round(discount, 2),
        "total": round(total, 2),
        "payment_mode": payment_mode,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    invoices_collection.insert_one(invoice)
    return invoice

def get_all_invoices():
    return list(invoices_collection.find().sort("created_at", -1))
