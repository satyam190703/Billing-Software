from models.invoice import create_invoice

def test_invoice_total():
    items = [{"name": "Item A", "price": 100, "quantity": 2, "gst": 5}]
    invoice = create_invoice("Test", items, "cash")
    assert round(invoice["total"], 2) == 210.0
