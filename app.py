from flask import Flask
from config import config
from banco import db
from resources.carros import carros
from resources.marcas import marcas
from resources.usuarios import usuarios
from flask_jwt_extended import JWTManager
from blacklist import blacklist
import smtplib

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(carros)
app.register_blueprint(marcas)
app.register_blueprint(usuarios)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/')
def raiz():
    db.create_all()
    return '<h2>Revenda Herbie</h2>'


@app.route('/envia_email')
def envia():
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('conta.teste.laravel@gmail.com','conta#teste#laravel')
    server.set_debuglevel(1)
    msg = 'Subject: Teste PI2\nÓla Teste de Envio de e-mail pelo Python\nÉ bom esse Python!!'.encode('utf-8')
    server.sendmail('conta.teste.laravel@gmail.com','dasilvanatanael700@gmail.com', msg)
    server.quit()    
    return "OK! E-mail Enviado."


if __name__ == '__main__':
    app.run(debug=True)
