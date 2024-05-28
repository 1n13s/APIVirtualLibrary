from typing import Dict, Any
import random
import string


def obtain_valid_code(first_letter:str,collection:any) -> str:
    code_repeated=True
    while code_repeated:
        code=first_letter+generate_code(7)
        if not validate_code(code,collection): code_repeated=False
    return code

def generate_code(large:int) -> str:
    chars = string.ascii_letters.upper() + string.digits
    return ''.join(random.choice(chars) for _ in range(large))

def validate_code(code:str,collection:any) -> bool:
        return bool(list(collection.find({"code": code})))

def obtain_query(data_query:Dict[str,any]) -> Dict[str,any]:
        """
            Provides the query to use in the filter based on the keys in the dictionary
            Args:
                book_queries(Dict[str,any]): The filter data
        """
        keys=data_query.keys()
        query={}
        for key in keys:
            if data_query[key] is not None:
                query |= {key:{"$regex":data_query[key]}}
        return query


"""
def obtain_pages() :
    return random.randint(50, 350)

def random_pages_code(self,books_dic):
        book_list=books_dic["books"]
        for book_info in book_list:
            #query={"title":book_info["title"]}
            #set_={"num_pages":obtain_pages(),"code":obtain_valid_code(book_info["title"][0].upper(),self.books_collection)}
            self.books_collection.update_one(
                {
                    "title":book_info["title"]
                },
                {
                    "$set":
                        {
                            "num_pages":obtain_pages(),
                            "code":obtain_valid_code(
                                book_info["title"][0].upper(),
                                self.books_collection
                                )
                        }
                }
            )
"""