import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'some_secret_key')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Lameck28@localhost/job-posting'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwt_secret_key'