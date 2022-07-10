from __future__ import print_function
from http.client import HTTPException

import os.path
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List

import dotenv
from dotenv import dotenv_values
credentials = dotenv_values(".env")


class GoogleSheets:
    """Google Sheets Class"""

    def __init__(self, credentials_file: str, sheet_key: str, worksheet_name: str):
        self.credentials_file = credentials_file
        self.sheet_key = sheet_key
        self.worksheet_name = worksheet_name
        self.scope = [
            "https://spreadsheets.google.com/feeds",
        ]
        self.sheet_object = self._get_sheet_object()

    def _get_sheet_object(self): #-> gspread.models.Worksheet:
        """get google sheet object"""

        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            self.credentials_file, self.scope
        )

        client = gspread.authorize(credentials)

        return client.open_by_key(self.sheet_key).worksheet(self.worksheet_name)

    def write_header_if_doesnt_exist(self, columns: List[str]) -> None:
        """write the columns for the google sheet if there is None """

        data = self.sheet_object.get_all_values()
        if not data:
            self.sheet_object.insert_row(columns)

    def append_rows(self, rows: List[List]) -> None:
        """append rows to google sheet"""

        last_row_number = len(self.sheet_object.col_values(1)) + 1
        self.sheet_object.insert_rows(rows, last_row_number)

    
if __name__== "__main__":
    google_sheets = GoogleSheets(
                                credentials_file= "gsheets_keys.json",
                                sheet_key = credentials["GOOGLE_SHEET_ID"],
                                worksheet_name = credentials['GOOGLE_SHEET_NAME'])

    google_sheets.write_header_if_doesnt_exist(["Program","Course","Study_Center","Name","Registration_ID","Email","Complaint"])
    google_sheets.append_rows([["Education","Early Childhood","Cape Coast","Michael Kofi Armah","BECE/CR/01/17/0001","mikeyarmah@gmail.com","modules"]])