import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

STATUS_ABERTA = 'aberta'
STATUS_EM_ANALISE = 'em_analise'
STATUS_ENCERRADO = 'encerrado'

STATUS_LABELS = {
    STATUS_ABERTA: 'Aberta',
    STATUS_EM_ANALISE: 'Em Análise',
    STATUS_ENCERRADO: 'Encerrada',
}

TIPOS_VIOLENCIA = [
    ('fisica', 'Física'),
    ('verbal', 'Verbal'),
    ('psicologica', 'Psicológica'),
    ('sexual', 'Sexual'),
    ('patrimonial', 'Patrimonial'),
    ('outra', 'Outra'),
]

TIPOS_VITIMA = [
    ('profissional_saude', 'Profissional de Saúde'),
    ('doente', 'Doente'),
    ('visitante', 'Visitante'),
    ('outro', 'Outro'),
]

TIPOS_PERPETRADOR = [
    ('doente', 'Doente'),
    ('familiar', 'Familiar / Visita'),
    ('profissional', 'Profissional'),
    ('desconhecido', 'Desconhecido'),
    ('outro', 'Outro'),
]

UNIDADES_LOCAL = [
    ('Centro de Saúde Alfândega da Fé', 'Centro de Saúde Alfândega da Fé'),
    ('Centro de Saúde Bragança I Sé', 'Centro de Saúde Bragança I Sé'),
    ('Centro de Saúde Bragança II Santa Maria', 'Centro de Saúde Bragança II Santa Maria'),
    ('Centro de Saúde Carrazeda de Ansiães', 'Centro de Saúde Carrazeda de Ansiães'),
    ('Centro de Saúde Freixo de Espada-à-Cinta', 'Centro de Saúde Freixo de Espada-à-Cinta'),
    ('Centro de Saúde Macedo de Cavaleiros', 'Centro de Saúde Macedo de Cavaleiros'),
    ('Centro de Saúde Mirandela I', 'Centro de Saúde Mirandela I'),
    ('Centro de Saúde Mirandela II', 'Centro de Saúde Mirandela II'),
    ('Centro de Saúde Miranda do Douro', 'Centro de Saúde Miranda do Douro'),
    ('Centro de Saúde Mogadouro', 'Centro de Saúde Mogadouro'),
    ('Centro de Saúde Torre de Moncorvo', 'Centro de Saúde Torre de Moncorvo'),
    ('Centro de Saúde Vila Flor', 'Centro de Saúde Vila Flor'),
    ('Centro de Saúde Vimioso', 'Centro de Saúde Vimioso'),
    ('Centro de Saúde Vinhais', 'Centro de Saúde Vinhais'),
    ('Extensão de Saúde de Carviçais', 'Extensão de Saúde de Carviçais'),
    ('Extensão de Saúde de Izeda', 'Extensão de Saúde de Izeda'),
    ('Extensão de Saúde de Sendim', 'Extensão de Saúde de Sendim'),
    ('Extensão de Saúde de Torre de Dona Chama', 'Extensão de Saúde de Torre de Dona Chama'),
    ('Hospital de Bragança', 'Hospital de Bragança'),
    ('Hospital de Macedo de Cavaleiros', 'Hospital de Macedo de Cavaleiros'),
    ('Hospital de Mirandela', 'Hospital de Mirandela'),
    ('Praça Cavaleiro Ferreira', 'Praça Cavaleiro Ferreira'),
    ('UDEP', 'UDEP'),
]

CATEGORIAS_PROFISSIONAIS = [
    ('assistente_operacional', 'Assistente Operacional'),
    ('assistente_tecnico', 'Assistente Técnico'),
    ('enfermeiro', 'Enfermeiro'),
    ('medico', 'Médico'),
    ('tecnico_auxiliar_saude', 'Técnico Auxiliar de Saúde'),
    ('tecnico_diagnostico_terapeutica', 'Técnico de Diagnóstico e Terapêutica'),
    ('tecnico_superior', 'Técnico Superior'),
    ('tecnico_superior_saude', 'Técnico Superior de Saúde'),
    ('outro', 'Outro'),
]


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    status = db.Column(db.String(20), nullable=False, default=STATUS_ABERTA)

    data_incidente = db.Column(db.Date, nullable=False)
    hora_incidente = db.Column(db.Time, nullable=True)
    local_incidente = db.Column(db.String(200), nullable=False)
    unidade_local = db.Column(db.String(200), nullable=True)
    servico = db.Column(db.String(200), nullable=True)

    tipos_violencia = db.Column(db.String(200), nullable=False)
    tipo_vitima = db.Column(db.String(50), nullable=False)
    categoria_profissional = db.Column(db.String(100), nullable=True)
    tipo_perpetrador = db.Column(db.String(50), nullable=False)

    descricao = db.Column(db.Text, nullable=False)
    testemunhas = db.Column(db.Text, nullable=True)
    medidas_tomadas = db.Column(db.Text, nullable=True)
    impacto = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    comments = db.relationship('Comment', backref='notification', lazy=True, order_by='Comment.created_at')

    @property
    def status_label(self):
        return STATUS_LABELS.get(self.status, self.status)

    @property
    def tipos_violencia_list(self):
        return [t.strip() for t in self.tipos_violencia.split(',') if t.strip()]

    @property
    def tipos_violencia_labels(self):
        mapping = dict(TIPOS_VIOLENCIA)
        return [mapping.get(t, t) for t in self.tipos_violencia_list]


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'), nullable=False)
    author_type = db.Column(db.String(10), nullable=False)  # 'user' or 'manager'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship('User', foreign_keys=[user_id])


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)


class SMTPConfig(db.Model):
    __tablename__ = 'smtp_config'

    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(200), nullable=False, default='localhost')
    port = db.Column(db.Integer, nullable=False, default=25)
    use_tls = db.Column(db.Boolean, default=False)
    from_email = db.Column(db.String(200), nullable=False, default='notificacoes@ulsne.min-saude.pt')
    to_email = db.Column(db.String(200), nullable=False, default='')

    @staticmethod
    def get():
        config = SMTPConfig.query.first()
        if not config:
            config = SMTPConfig()
            db.session.add(config)
            db.session.commit()
        return config
