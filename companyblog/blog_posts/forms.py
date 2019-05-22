from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileAllowed

class BlogPostForm(FlaskForm):
    title = StringField('イベント名',validators=[DataRequired()])
    text = TextAreaField('イベント詳細',validators=[DataRequired()])
    image = FileField('イメージ画像',validators=[FileAllowed(['jpg','png'])])
    organizer = StringField('主催者',validators=[DataRequired()])
    place = StringField('場所',validators=[DataRequired()])
    entry = StringField('参加条件',validators=[DataRequired()])
    way = StringField('参加方法',validators=[DataRequired()])
    cost = StringField('参加費用',validators=[DataRequired()])
    contact = StringField('問い合わせ',validators=[DataRequired()])
    image = FileField('イメージ画像',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField("新規イベントを投稿する")

class CommentForm(FlaskForm):
    body = StringField('Add Comment',validators=[DataRequired()])
    submit = SubmitField('Comment')
