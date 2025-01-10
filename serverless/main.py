from flask import Flask, request
from google.cloud import firestore
import datetime

app = Flask(__name__)
db = firestore.Client()

@app.route("/", methods=["POST"])
def log_invoice():
    data = request.get_json()
    if not data:
        return {"error": "Invalid request"}, 400

    # Extract required fields
    invoice_id = data.get("invoice_id")
    sender_name = data.get("sender_name")
    receiver_name = data.get("receiver_name")
    amount = data.get("amount")
    timestamp = data.get("timestamp")

    if not all([invoice_id, sender_name, receiver_name, amount]):
        return {"error": "Missing required fields"}, 400

    # Log to Firestore
    log_entry = {
        "invoice_id": invoice_id,
        "sender_name": sender_name,
        "receiver_name": receiver_name,
        "amount": amount,
        "timestamp": timestamp,
    }
    db.collection("invoice_logs").add(log_entry)

    return {"status": "Invoice logged successfully"}, 200


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
