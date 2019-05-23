from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileAllowed

class BlogPostForm(FlaskForm):
    title = StringField('イベント名',validators=[DataRequired("イベント名を入力してください。")])
    text = TextAreaField('イベント詳細',validators=[DataRequired("イベント詳細を入力してください。")])
    image = FileField('イメージ画像',validators=[FileAllowed(['jpg','png'])])
    organizer = StringField('主催者',validators=[DataRequired("主催者を入力してください。")])
    place = StringField('場所',validators=[DataRequired("場所を入力してください。")])
    entry = StringField('参加条件',validators=[DataRequired("参加条件を入力してください。")])
    way = StringField('参加方法',validators=[DataRequired("参加方法を入力してください。")])
    cost = StringField('参加費用',validators=[DataRequired("参加費用を入力してください。")])
    contact = StringField('問い合わせ',validators=[DataRequired("問い合わせ先を入力してください。")])
    image = FileField('イメージ画像',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField("新規イベントを投稿する")

class CommentForm(FlaskForm):
    body = StringField('Add Comment',validators=[DataRequired()])
    submit = SubmitField('Comment')
