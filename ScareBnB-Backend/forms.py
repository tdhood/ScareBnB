from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, BooleanField, FileField
from wtforms.validators import DataRequired, InputRequired, Email, Length, Optional


# class MessageForm(FlaskForm):
#     """Form for adding/editing messages."""

#     text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    class Meta:
        csrf = False

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name',validators=[DataRequired()])
    bio = StringField('Bio', validators=[Optional()])
    is_host = BooleanField('Host', validators=[Optional()])
    # image_url = StringField('(Optional) Image URL')


class UserEditForm(FlaskForm):
    """Form for adding users."""

    class Meta:
        csrf = False

    username = StringField('Username', validators=[Optional()])
    email = StringField('E-mail', validators=[Optional(), Email()])
    # image_url = StringField(
    #                         '(Optional) Profile Image URL',
    #                         validators=[Optional()])
    bio = TextAreaField('text', validators=[Optional()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    class Meta:
        csrf = False

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class ListingAddForm(FlaskForm):
    """Form for adding listings."""

    class Meta:
        csrf = False

    title = StringField('Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    price = IntegerField('Price', validators=[InputRequired()])
    image_file = StringField('image_file', validators=[Optional()])
    rating = IntegerField('Rating', validators=[Optional()])
    user_id = IntegerField('User id', validators=[InputRequired()])
    files = FileField('Files', validators=[Optional()])


