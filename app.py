from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

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
        recipients=[os.getenv('RECEIVER_EMAIL')],
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

    mail.send(msg)

    return jsonify({'status': 'success'})

@app.route('/')
def home():
    return 'Backend is running'

if __name__ == '__main__':
    app.run(debug=True)