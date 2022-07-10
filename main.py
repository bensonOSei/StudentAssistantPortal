"""
FastAPI Backend
Author : Michael Kofi Armah
"""

# fastapi dependencies
from temp import load_json
from email import message

from fastapi import (
    Depends,
    FastAPI,
    Body,
    status,
    Request,
    Form,
    Query)

from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException

# fastapi_mail dependencies
from fastapi_mail import FastMail
from fastapi_mail.connection import ConnectionErrors

# starlette dependencies
from starlette.responses import Response, JSONResponse, HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

# pydantic dependencies
from pydantic import BaseModel, Field, EmailStr

# python type hints
from typing import List, Optional
# dependency to run fastapi


# custom libraries
from notification import (
    NotifyUser,
    EmailSchema,
    complaint_email_msg,
    complaint_email_subj,
    access_module_message,
    access_module_subj
)

from regex_validation import ValidateForm

# other

# from sqlite_db.database import SessionLocal, engine
# from sqlite_db import db_models
# from sqlalchemy.orm import Session
# import sqlite_db.services as services

import json
import datetime
from google_sheets_plugin.gsheets import GoogleSheets
from google.auth.exceptions import TransportError
import os
from dotenv import dotenv_values, load_dotenv
import json

load_dotenv(".env")
GOOGLE_SHEET_NAME = os.environ.get("GOOGLE_SHEET_NAME")
GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID")

# credentials = dotenv_values(".env")

# services.create_database() #creates an sqlite db

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


class ComplaintSchema(GeneralBioModel):
    course: str = Form(...)
    study_center: str = Form(...)
    name: str = Form(...)
    Registration_Number: str = Form(...)
    email: List[EmailStr] = Form(...)
    complain_msg: str = Form(...)


templates = Jinja2Templates(directory="./templates")

app.mount(
    "/templates/js",
    StaticFiles(
        directory="templates/js"),
    name="js")

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


async def get_resources():
    with open("resources.json", "r") as jfile:
        file = json.load(jfile)
    return file


@app.get("/")
async def index(request: Request, resources=Depends(get_resources)):
    """Program Homepage"""
    # with open("resources.json","r") as jfile:
    #     file = json.load(jfile)
    load_json()

    return templates.TemplateResponse(
        "index.html", {
            "request": request, "resources": resources})


@app.get("/status")
async def form_status(request: Request):
    """Returns the status of the request after submission"""
    return templates.TemplateResponse("success.html", {"request": request})


def get_strtime():
    time = datetime.datetime.now()
    time = "{} | {} | {} - {}:{}:{}".format(time.day,
                                            time.month,
                                            time.year,
                                            time.hour,
                                            time.minute,
                                            time.second)
    return str(time)


@app.post("/accessmodules")
async def accessmodules(*,
                        request: Request,
                        name: str = Form(...),
                        Registration_Number: str = Form(...),
                        email: List[EmailStr] = Form(...),
                        program: str = Form(...),
                        ):

    """access course modules"""

    # to do : Take email validation from parameters of this function to the
    # regex_validation

    form = ValidateForm(request)
    await form.load_data()
    if await form.is_valid() == True:  # if the registration id and email are valid

        try:

            ###### database script goes here   ####

            # email script
            email: List[EmailStr]
            time = get_strtime()

            message = access_module_message.format(time)
            model = NotifyUser(message=message,
                               subject=access_module_subj, email=email)

            fm = FastMail(model.config)
            await fm.send_message(model.message)

            form.__dict__.update(
                msg="Requesting modules is currently unavailable")

            response = templates.TemplateResponse(
                "success.html", context=form.__dict__)
            return response

        # handle internet connection errors

        except ConnectionErrors:
            resources = await get_resources()
            form.__dict__.update(
                connection_error="Please Check Your Internet Connection",
                resources=resources)
            response = templates.TemplateResponse(
                "index.html", context=form.__dict__)
            return response

    form.__dict__.update(msg="")
    form.__dict__.get("errors").append(
        "Incorrect Name or Registration ID")

    return templates.TemplateResponse(
        "success.html",
        form.__dict__)  # should be the redirection html


