"""
Author: Michael Kofi Armah
Description: Script Package for sending Email Replies to Users
"""

from typing import List
from fastapi_mail.email_utils import DefaultChecker
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, Field, EmailStr

# some things are meant to be kept as secrets

from dotenv import dotenv_values, load_dotenv
import os

load_dotenv(".env")

MAIL_USERNAME = os.environ.get("EMAIL")
MAIL_PASSWORD = os.environ.get("PASSWORD")
BCC = os.environ.get("BCC")


class EmailSchema(BaseModel):
    email: List[EmailStr]


class NotifyUser:
    def __init__(
            self,
            subject: str,
            message: str,
            email: list[str]):

        self.config = ConnectionConfig(

            MAIL_USERNAME=MAIL_USERNAME,
            MAIL_PASSWORD=MAIL_PASSWORD,
            MAIL_FROM=MAIL_USERNAME,
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_FROM_NAME="E-LEARNING UNIT COLLAGE OF DISTANCE EDU",
            MAIL_TLS=True,
            MAIL_SSL=False,
            USE_CREDENTIALS=True)

        self.message = MessageSchema(
            subject=subject,  # subject of the email
            recipients=email,  # List of recipients, as many as you can pass
            body=message,  # message to be sent
            # bcc = [BCC], #Blind carbon copy - General Office's Email Address
            # subtype="html"
        )


access_module_message = """Module Request server is currently down, Please try again later\n\nTimestamp : {} \n \n  \n \n
            E-Learning Unit
            Collage of Distance Education
            University of Cape Coast
            """
access_module_subj = "Module Request"

complaint_email_msg = """Hello {name}, your complaint has been recieved by the E-learning Unit -CoDE, be sure to check your email regularly for a feedback on the reported issue.

If no feedback is recieved within 72 hours from the time of recieving this email,
Please contact the E-learning Unit using the provided complaint token as reference \n
Thanks for being part of CoDE

complaint token: {token}
Timestamp : {stamp} \n
\n\n\n
---------------------------------------------------
                    recieved complaint
---------------------------------------------------\n
{complaint_msg} \n \n  \n
            E-Learning Unit
            Collage of Distance Education
            University of Cape Coast"""

complaint_email_subj = "Complaint Logged"

if __name__ == "__main__":
    print(access_module_message.format("time"))
