import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from notification_protocols.admin_request_body import email_body
load_dotenv()



class Create_req_email_notification():
    def __init__(self, artifacts:dict):
        self.user_email=artifacts['email']
        self.sender_email=os.getenv('SENDERS_EMAIL')
        self.auth_password=os.getenv('SENDERS_PASSWORD')
        self.body_artifacts=artifacts

    def send_mail(self): # Verification email - change name
        '''SEND MAIL TO CLIENT'''
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.user_email
        message["Subject"] = "Helix Proptery Management - Access Request"
        body = email_body(self.body_artifacts)
        message.attach(MIMEText(body, "html"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(self.sender_email, self.auth_password)
            server.sendmail(self.sender_email, self.user_email, message.as_string())
            print("Email was sent...")
