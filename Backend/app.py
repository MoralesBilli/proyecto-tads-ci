from flask import Flask
from Backend.Extensiones import db
from Backend.Rutas.Rutas import blueprints
from dotenv import load_dotenv
import os
from flask_cors import CORS

app = Flask(__name__)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.secret_key = os.getenv('SECRET_KEY')
# Configure CORS
# Set CORS_ORIGINS in .env to a comma-separated list of allowed origins, or '*' for all.
cors_origins = os.getenv('CORS_ORIGINS', '*')
if cors_origins.strip() == '*':
    CORS(app)
else:
    origins = [o.strip() for o in cors_origins.split(',') if o.strip()]
    CORS(app, resources={r"/*": {"origins": origins}})

for bp in blueprints:
    app.register_blueprint(bp)


if __name__ == '__main__':
    app.run(debug=True)