from flask import Flask

def create_app(config_name="config"):
  app = Flask(__name__)
  app.config.from_object(config_name)  # Налаштування з об'єкта

  with app.app_context():
    from .posts import post_bp
    from .users import users_bp
    app.register_blueprint(post_bp)
    app.register_blueprint(users_bp)
    from . import views

  return app