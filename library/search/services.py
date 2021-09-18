import library.utilities.utilities as utils


def search_for_items(user_input: str):
    book_results = []

    books = utils.get_list_of_books()
    authors = utils.get_authors()

    for book in books:
        if user_input in str(book.book_id):
            if book not in book_results:
                book_results.append(book)
        if user_input in book.title:
            if book not in book_results:
                book_results.append(book)

    for author in authors:
        if user_input in str(author.unique_id):
            if author not in books:
                books.append(author)
        if user_input in author.full_name:
            if author not in books:
                author.append(author)

    return book_results, author
