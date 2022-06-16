"""
FastAPI Backend
Author : Michael Kofi Armah
"""

# fastapi dependencies
from email import message
from os import access

from fastapi import (
    Depends,
    FastAPI,
    Body,
    File,
    UploadFile,
    status,
    Request,
    Form,
    Query)

from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException

# fastapi_mail dependencies
from fastapi_mail.email_utils import DefaultChecker
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_mail.connection import ConnectionErrors

# starlette dependencies
from starlette.responses import Response, RedirectResponse, JSONResponse, HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

# pydantic dependencies
from pydantic import BaseModel, Field, EmailStr

# python type hints
from typing import List, Optional, Union
from tomlkit import datetime

# depency to run fastapi
import uvicorn

# some things are meant to be kept as secrets
from dotenv import dotenv_values

# custom libraries
from notification import NotifyUser, EmailSchema
from regex_validation import ValidateForm

#other
import datetime
credentials = dotenv_values(".env")
#InVal = InputValidator()
app = FastAPI()


class EmailSchema(BaseModel):
    email: List[EmailStr]

# Universal Fields


class GeneralBioModel(BaseModel):
    """BaseModel for Intersection Bio Data"""
    name: str
    Registration_Number: str
    email: str


class Program(BaseModel):
    """BaseModel for Programs"""
    MathematicsandScience: Optional[str] | None
    Education: Optional[str] | None
    Business: Optional[str] | None
    ArtsandSocial: Optional[str] | None


templates = Jinja2Templates(directory="./templates")

app.mount("/templates/js", StaticFiles(directory="templates/js"), name="js")


app.mount(
    "/templates/style",
    StaticFiles(
        directory="templates/style"),
    name="style")

app.mount(
    "/templates/favicon",
    StaticFiles(
        directory="templates/favicon"),
    name="favicon")

message = """<p>'Fixing message repeatetions'</p>"""
subject = "TEST 5"


@app.get("/")
def index(request: Request):
    """Program Homepage"""
    return templates.TemplateResponse("index.html",
                                      {"request": request})


@app.get("/status")
def form_status(request: Request):
    """Returns the status of the request after submission"""
    return templates.TemplateResponse("success.html", {"request": request})


@app.post("/accessmodules")
async def accessmodules(*,
                        request: Request,
                        name: str = Form(...),
                        Registration_Number: str = Form(...),
                        email: List[EmailStr] = Form(...),
                        program: str = Form(...)
                        ):
                        
    """access course modules"""

    # to do : Take email validation from parameters of this function to the
    # regex_validation

    form = ValidateForm(request)
    await form.load_data()
    if await form.is_valid()==True:  # if the registration id and email are valid

        try:

            ######  database script goes here   ####

            # email script
            model = NotifyUser(message=message, subject=subject, email=email)
            fm = FastMail(model.config)
            await fm.send_message(model.message)

            form.__dict__.update(
                msg="Please check your email for the requested modules :)")

            response = templates.TemplateResponse(
                "success.html", context=form.__dict__)
            return response

        # handle internet connection errors
        except ConnectionErrors:
            form.__dict__.update(
                connection_error="Please Check Your Internet Connection")
            response = templates.TemplateResponse(
                "index.html", context=form.__dict__)
            return response

        except HTTPException:
            raise HTTPException  # temporary command

            # return templates.TemplateResponse(
            #     "success.html",context = form.__dict__)  # should be the redirection html

    form.__dict__.update(msg="")
    form.__dict__.get("errors").append(
        "Incorrect Name or Registration ID")

    return templates.TemplateResponse(
        "success.html",
        form.__dict__)  # should be the redirection html


@app.post("/makecomplaint")
async def makecomplaint(*,
                        request: Request,
                        program: str = Form(..., description="The program offered by the user"),
                        course: str = Form(..., description="The course specific to the program given"),
                        study_center: str = Form(..., description="The study center of the user"),
                        name: str = Form(...),
                        Registration_Number: str = Form(...),
                        email: List[EmailStr] = Form(...),
                        complain_msg: str = Form(..., descrition="Send in your complains Ucc office", max_length=500)):

    """make a complaint"""

    form = ValidateForm(request)
    await form.load_data()
    if await form.is_valid()==True:  # if the registration id and email are valid

        try:

            ######  database script goes here   ####

            # email script

            message = "complaint recieved at {}\n\n\n\n YOUR COMPLAINT \n\n{}".format(datetime.datetime.now(),complain_msg)
            model = NotifyUser(message=message, subject=subject, email=email)
            fm = FastMail(model.config)
            await fm.send_message(model.message)

            form.__dict__.update(
                msg="Complaint Sent")

            response = templates.TemplateResponse(
                "success.html", context=form.__dict__)
            return response

        # handle internet connection errors
        except ConnectionErrors:
            form.__dict__.update(
                connection_error="Please Check Your Internet Connection")
            response = templates.TemplateResponse(
                "index.html", context=form.__dict__)
            return response

        except HTTPException:
            raise HTTPException  # temporary command

            # return templates.TemplateResponse(
            #     "success.html",context = form.__dict__)  # should be the redirection html

    form.__dict__.update(msg="")
    form.__dict__.get("errors").append(
        "Incorrect Name or Registration ID")

    return templates.TemplateResponse(
        "success.html",
        form.__dict__)  # should be the redirection html



    # return {"status": "The system is working 24/7"}
