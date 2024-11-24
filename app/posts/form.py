from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired
from app.posts.models import Post
from app import db

class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Контент', validators=[DataRequired()])
    posted = DateTimeLocalField('Дата публікації', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Зберегти')

def save_post(form):
    """Зберігає пост із форми у базу даних."""
    post = Post(
        title=form.title.data,
        content=form.content.data,
        posted=form.posted.data
    )
    db.session.add(post)
    db.session.commit()
