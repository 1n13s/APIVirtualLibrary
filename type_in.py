from pydantic import BaseModel,Field
from typing import Optional

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
    birth_day:int = Field(ge=1,le=31)
    birth_month:int = Field(ge=1,le=12)
    birth_year:int = Field(ge=1900,le=2024)
    direction:str = Field(min_length=1)
    class Config:
        schema_extra = {
            'example':{
                "name": "Ivonne",
                "age": 23,
                "birth_day": 28,
                "birth_month": 12,
                "birth_year": 2000,
                "direction": "Street Blue #1"
            }
        }


class GetBookFiltred(BaseModel):
    title: Optional[str] = Field(min_length=1)
    author: Optional[str] = Field(min_length=1)
    num_pages: Optional[int] = Field(gt=0)
    gender: Optional[str] = Field(min_length=1)
    clasification: Optional[int] = Field(ge=0,le=5)
    num_copies: Optional[int] = Field(gt=0)
    available_copies: Optional[int] = Field(gt=0)
    code: Optional[str] = Field(min_length=1)
