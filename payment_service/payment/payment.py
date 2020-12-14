from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@payment-mysql/maccshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
db = SQLAlchemy(app)


class Payment(db.Model):
    __tablename__ = "payment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numCard = db.Column(db.String(16))
    vencCard = db.Column(db.String(100))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, numCard, vencCard):
        self.numCard = numCard
        self.vencCard = vencCard

    def __repr__(self):
        return '' % self.id


db.create_all()


class PaymentSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Payment
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    numCard = fields.String(required=True)
    numVenc = fields.String(required=True)


@app.route('/payment', methods=['GET'])
def index():
    get_payment = Payment.query.all()
    payment_schema = PaymentSchema(many=True)
    payment = payment_schema.dump(get_payment)
    return make_response(jsonify({"payment": payment}))


@app.route('/payment/<id>', methods=['GET'])
def get_payment_by_id(id):
    get_payment = Payment.query.get(id)
    payment_schema = PaymentSchema()
    payment = payment_schema.dump(get_payment)
    return make_response(jsonify({"payment": payment}))


@app.route('/payment/<id>', methods=['PUT'])
def update_payment_by_id(id):
    data = request.get_json()
    get_payment = Payment.query.get(id)
    if data.get('numCard'):
        get_payment.numCard = data['numCard']
    if data.get('numVenc'):
        get_payment.numVenc = data['numVenc']
    db.session.add(get_payment)
    db.session.commit()
    payment_schema = PaymentSchema(only=['id', 'numCard', 'numVenc'])
    payment = payment_schema.dump(get_payment)
    return make_response(jsonify({"payment": payment}))


@app.route('/payment/<id>', methods=['DELETE'])
def delete_payment_by_id(id):
    get_payment = Payment.query.get(id)
    db.session.delete(get_payment)
    db.session.commit()
    return make_response("", 204)


@app.route('/payment', methods=['POST'])
def create_payment():
    data = request.get_json()
    payment_schema = PaymentSchema()
    payment = payment_schema.load(data)
    result = payment_schema.dump(payment.create())
    return make_response(jsonify({"payment": result}), 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
