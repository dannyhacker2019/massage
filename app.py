from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ----------------------------
# Flask-Mail configuration
# ----------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # your Gmail
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Gmail App Password
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# ----------------------------
# Booking endpoint
# ----------------------------
@app.route('/book', methods=['POST'])
def book():
    data = request.json

    name = data.get('name')
    phone = data.get('phone')
    service = data.get('service')
    date = data.get('date')
    message = data.get('message', '')

    if not name or not phone:
        return jsonify({'error': 'Missing required fields'}), 400

    msg = Message(
        subject='New Booking Request',
        recipients=[os.getenv('RECEIVER_EMAIL')],  # where you want to receive bookings
        body=f"""
New Massage Booking Request 💆‍♀️

Name: {name}
Phone: {phone}
Service: {service}
Preferred Date: {date}

Notes:
{message}
        """
    )

    try:
        mail.send(msg)
        print(f"[INFO] Booking email sent for {name}")
        return jsonify({'status': 'success'})
    except Exception as e:
        # Log the error and return it in the response
        print(f"[ERROR] Failed to send email: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/')
def home():
    return 'Backend is running'

if __name__ == '__main__':
    # Make sure environment variables are set before running
    if not os.getenv('MAIL_USERNAME') or not os.getenv('MAIL_PASSWORD') or not os.getenv('RECEIVER_EMAIL'):
        print("[WARNING] Please set MAIL_USERNAME, MAIL_PASSWORD, and RECEIVER_EMAIL environment variables")
    app.run(debug=True)