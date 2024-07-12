# app.py
from flask import Flask, request
from celery import Celery, shared_task
import smtplib
from email.mime.text import MIMEText
from custom_logs import Log
from datetime import datetime
import os
from typing import Any
import logging
from flask import abort
from dotenv import load_dotenv
import subprocess



app = Flask(__name__)
load_dotenv()

# Configure Celery
# Configure RabbitMQ and Celery
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['result_backend'] = 'rpc://'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
celery.conf.broker_connection_retry_on_startup = True

#Logs
file_path = "/var/log/messaging_system.log"
log = Log(file_path)
# sudo touch /var/log/messaging_system.log

# Check if the file exists
if os.path.exists(file_path):
    subprocess.run(["sudo", "chmod", "a+rw", file_path], check=True)
else:
    # File does not exist, create it
    with open(file_path, 'a'):  # Open the file in append mode to create it if it doesn't exist
        pass

    # Set permissions
    try:
        subprocess.run(["sudo", "chmod", "a+rw", file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to set permissions: {e}")


@celery.task
def send_email(recipient: str) -> Any:
    sender_email = os.getenv("EMAIL")
    sender_passkey = os.getenv("PASSKEY")
    
    # Create the mail
    msg = MIMEText("This is a test email sent from the messaging system.")
    msg['Subject'] = "Test Email"
    msg['From'] = sender_email
    msg['To'] = recipient

    # send mail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_passkey)
        server.send_message(msg)
    



@app.route('/')
def index() -> str:
    if 'sendmail' in request.args:
        recipient = request.args.get('sendmail')
        send_email.delay(recipient)
        return f"Email queued for sending to {recipient}"
    
    elif 'talktome' in request.args:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.log(f"Talktome request received at {current_time}\n")
        return f"Request logged at {current_time}"
    
    else:
        return "Welcome to the messaging system!"
    

@app.route('/logs')
def logs():
    log_path = '/var/log/messaging_system.log'
    if not os.path.exists(log_path):
        abort(404, description="Log file does not exist.")

    try:
        with open(log_path, 'r') as log_file:
            log_content = log_file.read()
        return f"<pre>{log_content}</pre>"
    except IOError as e:
        abort(500, description=f"An error occurred while reading the log file: {e}")

if __name__ == '__main__':
    app.run(debug=True)