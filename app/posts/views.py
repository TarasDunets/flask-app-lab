from app.posts.form import PostForm, save_post
from . import post_bp
from flask import render_template, abort, redirect, url_for, flash, session, request
from .models import Post
from app import db
from datetime import datetime

@post_bp.route('/')
def get_posts():
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>')
def detail_post(id):
    """Показує деталі поста за його ID."""
    # Отримуємо пост за ID з бази даних
    post = Post.query.get_or_404(id)

    # Відображаємо шаблон із деталями поста
    return render_template("detail_post.html", post=post)

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    # Перевіряємо, чи користувач увійшов у систему
    if 'user' not in session:
        flash('Будь ласка, увійдіть, щоб створити пост.', 'error')
        return redirect(url_for('users.login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        is_active = request.form['is_active']
        category = request.form['category']
        author = request.form['author']
        posted = datetime.strptime(request.form['posted'], '%Y-%m-%dT%H:%M')

        # Конвертація is_active у булевий тип
        is_active = True if is_active.lower() == 'true' else False

        post = Post(title=title, content=content, posted=posted, is_active=is_active, category=category, author=author)
        db.session.add(post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for('posts.get_posts'))
    return render_template('add_form.html')

@post_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        posted = request.form.get('posted')

        if not post.title or not post.content or not posted:
            flash('Будь ласка, заповніть всі поля!', 'error')
            return redirect(url_for('posts.edit_post', post_id=post_id))

        try:
            post.posted = datetime.strptime(posted, '%Y-%m-%dT%H:%M')
            db.session.commit()
            flash('Пост успішно оновлено!', 'success')
            return redirect(url_for('posts.list_posts'))
        except ValueError:
            flash('Неправильний формат дати!', 'error')
            return redirect(url_for('posts.edit_post', post_id=post_id))

    return render_template('edit.html', post=post)

@post_bp.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Пост успішно видалено!', 'success')
    return redirect(url_for('posts.get_posts'))
