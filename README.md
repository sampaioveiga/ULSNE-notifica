# Registo de Notificações de Violência contra Profissionais de Saúde

Sistema seguro e anónimo de notificação de incidentes de violência contra profissionais de saúde na ULS-NE (Nordeste - Portugal).

## 📋 Principais Funcionalidades

- **Formulário Detalhado**: 10 seções cobrindo completamente cada incidente
- **Anonimato Garantido**: Opção de manter identidade completamente privada
- **Confidencialidade**: Proteção total dos dados e comunicações
- **Dashboard de Gestão**: Análise e acompanhamento de incidentes
- **Comunicação Integrada**: Comentários entre notificante e gestores
- **Rastreamento Completo**: Histórico desde submissão até resolução
- **Gestão de Estado**: Acompanhamento (Aberta → Em Análise → Encerrada)

## 📝 Seções do Formulário

1. **Identificação da Instituição** - Unidade/centro de saúde e departamento
2. **Informação sobre a Notificação** - Quem notifica, anonimato, data
3. **Informação sobre o Incidente** - Data/hora, local, tipos específicos
4. **Informação sobre a Vítima** - Tipo (profissional/utente/familiar), categoria
5. **Informação sobre o Agressor** - Tipo, número, identidade conhecida
6. **Consequências do Incidente** - Danos físicos, impacto psicológico
7. **Resposta ao Incidente** - Quem foi informado, medidas imediatas
8. **Testemunhas** - Existência e descrição de testemunhas
9. **Descrição Detalhada** - Narrativa completa do incidente
10. **Avaliação de Risco** - Risco de repetição, contacto contínuo

## 🚀 Primeiros Passos

### Instalação e Setup

```bash
# 1. Criar ambiente virtual
python3 -m venv venv

# 2. Ativar (Linux/Mac)
source venv/bin/activate
# ou (Windows)
venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. IMPORTANTE: Limpar base de dados antiga (primeira execução)
rm instance/notificacoes.db
```

### Executar em Desenvolvimento

```bash
source venv/bin/activate
python run.py
```

Acesso:
- **Página Pública**: http://localhost:5000
- **Painel de Gestão**: http://localhost:5000/admin/notificacoes
- **Login**: admin / Admin1234!

**⚠️ ALTERE IMEDIATAMENTE as credenciais padrão!**

## 🌐 Funcionalidades Públicas

- **Submeter Notificação** - Formulário completo de 10 seções
- **Consultar Estado** - Verificar progresso com token único
- **Comunicar com Gestores** - Adicionar comentários e informações

## 🔧 Funcionalidades de Gestão (Admin)

- **Dashboard de Notificações** - Listagem filtrada e ordenável
- **Detalhes Completos** - Visualização de todas as 10 seções
- **Atualizar Estado** - Mudar status de processamento
- **Respostas** - Comentários para feedback ao notificante
- **Gestão de Gestores** - Criar, editar, desativar gestores
- **Configuração SMTP** - Setup para envio automático de emails

## 💾 Base de Dados

- **Engine**: SQLite (`instance/notificacoes.db`)
- **Auto-criação**: Na primeira execução
- **Reset**: Apague o ficheiro `.db` e reinicie
- **Admin Padrão**: Criado automaticamente

## 🏭 Produção

### Ubuntu 22.04

```bash
# Executar script de deploy
sudo bash deploy.sh
```

O script:
1. Instala Python 3.10 e dependências
2. Cria utilizador de serviço (`ulsne`)
3. Gera `SECRET_KEY` segura em `.env`
4. Configura systemd service
5. Inicia via Gunicorn (4 workers, porta 8000)

### Gestão em Produção

```bash
# Status
systemctl status ulsne-notificacoes

# Logs
journalctl -u ulsne-notificacoes -f

# Reiniciar
systemctl restart ulsne-notificacoes
```

### Nginx (Reverse Proxy)

```bash
# Instalar
apt-get install -y nginx

# Configurar proxy para porta 8000
# Editar: /etc/nginx/sites-available/ulsne-notificacoes
```

## 📁 Estrutura do Projeto

```
app/
  ├── __init__.py              Factory e setup Flask
  ├── config.py                Configuração da app
  ├── models.py                Modelos SQLAlchemy
  ├── email_utils.py           Envio de emails
  ├── routes/
  │   ├── public.py            Formulário e consulta pública
  │   ├── auth.py              Autenticação
  │   ├── backoffice.py        Dashboard de gestão
  │   ├── users.py             Gestão de gestores
  │   └── settings.py          Configuração SMTP
  └── templates/
      ├── public/              Páginas públicas
      │   ├── index.html
      │   ├── form.html        Formulário 10 seções
      │   ├── sucesso.html
      │   ├── consultar.html
      │   └── estado.html
      └── admin/               Dashboard de gestão
          ├── base_admin.html
          ├── notifications.html
          ├── detail.html      Detalhe completo
          ├── users.html
          └── settings.html
```

## 🔐 Segurança

- ✅ CSRF Protection ativado globalmente
- ✅ Autenticação obrigatória para admin
- ✅ Passwords hasheadas (werkzeug)
- ✅ Suporte completo a anonimato
- ✅ Validação em todos os inputs
- ✅ Emails confidenciais (SMTP configurável)
- ✅ Permissões restritivas em ficheiros sensíveis

## 🛠 Tecnologia

- **Backend**: Flask 2.3.3
- **ORM**: SQLAlchemy 3.1.1
- **Autenticação**: Flask-Login 0.6.3
- **Formulários**: Flask-WTF 1.2.1 (com CSRF)
- **Validação**: WTForms 3.1.1
- **Email**: Python smtplib
- **WSGI (Prod)**: Gunicorn 21.2.0
- **BD**: SQLite

## 📚 Documentação Interna

Veja `CLAUDE.md` para orientação técnica de desenvolvimento.

## 📞 Contacto

Desenvolvido para **Unidade Local de Saúde do Nordeste (ULSNE)**

Questões: sampaio.veiga@gmail.com
