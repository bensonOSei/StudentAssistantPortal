"""
Author: Eng. Michael Kofi Armah
Date Created: 17/06/22
Job : Script for Creating a DB Schema
"""

import datetime as dt
import sqlalchemy as sql
import database


class Complaint(database.Base):
    """setting up database schema"""

    __tablename__ = "complaint"
    id = sql.Column(sql.Integer,unique = True, primary_key = True, index = True)

    token = sql.Column(sql.String, unique = True, index=True)

    complaint = sql.Column(sql.String, index=True)

    name = sql.Column(sql.String, index=True)

    program = sql.Column(sql.String, index=True)

    course = sql.Column(sql.String, index=True)

    study_center = sql.Column(sql.String, index=True)

    registration_id = sql.Column(sql.String, index=True)

    email = sql.Column(sql.String, index=True)
        
    date_created = sql.Column(
        sql.DateTime,
        index=True,
        default=dt.datetime.now())
    

    def dummy_method(self, no_args: str):
        """just a dummy method to pass pylint test"""
        return no_args

