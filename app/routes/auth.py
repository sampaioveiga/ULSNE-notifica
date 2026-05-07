from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from ..models import User

bp = Blueprint('auth', __name__)


class LoginForm(FlaskForm):
    username = StringField('Utilizador', validators=[DataRequired()])
    password = PasswordField('Palavra-passe', validators=[DataRequired()])
    remember = BooleanField('Manter sessão')
    submit = SubmitField('Entrar')


@bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('backoffice.notifications'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.is_active and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('backoffice.notifications'))
        flash('Credenciais inválidas ou conta desativada.', 'danger')

    return render_template('admin/login.html', form=form)


@bp.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
