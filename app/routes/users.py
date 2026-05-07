from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo, ValidationError
from ..models import db, User

bp = Blueprint('users', __name__, url_prefix='/admin/utilizadores')


class UserForm(FlaskForm):
    username = StringField('Nome de Utilizador', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    is_admin = BooleanField('Administrador')
    password = PasswordField('Palavra-passe', validators=[Optional(), Length(min=8)])
    password2 = PasswordField('Confirmar Palavra-passe', validators=[EqualTo('password')])
    submit = SubmitField('Guardar')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user

    def validate_username(self, field):
        q = User.query.filter_by(username=field.data)
        if self._user:
            q = q.filter(User.id != self._user.id)
        if q.first():
            raise ValidationError('Nome de utilizador já existe.')

    def validate_email(self, field):
        q = User.query.filter_by(email=field.data)
        if self._user:
            q = q.filter(User.id != self._user.id)
        if q.first():
            raise ValidationError('Email já registado.')


@bp.route('/')
@login_required
def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


@bp.route('/novo', methods=['GET', 'POST'])
@login_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        if not form.password.data:
            flash('A palavra-passe é obrigatória para novos utilizadores.', 'danger')
            return render_template('admin/user_form.html', form=form, title='Novo Utilizador')
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=form.is_admin.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Utilizador "{user.username}" criado com sucesso.', 'success')
        return redirect(url_for('users.list_users'))
    return render_template('admin/user_form.html', form=form, title='Novo Utilizador')


@bp.route('/<int:user_id>/editar', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(user=user, obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash(f'Utilizador "{user.username}" atualizado.', 'success')
        return redirect(url_for('users.list_users'))
    return render_template('admin/user_form.html', form=form, title='Editar Utilizador', user=user)


@bp.route('/<int:user_id>/toggle', methods=['POST'])
@login_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Não pode desativar a sua própria conta.', 'warning')
    else:
        user.is_active = not user.is_active
        db.session.commit()
        state = 'ativado' if user.is_active else 'desativado'
        flash(f'Utilizador "{user.username}" {state}.', 'success')
    return redirect(url_for('users.list_users'))
