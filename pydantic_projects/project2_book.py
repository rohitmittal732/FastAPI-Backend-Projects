from fastapi import FastAPI,Query,HTTPException,status
from pydantic import BaseModel
from typing import Optional,Annotated

app=FastAPI()

class Book(BaseModel):
    name:str
    page:int
    paragraph:str
    contents:Optional[str]=None
    

my_book=[{"name":"atomic habits","page":1,"paragraph":
          "the more attractive an opportunity is,the more likely it is to be come habit forming."},
         {"name":"atomic habits","page":2,"paragraph":"prime your future to make future actions easier"}]

@app.post("/book")
def post_book(bk:Book):
    data=bk.model_dump()
    my_book.append(data)
    return data
   

@app.get("/book")
def get_book():
    return my_book

@app.get("/book/{book_page}")
def get_id(book_page:int):
    for book in my_book:
        if(book_page==book["page"]):
            return book
    return{"message":"page not found"}

@app.put("/book/{book_page}")
def updated_book(book_page:int,bk:Book):
    data=bk.model_dump()
    for i in range(len(my_book)):
        if my_book[i]["page"]==book_page:
            data["page"]=book_page
            my_book[i].update(data)
            return my_book[i]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{book_page} is not found")

@app.delete("/book/{book_page}",status_code=status.HTTP_200_OK)
def deleted_book(book_page:int):
    for i in range(len(my_book)):
        if my_book[i]["page"]==book_page:
            my_book.pop(i)
            return f"book deleted successfully for index{book_page}"
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{book_page} is not found")

            
    
    
    


    

