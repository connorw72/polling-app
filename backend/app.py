# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO

# Load .env
load_dotenv()

if not os.getenv("JWT_SECRET_KEY"):
    print("Warning: JWT_SECRET_KEY not set in .env. Using fallback.")

# create flask app 
app = Flask(__name__)

# connection between backend and frontend
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Uses database file called polling_app.db 
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///polling_app.db")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///polling_app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Ensures secure logins
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback_key_for_dev")

# login token setup
jwt = JWTManager(app)
# database setup
db = SQLAlchemy(app)
# migrate
migrate = Migrate(app, db)
# socketIO
socketio = SocketIO(app)
@socketio.on('connect')
def handle_connect():
    app.logger.info('Client connected.')

import os
import sys
sys.path.append(os.path.dirname(__file__))  # Ensure backend directory is in the path
from routes import *


# create tables (only if app is running)
with app.app_context():
    db.create_all()

# start app
if __name__ == "__main__":
    socketio.run(app, debug=True)
