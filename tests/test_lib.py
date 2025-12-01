from src.lib import Library, PrintedBook, EBook, User, Librarian


def test_register_user():
    lib = Library()
    librarian = Librarian("Мария")
    user = User("Анна")

    librarian.register_user(lib, user)

    assert lib._find_user("Анна") is not None


def test_add_book():
    lib = Library()
    librarian = Librarian("Мария")

    book = PrintedBook("Тест", "Автор", 2000, 150, "хорошая")
    librarian.add_book(lib, book)

    assert lib.find_book("Тест") is not None


def test_lend_and_return_book():
    lib = Library()
    librarian = Librarian("Мария")
    user = User("Анна")

    librarian.register_user(lib, user)

    book = PrintedBook("ТестКнига", "Автор", 2001, 120, "плохая")
    librarian.add_book(lib, book)

    lib.lend_book("ТестКнига", "Анна")
    assert len(user.get_borrowed_books()) == 1
    assert user.get_borrowed_books()[0].get_title() == "ТестКнига"
    assert not book.is_available()

    lib.return_book("ТестКнига", "Анна")
    assert len(user.get_borrowed_books()) == 0
    assert book.is_available()
