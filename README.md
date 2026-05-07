First time setup:


# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
Run in development:


source venv/bin/activate
python run.py
App starts at http://localhost:5000

Default admin credentials:

Username: admin
Password: Admin1234!
Admin panel: http://localhost:5000/admin/login
The SQLite database (instance/notificacoes.db) is created automatically on first run. If you ever need to reset the schema (e.g. after model changes), just delete that file and restart.


# Production
verify deploy
sudo bash deploy.sh