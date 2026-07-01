from datetime import date, datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, SelectField, SelectMultipleField, SubmitField, IntegerField, widgets, RadioField
from wtforms.validators import DataRequired, Optional, Length
from ..models import (
    db, Notification, Comment,
    TIPOS_INCIDENTE, LOCAIS_INCIDENTE, CATEGORIAS_PROFISSIONAIS,
    TIPOS_VITIMA, TIPOS_AGRESSOR, UNIDADES_LOCAL,
    OPCOES_SIM_NAO, OPCOES_SIM_NAO_DESC
)
from ..email_utils import send_new_notification_email

bp = Blueprint('public', __name__)


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class NotificationForm(FlaskForm):
    # 1. Identificação da Instituição
    unidade_local = SelectField(
        'Unidade/Instituição',
        choices=UNIDADES_LOCAL,
        validators=[DataRequired()]
    )
    servico = StringField('Serviço/Departamento', validators=[Optional(), Length(max=200)])

    # 2. Informação sobre a Notificação
    quem_notifica = RadioField(
        'Quem realiza a notificação?',
        choices=[('proprio', 'Próprio'), ('outro', 'Outro')],
        validators=[DataRequired()]
    )
    quem_notifica_outro = StringField('Especifique quem:', validators=[Optional(), Length(max=200)])

    eh_anonimo = RadioField(
        'Pretende manter o anonimato?',
        choices=[('sim', 'Sim'), ('nao', 'Não')],
        validators=[DataRequired()]
    )
    nome_notificante = StringField('Nome (opcional)', validators=[Optional(), Length(max=200)])
    contacto_notificante = StringField('Contacto (opcional)', validators=[Optional(), Length(max=200)])
    data_notificacao = DateField('Data da notificação', validators=[DataRequired()], default=date.today)

    # 3. Informação sobre o Incidente
    data_incidente = DateField('Data do incidente', validators=[DataRequired()])
    hora_incidente = TimeField('Hora (aproximada)', validators=[Optional()])

    local_incidente = SelectField(
        'Local onde ocorreu o incidente',
        choices=LOCAIS_INCIDENTE,
        validators=[DataRequired()]
    )
    local_incidente_outro = StringField('Outro local (especifique):', validators=[Optional(), Length(max=200)])

    tipos_incidente = MultiCheckboxField(
        'Tipo(s) de incidente',
        choices=TIPOS_INCIDENTE,
        validators=[DataRequired(message='Selecione pelo menos um tipo de incidente.')]
    )
    tipos_incidente_outro = StringField('Outro tipo (especifique):', validators=[Optional(), Length(max=200)])

    # 4. Informação sobre a Vítima
    tipo_vitima = SelectField(
        'Quem foi a vítima?',
        choices=TIPOS_VITIMA,
        validators=[DataRequired()]
    )
    categoria_profissional = SelectField(
        'Categoria profissional da vítima',
        choices=CATEGORIAS_PROFISSIONAIS,
        validators=[Optional()]
    )
    nome_vitima = StringField('Nome da vítima (opcional)', validators=[Optional(), Length(max=200)])

    # 5. Informação sobre o Agressor
    tipo_agressor = SelectField(
        'Quem foi o agressor?',
        choices=TIPOS_AGRESSOR,
        validators=[DataRequired()]
    )
    numero_agressores = IntegerField('Número de agressores', validators=[Optional()])
    identidade_conhecida = RadioField(
        'A identidade do agressor é conhecida?',
        choices=[('sim', 'Sim'), ('nao', 'Não'), ('desconhecido', 'Desconhecido')],
        validators=[Optional()]
    )
    nome_agressor = StringField('Nome do agressor (se conhecido)', validators=[Optional(), Length(max=200)])

    # 6. Consequências do Incidente
    danos_fisicos = RadioField(
        'O incidente provocou danos físicos?',
        choices=OPCOES_SIM_NAO_DESC,
        validators=[Optional()]
    )
    impacto_psicologico = RadioField(
        'Impacto psicológico ou emocional?',
        choices=OPCOES_SIM_NAO_DESC,
        validators=[Optional()]
    )
    assistencia_medica = RadioField(
        'Foi necessária assistência médica?',
        choices=OPCOES_SIM_NAO,
        validators=[Optional()]
    )
    intervencao_autoridades = RadioField(
        'Intervenção de segurança ou autoridades?',
        choices=OPCOES_SIM_NAO,
        validators=[Optional()]
    )

    # 7. Resposta ao Incidente
    quem_foi_informado = MultiCheckboxField(
        'Quem foi informado?',
        choices=[
            ('responsavel', 'Responsável de Serviço'),
            ('direcao', 'Direção'),
            ('seguranca', 'Segurança'),
            ('focal', 'Ponto Focal'),
            ('outro', 'Outro'),
        ],
        validators=[Optional()]
    )
    quem_informado_outro = StringField('Outro (especifique):', validators=[Optional(), Length(max=200)])

    medidas_aplicadas = MultiCheckboxField(
        'Foram aplicadas medidas imediatas?',
        choices=[
            ('intervencao_seguranca', 'Intervenção da Segurança'),
            ('retirada_agressor', 'Retirada do Agressor'),
            ('apoio_vitima', 'Apoio à Vítima'),
            ('nenhuma', 'Nenhuma'),
            ('outro', 'Outro'),
        ],
        validators=[Optional()]
    )
    medidas_outro = StringField('Outra medida (especifique):', validators=[Optional(), Length(max=200)])

    # 8. Testemunhas
    existem_testemunhas = RadioField(
        'Existiam testemunhas do incidente?',
        choices=OPCOES_SIM_NAO_DESC,
        validators=[Optional()]
    )
    descricao_testemunhas = TextAreaField(
        'Descreva as testemunhas',
        validators=[Optional(), Length(max=500)]
    )

    # 9. Descrição do Incidente
    descricao = TextAreaField(
        'Descrição detalhada do incidente',
        validators=[DataRequired(), Length(min=20, max=5000)],
        render_kw={'rows': 6, 'placeholder': 'Descreva o que aconteceu, quem esteve envolvido e como terminou a situação...'}
    )

    # 10. Avaliação de Risco
    risco_repeticao = RadioField(
        'Considera existir risco de repetição?',
        choices=[('sim', 'Sim'), ('nao', 'Não'), ('nao_sei', 'Não Sei')],
        validators=[Optional()]
    )
    agressor_contacto = RadioField(
        'O agressor mantém contacto com a vítima?',
        choices=OPCOES_SIM_NAO_DESC,
        validators=[Optional()]
    )

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
            # 1. Instituição
            unidade_local=form.unidade_local.data,
            servico=form.servico.data,
            # 2. Notificação
            quem_notifica=form.quem_notifica.data,
            quem_notifica_outro=form.quem_notifica_outro.data,
            eh_anonimo=form.eh_anonimo.data == 'sim',
            nome_notificante=form.nome_notificante.data,
            contacto_notificante=form.contacto_notificante.data,
            data_notificacao=form.data_notificacao.data,
            # 3. Incidente
            data_incidente=datetime.combine(form.data_incidente.data, form.hora_incidente.data or datetime.min.time()),
            local_incidente=form.local_incidente.data,
            local_incidente_outro=form.local_incidente_outro.data,
            tipos_incidente=','.join(form.tipos_incidente.data),
            tipos_incidente_outro=form.tipos_incidente_outro.data,
            # 4. Vítima
            tipo_vitima=form.tipo_vitima.data,
            categoria_profissional=form.categoria_profissional.data or None,
            nome_vitima=form.nome_vitima.data,
            # 5. Agressor
            tipo_agressor=form.tipo_agressor.data,
            numero_agressores=form.numero_agressores.data,
            identidade_conhecida=form.identidade_conhecida.data,
            nome_agressor=form.nome_agressor.data,
            # 6. Consequências
            danos_fisicos=form.danos_fisicos.data,
            impacto_psicologico=form.impacto_psicologico.data,
            assistencia_medica=form.assistencia_medica.data,
            intervencao_autoridades=form.intervencao_autoridades.data,
            # 7. Resposta
            quem_foi_informado=','.join(form.quem_foi_informado.data) if form.quem_foi_informado.data else None,
            quem_informado_outro=form.quem_informado_outro.data,
            medidas_aplicadas=','.join(form.medidas_aplicadas.data) if form.medidas_aplicadas.data else None,
            medidas_outro=form.medidas_outro.data,
            # 8. Testemunhas
            existem_testemunhas=form.existem_testemunhas.data,
            descricao_testemunhas=form.descricao_testemunhas.data,
            # 9. Descrição
            descricao=form.descricao.data,
            # 10. Risco
            risco_repeticao=form.risco_repeticao.data,
            agressor_contacto=form.agressor_contacto.data,
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
