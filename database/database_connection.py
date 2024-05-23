from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
CONNECTION_STRING=os.getenv("CONNECTION_STRING")
class DatabaseConnection:
    def __init__(self) -> None:
        self.connection_string=CONNECTION_STRING
        self.client = MongoClient(self.connection_string)
        self.data_base_name=self.client["library"]
        self.books_collection=self.data_base_name["books"]
        self.book_loans_collection=self.data_base_name["book_oans"]
        self.users_collection=self.data_base_name["users"]
        