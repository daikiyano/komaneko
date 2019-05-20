from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileAllowed

class BlogPostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    text = TextAreaField('Text',validators=[DataRequired()])
    image = FileField('Upload image picture',validators=[FileAllowed(['jpg','png'])])
        # picture = FileField('Update profile Picture',validators=[FileAllowed(['jpg','png'])])

    submit = SubmitField("Post")

class CommentForm(FlaskForm):
    body = StringField('Add Comment',validators=[DataRequired()])
    submit = SubmitField('Comment')
