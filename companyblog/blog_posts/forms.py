from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired

class BlogPostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    text = TextAreaField('Text',validators=[DataRequired()])
    submit = SubmitField("Post")

class CommentForm(FlaskForm):
    body = StringField('post',validators=[DataRequired()])
    submit = SubmitField('Comment')
