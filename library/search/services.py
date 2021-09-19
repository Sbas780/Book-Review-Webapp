import library.utilities.utilities as utils


def search_for_items(user_input: str):
    book_results = []
    user_input = user_input.lower()
    books = utils.get_list_of_books()

    if user_input == "":
        return books
    for book in books:
        if user_input in str(book.book_id):
            if book not in book_results:
                book_results.append(book)

        if user_input in book.title.lower():
            if book not in book_results:
                book_results.append(book)

        if user_input in book.publisher.name.lower():
            if book not in book_results:
                book_results.append(book)

    utils.set_search_results(book_results)
    return book_results
