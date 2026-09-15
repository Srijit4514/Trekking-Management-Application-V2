import os
from celery import Celery
from smtplib import SMTP   # connect to an email server SMTP(Simple Mail Transfer Protocol) to send emails
from email.mime.text import MIMEText  # create the actual email message
from email.mime.multipart import MIMEMultipart  # create am email that can contain multiple parts

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task
def send_staff_credentials_email(email, username, password):
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = "Your Trekking Dashboard Staff Account Credentials"

    body = f""" 
    Hello {username},

    An administrator has created a staff account for you.
    Here are your official login credentals:

    Username: {username}
    Password: {password}

    Please log in and update your password as soon as possible.
    """
    msg.attach(MIMEText(body, "plain"))

    try: 
        with SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return f"Credentials successfully emailed to {email}"
    except Exception as e:
        return f"Failed to send email to {email}: {str(e)}"