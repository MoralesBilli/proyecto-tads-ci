from flask import Flask
from Extensiones import db
from Rutas.Rutas import blueprints



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:adnatfhso4@localhost/ExamenU2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

for bp in blueprints:
    app.register_blueprint(bp)


if __name__ == '__main__':
    app.run(debug=True)