from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms import BooleanField, SelectField, DateField
import os
import json
from datetime import datetime

CATEGORIES = [('tech', 'Tech'), ('science', 'Science'), ('lifestyle', 'Lifestyle')]

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', render_kw={'rows': 5, 'cols': 40 }, validators=[DataRequired()])
    is_active = BooleanField('Active')
    category = SelectField('Category', choices=CATEGORIES)
    publication_date = DateField('Publication Date', format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField('Add Post')



def save_post(title, content, category, is_active, publication_date, author):
    """
    Зберігає новий пост у файлі `posts.json`.
    Якщо файл ще не існує, створює його з порожнім списком постів.

    :param title: Заголовок поста
    :param content: Контент поста
    :param category: Категорія поста
    :param is_active: Чи активний пост (bool)
    :param publication_date: Дата публікації (datetime object)
    :param author: Автор поста
    """
    post = {
        "id": None,  # Ідентифікатор буде обчислено динамічно
        "title": title,
        "content": content,
        "category": category,
        "is_active": is_active,
        "publication_date": publication_date.strftime('%Y-%m-%d'),
        "author": author
    }

    current_dir = os.path.dirname(__file__)  # Папка, де знаходиться form.py
    file_path = os.path.join(current_dir, 'post.json')
    try:
        
        # Читання існуючого вмісту файлу
        with open(file_path, 'r+') as file:
            try:
                posts = json.load(file)
            except json.JSONDecodeError:
                # Якщо файл пустий або пошкоджений, створюємо порожній список
                posts = []

            # Додавання ідентифікатора
            post["id"] = len(posts) + 1

            # Додавання нового поста до списку
            posts.append(post)

            # Перемотка на початок і перезапис файлу
            file.seek(0)
            json.dump(posts, file, indent=4)
            file.truncate()  # Видалення залишків старого вмісту, якщо файл скоротився
    except FileNotFoundError:
        # Якщо файл не існує, створюємо його
        with open(file_path, 'w') as file:
            posts = [post]
            post["id"] = 1  # Перший запис отримує ID 1
            json.dump(posts, file, indent=4)
