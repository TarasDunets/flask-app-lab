from app.posts.form import PostForm, save_post
from . import post_bp
from flask import render_template, abort, redirect, url_for, flash, session
import json
import os

def load_posts():
    """Завантажує пости з JSON-файлу."""
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'posts.json')  # Отримує повний шлях до файлу
        with open(file_path, 'r', encoding='utf-8') as file:
            posts = json.load(file)
        return posts
    except FileNotFoundError:
        print(f"Файл posts.json не знайдено! {file_path}")
        return []
    except json.JSONDecodeError:
        print("Помилка декодування JSON-файлу.")
        return []

@post_bp.route('/')
def get_posts():
    posts = load_posts()  # Завантажуємо пости з JSON
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>')
def detail_post(id):
    """Показує деталі поста за його ID."""
    posts = load_posts()  # Завантажуємо всі пости
    post = next((post for post in posts if post['id'] == id), None)  # Знаходимо пост за ID

    if post is None:
        # Якщо пост не знайдено, повертаємо помилку 404
        abort(404)

    # Відображаємо шаблон із деталями поста
    return render_template("detail_post.html", post=post)

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    # Перевіряємо, чи користувач увійшов у систему
    if 'user' not in session:
        flash('Будь ласка, увійдіть, щоб створити пост.', 'error')
        return redirect(url_for('users.login'))

    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        category = form.category.data
        is_active = form.is_active.data
        publication_date = form.publication_date.data
        author = session['user']

        # Виклик функції для збереження поста
        save_post(title, content, category, is_active, publication_date, author)

        flash(f'Пост "{title}" успішно додано автором {author}!', 'success')
        return redirect(url_for('posts.add_post'))
    return render_template('add_form.html', form=form)