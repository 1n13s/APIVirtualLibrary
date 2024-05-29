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
        try:
            return {"books":list(self.collection.find({},{"_id":0}))}
        except Exception as err:
            # sourcery skip: raise-specific-error
            raise Exception(f"Get books failed: {err}") from err
    
    def get_books_filtred(self,book_queries:Dict[str,any]) -> Dict[str,List[Dict[str,any]]]:
        """
            Provides some books filtred in the Mongo Database
            Args:
                book_queries(Dict[str,any]): The filter data
        """
        query=obtain_query(book_queries)
        try:
            return{"books":(list(self.collection.find(query,{"_id":0})))}
        except Exception as err:
            # sourcery skip: raise-specific-error
            raise Exception(f"Get books failed: {err}") from err
    
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
        try:
            self.collection.update_one(query, new_values, upsert=True)
            return {"message": f"The book has been added successfully with the code {code}"}
        except Exception as err:
            # sourcery skip: raise-specific-error
            raise Exception(f"Add book failed: {err}") from err
        
    def obtain_available_copies(self,code_book:str)->int:
        """Obtains the available copies of a book

        Args:
            code_book (str): The code of the book

        Returns:
            int: Number of available copies
        """
        try:
            book_filtred=self.get_books_filtred({"code":code_book})
            book_info=book_filtred["books"]
            return book_info[0]["available_copies"]
        except Exception as err:
            # sourcery skip: raise-specific-error
            raise Exception(f"Obtain available copies book failed: {err}") from err

    def update_available_copies(self,code_book:str,return_book:bool) -> bool:
        """Updates the available copies from a book

        Args:
            code_book (str): The code of the book
            return_book (bool): Evaluates whether the available copy will be increased or not

        Returns:
            bool: Validation of the operation
        """
        available_copies_set=self.obtain_available_copies(code_book=code_book)
        if return_book: available_copies_set+=1
        else: available_copies_set-=1
        try:
            self.collection.update_one({"code":code_book},{"$set":{"available_copies":available_copies_set}})
        except Exception as e:
            raise ValueError(f"The book update has failed: {e}") from e

    def validation_existing_code(self, book_code:str)->bool:
        """Validates if the book code exists

        Args:
            code_book (str): The code of the book

        Returns:
            bool: Validation of the operation
        """
        try:
            query={"code":book_code}
            book=list(self.collection.find(query))
            return bool(len(book))
        except Exception as err:
            # sourcery skip: raise-specific-error
            raise Exception(f"Validate existing code failed: {err}") from err

    """def correction_code(self,books_dic):
            book_list=books_dic["books"]
            for book_info in book_list:
                #query={"title":book_info["title"]}
                #set_={"num_pages":obtain_pages(),"code":obtain_valid_code(book_info["title"][0].upper(),self.books_collection)}
                self.collection.update_one(
                    {
                        "code":book_info["code"]
                    },
                    {
                        "$set":
                            {
                                "code":obtain_valid_code(
                                    "B_",
                                    self.collection
                                    )
                            }
                    }
                )"""



