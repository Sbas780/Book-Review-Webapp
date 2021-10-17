from sqlalchemy import select, inspect

from library.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)

    assert inspector.get_table_names() == ['authors', 'book_authors', 'book_reviews', 'books', 'publishers', 'reviews', 'user_reading_lists', 'user_reviews', 'users']

def test_database_populate_select_all_users(database_engine):
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['jasveer', 'nishansala', 'unaruto', 'usasuke']

def test_database_populate_select_all_reviews(database_engine):
    inspector = inspect(database_engine)
    name_of_comments_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_comments_table]])
        result = connection.execute(select_statement)

        all_comments = []
        for row in result:
            all_comments.append((row['id'], row['user_id'], row['book_id'], row['comment']))

        assert all_comments == [(1, 4, 1, 'Good book!'), (2, 2, 1, 'It was alright.')]

def test_database_populate_select_all_books(database_engine):
    inspector = inspect(database_engine)
    name_of_articles_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_articles_table]])
        result = connection.execute(select_statement)

        all_books = []
        for row in result:
            all_books.append((row['id'], row['title']))

        nr_books = len(all_books)
        assert nr_books == 20

        assert all_books[0] == (1, '20th Century Boys, Libro 15: ¡Viva la Expo! (20th Century Boys, #15)')


