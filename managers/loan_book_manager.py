from typing import Dict, Any
from tools.tools import *
from datetime import datetime,timedelta
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

    def add_book_loan(self,book_loan_info:Dict[str,any],book_manager:BookManager) -> Dict[str,str]:
        # sourcery skip: extract-method, remove-redundant-fstring
        """Adds a book loan based on the book loan information provided

        Args:
            book_loan_info (Dict[str,any]): The book loan info

        Returns:
            Dict[str,str]: A message about the book loan added
        """
        if book_manager.obtain_available_copies(book_loan_info["book_code"])>0:
            book_code=book_loan_info["book_code"]
            code=obtain_valid_code("L_",self.collection)
            finish_date=str(book_loan_info["init_date"]+timedelta(days=5))
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
                raise ValueError(f"The insert loan book has failed: {e}") from e
            
            book_manager.update_available_copies(code_book=book_code,return_book=False)
            return {"message": f"The loan with the code: {code} has been added successfully"}
        else: return {"message": f"This book has not copies available"}

    def filtred_loan(self,code:str):
        return list(self.collection.find({"code":code}))

    def update_loan_book(self,code_loan:str) -> bool:
        """Updates the loan book

        Args:
            code_loan (str): The code of the loan book

        Returns:
            bool: Validation of the operation
        """
        update = {"state": "Returned", "return_date": str(datetime.now())}
        self.collection.update_one({"code":code_loan},{"$set":update})
        return True

    def return_book(self,code_loan:str,book_manager:BookManager) -> Dict[str,str]:
        """Updates the state of loan books

        Args:
            code_loan (str): The code of the loan

        Returns:
            Dict[str,str]: Message of the operation
        """
        self.update_loan_book(code_loan=code_loan)
        book_loan_list=self.filtred_loan(code=code_loan)
        book_manager.update_available_copies(code_book=book_loan_list[0]["book_code"],return_book=True)
        return {"message": "The book has been returned successfully"}