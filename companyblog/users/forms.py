from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField,PasswordField,SubmitField,TextAreaField,SelectField,HiddenField
from wtforms.validators import DataRequired,Email,EqualTo,Length,Regexp
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed
from companyblog import db,login_manager,app
from flask_login import current_user
from companyblog.models import User


####################################
##########Form for User ############
####################################

####################################
##########Login Form################
####################################
class LoginForm(FlaskForm):
    email = StringField('メールアドレス',validators=[DataRequired("メールアドレスを入力してください"),Email('このメールアドレスは無効です')])
    password = HiddenField('パスワード')
    submit = SubmitField('ログイン')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('入力したメールアドレスは登録されていません')
        # if not user.check_password(self.password.data):
        #     raise ValidationError('メールアドレスまたはパスワードが不正です')


########################################################
##########Registration Form For Group user#########
######################################################
class RegistrationForm(FlaskForm):
    email = StringField('メールアドレス',validators=[DataRequired('メールアドレスを入力してください'),Email('このメールアドレスは無効です')])
    username = StringField('KOMANEKO ID(15文字以内)',validators=[DataRequired('KOMANEKO IDを入力してください'),Regexp(regex='^[a-zA-Z0-9]+$', message='半角英数字のみ有効です'),Length(max=15, message='15文字以内で入力してください')])
    name = StringField('代表者',validators=[DataRequired('代表者を入力してください')])
    club_name = StringField('団体名(30文字以内)',validators=[DataRequired('団体名を入力してください'),Length(max=30, message='30文字以内で入力してください')])
    university = SelectField(u'所属大学',choices=[(1, '駒澤大学')],coerce=int, default=0)
    type = SelectField(u'団体カテゴリ',choices=[(0, '所属を選択してください'),(2, '体育会部'),(3, '文化部'),(4, '【公認】任意団体/サークル'),(5, '【準公認】任意団体/サークル'),(6,  '【非公認】任意団体/サークル'),(7, 'ゼミナール/研究室'),(8, 'その他の団体')],coerce=int, default=0)
    password = HiddenField('パスワード')

    # password = PasswordField('パスワード',validators=[DataRequired('パスワードを入力してください'),EqualTo('pass_confirm',message='パスワードが一致しません。'),Regexp(regex='^[a-zA-Z0-9]+$', message='半角英数字で8文字以上のパスワードを設定してください')])
    # pass_confirm = PasswordField('パスワード確認',validators=[DataRequired('再確認用のパスワードを入力してください')])
    recaptcha = RecaptchaField('不正利用防止のためのチェックをお願いします')
    submit = Submit = SubmitField('利用規約に同意して登録')


    #########Validation for Email#################
    def validate_email(self,email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('このメールアドレスアドレスは既に登録されています')

    #########Validation for Username#################
    def validate_username(self,username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('このKOMANEKOIDは既に使われています')

    #########Validation for Password#################

    # def validate_password(self, password):
    #     if len(password.data) < 7:
    #         raise ValidationError('8文字以上のパスワードを設定してください')


    def validate_type(self,type):
        if type.data == 0:
            raise ValidationError('団体カテゴリを選択してください')



########################################################
##########Registration Form For individual user#########
######################################################

class SignupForm(FlaskForm):
    email = StringField('メールアドレス',validators=[DataRequired('メールアドレスを入力してください'),Email('このメールアドレスは無効です')])
    username = StringField('KOMANEKO ID(15文字以内)',validators=[DataRequired('KOMANEKO IDを入力してください'),Regexp(regex='^[a-zA-Z0-9]+$', message='半角英数字のみ有効です'),Length(max=15, message='15文字以内で入力してください')])
    club_name = StringField('ユーザー名(20文字以内)',validators=[DataRequired('ユーザー名を入力してください'),Length(max=15, message='20文字以内で入力してください')])
    university = SelectField(u'所属大学',choices=[(1, '駒澤大学')],coerce=int, default=0)
    type = SelectField(u'アカウントの種類',choices=[(1, '個人')],coerce=int, default=0)
    password = HiddenField('パスワード')
    recaptcha = RecaptchaField('不正利用防止のためチェックをお願いします')
    submit = Submit = SubmitField('利用規約に同意して登録')


    def validate_email(self,email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('このメールアドレスは既に登録されています')

    def validate_username(self,username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('このユーザー名は既に使われています')

    # def validate_password(self, password):
    #     if len(password.data) < 7:
    #         raise ValidationError('8文字以上のパスワードを設定してください')

class EmailForm(FlaskForm):
    email = StringField('新しいメールアドレス', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    # password = PasswordField('確認のためのパスワード',validators=[DataRequired("パスワードを入力してください")])
    submit = SubmitField('メールアドレスを変更')
    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('このメールアドレスは既に登録されています')

        # user = User.query.filter_by(email=current_user.email).first()
        # if not user.check_password(self.password.data):
        #     raise ValidationError('パスワードが正しくありません')





##############################################
##########Form For Update Information#########
##############################################
class UpdateUserForm(FlaskForm):
    email = StringField('メールアドレス')
    username = StringField('KOMANEKO ID(20文字以内)',validators=[DataRequired(),Regexp(regex='^[a-zA-Z0-9]+$', message='KOMANEKO IDは半角英数字のみ有効です')])
    name = StringField('代表者')
    type = SelectField(u'団体カテゴリ',choices=[(0, '所属を選択してください'),(2, '体育会部'),(3, '文化部'),(4, '【公認】任意団体/サークル'),(5, '【準公認】任意団体/サークル'),(6,  '【非公認】任意団体/サークル'),(7, 'ゼミナール/研究室'),(8, 'その他の団体')],coerce=int)
    club_name = StringField('団体名(30文字以内)',validators=[Length(max=30, message='30文字以内で入力してください')])
    info = TextAreaField('詳細')
    event = TextAreaField('年間行事')
    university = SelectField(u'所属大学',choices=[(1, '駒澤大学')],coerce=int, default=0)
    # type = SelectField(u'団体カテゴリ',choices=[(0, '所属を選択してください。'),(1, '個人'),(2, '(団体)体育会部'),(3, '(団体)文化部'),(4, '任意団体/サークル'),(5, 'ゼミナール/その他の団体')],coerce=int)

    url = StringField('団体HP URL')
    club_number = StringField('活動人数(50文字以内)',validators=[Length(max=50, message='50文字以内で入力してください')])
    club_place = StringField('活動場所(50文字以内)',validators=[Length(max=50, message='50文字以内で入力してください')])
    club_active = StringField('活動頻度(50文字以内)',validators=[Length(max=50, message='50文字以内で入力してください')])
    money = StringField('会費(50文字以内)',validators=[Length(max=50, message='50文字以内で入力してください')])
    twitter = StringField('twitterアカウント',validators=[Length(max=50, message='50文字以内で入力してください')])
    facebook = StringField('Facebookアカウント',validators=[Length(max=50, message='50文字以内で入力してください')])
    instagram = StringField('instagramアカウント',validators=[Length(max=50, message='50文字以内で入力してください')])
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
