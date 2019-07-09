from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField,PasswordField,SubmitField,TextAreaField,SelectField,HiddenField
from wtforms.validators import DataRequired,Email,EqualTo,Length,Regexp
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from companyblog.models import User


class LoginForm(FlaskForm):
    email = StringField('メールアドレス',validators=[DataRequired("メールアドレスを入力してください"),Email('このメールアドレスは無効です')])
    password = PasswordField('パスワード',validators=[DataRequired("パスワードを入力してください")])
    submit = SubmitField('ログイン')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('メールアドレスまたはパスワードが不正です')
        if not user.check_password(self.password.data):
            raise ValidationError('メールアドレスまたはパスワードが不正です')
class RegistrationForm(FlaskForm):
    email = StringField('メールアドレス',validators=[DataRequired('メールアドレスを入力してください'),Email('このメールアドレスは無効です')])
    username = StringField('KOMANEKO ID',validators=[DataRequired('KOMANEKO IDを入力してください'),Regexp(regex='^[a-zA-Z0-9]+$', message='半角英数字のみ有効です')])
    name = StringField('代表者',validators=[DataRequired('代表者を入力してください')])
    club_name = StringField('団体名',validators=[DataRequired('団体名を入力してください')])
    university = SelectField(u'所属大学',choices=[(1, '駒澤大学')],coerce=int, default=0)
    type = SelectField(u'団体カテゴリ',choices=[(0, '所属を選択してください'),(2, '(団体)体育会部'),(3, '(団体)文化部'),(4, '任意団体/サークル'),(5, 'ゼミ/その他の団体')],coerce=int, default=0)
    password = PasswordField('パスワード',validators=[DataRequired('パスワードを入力してください'),EqualTo('pass_confirm',message='パスワードが一致しません。')])
    pass_confirm = PasswordField('パスワード確認',validators=[DataRequired('再確認用のパスワードを入力してください')])
    recaptcha = RecaptchaField()
    submit = Submit = SubmitField('利用規約に同意して登録')


    def validate_email(self,email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('このメールアドレスアドレスは既に登録されています')

    def validate_username(self,username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('このKOMANEKOIDは既に使われています')

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError('8文字以上のパスワードを設定してください')


    def validate_type(self,type):
        if type.data == 0:
            raise ValidationError('団体カテゴリを選択してください')

class SignupForm(FlaskForm):
    email = StringField('Eメールアドレス',validators=[DataRequired('メールアドレスを入力してください'),Email('このメールアドレスは無効です')])
    username = StringField('KOMANEKO ID',validators=[DataRequired('KOMANEKO IDを入力してください'),Regexp(regex='^[a-zA-Z0-9]+$', message='半角英数字のみ有効です')])
    club_name = StringField('ユーザー名',validators=[DataRequired('ユーザー名を入力してください')])
    university = SelectField(u'所属大学',choices=[(1, '駒澤大学')],coerce=int, default=0)
    type = SelectField(u'アカウントの種類',choices=[(1, '個人')],coerce=int, default=0)
    password = PasswordField('パスワード',validators=[DataRequired('パスワードを入力してください'),EqualTo('pass_confirm',message='パスワードが一致しません。')])
    pass_confirm = PasswordField('パスワード確認',validators=[DataRequired('再確認用のパスワードを入力してください')])
    recaptcha = RecaptchaField()
    submit = Submit = SubmitField('利用規約に同意して登録')


    def validate_email(self,email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('このメールアドレスは既に登録されています')

    def validate_username(self,username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('このユーザー名は既に使われています')

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError('8文字以上のパスワードを設定してください')




class UpdateUserForm(FlaskForm):
    email = StringField('Eメール',validators=[DataRequired(),Email()])
    username = StringField('KOMANEKO ID',validators=[DataRequired(),Regexp(regex='^[a-zA-Z0-9]+$', message='半角英数字のみ有効です')])
    name = StringField('代表者')
    club_name = StringField('団体名')
    info = TextAreaField('詳細')
    event = TextAreaField('年間行事')
    university = SelectField(u'所属大学',choices=[(1, '駒澤大学')],coerce=int, default=0)
    type = SelectField(u'団体カテゴリ',choices=[(0, '所属を選択してください。'),(2, '(団体)体育会部'),(3, '(団体)文化部'),(4, '任意団体/サークル'),(5, 'ゼミ/その他の団体')],coerce=int)
    url = StringField('団体HP URL')
    twitter = StringField('twitterアカウント')
    facebook = StringField('Facebookアカウント')
    instagram = StringField('instagramアカウント')
    picture = FileField('団体イメージ画像',validators=[FileAllowed(['jpg','png','jpeg','gif'])])
    submit = SubmitField('プロフィールを更新')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('このメールアドレスは既に登録されています')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('このKOMANEKOIDは既に使われています')

    def validate_type(self,type):
        if type.data == 0:
            raise ValidationError('団体カテゴリを選択してください')
