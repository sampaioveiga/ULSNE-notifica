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

# Instituições
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

# Tipos de Incidente (novo)
TIPOS_INCIDENTE = [
    ('verbal', 'Violência Verbal'),
    ('ameaca', 'Ameaça'),
    ('psicologica', 'Violência Psicológica'),
    ('fisica', 'Violência Física'),
    ('assedio', 'Assédio'),
    ('discriminacao', 'Discriminação'),
    ('intimidatorio', 'Comportamento Intimidatório'),
    ('outro', 'Outro'),
]

# Local do Incidente (novo)
LOCAIS_INCIDENTE = [
    ('gabinete', 'Gabinete/Consultório'),
    ('sala_espera', 'Sala de Espera'),
    ('servico_clinico', 'Serviço/Unidade Clínica'),
    ('corredor', 'Corredor ou Espaço Comum'),
    ('exterior', 'Exterior da Instituição'),
    ('outro', 'Outro'),
]

# Categorias Profissionais
CATEGORIAS_PROFISSIONAIS = [
    ('medico', 'Médico'),
    ('enfermeiro', 'Enfermeiro'),
    ('psicologo', 'Psicólogo'),
    ('tecnico', 'Técnico'),
    ('assistente_operacional', 'Assistente Operacional'),
    ('administrativo', 'Administrativo'),
    ('outro', 'Outro'),
]

# Tipos de Vítima (novo)
TIPOS_VITIMA = [
    ('profissional', 'Profissional da Instituição'),
    ('utente', 'Utente'),
    ('familiar', 'Familiar/Acompanhante'),
    ('outro', 'Outro'),
]

# Tipos de Agressor (novo)
TIPOS_AGRESSOR = [
    ('utente', 'Utente'),
    ('familiar', 'Familiar/Acompanhante'),
    ('profissional', 'Profissional da Instituição'),
    ('externa', 'Pessoa Externa à Instituição'),
    ('desconhecido', 'Desconhecido'),
]

# Opções Sim/Não/Desconhecido
OPCOES_SIM_NAO_DESC = [
    ('sim', 'Sim'),
    ('nao', 'Não'),
    ('desconhecido', 'Desconhecido'),
]

OPCOES_SIM_NAO = [
    ('sim', 'Sim'),
    ('nao', 'Não'),
]


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    status = db.Column(db.String(20), nullable=False, default=STATUS_ABERTA)

    # 1. Identificação da Instituição
    unidade_local = db.Column(db.String(200), nullable=False)
    servico = db.Column(db.String(200), nullable=True)

    # 2. Informação sobre a Notificação
    quem_notifica = db.Column(db.String(50), nullable=False)  # 'proprio', 'outro'
    quem_notifica_outro = db.Column(db.String(200), nullable=True)
    eh_anonimo = db.Column(db.Boolean, default=True)
    nome_notificante = db.Column(db.String(200), nullable=True)
    contacto_notificante = db.Column(db.String(200), nullable=True)
    data_notificacao = db.Column(db.Date, nullable=False)

    # 3. Informação sobre o Incidente
    data_incidente = db.Column(db.DateTime, nullable=False)
    local_incidente = db.Column(db.String(50), nullable=False)
    local_incidente_outro = db.Column(db.String(200), nullable=True)
    tipos_incidente = db.Column(db.String(500), nullable=False)  # CSV
    tipos_incidente_outro = db.Column(db.String(200), nullable=True)

    # 4. Informação sobre a Vítima
    tipo_vitima = db.Column(db.String(50), nullable=False)
    categoria_profissional = db.Column(db.String(50), nullable=True)
    nome_vitima = db.Column(db.String(200), nullable=True)

    # 5. Informação sobre o Agressor
    tipo_agressor = db.Column(db.String(50), nullable=False)
    numero_agressores = db.Column(db.Integer, nullable=True)
    identidade_conhecida = db.Column(db.String(50), nullable=True)  # 'sim', 'nao'
    nome_agressor = db.Column(db.String(200), nullable=True)

    # 6. Consequências do Incidente
    danos_fisicos = db.Column(db.String(50), nullable=True)  # 'sim', 'nao', 'desconhecido'
    impacto_psicologico = db.Column(db.String(50), nullable=True)
    assistencia_medica = db.Column(db.String(50), nullable=True)
    intervencao_autoridades = db.Column(db.String(50), nullable=True)

    # 7. Resposta ao Incidente
    quem_foi_informado = db.Column(db.String(500), nullable=True)  # CSV
    quem_informado_outro = db.Column(db.String(200), nullable=True)
    medidas_aplicadas = db.Column(db.String(500), nullable=True)  # CSV
    medidas_outro = db.Column(db.String(200), nullable=True)

    # 8. Testemunhas
    existem_testemunhas = db.Column(db.String(50), nullable=True)
    descricao_testemunhas = db.Column(db.Text, nullable=True)

    # 9. Descrição do Incidente
    descricao = db.Column(db.Text, nullable=False)

    # 10. Avaliação de Risco
    risco_repeticao = db.Column(db.String(50), nullable=True)  # 'sim', 'nao', 'nao_sei'
    agressor_contacto = db.Column(db.String(50), nullable=True)

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    comments = db.relationship('Comment', backref='notification', lazy=True, order_by='Comment.created_at')

    @property
    def status_label(self):
        return STATUS_LABELS.get(self.status, self.status)

    @property
    def tipos_incidente_list(self):
        return [t.strip() for t in self.tipos_incidente.split(',') if t.strip()]

    @property
    def tipos_incidente_labels(self):
        mapping = dict(TIPOS_INCIDENTE)
        return [mapping.get(t, t) for t in self.tipos_incidente_list]


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
    is_manager = db.Column(db.Boolean, default=False)
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
