from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class OrderForm(Form):
    order_id = TextField(
            'Order Id', validators=[DataRequired(), Length(min=1, max=32)]
    )
    order_status = TextField(
            'Order Status', validators=[DataRequired(), Length(min=6, max=40)]
    )
    product_name = TextField(
            'Product Name', validators=[DataRequired(), Length(min=6, max=400)]
    )
    product_url  = TextField(
            'URL', validators=[DataRequired(), Length(min=10, max=400)]
    )
    cost_price   = TextField(
            'Price', validators=[DataRequired(), Length(min=1, max=6)]
    )





class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
