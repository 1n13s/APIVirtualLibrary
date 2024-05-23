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
        #month=user_info["birth_month"]
        #year=user_info["birth_year"]
        #birth_date=(str(f"{year}-{month}-{day}"))

        role = "admin" if is_admin else "user"
        query={
            "name": user_info["name"],
            "code": obtain_valid_code(user_info["name"][0].upper(),self.collection),
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

