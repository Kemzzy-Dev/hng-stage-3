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


app = Flask(__name__)

# Configure Celery
# Configure RabbitMQ and Celery
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['result_backend'] = 'rpc://'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
celery.conf.broker_connection_retry_on_startup = True

#Logs
log = Log("/var/log/messaging_system.log")
logger = logging.getLogger(__name__)
logging.basicConfig(filename='./messaging_system.log', level=logging.INFO)



@celery.task
def send_email(recipient: str) -> Any:
    logger.info(f"send_email task started for {recipient}")

    sender = "ekemini.udongwo11@gmail.com"
    msg = MIMEText("This is a test email sent from the messaging system.")
    msg['Subject'] = "Test Email"
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, 'gvtv jvlz unmm xngo')
        server.send_message(msg)
    
    logger.info(f"send_email task completed for {recipient}")




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

if __name__ == '__main__':
    app.run(debug=True)