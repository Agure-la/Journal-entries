from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, supports_credentials=True)

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

from app import routes, models

if __name__=='__main__':
    app.run(debug=True, port=5000)