from typing import Dict, Any
from tools.tools import *
from datetime import timedelta
from managers.books_manager import BookManager
from database.database_connection import DatabaseConnection

class LoanBookManager:
    """This Class provides de managment of the loan book collection"""
    def __init__(self,collection) -> None:
        """
            Initializes the object with the parameter collection, saving the books_collection

            Args:
                collection(any): Is the book_loans_collection from the MongoDB
        """
        self.collection=collection

    def add_book_loan(self,book_loan_info:Dict[str,any]) -> Dict[str,str]:
        """Adds a book loan based on the book loan information provided

        Args:
            book_loan_info (Dict[str,any]): The book loan info

        Returns:
            Dict[str,str]: A message about the book loan added
        """
        db=DatabaseConnection()
        book_manager=BookManager(db.books_collection)
        if book_manager.valid_available_copies(book_loan_info["book_code"]):
            code=obtain_valid_code("L_",self.collection)
            finish_date=str(book_loan_info["init_date"]-timedelta(days=5))
            query={
                "book_code":book_loan_info["book_code"],
                "user_code":book_loan_info["user_code"],
                "init_date":str(book_loan_info["init_date"]),
                "finish_date":finish_date,
                "code":code,
                "state":book_loan_info["state"]
            }
            new_values = {"$set": query}
            try:
                self.collection.update_one(query, new_values, upsert=True)
            except Exception as e:
                raise ValueError(f"The insert user has failed: {e}") from e
            return {"message": f"The loan with the code: {code} has been added successfully"}
        else: return {"message": f"This book has not copies available"}
