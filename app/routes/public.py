from datetime import date, datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, SelectField, SelectMultipleField, SubmitField, widgets
from wtforms.validators import DataRequired, Optional, Length
from ..models import db, Notification, Comment, TIPOS_VIOLENCIA, TIPOS_VITIMA, TIPOS_PERPETRADOR, UNIDADES_LOCAL, CATEGORIAS_PROFISSIONAIS
from ..email_utils import send_new_notification_email

bp = Blueprint('public', __name__)


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class NotificationForm(FlaskForm):
    data_incidente = DateField('Data do Incidente', validators=[DataRequired()], default=date.today)
    hora_incidente = TimeField('Hora (aproximada)', validators=[Optional()])
    local_incidente = StringField('Local do Incidente', validators=[DataRequired(), Length(max=200)])
    unidade_local = SelectField(
        'Unidade do Local do Incidente',
        choices=[('', '— Selecione —')] + UNIDADES_LOCAL,
        validators=[DataRequired()]
    )
    servico = StringField('Serviço / Unidade', validators=[Optional(), Length(max=200)])
    tipos_violencia = MultiCheckboxField(
        'Tipo(s) de Violência',
        choices=TIPOS_VIOLENCIA,
        validators=[DataRequired(message='Selecione pelo menos um tipo de violência.')]
    )
    tipo_vitima = SelectField('Tipo de Vítima', choices=[('', '— Selecione —')] + TIPOS_VITIMA, validators=[DataRequired()])
    categoria_profissional = SelectField(
        'Categoria Profissional da Vítima',
        choices=[('', '— Selecione —')] + CATEGORIAS_PROFISSIONAIS,
        validators=[Optional()]
    )
    tipo_perpetrador = SelectField('Tipo de Perpetrador', choices=[('', '— Selecione —')] + TIPOS_PERPETRADOR, validators=[DataRequired()])
    descricao = TextAreaField('Descrição do Incidente', validators=[DataRequired(), Length(min=20, max=3000)])
    testemunhas = TextAreaField('Testemunhas (opcional)', validators=[Optional(), Length(max=500)])
    medidas_tomadas = TextAreaField('Medidas Imediatas Tomadas (opcional)', validators=[Optional(), Length(max=1000)])
    impacto = TextAreaField('Impacto Percebido (opcional)', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Submeter Notificação')


class TokenForm(FlaskForm):
    token = StringField('Token da Notificação', validators=[DataRequired()])
    submit = SubmitField('Consultar')


class CommentForm(FlaskForm):
    text = TextAreaField('O seu comentário', validators=[DataRequired(), Length(min=5, max=2000)])
    submit = SubmitField('Enviar Comentário')


@bp.route('/')
def index():
    return render_template('public/index.html')


@bp.route('/notificacao/nova', methods=['GET', 'POST'])
def nova_notificacao():
    form = NotificationForm()
    if form.validate_on_submit():
        notif = Notification(
            data_incidente=form.data_incidente.data,
            hora_incidente=form.hora_incidente.data,
            local_incidente=form.local_incidente.data,
            unidade_local=form.unidade_local.data or None,
            servico=form.servico.data,
            tipos_violencia=','.join(form.tipos_violencia.data),
            tipo_vitima=form.tipo_vitima.data,
            categoria_profissional=form.categoria_profissional.data or None,
            tipo_perpetrador=form.tipo_perpetrador.data,
            descricao=form.descricao.data,
            testemunhas=form.testemunhas.data,
            medidas_tomadas=form.medidas_tomadas.data,
            impacto=form.impacto.data,
        )
        db.session.add(notif)
        db.session.commit()
        send_new_notification_email(notif)
        return redirect(url_for('public.sucesso', token=notif.token))

    return render_template('public/form.html', form=form)


@bp.route('/notificacao/sucesso/<token>')
def sucesso(token):
    notif = Notification.query.filter_by(token=token).first_or_404()
    return render_template('public/sucesso.html', notif=notif)


@bp.route('/notificacao/estado', methods=['GET', 'POST'])
def consultar():
    form = TokenForm()
    if form.validate_on_submit():
        return redirect(url_for('public.estado', token=form.token.data.strip()))
    return render_template('public/consultar.html', form=form)


@bp.route('/notificacao/<token>', methods=['GET', 'POST'])
def estado(token):
    notif = Notification.query.filter_by(token=token).first_or_404()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            notification_id=notif.id,
            author_type='user',
            text=form.text.data,
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comentário enviado com sucesso.', 'success')
        return redirect(url_for('public.estado', token=token))

    return render_template('public/estado.html', notif=notif, form=form)
