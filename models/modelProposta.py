from banco import db
from datetime import datetime

# quinta parte


class Proposta(db.Model):
    __tablename__ = 'propostas'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    lance = db.Column(db.Float, nullable=False)
    nomePessoa = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    data_proposta = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    carro_id = db.Column(db.Integer, db.ForeignKey(
        'carros.id'), nullable=False)

    carro = db.relationship('Carro')

    def to_json(self):
        json_propostas = {
            'id': self.id,
            'lance': self.lance,
            'nomePessoa': self.nomePessoa,
            'telefone': self.telefone,
            'email': self.email,
            'modelo': self.carro.modelo,
            'preco': self.carro.preco,
            'ano': self.carro.ano,
            'carro_id': self.carro_id
        }
        return json_propostas

    @staticmethod
    def from_json(json_propostas):
        lance = json_propostas.get('lance')
        carro_id = json_propostas.get('carro_id')
        return Proposta(lance=lance, carro_id=carro_id, nomePessoa=nomePessoa, telefone=telefone, email=email)
