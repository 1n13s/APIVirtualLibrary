from pydantic import BaseModel,Field, validator
from enum import Enum, IntEnum
from typing import Optional
from datetime import date

class LoanState(str,Enum):
    borrowed="Borrowed"
    on_hold="On_hold"
    returned="Returned"
    renewed="Renewed"
    lost="Lost"
    damaged="Damaged"

class AddBook(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    num_pages: int = Field(gt=0)
    gender: str = Field(min_length=1)
    clasification: int = Field(ge=0,le=5)
    num_copies: int = Field(gt=0)
    available_copies: int = Field(gt=0)
    class Config:
        schema_extra = {
            'example':{
                "title": "The amazing Book",
                "author": "Ivonne",
                "num_pages": 500,
                "gender": "Adventure",
                "clasification": 5,
                "num_copies": 8,
                "available_copies": 8
            }
        }

class AddUser(BaseModel):
    name:str = Field(min_length=1)
    age:int = Field(gt=5)
    birth_date:date
    direction:str = Field(min_length=1)
    class Config:
        schema_extra = {
            'example':{
                "name": "Ivonne",
                "age": 23,
                "birth_date": "2024-05-12",
                "direction": "Street Blue #1"
            }
        }
    @validator('birth_date')
    def inid_date_validation(cls, v):
        if v > date.today():
            raise ValueError('The date should be before today')
        return v

class AddBookLoan(BaseModel):
    book_code:str = Field(min_length=8,max_length=10)
    user_code:str = Field(min_length=8,max_length=10)
    init_date:date
    state:LoanState

    class Config:
        schema_extra={
            'example':{
                "book_code": "A12BC6DE",
                "user_code": "EF12GHIJ",
                "init_date": "2024-08-23",
                "state":"Borrowed | On_hold | Returned | Renewed | Lost | Damaged"
            }
        }

    @validator('init_date')
    def inid_date_validation(cls, v):
        if v < date.today():
            raise ValueError('The date should be after today')
        return v

class GetBookFiltred(BaseModel):
    title: Optional[str] = Field(min_length=1)
    author: Optional[str] = Field(min_length=1)
    num_pages: Optional[int] = Field(gt=0)
    gender: Optional[str] = Field(min_length=1)
    clasification: Optional[int] = Field(ge=0,le=5)
    num_copies: Optional[int] = Field(gt=0)
    available_copies: Optional[int] = Field(gt=0)
    code: Optional[str] = Field(min_length=1)
