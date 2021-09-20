import math

from better_profanity import profanity
from flask import Blueprint, render_template, request, url_for
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError, NumberRange, Length
from flask_paginate import Pagination,get_page_parameter
import library.utilities.utilities as utils
import library.adapters.repository as repo
from library.browser import services

browser_bp = Blueprint('browser_bp', __name__, url_prefix='/browsing')

INVALID_CHOICE_MESSAGE = 'Invalid Choice: not an Int'

INVALID_REVIEW_TEXT_MESSAGE = 'Invalid review text.'
RATING_REQUIRED_MESSAGE = 'Ratings must be an integer between 1 and 10.'
INVALID_RATING_RANGE_MESSAGE = 'Ratings must be an integer between 1 and 10.'

REVIEW_TEXT_REQUIRED_MESSAGE = 'Reviews must be at least one character long.'
INVALID_REVIEW_TEXT_LENGTH_MESSAGE = 'Reviews must be at least one character long.'
REVIEW_TEXT_CONTAINS_PROFANITY_MESSAGE = 'No profanity'

@browser_bp.route('/books', methods=['GET', 'POST'])
def browse_books():
    books = utils.get_list_of_books()
    return render_template('books.html', book_list=books)

@browser_bp.route('/authors', methods=['GET'])
def browse_authors():
    authors = utils.get_authors()
    return render_template('authors.html', author_list=authors)


@browser_bp.route('/publishers', methods=['GET'])
def browse_publishers():
    publishers = utils.get_publishers()
    return render_template('publishers.html', publisher_list=publishers)


@browser_bp.route('/books/<book_id>', methods=['GET', 'POST'])
def book_extend(book_id):
    book = utils.get_book_by_id(book_id)
    return render_template('book_extend.html', book=book)


@browser_bp.route('/books/<book_id>/reviews', methods=['GET', 'POST'])
def reviews(book_id):
    form = ReviewForm()
    book = utils.get_book_by_id(book_id)

    list_of_reviews = utils.get_review_by_book(book)
    if form.validate_on_submit():
        services.add_review(repo.repo_instance, form.review.data, form.rating.data, book)
        return redirect(url_for('browser_bp.reviews', book_id=book_id))
    list_of_reviews = utils.get_review_by_book(book)

    return render_template('review.html', form=form, book=book, reviews=list_of_reviews)


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = INVALID_REVIEW_TEXT_MESSAGE
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    rating = SelectField('Rating: ',
                         [DataRequired(message=RATING_REQUIRED_MESSAGE),
                          NumberRange(min=1, max=5, message=INVALID_RATING_RANGE_MESSAGE)],
                         choices=range(1, 6),
                         coerce=int,
                         default=6,

                         )
    review = TextAreaField('Review: ', [
        DataRequired(message=REVIEW_TEXT_REQUIRED_MESSAGE),
        Length(min=1, message=INVALID_REVIEW_TEXT_LENGTH_MESSAGE),
        ProfanityFree(message=REVIEW_TEXT_CONTAINS_PROFANITY_MESSAGE)
    ])
    submit = SubmitField('Submit')