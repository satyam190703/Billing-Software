from fpdf import FPDF
import os

class PDF(FPDF):
    pass

def generate_invoice_pdf(invoice_data, filename):
    pdf = PDF()
    pdf.add_page()

    # ➕ Load Unicode Font for ₹ symbol (regular only)
    font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", "", 14)  # ✅ Use regular, not 'B'

    # Invoice title
    pdf.cell(200, 10, txt="BillingSoft Pro - Invoice", ln=True, align='C')
    pdf.ln(5)

    # Invoice metadata
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(100, 10, txt=f"Invoice No: {invoice_data.get('invoice_no', 'N/A')}", ln=True)
    pdf.cell(100, 10, txt=f"Date: {invoice_data.get('created_at', 'N/A')}", ln=True)
    pdf.cell(100, 10, txt=f"Customer: {invoice_data['customer_name']}", ln=True)
    pdf.ln(10)

    # Table header
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(80, 10, "Item", border=1)
    pdf.cell(30, 10, "Qty", border=1)
    pdf.cell(40, 10, "Price", border=1)
    pdf.cell(40, 10, "GST %", border=1)
    pdf.ln()

    # Item rows
    for item in invoice_data["items"]:
        pdf.cell(80, 10, item['name'], border=1)
        pdf.cell(30, 10, str(item['quantity']), border=1)
        pdf.cell(40, 10, f"₹{item['price']:.2f}", border=1)
        pdf.cell(40, 10, f"{item['gst']}%", border=1)
        pdf.ln()

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Subtotal: ₹{invoice_data['subtotal']:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Tax: ₹{invoice_data['tax']:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Discount: ₹{invoice_data['discount']:.2f}", ln=True)
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(200, 10, txt=f"Total: ₹{invoice_data['total']:.2f}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Payment Mode: {invoice_data['payment_mode']}", ln=True)

    pdf.output(filename)