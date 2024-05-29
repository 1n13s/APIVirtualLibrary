from typing import Dict, Any
from tools.tools import *

class UserManager:
    """
        This Class provides de managment of the user collection
    """

    def __init__(self,collection:any) -> None:
        """
            Initializes the object with the parameter collection, saving the users_collection

            Args:
                collection(any): Is the users_collection from the MongoDB
        """
        self.collection=collection

    def add_user(self,user_info: Dict[str, Any],is_admin=bool) -> Dict[str, str]:
        """
            Adds an user or admin with the data provided

            Args:
                user_info(Dict[str, Any]): The user info.

            Returns:
                Dict[str, str]: The message before the user addition
        """
        role = "admin" if is_admin else "user"
        code = obtain_valid_code("U_" if role=="user" else "A_",self.collection)
        query={
            "name": user_info["name"],
            "code": code,
            "age": user_info["age"],
            "birth_day": str(user_info["birth_date"]),
            "direction":user_info["direction"],
            "role":role
        }
        new_values = {"$set": query}
        try:
            self.collection.update_one(query, new_values, upsert=True)
        except Exception as e:
            raise f"The instert user has failed {e}" from e
        return {"message": f"{role} added successfully"}

    def validation_existing_code(self, user_code:str)->bool:
        """Validates if the user code exists

        Args:
            code_book (str): The code of the book

        Returns:
            bool: Validation of the operation
        """
        try:
            query={"code":user_code}
            user=list(self.collection.find(query))
            return bool(len(user))
        except Exception as err:
            # sourcery skip: raise-specific-error
            raise Exception(f"Validation existing code failed: {err}") from err  

