"""
Author: Michael Kofi Armah
Description:For validating user inputs in other to avoid cyber attacks on the expose form
"""

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

        """get name and registration number from html inputs"""

        form = await self.request.form()

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
        if self.name or self.regID is not None:

            try:
                validate_name = self.validateName()
                assert validate_name.status_code == 200
            except AssertionError:
                return validate_name

        # run checks for registration id field
            try:  
                validate_regid = self.validateRegID()
                assert validate_regid.status_code == 200
            except AssertionError:
                return validate_regid

        else:
            self.errors.append("Name and Valid Registration ID Fields are required")

        return True

    def validateName(self):
        """validates Names
        Accepted names > Michael Kofi Armah
        Unacepted names >> Any name with symbols
        Args:
            None
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
            None
        Return:
            JSONResponse with status code 200 if validation passes
            JSONResponse with status code 400 if validation fails"""

        pattern = "[A-Z]+/[A-Z]+/[0-9]+/[0-9]+/[0-9]+[0-9]"
        try:
            x = re.match(pattern, self.regID)
            assert x is not None
            response= JSONResponse(content=True, status_code=200)

        except AssertionError:
            response = JSONResponse(content="Invalid Registration ID {}".format(
                self.regID), status_code=400)
                
        return response
