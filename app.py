from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
CORS(app)

@app.route('/book', methods=['POST'])
def book():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    service = data.get('service')
    date = data.get('date')
    message_text = data.get('message', '')

    if not name or not phone:
        return jsonify({'error': 'Missing required fields'}), 400

    # Get sender and receiver from environment variables
    sender_email = os.getenv('SENDGRID_SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')

    message = Mail(
        from_email=sender_email,
        to_emails=receiver_email,
        subject='New Booking Request 💆‍♀️',
        plain_text_content=f"""
New Massage Booking Request

Name: {name}
Phone: {phone}
Service: {service}
Preferred Date: {date}

Notes:
{message_text}
        """
    )

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        sg.send(message)
        return jsonify({'status': 'success'})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error sending booking, try again'}), 500

@app.route('/')
def home():
    return 'Backend is running'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)