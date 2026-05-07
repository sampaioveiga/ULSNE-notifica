from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from ..models import db, Notification, Comment, STATUS_ABERTA, STATUS_EM_ANALISE, STATUS_ENCERRADO, STATUS_LABELS

bp = Blueprint('backoffice', __name__, url_prefix='/admin')


class CommentForm(FlaskForm):
    text = TextAreaField('Comentário', validators=[DataRequired(), Length(min=3, max=2000)])
    submit = SubmitField('Adicionar Comentário')


class StatusForm(FlaskForm):
    status = SelectField('Mudar Estado', choices=[
        (STATUS_EM_ANALISE, STATUS_LABELS[STATUS_EM_ANALISE]),
        (STATUS_ENCERRADO, STATUS_LABELS[STATUS_ENCERRADO]),
    ])
    submit = SubmitField('Atualizar Estado')


@bp.route('/notificacoes')
@login_required
def notifications():
    status_filter = request.args.get('status', '')
    sort = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')

    query = Notification.query
    if status_filter:
        query = query.filter_by(status=status_filter)

    col = getattr(Notification, sort, Notification.created_at)
    if order == 'asc':
        query = query.order_by(col.asc())
    else:
        query = query.order_by(col.desc())

    notifications = query.all()
    return render_template(
        'admin/notifications.html',
        notifications=notifications,
        status_filter=status_filter,
        sort=sort,
        order=order,
        status_labels=STATUS_LABELS,
    )


@bp.route('/notificacoes/<int:notif_id>', methods=['GET', 'POST'])
@login_required
def notification_detail(notif_id):
    notif = Notification.query.get_or_404(notif_id)
    comment_form = CommentForm(prefix='comment')
    status_form = StatusForm(prefix='status')

    if request.method == 'POST':
        if 'comment-submit' in request.form and comment_form.validate():
            from flask_login import current_user
            comment = Comment(
                notification_id=notif.id,
                author_type='manager',
                user_id=current_user.id,
                text=comment_form.text.data,
            )
            db.session.add(comment)
            db.session.commit()
            flash('Comentário adicionado.', 'success')
            return redirect(url_for('backoffice.notification_detail', notif_id=notif_id))

        if 'status-submit' in request.form and status_form.validate():
            new_status = status_form.status.data
            if notif.status != STATUS_ENCERRADO:
                notif.status = new_status
                db.session.commit()
                flash(f'Estado atualizado para "{STATUS_LABELS[new_status]}".', 'success')
            else:
                flash('Não é possível alterar o estado de uma notificação encerrada.', 'warning')
            return redirect(url_for('backoffice.notification_detail', notif_id=notif_id))

    return render_template(
        'admin/detail.html',
        notif=notif,
        comment_form=comment_form,
        status_form=status_form,
        STATUS_EM_ANALISE=STATUS_EM_ANALISE,
        STATUS_ENCERRADO=STATUS_ENCERRADO,
    )
