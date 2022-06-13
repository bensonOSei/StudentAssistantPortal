<<<<<<< HEAD
import re
from fastapi.responses import JSONResponse

class InputValidator:

    def NameStr(self,name):
        """validates Names
            Ensures that registration ID's (string) follow the convention below
        >>> BECE/CR/01/17/0001
        
        Args:
            regID:str: Registration ID

        Return:
            JSONResponse with status code 200 if validation passes
            JSONResponse with status code 400 if validation fails"""
        pattern = "([a-z]+)*( [a-z]+)*( [a-z]+)*$"
        x = re.match(pattern,name,re.IGNORECASE)
        
        try:
            assert x!=None
        except AssertionError:
            return JSONResponse({"message":"Provided name is Ambigious, Name should not contain numbers and symbols"}, status_code = 400)
        else:
            return JSONResponse(True,status_code = 200)
        
    def regID(self,regID):
        """validates registration ID
            Ensures that registration ID's follow the convention below
        >>> BECE/CR/01/17/0001
        
        Args:
            regID:str: Registration ID

        Return:
            JSONResponse with status code 200 if validation passes
            JSONResponse with status code 400 if validation fails"""
        
        pattern = "[A-Z]+/[A-Z]+/[0-9]+/[0-9]+/[0-9]+[0-9]"
        x = re.match(pattern,regID)
        
        try:
            assert x!=None
        except AssertionError:
            # print("Registration ID is Invalid")
            return JSONResponse("Invalid Registration ID {}".format(regID),status_code = 400) #status code 400 is used for generic client error
        else:
            return JSONResponse(True,status_code = 200)
        
    

if __name__ == "__main__":
    # validator = InputValidator()
    #output = validator.regID("BECEjk/CR/01/17/0001")
    # # print(output.status_code)
    # print(output.message)

    validator = InputValidator()
    output = validator.name("michael kofi armah junior")
    print(output.status_code)