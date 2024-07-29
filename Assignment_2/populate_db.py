from datetime import datetime
from Assignment_2.book_data import Book

# Populate database with fake data
def populate_db(session):
    books = [
        {
            'title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'publication_date': datetime.strptime('1960-07-11', '%Y-%m-%d'),
            'sales_data': '10 million copies sold'
        },
        {
            'title': 'The Lord of the Rings',
            'author': 'J.R.R. Tolkien',
            'publication_date': datetime.strptime('1954-07-29', '%Y-%m-%d'),
            'sales_data': '150 million copies sold'
        },
        {
            'title': 'The Hunger Games',
            'author': 'Suzanne Collins',
            'publication_date': datetime.strptime('2008-09-14', '%Y-%m-%d'),
            'sales_data': '100 million copies sold'
        },
        {
            'title': 'Pride and Prejudice',
            'author': 'Jane Austen',
            'publication_date': datetime.strptime('1813-01-28', '%Y-%m-%d'),
            'sales_data': '20 million copies sold'
        },
        {
            'title': 'The Lion, the Witch and the Wardrobe',
            'author': 'C.S. Lewis',
            'publication_date': datetime.strptime('1950-11-16', '%Y-%m-%d'),
            'sales_data': '85 million copies sold'
        }
    ]

    for book in books:
        new_book = Book(title=book["title"], author=book["author"], publication_date=book["publication_date"], sales_data=book["sales_data"])
        session.add(new_book)
    session.commit()
