from typing import List, Optional


class Book:
    def __init__(self, title: str, author: str, year: int) -> None:
        self.__title = title
        self.__author = author
        self.__year = year
        self.__available = True

    def get_title(self) -> str:
        return self.__title

    def get_author(self) -> str:
        return self.__author

    def get_year(self) -> int:
        return self.__year

    def is_available(self) -> bool:
        return self.__available

    def mark_as_taken(self) -> None:
        self.__available = False

    def mark_as_returned(self) -> None:
        self.__available = True

    def __str__(self) -> str:
        status = "доступна" if self.__available else "выдана"
        return f'"{self.__title}" — {self.__author} ({self.__year}) [{status}]'


class PrintedBook(Book):
    def __init__(self, title: str, author: str, year: int,
                 pages: int, condition: str) -> None:
        super().__init__(title, author, year)
        self.pages = pages
        self.condition = condition

    def repair(self) -> None:
        if self.condition == "плохая":
            self.condition = "хорошая"
        elif self.condition == "хорошая":
            self.condition = "новая"

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | {self.pages} стр., состояние: {self.condition}"


class EBook(Book):
    def __init__(self, title: str, author: str, year: int,
                 file_size: float, file_format: str) -> None:
        super().__init__(title, author, year)
        self.file_size = file_size
        self.file_format = file_format

    def download(self) -> None:
        print(f"Книга '{self.get_title()}' загружается... ({self.file_size} МБ, формат {self.file_format})")

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | {self.file_size} МБ, формат: {self.file_format}"


class User:
    def __init__(self, name: str) -> None:
        self.name = name
        self.__borrowed_books: List[Book] = []

    def borrow(self, book: Book) -> bool:
        if not book.is_available():
            print(f"Книга '{book.get_title()}' сейчас недоступна.")
            return False
        book.mark_as_taken()
        self.__borrowed_books.append(book)
        print(f"{self.name} взял(а) книгу: {book.get_title()}")
        return True

    def return_book(self, book: Book) -> bool:
        if book not in self.__borrowed_books:
            print(f"{self.name} не брал(а) книгу: {book.get_title()}")
            return False
        book.mark_as_returned()
        self.__borrowed_books.remove(book)
        print(f"{self.name} вернул(а) книгу: {book.get_title()}")
        return True

    def show_books(self) -> None:
        if not self.__borrowed_books:
            print(f"У пользователя {self.name} нет взятых книг.")
            return
        print(f"Книги пользователя {self.name}:")
        for book in self.__borrowed_books:
            print(" •", book)

    def get_borrowed_books(self) -> List[Book]:
        return list(self.__borrowed_books)


class Librarian(User):
    def add_book(self, library: "Library", book: Book) -> None:
        library.add_book(book)
        print(f"Библиотекарь {self.name} добавил(а) книгу: {book.get_title()}")

    def remove_book(self, library: "Library", title: str) -> None:
        removed = library.remove_book(title)
        if removed:
            print(f"Библиотекарь {self.name} удалил(а) книгу: {title}")
        else:
            print(f"Книга '{title}' не найдена. Удалить не удалось.")

    def register_user(self, library: "Library", user: User) -> None:
        library.add_user(user)
        print(f"Библиотекарь {self.name} зарегистрировал(а) пользователя: {user.name}")


class Library:
    def __init__(self) -> None:
        self.__books: List[Book] = []
        self.__users: List[User] = []

    def add_book(self, book: Book) -> None:
        self.__books.append(book)

    def remove_book(self, title: str) -> bool:
        for book in self.__books:
            if book.get_title() == title:
                if not book.is_available():
                    print(f"Нельзя удалить книгу '{title}', она сейчас выдана.")
                    return False
                self.__books.remove(book)
                return True
        return False

    def find_book(self, title: str) -> Optional[Book]:
        for book in self.__books:
            if book.get_title() == title:
                return book
        return None

    def show_all_books(self) -> None:
        if not self.__books:
            print("В библиотеке нет книг.")
            return
        print("Все книги в библиотеке:")
        for book in self.__books:
            print(" •", book)

    def show_available_books(self) -> None:
        available = [book for book in self.__books if book.is_available()]
        if not available:
            print("Нет доступных книг.")
            return
        print("Доступные книги:")
        for book in available:
            print(" •", book)

    def add_user(self, user: User) -> None:
        if user in self.__users:
            print(f"Пользователь {user.name} уже зарегистрирован.")
            return
        self.__users.append(user)

    def _find_user(self, name: str) -> Optional[User]:
        for user in self.__users:
            if user.name == name:
                return user
        return None

    def lend_book(self, title: str, user_name: str) -> None:
        book = self.find_book(title)
        if book is None:
            print(f"Книга '{title}' не найдена в библиотеке.")
            return
        user = self._find_user(user_name)
        if user is None:
            print(f"Пользователь '{user_name}' не зарегистрирован.")
            return
        user.borrow(book)

    def return_book(self, title: str, user_name: str) -> None:
        user = self._find_user(user_name)
        if user is None:
            print(f"Пользователь '{user_name}' не зарегистрирован.")
            return
        for book in user.get_borrowed_books():
            if book.get_title() == title:
                user.return_book(book)
                return
        print(f"У пользователя {user_name} нет книги '{title}'.")


if __name__ == "__main__":
    lib = Library()

    b1 = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")
    b2 = EBook("Мастер и Маргарита", "Булгаков", 1966, 5, "epub")
    b3 = PrintedBook("Преступление и наказание", "Достоевский", 1866, 480, "плохая")

    user1 = User("Анна")
    librarian = Librarian("Мария")

    librarian.add_book(lib, b1)
    librarian.add_book(lib, b2)
    librarian.add_book(lib, b3)

    librarian.register_user(lib, user1)

    lib.lend_book("Война и мир", "Анна")
    user1.show_books()
    lib.return_book("Война и мир", "Анна")

    b2.download()

    print(b3)
    b3.repair()
    print(b3)
