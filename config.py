import os

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_SENDER = "type2talkhelpdesk@gmail.com"
EMAIL_PASSWORD = "okjyhiuuxcvaerpi"  # Use an app password, not your real one
SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
DB_FOLDER = "db"
DB_PATH = os.path.join(DB_FOLDER, "database.db")