from flask_wtf import FlaskForm # type: ignore
from wtforms import StringField, TextAreaField, BooleanField, SelectField, DateTimeLocalField, SubmitField, SelectMultipleField # type: ignore
from wtforms.validators import DataRequired # type: ignore
from app.posts.models import Post
from app.posts.models import Tag
from app.users.models import User 

from app import db

class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Контент', validators=[DataRequired()])
    is_active = SelectField(
        'Активний',
        choices=[('true', 'Так'), ('false', 'Ні')],
        validators=[DataRequired()]
    )
    category = StringField('Категорія', validators=[DataRequired()])
    author_id = SelectField('Автор', coerce=int)
    posted = DateTimeLocalField('Дата публікації', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Зберегти')
    tags = SelectMultipleField('Tags', coerce=int)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]

def save_post(form):
    """Зберігає пост із форми у базу даних."""
    # Extract data
    title = form.title.data
    content = form.content.data
    is_active = form.is_active.data == 'true'
    category = form.category.data
    author_id = form.author_id.data
    tags_ids = form.tags.data
    posted = form.posted.data

    # Validate author existence
    author = User.query.get(author_id)
    if not author:
        raise ValueError(f"Author with ID {author_id} does not exist")

    # Validate tags existence
    tags = Tag.query.filter(Tag.id.in_(tags_ids)).all()
    if len(tags) != len(tags_ids):
        raise ValueError("One or more tags are invalid")

    # Create the post
    post = Post(
        title=title,
        content=content,
        posted=posted,
        is_active=is_active,
        category=category,
        user_id=author.id,
    )

    # Associate tags
    post.tags = tags  # Assuming a relationship

    # Save to database
    try:
        db.session.add(post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Failed to save post: {str(e)}")
