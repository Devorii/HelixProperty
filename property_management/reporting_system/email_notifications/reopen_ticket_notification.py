import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from property_management.reporting_system.email_notifications.reopen_ticket_email_body import email_body
load_dotenv()


class ReOpenTicket_email_notification():
    def __init__(self, artifacts:dict):
        self.user_email=artifacts['email']
        self.username=artifacts['username']
        self.sender_email=os.getenv('SENDERS_EMAIL')
        self.auth_password=os.getenv('SENDERS_PASSWORD')
        self.body_artifacts=artifacts


    def send_mail(self): # Verification email - change name
        '''SEND MAIL TO CLIENT'''
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = ", ".join(self.user_email)
        message["Subject"] = f"Peach Street - {self.username} Re-Opened a ticket"
        body = email_body(self.body_artifacts)
        message.attach(MIMEText(body, "html"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(self.sender_email, self.auth_password)
            server.sendmail(self.sender_email, self.user_email, message.as_string())
            print("Email was sent...")