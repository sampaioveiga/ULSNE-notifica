#!/usr/bin/env bash
# ULSNE — Deployment script for Ubuntu 22.04.5 LTS (Python 3.10.12)
# Run as: sudo bash deploy.sh

set -e

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVICE_USER="ulsne"
SERVICE_NAME="ulsne-notificacoes"
PORT=8000

echo "==> Installing Python 3.10 and dependencies..."
apt-get update
apt-get install -y python3.10 python3.10-venv python3.10-dev python3-pip

echo "==> Creating service user..."
id -u "$SERVICE_USER" &>/dev/null || useradd -r -s /bin/false "$SERVICE_USER"

echo "==> Setting up virtual environment..."
cd "$APP_DIR"
python3.10 -m venv venv
chown -R "$SERVICE_USER":"$SERVICE_USER" "$APP_DIR"
sudo -u "$SERVICE_USER" venv/bin/python -m pip install --upgrade pip
sudo -u "$SERVICE_USER" venv/bin/python -m pip install -r requirements.txt

echo "==> Generating secret key..."
SECRET_KEY=$(python3.10 -c "import secrets; print(secrets.token_hex(32))")
ENV_FILE="$APP_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
  echo "SECRET_KEY=$SECRET_KEY" > "$ENV_FILE"
  chown "$SERVICE_USER":"$SERVICE_USER" "$ENV_FILE"
  chmod 600 "$ENV_FILE"
fi

echo "==> Creating systemd service..."
cat > /etc/systemd/system/"$SERVICE_NAME".service <<EOF
[Unit]
Description=ULSNE Notificação de Incidentes
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$APP_DIR
EnvironmentFile=$ENV_FILE
ExecStart=$APP_DIR/venv/bin/gunicorn -w 4 -b 127.0.0.1:$PORT "app:create_app()"
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"

echo ""
echo "==> Done. Application running on port $PORT"
echo "    Service: systemctl status $SERVICE_NAME"
echo "    Logs:    journalctl -u $SERVICE_NAME -f"
echo ""
echo "==> Default admin credentials:"
echo "    Username: admin"
echo "    Password: Admin1234!"
echo "    CHANGE IMMEDIATELY via /admin/utilizadores"
echo ""
echo "==> To expose publicly, configure a reverse proxy (Nginx) to port $PORT:"
echo "    apt-get install -y nginx"
echo "    # Configure /etc/nginx/sites-available/$SERVICE_NAME"
