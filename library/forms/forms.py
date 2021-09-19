from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class RequiredForms(FlaskForm):
    search = StringField('search')
    submit = SubmitField('Find')
    sort = SelectField("Sort by:", choices=[(1, "Default"), (2, "New"), (3, "Old"),
                                            (4, "Rating"), (5, "Alphabetical")],
                       default=1, validators=[DataRequired()])
    refresh = SubmitField('refresh')