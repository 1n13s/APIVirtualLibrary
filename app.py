from typing import List
from fastapi import FastAPI
from starlette import status
from database.database_connection import DatabaseConnection
from managers.users_manager import UserManager
from managers.books_manager import BookManager
from managers.loan_book_manager import LoanBookManager
from type_in import *
import uvicorn


DATABASE=DatabaseConnection()
USERS=UserManager(DATABASE.users_collection)
BOOKS=BookManager(DATABASE.books_collection)
LOANS=LoanBookManager(DATABASE.book_loans_collection)

app = FastAPI()

@app.get("/",status_code=status.HTTP_200_OK)
def read_root():
    return {"Hello": "World"}

@app.get("/get_books",status_code=status.HTTP_200_OK)
def get_books():
    """Gets all books"""
    return BOOKS.get_books()

@app.post("/get-books_filtred",status_code=status.HTTP_200_OK)
def get_books(filter_book:GetBookFiltred):
    """
        Gets books with a filter
    """
    return BOOKS.get_books_filtred(dict(filter_book))


@app.post("/add-book",status_code=status.HTTP_201_CREATED)
def add_books(book: AddBook):
    """
        Adds a book
    """
    return BOOKS.add_book(dict(book))

@app.post("/add-user",status_code=status.HTTP_201_CREATED)
def add_user_endpoint(user: AddUser):
    """
        Adds an user
    """
    return USERS.add_user(dict(user),False)

@app.post("/add-admin",status_code=status.HTTP_201_CREATED)
def add_admin_endpoint(user: AddUser):
    """
        Adds an admin
    """
    return USERS.add_user(dict(user),True)

@app.post("/add-loan-request",status_code=status.HTTP_201_CREATED)
def loan_request(loan: AddBookLoan):
    """Adds a book loan with the boos and user data

    Args:
        loan (AddBookLoan): The book loan data.

    Returns:
        _type_: _description_
    """
    return LOANS.add_book_loan(dict(loan))

@app.post("/return-request")
def return_request(book: AddBook):
    # Implement logic for return request
    return {"message": f"Return request for book '{book.title}' received"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
