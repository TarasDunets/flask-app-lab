from . import users_bp
from flask import render_template, redirect, request, url_for, make_response, session, flash
from datetime import timedelta, datetime

@users_bp.route("/hi/<string:name>")   #/hi/ivan?age=45&q=fdfdf
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    
    return render_template("hi.html", name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)     # "http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)

@users_bp.route('/get_cookie/<key>')
def get_cookie(key):
    value = request.cookies.get(key)
    if value:
        return f'Кукі {key}: {value}'
    else:
        return f'Кукі {key} не знайдено', 404

@users_bp.route('/set_cookie', methods=['POST'])
def set_cookie():
    key = request.form['key']
    value = request.form['value']
    duration = int(request.form.get('duration', 0))  # Час зберігання кукі в секундах
    max_age = timedelta(seconds=duration)
    
    resp = make_response(redirect(url_for('users.get_profile')))
    resp.set_cookie(key, value, max_age=max_age)
    
    flash(f'Кукі {key} було встановлено на {duration} секунд!', 'success')
    return resp

@users_bp.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    key = request.form['key']
    resp = make_response(redirect(url_for('users.get_profile')))
    resp.delete_cookie(key)
    flash(f'Кукі {key} було видалено!', 'success')
    return resp

@users_bp.route('/delete_all_cookies', methods=['POST'])
def delete_all_cookies():
    resp = make_response(redirect(url_for('users.get_profile')))
    
    for key in request.cookies.keys():  # Видаляємо кожен кукі
        resp.delete_cookie(key)
    
    flash('Усі кукі були видалені!', 'success')
    return resp

@users_bp.route("/profile")
def get_profile():
    if 'user' not in session:
        flash('Спочатку увійдіть до системи!', 'error')
        return redirect(url_for('login'))
    
    theme = request.cookies.get("theme", "light")
    cookies = request.cookies  # Отримання всіх кукі для відображення
    return render_template('profile.html', username=session['user'], cookies=cookies, theme=theme)

@users_bp.route("/login",  methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':  # Перевірка автентифікації
            session['user'] = username
            flash('Вхід успішний!', 'success')
            return redirect(url_for('users.get_profile'))
        else:
            flash('Невірне ім’я користувача або пароль!', 'error')
            return redirect(url_for('users.login'))
    return render_template("login.html")

@users_bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('age', None)
    return redirect(url_for('users.login'))

@users_bp.route("/set_theme/<theme>")
def set_theme(theme):
    if theme not in ["light", "dark"]:
        flash("Невідома кольорова схема!", "error")
        return redirect(url_for("users.get_profile"))

    # Створюємо відповідь з кукі для збереження теми
    response = redirect(url_for("users.get_profile"))
    response.set_cookie("theme", theme)
    flash("Кольорова схема змінена!", "success")
    return response
