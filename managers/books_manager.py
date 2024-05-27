from typing import Dict, Any, List
from tools import *
from tools.tools import *

class BookManager:
    """
        This Class provides de managment of the book collection
    """
    def __init__(self,collection:any) -> None:
        """
            Initializes the object with the parameter collection, saving the books_collection

            Args:
                collection(any): Is the books_collection from the MongoDB
        """
        self.collection=collection
    
    def get_books(self) -> Dict[str,List[Dict[str,any]]]:
        """
            Provides all the books in the Mongo Database
        """
        return {"books":list(self.collection.find({},{"_id":0}))}
    
    def get_books_filtred(self,book_queries:Dict[str,any]) -> Dict[str,List[Dict[str,any]]]:
        """
            Provides some books filtred in the Mongo Database
            Args:
                book_queries(Dict[str,any]): The filter data
        """
        query=obtain_query(book_queries)
        return{"books":(list(self.collection.find(query,{"_id":0})))}
           
    def add_book(self,book_info: Dict[str,any]) -> Dict[str,str]:
        """
            Adds a book in the MongoDB

            Args:
                book_info(Dict[str,any]): The book data
        """
        code=obtain_valid_code("B_",self.collection)
        query={
            "title":book_info["title"],
            "author":book_info["author"],
            "num_pages":book_info["num_pages"],
            "gender":book_info["gender"],
            "clasification":book_info["clasification"],
            "num_copies":book_info["num_copies"],
            "available_copies":book_info["available_copies"],
            "code":code
        }
        new_values = {"$set": query}
        self.collection.update_one(query, new_values, upsert=True)
        return {"message": f"The book has been added successfully with the code {code}"}
    
    def valid_available_copies(self,code_book:str) -> bool:
        """Validates if the book to loan has an available copy

        Args:
            code_book (str): The code of the book

        Returns:
            bool: Validation
        """
        book_filtred=self.get_books_filtred({"code":code_book})
        book_info=book_filtred["books"]
        return book_info[0]["available_copies"] > 0




