from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .models import db, User
from .config import Config


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Precisa de autenticar-se para aceder ao backoffice.'
login_manager.login_message_category = 'warning'

csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .routes.public import bp as public_bp
    from .routes.auth import bp as auth_bp
    from .routes.backoffice import bp as backoffice_bp
    from .routes.users import bp as users_bp
    from .routes.settings import bp as settings_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(backoffice_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(settings_bp)

    from datetime import datetime

    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    with app.app_context():
        db.create_all()
        _seed_admin()

    return app


def _seed_admin():
    from .models import User
    if User.query.count() == 0:
        admin = User(username='admin', email='admin@ulsne.min-saude.pt', is_manager=True)
        admin.set_password('Admin1234!')
        db.session.add(admin)
        db.session.commit()
