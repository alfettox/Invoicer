import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus.flowables import Spacer, Image
from reportlab.lib import colors

import csv

def get_sample_styles():
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle(name="CustomNormal", parent=styles["Normal"])
    custom_style.fontName = "Helvetica"
    custom_style.fontSize = 12
    custom_style.leading = 14
    return {"Normal": custom_style}


def calculate_total(quantity, unitary_cost):
    return quantity * unitary_cost


def generate_invoice_pdf(client_info, invoice_date, invoice_number, items, grand_total, save_folder):
    pdf_filename = f"{save_folder}/invoice_{invoice_number}.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()  # Add this line to define styles

    header_data = [
        [Paragraph(f"<font color=white><b>Invoice #: {invoice_number}</b></font>", styles['Normal']), ""],
        ["Name: " + client_info["Name"], f"Address: {client_info['Address']}"],
        ["Telephone: " + client_info["Telephone"], f"ZIP Code: {client_info['ZipCode']}"],
        ["Email: " + client_info["Email"], f"Town: {client_info['Town']}"],
    ]

    header_table = Table(header_data, colWidths=[3*inch, 2*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ]))
    elements.append(header_table)

    elements.append(Spacer(1, 0.2*inch))

    item_data = [["Item", "Quantity", "Unit Cost", "Total"]]
    for item in items:
        item_data.append(item)

    item_table = Table(item_data, colWidths=[2*inch, 1*inch, 1*inch, 1*inch])
    item_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 1), (-1, -1), 1, colors.black),
    ]))
    elements.append(item_table)

    elements.append(Spacer(1, 0.2*inch))

    grand_total_text = f"Grand Total: ${grand_total: .2f}"
    grand_total_style = getSampleStyleSheet()["Normal"]
    grand_total_style.alignment = 2
    elements.append(Paragraph(grand_total_text, grand_total_style))

    elements.append(Spacer(1, 0.2*inch))

    doc.build(elements)
    messagebox.showinfo("Invoice Generated", f"Invoice {
                        invoice_number}.pdf has been generated!")


def get_default_hours():
    return 35


def get_next_invoice_number():
    try:
        with open('factures_numbers.csv', 'r') as file:
            lines = file.readlines()
            if lines:
                invoice_numbers = [int(num.strip())
                                   for num in lines[-1].split(',') if num.strip()]
                if invoice_numbers:
                    last_invoice_number = max(invoice_numbers)
                    return last_invoice_number + 1
    except FileNotFoundError:
        pass

    return 1


def update_invoice_number(invoice_number):
    with open('factures_numbers.csv', 'a') as file:
        file.write(str(invoice_number) + ',\n')


def submit_invoice():
    try:
        invoice_number = get_next_invoice_number()
    except ValueError:
        messagebox.showerror("Invalid Invoice Number",
                             "Failed to retrieve the next invoice number.")
        return

    try:
        hours_worked = float(hours_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Hours Worked",
                             "Please enter a valid number for hours worked.")
        return

    service_type = service_combobox.get()
    hourly_rate = 35
    total_amount = calculate_total(hours_worked, hourly_rate)

    client_info = {
        "Name": "Giovanni De Franceschi",
        "Address": "123 Main Levesque",
        "Telephone": "+1 (514) 456-7890",
        "Town": "Montréal",
        "ZipCode": "H1W 3J9",
        "Email": "test@mail.com"
    }

    items = [
        [service_type, hours_worked, hourly_rate, total_amount]
    ]

    grand_total = total_amount

    save_folder = "invoices"

    generate_invoice_pdf(client_info, date.today().strftime(
        "%Y-%m-%d"), invoice_number, items, grand_total, save_folder)
    update_invoice_number(invoice_number)


app = tk.Tk()
app.title("Freelance Invoice Creator")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
window_width = int(0.3 * screen_width)
window_height = int(0.2 * screen_height)
window_geometry = f"{window_width}x{
    window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}"
app.geometry(window_geometry)

app_style = ttk.Style()
app_style.configure("My.TFrame", background="#333", foreground="white")

frame = ttk.Frame(app, style="My.TFrame")
frame.pack(fill=tk.BOTH, expand=True)

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.columnconfigure(2, weight=1)
frame.rowconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)
frame.rowconfigure(2, weight=1)

tk.Label(frame, text="Invoice Number:", background="#333",
         foreground="white").grid(row=0, column=0)
invoice_number_entry = tk.Entry(frame, justify="right")
invoice_number_entry.insert(0, str(get_next_invoice_number()))
invoice_number_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Hours Worked:", background="#333",
         foreground="white").grid(row=1, column=0)
hours_entry = tk.Entry(frame, justify="right")
hours_entry.insert(0, str(get_default_hours()))
hours_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Service Type:", background="#333",
         foreground="white").grid(row=2, column=0)
services = []

with open('services.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        services.append(row[0])

service_combobox = ttk.Combobox(frame, values=services)
service_combobox.grid(row=2, column=1, padx=5, pady=5)
service_combobox.set(services[0])

submit_button = tk.Button(frame, text="Generate Invoice", command=submit_invoice,
                          background="#007acc", foreground="white", borderwidth=0, relief="solid", padx=20)
submit_button.grid(row=3, columnspan=2, padx=5, pady=5)

app.mainloop()
