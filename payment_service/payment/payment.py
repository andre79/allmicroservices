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


#Numero, nome do titular, data de vencimento e código de segurança
class Payment(db.Model):
    __tablename__ = "payment"
    numCard     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nameCard    = db.Column(db.String(255))
    vencCard    = db.Column(db.String(255))
    ccvCard     = db.Column(db.String(255))
    flagCard    = db.Column(db.String(255))
    creditCard  = db.Column(db.String(255))
    authCard    = db.Column(db.String(255))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, nameCard, vencCard, ccvCard, flagCard, creditCard, authCard):
        self.nameCard = nameCard
        self.vencCard = vencCard
        self.ccvCard = ccvCard
        self.flagCard = flagCard
        self.creditCard = creditCard
        self.authCard = authCard

    def __repr__(self):
        return '' % self.id


db.create_all()


class PaymentSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Payment
        sqla_session = db.session

    numCard    = fields.Number(dump_only=True)
    nameCard   = fields.String(required=True)
    vencCard   = fields.String(required=True)
    ccvCard    = fields.String(required=True)
    flagCard   = fields.String(required=True)
    creditCard = fields.String(required=True)
    authCard   = fields.String(required=True)


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
