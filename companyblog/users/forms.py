from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from companyblog.models import User


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('パスワード',validators=[DataRequired()])
    submit = SubmitField('ログイン')

class RegistrationForm(FlaskForm):
    email = StringField('Eメールアドレス',validators=[DataRequired(),Email()])
    username = StringField('ユーザー名',validators=[DataRequired()])
    password = PasswordField('パスワード',validators=[DataRequired(),EqualTo('pass_confirm',message='Passwords must match!')])
    pass_confirm = PasswordField('パスワード確認',validators=[DataRequired()])
    submit = Submit = SubmitField('登録する')

    def validate_email(self,email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('your email has been registered already!')

    def validate_username(self,username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('your username has been registered already!')

class UpdateUserForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    info = StringField('Write your profile')
    picture = FileField('Update profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('your email has been registered already!')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('your username has been registered already!')