@app.post("/makecomplaint")
async def makecomplaint(*,
                        request: Request,
                        program: str = Form(...,
                                            description="The program offered by the student"),
                        course: str = Form(...,
                                           description="The course specific to the program given"),
                        study_center: str = Form(...,
                                                 description="The study center of the student"),
                        name: str = Form(...),
                        Registration_Number: str = Form(...),
                        email: List[EmailStr] = Form(...),
                        complain_msg: str = Form(...,
                                                 descrition="Send in your complains Ucc office",
                                                 max_length=500),
                        # db: Session = Depends(services.get_db)
                        ):

    """make a complaint"""
    resources = await get_resources()
    
    form = ValidateForm(request)
    await form.load_data()
    if await form.is_valid() == True:  # if the registration id and email are valid

        try:
            ###generate token #####
            index = Registration_Number.split("/")[3]
            token = "CoDE-{}-{}".format(index,
                                        datetime.datetime.now().timestamp())

            ######  database script   ####
            # db_client = db_models.Complaint(program = program,
            #                     token = token,
            #                     course = course,
            #                     study_center = study_center,
            #                     name = name,
            #                     registration_id = Registration_Number,
            #                     email = email[0],
            #                     complaint = complain_msg)

            # db.add(db_client)
            # db.commit()
            # db.refresh(db_client)

            # google sheets
            # load_json()

        
            GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_CREDENTIALS")
            GOOGLE_CREDENTIALS = dict(json.loads(GOOGLE_CREDENTIALS)) #load environment as string with json and convert to dict

            google_sheets = GoogleSheets(
                            credentials_file= GOOGLE_CREDENTIALS, #credentials_file,
                            sheet_key = os.environ.get("GOOGLE_SHEET_ID"),
                            worksheet_name = os.environ.get('GOOGLE_SHEET_NAME'))

            
            study_center = resources['study centers'].get(study_center)
            program = resources['programs'].get(program)
            course = resources['courses'].get(course)

            google_sheets.write_header_if_doesnt_exist([
                "token",
                "Program",
                "Course",
                "Study_Center",
                "Name",
                "Registration_ID",
                "Email",
                "Complaint",
                "log_time"])

            #time = get_strtime()
            time = str(datetime.datetime.now())

            form_ = await request.form()
            google_sheets.append_rows([[token,
                                        program,
                                        course,
                                        study_center,
                                        name,
                                        Registration_Number,
                                        email[0],
                                        complain_msg,
                                        time]])

            # email script

            message = complaint_email_msg.format(
                name=name, token=token, stamp= time, complaint_msg=complain_msg)

            model = NotifyUser(
                message=message,
                subject=complaint_email_subj,
                email=email)
            fm = FastMail(model.config)
            await fm.send_message(model.message)

            form.__dict__.update(
                msg="Complaint Sent")

            response = templates.TemplateResponse(
                "success.html", context=form.__dict__)
            return response

        # handle internet connection errors
        # ConnectError ==> Email
        # TransportError ==> Google api

        except (ConnectionErrors, TransportError) as internet_connection_error:

            # with open("resources.json","r") as jfile:
            #     resources = json.load(jfile)

            # resources = await get_resources()
            form.__dict__.update(
                connection_error="Please Check Your Internet Connection",
                resources=resources)

            response = templates.TemplateResponse(
                "index.html", context=form.__dict__)
            return response

    form.__dict__.update(msg="")
    form.__dict__.get("errors").append(
        "Incorrect Name or Registration ID")

    return templates.TemplateResponse(
        "success.html",
        form.__dict__)  # should be the redirection html


# @app.get("/database")
# def check_db(db: Session = Depends(services.get_db)):
#     output = db.query(db_models.Complaint)
#     return {"state": output.all()}
