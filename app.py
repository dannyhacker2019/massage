from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
CORS(app)

# --- Environment variables ---
# SENDGRID_API_KEY -> your SendGrid API key
# SENDER_EMAIL -> verified SendGrid sender email
# RECEIVER_EMAIL -> email to receive booking notifications

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

if not SENDGRID_API_KEY or not SENDER_EMAIL or not RECEIVER_EMAIL:
    raise Exception("Please set SENDGRID_API_KEY, SENDER_EMAIL, and RECEIVER_EMAIL environment variables")

# --- Routes ---

@app.route("/book", methods=["POST"])
def book():
    data = request.json

    name = data.get("name")
    phone = data.get("phone")
    service = data.get("service")
    date = data.get("date")
    message = data.get("message", "")

    if not name or not phone:
        return jsonify({"error": "Missing required fields"}), 400

    email_content = f"""
New Massage Booking Request 💆‍♀️

Name: {name}
Phone: {phone}
Service: {service}
Preferred Date: {date}

Notes:
{message}
    """

    email = Mail(
        from_email=SENDER_EMAIL,
        to_emails=RECEIVER_EMAIL,
        subject="New Booking Request",
        plain_text_content=email_content
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(email)
    except Exception as e:
        print("Error sending email:", e)
        return jsonify({"error": "Failed to send email"}), 500

    return jsonify({"status": "success"})


@app.route("/")
def home():
    return "Backend is running"


if __name__ == "__main__":
    # Use Railway port or default 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)