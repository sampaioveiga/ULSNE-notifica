from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange
from ..models import db, SMTPConfig

bp = Blueprint('settings', __name__, url_prefix='/admin/configuracoes')


class SMTPForm(FlaskForm):
    host = StringField('Servidor SMTP', validators=[DataRequired()])
    port = IntegerField('Porta', validators=[DataRequired(), NumberRange(min=1, max=65535)])
    use_tls = BooleanField('Usar TLS')
    from_email = StringField('Email de Origem', validators=[DataRequired()])
    submit = SubmitField('Guardar Configuração')


@bp.route('/smtp', methods=['GET', 'POST'])
@login_required
def smtp():
    config = SMTPConfig.get()
    form = SMTPForm(obj=config)
    if form.validate_on_submit():
        config.host = form.host.data
        config.port = form.port.data
        config.use_tls = form.use_tls.data
        config.from_email = form.from_email.data
        db.session.commit()
        flash('Configuração SMTP guardada com sucesso.', 'success')
        return redirect(url_for('settings.smtp'))
    return render_template('admin/smtp_settings.html', form=form)
