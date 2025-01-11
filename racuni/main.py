from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
from fpdf import FPDF
import os
from datetime import datetime

app = FastAPI()

# Define Models
class InvoiceRequest(BaseModel):
    sender_name: str
    receiver_name: str
    amount: float


# Configurations
SERVERLESS_FUNCTION_URL = os.getenv("SERVERLESS_FUNCTION_URL", "https://log-activity-1059882736634.us-central1.run.app")
PDF_DIRECTORY = os.getenv("PDF_DIRECTORY", "./invoices")

# Ensure the PDF directory exists
os.makedirs(PDF_DIRECTORY, exist_ok=True)


def generate_pdf_invoice(invoice_id: str, sender_name: str, receiver_name: str, amount: float) -> str:
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="INVOICE", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    current_date = datetime.now().strftime("%Y-%m-%d")
    pdf.cell(100, 10, txt=f"Invoice ID: {invoice_id}", ln=True)
    pdf.cell(100, 10, txt=f"Date: {current_date}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, txt="Sender Details:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(100, 10, txt=f"Name: {sender_name}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, txt="Receiver Details:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(100, 10, txt=f"Name: {receiver_name}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, txt="Invoice Summary:", ln=True)
    pdf.set_font("Arial", size=12)
    
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(60, 10, txt="Description", border=1, fill=1, align="C")
    pdf.cell(40, 10, txt="Amount", border=1, fill=1, align="C")
    pdf.ln()
    pdf.cell(60, 10, txt="Service/Payment", border=1, align="C")
    pdf.cell(40, 10, txt=f"${amount:.2f}", border=1, align="C")
    pdf.ln(15)
    
    pdf.set_font("Arial", "I", 10)
    pdf.set_y(-30)
    pdf.cell(0, 10, txt="Thank you for your business!", ln=True, align="C")
    pdf.cell(0, 10, txt="If you have any questions, contact us at support@example.com", ln=True, align="C")
    
    pdf_file_path = os.path.join(PDF_DIRECTORY, f"invoice_{invoice_id}.pdf")
    pdf.output(pdf_file_path)
    
    return pdf_file_path


@app.post("/generate-invoice", response_class=FileResponse)
def generate_invoice(invoice: InvoiceRequest):
    try:
        invoice_id = f"{invoice.sender_name}_{invoice.receiver_name}_{invoice.amount}".replace(" ", "_")
        
        pdf_path = generate_pdf_invoice(
            invoice_id, invoice.sender_name, invoice.receiver_name, invoice.amount
        )
        
        log_payload = {
            "invoice_id": invoice_id,  # Ensure this is a unique identifier for the invoice
            "sender_name": invoice.sender_name,  # Match key expected by serverless function
            "receiver_name": invoice.receiver_name,  # Match key expected by serverless function
            "amount": invoice.amount,  # Ensure the amount is correct
            "timestamp": datetime.now().isoformat(),  # Add a timestamp
        }

        # Debug: Log the payload to verify its structure
        print(f"Payload being sent to serverless function: {log_payload}")

        # Send the POST request to the serverless function
        try:
            response = requests.post(SERVERLESS_FUNCTION_URL, json=log_payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to log invoice: {e}")


        return FileResponse(pdf_path, media_type="application/pdf", filename=f"invoice_{invoice_id}.pdf")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
def get_status():
    return {"status": "Invoice Service is running"}
