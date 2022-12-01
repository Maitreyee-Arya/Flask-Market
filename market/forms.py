from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, DataRequired, EqualTo, Email, ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exist. Please try with different one")

    def validate_email(self,email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError("Email already exist. Please try with different one")

    username = StringField(label='User Name :', validators=[Length(min=3, max=10), DataRequired()])
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=5), DataRequired()])
    con_pwd = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name :',validators=[DataRequired()])
    password = PasswordField(label='Password :', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class Add_Item(FlaskForm):
    name = StringField(label="Item Name",validators=[DataRequired()])
    price = StringField(label="Item Price", validators=[DataRequired()])
    barcode = StringField(label='Barcode', validators=[DataRequired()])
    desc = TextAreaField(label='Item Description')
    submit = SubmitField(label='Add Item')


class Edit_item(FlaskForm):
    name = StringField(label="Item Name", validators=[DataRequired()])
    price = StringField(label="Item Price", validators=[DataRequired()])
    barcode = StringField(label='Barcode', validators=[DataRequired()])
    desc = TextAreaField(label='Item Description')
    submit = SubmitField(label='Edit Item')