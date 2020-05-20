from flask import Blueprint, jsonify, request
from banco import db
from models.modelCarro import Carro
from flask_jwt_extended import jwt_required

carros = Blueprint('carros', __name__)


@carros.route('/carros')
def listagem():
    carros = Carro.query.order_by(Carro.modelo).all()
    return jsonify([carro.to_json() for carro in carros])


@carros.route('/carros', methods=['POST'])
@jwt_required
def inclusao():
    carro = Carro.from_json(request.json)
    db.session.add(carro)
    db.session.commit()
    return jsonify(carro.to_json()), 201
