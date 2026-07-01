# Registo de Notificações de Violência contra Profissionais de Saúde

Esta aplicação foi desenvolvida para simplificar e centralizar a recolha, o acompanhamento e a análise de incidentes de violência (verbal, física ou psicológica) reportados por profissionais de saúde no seu ambiente de trabalho. 

O objetivo principal é dotar as equipas e as administrações de uma ferramenta ágil para mapear situações de risco, gerar relatórios estatísticos e apoiar a tomada de decisões na proteção de quem cuida.

### Principais Funcionalidades:
*   **Registo Rápido:** Formulário intuitivo para reportar incidentes em poucos passos.
*   **Anonimato ou Confidencialidade:** Opções seguras para proteger a identidade do relator.
*   **Painel de Análise:** Visualização de dados por unidade, tipo de violência e horário para identificar padrões.
*   **Acompanhamento:** Estado da notificação (em análise, resolvida, encaminhada).


# Running

## Development

# Activate virtual environment
source venv/bin/activate        # Linux/Mac
# or
venv\Scripts\activate           # Windows

# Install dependencies (if not already done)
pip install -r requirements.txt

# Run the app
python run.py

Then:
- App: http://localhost:5000
- Admin panel: http://localhost:5000/admin/login
- Default credentials: admin / Admin1234!

The SQLite database auto-creates at instance/notificacoes.db on first run. If you modify models and need to reset the schema, just delete that file and restart.

# Production

To run in production on Ubuntu 22.04:

sudo bash deploy.sh

This script:
1. Installs Python 3.10 and dependencies
2. Creates a service user (ulsne) to run the app
3. Sets up a virtual environment
4. Generates a secure SECRET_KEY and saves to .env
5. Creates a systemd service (ulsne-notificacoes)
6. Starts the app via Gunicorn on port 8000 (4 workers)

After Deployment

# Check service status
systemctl status ulsne-notificacoes

# View logs
journalctl -u ulsne-notificacoes -f

# Restart if needed
systemctl restart ulsne-notificacoes

Web Server (Nginx)

The app runs on 127.0.0.1:8000. Configure Nginx as a reverse proxy to expose it publicly:

apt-get install -y nginx
# Edit /etc/nginx/sites-available/ulsne-notificacoes to proxy to port 8000

Important

- Change default admin credentials immediately — Username: admin / Password: Admin1234! via /admin/utilizadores
- SECRET_KEY is auto-generated and stored in .env (600 permissions, readable only by service user)
- Database remains SQLite at instance/notificacoes.db