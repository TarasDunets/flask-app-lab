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

    form = PostForm()

    if form.validate_on_submit():
        try:
            # Отримуємо дані з форми
            title = form.title.data
            content = form.content.data
            is_active = form.is_active.data
            category = form.category.data
            author = form.author.data
            posted = form.posted.data

            # Конвертація is_active у булевий тип
            is_active = True if is_active == 'true' else False

            # Створюємо новий об'єкт Post
            post = Post(
                title=title,
                content=content,
                posted=posted,
                is_active=is_active,
                category=category,
                author=author
            )
            db.session.add(post)
            db.session.commit()

            flash("Пост успішно створено!", "success")
            return redirect(url_for('posts.get_posts'))

        except Exception as e:
            flash(f"Помилка: {str(e)}", "error")
            return redirect(url_for('posts.add_post'))

    return render_template('add_form.html', form=form)

@post_bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    # Отримуємо пост за ID
    post = Post.query.get_or_404(post_id)

    # Ініціалізуємо форму з даними поста
    form = PostForm(obj=post)

    if form.validate_on_submit():
        try:
            # Оновлюємо дані поста
            post.title = form.title.data
            post.content = form.content.data
            post.is_active = True if form.is_active.data == 'true' else False
            post.category = form.category.data
            post.author = form.author.data
            post.posted = form.posted.data

            db.session.commit()
            flash("Пост успішно оновлено!", "success")
            return redirect(url_for('posts.get_posts'))

        except Exception as e:
            flash(f"Помилка: {str(e)}", "error")
            return redirect(url_for('posts.edit_post', post_id=post_id))

    return render_template('edit.html', form=form, post=post)

@post_bp.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Пост успішно видалено!', 'success')
    return redirect(url_for('posts.get_posts'))
