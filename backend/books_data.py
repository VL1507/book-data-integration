from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    genre: str
    description: str
    image_filename: str


# База данных в виде списка книг
books_db = [
    Book(
        id=1,
        title="Мастер и Маргарита",
        author="Михаил Булгаков",
        year=1967,
        genre="Роман",
        description="Философский роман о добре и зле",
        image_filename="book1.jpg",
    ),
    Book(
        id=2,
        title="Преступление и наказание",
        author="Фёдор Достоевский",
        year=1866,
        genre="Психологическая драма",
        description="Роман о моральной дилемме и redemption",
        image_filename="book2.jpg",
    ),
    Book(
        id=3,
        title="Война и мир",
        author="Лев Толстой",
        year=1869,
        genre="Эпопея",
        description="Эпопея о жизни русского общества во время войны с Наполеоном",
        image_filename="book3.jpg",
    ),
    Book(
        id=4,
        title="1984",
        author="Джордж Оруэлл",
        year=1949,
        genre="Антиутопия",
        description="Роман-антиутопия о тоталитарном обществе",
        image_filename="book4.jpg",
    ),
    Book(
        id=5,
        title="Гарри Поттер и философский камень",
        author="Джоан Роулинг",
        year=1997,
        genre="Фэнтези",
        description="Первая книга о приключениях юного волшебника",
        image_filename="book5.jpg",
    ),
]
