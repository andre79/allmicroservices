from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@delivery-mysql/maccshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
db = SQLAlchemy(app)


class Delivery(db.Model):
    __tablename__ = "delivery"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(100))
    number = db.Column(db.String(100))
    neighborhood = db.Column(db.String(100))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, address, number, neighborhood):
        self.address = address
        self.number = number
        self.neighborhood = neighborhood

    def __repr__(self):
        return '' % self.id


db.create_all()


class DeliverySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Delivery
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    address = fields.String(required=True)
    number = fields.String(required=True)
    neighborhood = fields.String(required=True)


@app.route('/delivery', methods=['GET'])
def index():
    get_delivery = Delivery.query.all()
    delivery_schema = DeliverySchema(many=True)
    delivery = delivery_schema.dump(get_delivery)
    return make_response(jsonify({"delivery": delivery}))


@app.route('/delivery/<id>', methods=['GET'])
def get_delivery_by_id(id):
    get_delivery = Delivery.query.get(id)
    delivery_schema = DeliverySchema()
    delivery = delivery_schema.dump(get_delivery)
    return make_response(jsonify({"delivery": delivery}))


@app.route('/delivery/<id>', methods=['PUT'])
def update_delivery_by_id(id):
    data = request.get_json()
    get_delivery = Delivery.query.get(id)
    if data.get('address'):
        get_delivery.address = data['address']
    if data.get('number'):
        get_delivery.number = data['number']
    if data.get('neighborhood'):
        get_delivery.neighborhood = data['neighborhood']
    db.session.add(get_delivery)
    db.session.commit()
    delivery_schema = DeliverySchema(only=['id', 'address', 'number', 'neighborhood'])
    delivery = delivery_schema.dump(get_delivery)
    return make_response(jsonify({"delivery": delivery}))


@app.route('/delivery/<id>', methods=['DELETE'])
def delete_delivery_by_id(id):
    get_delivery = Delivery.query.get(id)
    db.session.delete(get_delivery)
    db.session.commit()
    return make_response("", 204)


@app.route('/delivery', methods=['POST'])
def create_delivery():
    data = request.get_json()
    delivery_schema = DeliverySchema()
    delivery = delivery_schema.load(data)
    result = delivery_schema.dump(delivery.create())
    return make_response(jsonify({"delivery": result}), 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)