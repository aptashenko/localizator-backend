from flask import Flask
from flask_cors import CORS
from dotenv import dotenv_values

env = dotenv_values(".env")
allowed_origins = env.get('ALLOWED_ORIGINS').split(',')

def create_app():
    app = Flask(__name__)
    CORS(app, resources={
        r"/*": {"origins": allowed_origins}
    }) 
    app.config.from_object('app.configs.Config')
    return app