from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from fastapi import Request
from typing import List
import re


class ValidateForm:

    """Form validation class; validates user inputs per CoDE's standards
        e.g Student's registration ID at CoDE is always in the format
        >   BECE/CR/01/17/0001"""

    def __init__(self, request: Request):

        self.request: Request = request
        self.errors: List = []
        self.name: Optional[str] = None
        self.regID: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        # since outh works on username field we are considering email as
        # username
        self.name = form.get("name")
        self.regID = form.get("Registration_Number")

    async def is_valid(self):
        """validates inputs provided
            Args:
                None
            Return:
                return True if validation is successful else and HTTPException will be raised according to the
                input Producing the error"""

        # run checks for name field
        if self.name is not None:
            try:
                assert self.validateName().status_code == 200
            except AssertionError:
                raise HTTPException(
                    detail="Provided name is Invalid",
                    status_code=422)
        else:
            self.errors.append("Name is required")

        # run checks for registration id field
        if self.regID is not None:
            try:
                assert self.validateRegID().status_code == 200
            except AssertionError:
                raise HTTPException(
                    detail="Registration ID is Invalid",
                    status_code=422)
        else:
            self.errors.append("A Valid Registration ID is required")

        return True

    def validateName(self):
        """validates Names
        Accepted names > Michael Kofi Armah
        Unacepted names >> ##############################

        Args:
            regID:str: Registration ID

        Return:
            JSONResponse with status code 200 if validation passes
            JSONResponse with status code 400 if validation fails"""

        pattern = "([a-z]+)*( [a-z]+)*( [a-z]+)*$"
        x = re.match(pattern, self.name, re.IGNORECASE)
        
        response = JSONResponse(
            content="Name :{} is Ambigious".format(
                self.name),
            status_code=400) if x is None else JSONResponse(
            content=True,
            status_code=200)
        
        return response

    def validateRegID(self):
        """validates registration ID
        Ensures that registration ID's follow the CoDE's Registration ID convention
        accepted formats >> BECE/CR/01/17/0001 or BPE/WR/01/18/0020

        Args:
            regID:str: Registration ID
        Return:
            JSONResponse with status code 200 if validation passes
            JSONResponse with status code 400 if validation fails"""

        pattern = "[A-Z]+/[A-Z]+/[0-9]+/[0-9]+/[0-9]+[0-9]"
        x = re.match(pattern, self.regID)
        
        response = JSONResponse(
            content="Invalid Registration ID {}".format(
                self.regID), status_code=400) if x is None else JSONResponse(
            content=True, status_code=200)
        
        return response
