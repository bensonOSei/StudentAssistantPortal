from typing import List
from fastapi_mail.email_utils import DefaultChecker
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import BaseModel,Field,EmailStr

# some things are meant to be kept as secrets
from dotenv import dotenv_values
credentials = dotenv_values(".env")


class EmailSchema(BaseModel):
    email: List[EmailStr]


class NotifyUser:
    def __init__(self,subject:str, message:str, email:list[str],credentials:dict = credentials):
        
        self.credentials = credentials

        self.config = ConnectionConfig(
            MAIL_USERNAME = self.credentials["EMAIL"],
            MAIL_PASSWORD = self.credentials["PASSWORD"],
            MAIL_FROM = self.credentials["EMAIL"],
            MAIL_PORT = 587,
            MAIL_SERVER = "smtp.gmail.com",
            MAIL_FROM_NAME="E-LEARNING UNIT COLLAGE OF DISTANCE EDU",
            MAIL_TLS = True,
            MAIL_SSL = False,
            USE_CREDENTIALS = True)
         
        self.message = MessageSchema(
            subject= subject, # subject of the email
            attachments= ["./requirements.txt"],
            recipients = email, # List of recipients, as many as you can pass 
            body= message, # message to be sent
            #bcc = ["kbenson643@gmail.com"], #General Office Email Address 
            # subtype="html"
            )
