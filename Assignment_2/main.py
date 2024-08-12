from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from book_data import book_data
from api_key import validate_api_keys
from book_model import BookModel

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database setup
engine = create_engine("sqlite:///books.db")
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publication_date = Column(DateTime, nullable=False)
    sales_data = Column(String, nullable=False)

Base.metadata.create_all(engine)

# Populate database with fake data
def populate_db():
    session = Session()
    books = book_data
    for book in books:
        new_book = Book(title=book["title"], author=book["author"], publication_date=book["publication_date"], sales_data=book["sales_data"])
        session.add(new_book)
    session.commit()

# Delete all records from the books table
def clean_db():
    session = Session()
    session.query(Book).delete()
    session.commit()

# The DB is already setup and populated, so we don't need to run these functions every time the app starts
# If you need to clean the data, uncomment the clean_db() function
# clean_db()
# populate_db()


# API endpoints
@app.get("/books/")
def read_books(api_key: str = Depends(validate_api_keys)):
    session = Session()
    books = session.query(Book).all()
    return JSONResponse(content=[{"id": book.id, "title": book.title, "author": book.author, "publication_date": book.publication_date.strftime('%Y-%m-%d'), "sales_data": book.sales_data} for book in books])

@app.get("/books/{book_id}")
def read_book(book_id: int, api_key: str = Depends(validate_api_keys)):
    session = Session()
    book = session.query(Book).get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return JSONResponse(content={
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "publication_date": book.publication_date.strftime('%Y-%m-%d'),
        "sales_data": book.sales_data
    })

    
@app.post("/books/")
def create_book(book: BookModel, api_key: str = Depends(validate_api_keys)):
    session = Session()

    new_book = Book(
        title=book.title, 
        author=book.author, 
        publication_date=datetime.strptime(book.publication_date, '%Y-%m-%d'), 
        sales_data=book.sales_data
    )
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    
    return JSONResponse(content={
        "id": new_book.id,
        "title": new_book.title,
        "author": new_book.author,
        "publication_date": new_book.publication_date.strftime('%Y-%m-%d'),
        "sales_data": new_book.sales_data
    }, status_code=201)

@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookModel, api_key: str = Depends(validate_api_keys)):
    session = Session()
    
    existing_book = session.query(Book).get(book_id)
    
    if existing_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    existing_book.title = book.title
    existing_book.author = book.author
    existing_book.publication_date = datetime.strptime(book.publication_date, '%Y-%m-%d')
    existing_book.sales_data = book.sales_data
    
    session.commit()
    
    return JSONResponse(content={
        "id": existing_book.id,
        "title": existing_book.title,
        "author": existing_book.author,
        "publication_date": existing_book.publication_date.strftime('%Y-%m-%d'),
        "sales_data": existing_book.sales_data
    })
    

@app.delete("/books/{book_id}")
def delete_book(book_id: int, api_key: str = Depends(validate_api_keys)):
    session = Session()
    
    existing_book = session.query(Book).get(book_id)
    
    if existing_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    session.delete(existing_book)
    session.commit()

    return JSONResponse(content={"message": "Book deleted successfully"}, status_code=200)