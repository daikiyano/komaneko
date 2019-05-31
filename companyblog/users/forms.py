from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField,SelectField
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
    username = StringField('ユーザー名/団体名',validators=[DataRequired()])
    type = SelectField(u'個人か団体アカウントか選択してください',choices=[(0, '所属を選択してください。'), (1, '個人'), (2, '団体(サークル、部活等)')],coerce=int, default=0)
    password = PasswordField('パスワード',validators=[DataRequired(),EqualTo('pass_confirm',message='パスワードが一致しません。')])
    pass_confirm = PasswordField('パスワード確認',validators=[DataRequired()])
    submit = Submit = SubmitField('登録する')

    def validate_email(self,email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('このEメールアドレスは既に登録されています')

    def validate_username(self,username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('このユーザー名は既に使われています')

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError('8文字以上のパスワードを設定してください')

class UpdateUserForm(FlaskForm):
    email = StringField('Eメール',validators=[DataRequired(),Email()])
    username = StringField('ユーザー名/団体名',validators=[DataRequired()])
    info = TextAreaField('詳細')
    type = SelectField(u'個人か団体アカウントか選択してください',choices=[(0, '所属を選択してください。'), (1, '個人'), (2, '団体(サークル、部活等)')],coerce=int)
    twitter = StringField('twitterアカウント')
    facebook = StringField('Facebookアカウント')
    instagram = StringField('instagramアカウント')
    picture = FileField('イメージ画像',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('プロフィールを更新する')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('このEメールアドレスは既に登録されています')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('このユーザー名は既に使われています')
