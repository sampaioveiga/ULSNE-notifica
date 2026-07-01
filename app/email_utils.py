import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


def send_new_notification_email(notification):
    from .models import SMTPConfig, User
    config = SMTPConfig.get()

    managers = User.query.filter_by(is_manager=True, is_active=True).all()
    if not managers:
        return

    manager_emails = [m.email for m in managers]

    subject = f'[ULSNE] Nova Notificação de Incidente — #{notification.id}'
    body = f"""
Foi submetida uma nova notificação de incidente de violência.

ID: {notification.id}
Token: {notification.token}
Data do Incidente: {notification.data_incidente}
Local: {notification.local_incidente}
Tipo(s) de Violência: {', '.join(notification.tipos_violencia_labels)}
Estado: {notification.status_label}

Aceda ao backoffice para gerir esta notificação.
    """.strip()

    msg = MIMEMultipart()
    msg['From'] = config.from_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP(config.host, config.port) as server:
            server.sendmail(config.from_email, manager_emails, msg.as_string())
    except Exception:
        logger.exception('Falha ao enviar email de notificação')
