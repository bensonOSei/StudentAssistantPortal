#fastapi dependencies
from email import message
from os import access
from fastapi import (Depends, FastAPI,Body, File, UploadFile,status,Request,Form,Query)
from fastapi.staticfiles import StaticFiles

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

credentials = dotenv_values(".env")



app = FastAPI()

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
                        

                        model = NotifyUser(message = message,subject = subject,email = email)
                        fm = FastMail(model.config)
                        
                        await fm.send_message(model.message)
                        
                        return {"bio":{"name":name,"Registration Number":Registration_Number,"email":email},"program":program}
                        #will return url_for(index) with a pop message display


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



class EmailSchema(BaseModel):
    email: List[EmailStr]


@app.post("/mail")
async def mail(email:EmailSchema,message:str,subject):


    model = NotifyUser(message,subject,email)
    fm = FastMail(model.config)
    await fm.send_message(model.message)


    # return response
    return {"status":"email sent"}