from google.cloud import firestore

db = firestore.Client()

def log_activity(request):
    request_json = request.get_json(silent=True)
    if not request_json:
        return {"error": "Invalid request"}, 400

    # Extract required fields
    user_id = request_json.get("user_id")
    activity = request_json.get("activity")
    timestamp = request_json.get("timestamp")

    if not user_id or not activity or not timestamp:
        return {"error": "Missing required fields"}, 400

    # Log to Firestore
    activity_log = {
        "user_id": user_id,
        "activity": activity,
        "timestamp": timestamp,
    }
    db.collection("user_activity").add(activity_log)

    return {"status": "Activity logged successfully"}, 200
