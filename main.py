#fastapi dependencies
from email import message
from os import access
from fastapi import (Depends, FastAPI,Body, File, UploadFile,status,Request,Form,Query)
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException

#fastapi_mail dependencies
from fastapi_mail.email_utils import DefaultChecker
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig

#starlette dependencies
from starlette.responses import Response,RedirectResponse,JSONResponse,HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

#pydantic dependencies
from pydantic import BaseModel,Field,EmailStr

#python type hints
from typing import List, Optional,Union

#depency to run fastapi
import uvicorn

#some things are meant to be kept as secrets
from dotenv import dotenv_values

#custom libraries
from notification import NotifyUser,EmailSchema
from regex_validation import ValidateForm

credentials = dotenv_values(".env")
#InVal = InputValidator()
app = FastAPI()



class EmailSchema(BaseModel):
    email: List[EmailStr]

#Universal Fields
class GeneralBioModel(BaseModel):
    name:str
    Registration_Number:str
    email:str


class Program(BaseModel):
    MathematicsandScience:Optional[str] | None
    Education:Optional[str] | None
    Business:Optional[str] | None
    ArtsandSocial:Optional[str] | None


templates = Jinja2Templates(directory="./templates")
app.mount("/templates/js",StaticFiles(directory= "templates/js"),name = "js")
app.mount("/templates/style",StaticFiles(directory= "templates/style"),name = "style")
app.mount("/templates/favicon",StaticFiles(directory= "templates/favicon"),name = "favicon")

# message = {"results":"email"}
message = """<p>'Fixing message repeatetions'</p>"""
subject = "TEST 5"


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html",
                                    #   {"request": request,"message":message})
                                      {"request": request})


@app.post("/accessmodules")
async def accessmodules(*,
                        request: Request, 
                        name:str = Form(...),
                        Registration_Number:str = Form(...),
                        email:List[EmailStr] = Form(...),
                        program:str = Form(...)
                        ):

                    form = ValidateForm(request)
                    await form.load_data()
                    if await form.is_valid(): #if the registration id and email are valid
                        try:
                            form.__dict__.update(msg="An email has been sent to {} :)".format(email))
                            ######  database script goes here   ####

                            #email script
                            model = NotifyUser(message = message,subject = subject,email = email)
                            fm = FastMail(model.config)
                            await fm.send_message(model.message)
                            #response = templates.TemplateResponse("index.html", form.__dict__)  #should be the redirection html
                            return JSONResponse("EMAIL SENT TO {}".format(email))
                            #return response

                        except HTTPException:
                            form.__dict__.update(msg="")
                            form.__dict__.get("errors").append("Incorrect Email or Registration ID")
                            return JSONResponse("Incorrect Email or Registration ID")
                            #return templates.TemplateResponse("auth/login.html", form.__dict__) #should be the redirection html

                    return templates.TemplateResponse("index.html", form.__dict__) #should be the redirection html


@app.post("/makecomplaint")
async def makecomplaint(*,
                        request:Request,
                        program:str = Form(...,description="The program offered by the user"),
                        course:str = Form(...,description = "The course specific to the program given"),
                        study_center:str = Form(...,description = "The study center of the user"),
                        name:str = Form(...),
                        Registration_Number:str = Form(...),
                        email:str = Form(...),
                        complain_msg:str = Form(...,descrition="Send in your complains Ucc office",max_length = 500)):
                        
                        
                        return {"status":"The system is working 24/7"}

@app.post("/mail")
async def mail(email:EmailSchema,message:str,subject):

    model = NotifyUser(message,subject,email)
    fm = FastMail(model.config)
    await fm.send_message(model.message)


    # return response
    return {"status":"email sent"}