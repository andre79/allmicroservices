from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@checkout-mysql/maccshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
db = SQLAlchemy(app)


class Checkout(db.Model):
    __tablename__ = "checkout"
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


class CheckoutSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Checkout
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    numCard = fields.String(required=True)
    numVenc = fields.String(required=True)


@app.route('/checkout', methods=['GET'])
def index():
    get_checkout = Checkout.query.all()
    checkout_schema = CheckoutSchema(many=True)
    checkout = checkout_schema.dump(get_checkout)
    return make_response(jsonify({"checkout": checkout}))


@app.route('/checkout/<id>', methods=['GET'])
def get_checkout_by_id(id):
    get_checkout = Checkout.query.get(id)
    checkout_schema = CheckoutSchema()
    checkout = checkout_schema.dump(get_checkout)
    return make_response(jsonify({"checkout": checkout}))


@app.route('/checkout/<id>', methods=['PUT'])
def update_checkout_by_id(id):
    data = request.get_json()
    get_checkout = Checkout.query.get(id)
    if data.get('numCard'):
        get_checkout.numCard = data['numCard']
    if data.get('numVenc'):
        get_checkout.numVenc = data['numVenc']
    db.session.add(get_checkout)
    db.session.commit()
    checkout_schema = CheckoutSchema(only=['id', 'numCard', 'numVenc'])
    checkout = checkout_schema.dump(get_checkout)
    return make_response(jsonify({"checkout": checkout}))


@app.route('/checkout/<id>', methods=['DELETE'])
def delete_checkout_by_id(id):
    get_checkout = Checkout.query.get(id)
    db.session.delete(get_checkout)
    db.session.commit()
    return make_response("", 204)


@app.route('/checkout', methods=['POST'])
def create_payment():
    data = request.get_json()
    checkout_schema = CheckoutSchema()
    checkout = checkout_schema.load(data)
    result = checkout_schema.dump(checkout.create())
    return make_response(jsonify({"checkout": result}), 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)