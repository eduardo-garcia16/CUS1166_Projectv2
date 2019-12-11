from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo, Length, NumberRange
from app.models import User

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError("Please use a different username")

class BookForm(FlaskForm):
    title = StringField('Name your BudgetBook', validators=[DataRequired()])
    description = TextAreaField('Enter BudgetBook description', validators=[Length(min=0, max=120)])
    revenue = StringField('Enter total budget / revenue', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditBookForm(FlaskForm):
    title = StringField('Change BudgetBook Title', validators=[DataRequired()])
    expense = StringField('Enter new expense', validators=[DataRequired()])
    submit = SubmitField('Submit new expense')

    def __init__(self, original_title, *args, **kwargs):
        super(EditBookForm, self).__init__(*args, **kwargs)
        self.original_title = original_title
