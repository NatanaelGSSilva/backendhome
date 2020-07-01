from flask import Blueprint, jsonify, request
from banco import db
from models.modelProposta import Proposta
from models.modelCarro import Carro
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
import smtplib

propostas = Blueprint('propostas', __name__)


@propostas.route('/propostas')
def listagem():
    # propostas = Proposta.query.order_by(Proposta.lance).all()
    propostas = Proposta.query.all()
    return jsonify([proposta.to_json() for proposta in propostas])


@propostas.route('/propostas', methods=['POST'])
# @jwt_required
def inclusao():
    proposta = Proposta.from_json(request.json)

    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.starttls()
    # server.login('dasilvanatanael700@gmail.com', 'senha')
    # server.set_debuglevel(1)
    # nomePessoa = request.json['nomePessoa']
    # email = request.json['email']
    # telefone = request.json['telefone']
    # lance = request.json['lance']
    # modelo = request.json['carro_id']
    # msg = 'Ola senhor(a) ' + nomePessoa + 'o seu lance foi ' + str(lance) + ', tal proposta sera avaliada e retornaremos por email ' + \
    #     email + ' ou telefone ' + telefone + 'sobre o veiculo' + str(modelo)
    # server.sendmail('f{email}', email, msg)
    # server.quit()

    db.session.add(proposta)
    db.session.commit()
    return jsonify(proposta.to_json()), 201


@propostas.errorhandler(404)
def id_invalido(error):
    return jsonify({'id': 0, 'message': 'not found'}), 404


@propostas.route('/propostas/<int:id>', methods=['PUT'])
def alteracao(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    proposta = Proposta.query.get_or_404(id)

    # recupera os dados enviados na requisição
    proposta.lance = request.json['lance']
    proposta.carro_id = request.json['carro_id']
    proposta.nomePessoa = request.json['nomePessoa']
    proposta.telefone = request.json['telefone']
    proposta.email = request.json['email']

    # altera (pois o id já existe)
    db.session.add(proposta)
    db.session.commit()
    return jsonify(proposta.to_json()), 204


@propostas.route('/propostas/<int:id>')
def consulta(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    proposta = Proposta.query.get_or_404(id)
    return jsonify(proposta.to_json()), 200


@propostas.route('/propostas/<int:id>', methods=['DELETE'])
def exclui(id):
    Proposta.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'id': id, 'message': 'Proposta excluída com sucesso'}), 200


# Parte 7 do Trabalho
# select count(*) as contagem, faixa salarial from usuarios GROUP BY;
@propostas.route('/propostas/estatisticas')
def estatisticas():
    if db.session.query(Proposta).count() == 0:
        numLance = 0
        lanceBaixo = 0
        lanceAlto = 0
    else:
        # numLance = db.session.query(db.func.count(Proposta.id)).first()[0]
        # funciona
        numLance = db.session.query(Proposta.carro_id, db.func.count(
            Proposta.id)).group_by(Proposta.carro_id).all()
        # lanceAlto =db.session.query(Proposta.id.desc()).group_by(Proposta.lance).limit(1).all()

        return jsonify({'numLance': numLance}), 200


@propostas.route('/propostas/modelos')
def carrosgraf():
    total = db.session.query(db.func.count(
        Proposta.carro_id)).group_by(Proposta.carro_id).all()
    propostas = db.session.query(Carro.modelo, db.func.count(
        Proposta.carro_id)/2).group_by(Carro.modelo).all()
    print(propostas)
    print(total)
    num = 0
    lista = []
    for proposta in propostas:
        lista.append({'modelo': proposta[0], 'num': total[num][0]})
        num = +1

    print(lista)
    return jsonify(lista), 201


@propostas.route('/cadastros/propostas')
def propostascad():
    propostas = db.session.query(db.func.year(Proposta.data_proposta)+'-'+db.func.month(Proposta.data_proposta), db.func.count(Proposta.id)) \
        .group_by(db.func.year(Proposta.data_proposta)+'-'+db.func.month(Proposta.data_proposta)) \
        .filter(Proposta.data_proposta > datetime.today() - timedelta(365))
    print(propostas)

    lista = []
    for proposta in propostas:
        lista.append({'data': proposta[0], 'num': proposta[1]})

    print(lista)

    return jsonify(lista), 201
