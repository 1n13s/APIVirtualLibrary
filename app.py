from typing import List
from fastapi import FastAPI
from database.database_connection import DatabaseConnection
from managers.users_manager import UserManager
from managers.books_manager import BookManager
from type_in import *
import uvicorn


DATABASE=DatabaseConnection()
USERS=UserManager(DATABASE.users_collection)
BOOKS=BookManager(DATABASE.books_collection)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/get_books")
def get_books():
    """Gets all books"""
    return BOOKS.get_books()

@app.post("/get-books_filtred")
def get_books(filter_book:GetBookFiltred):
    """
        Gets books with a filter
    """
    return BOOKS.get_books_filtred(dict(filter_book))


@app.put("/add-book")
def add_books(book: AddBook):
    """
        Adds a book
    """
    return BOOKS.add_book(dict(book))

@app.put("/add-user")
def add_user_endpoint(user: AddUser):
    """
        Adds an user
    """
    return USERS.add_user(dict(user),False)

@app.put("/add-admin")
def add_admin_endpoint(user: AddUser):
    """
        Adds an admin
    """
    return USERS.add_user(dict(user),True)

@app.post("/loan-request")
def loan_request(book: AddBook):
    # Implement logic for loan request
    return {"message": f"Loan request for book '{book.title}' received"}

@app.post("/return-request")
def return_request(book: AddBook):
    # Implement logic for return request
    return {"message": f"Return request for book '{book.title}' received"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
