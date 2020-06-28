from flask import Blueprint, jsonify, request
from banco import db
from models.modelProposta import Proposta
from models.modelCarro import Carro
from flask_jwt_extended import jwt_required

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


@propostas.route('/propostas/estatistica/total')
def totalPropostas():
    propostas = Proposta.query.count()

    return jsonify({'total': propostas})


@propostas.route('/propostas/estatistica/contagem/maior')
def contagemMaior():
    propostas = Proposta.query.order_by(Proposta.lance.desc()).limit(1).all()

    return jsonify([proposta.to_json() for proposta in propostas])

# @propostas.route('/propostas/estatistica/contagem/menor')
# def contagemMenor():
#     Propostas = Proposta.query.order_by(Proposta.lance.asc()).limit(1).all()

#     return jsonify([proposta.to_json() for proposta in propostas])
