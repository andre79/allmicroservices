from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@shipping-mysql/maccshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
db = SQLAlchemy(app)


class Shipping(db.Model):
    __tablename__ = "shipping"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    days = db.Column(db.Integer)
    value = db.Column(db.String(10))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, days, value):
        self.days = days
        self.value = value


    def __repr__(self):
        return '' % self.id


db.create_all()


class ShippingSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Shipping
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    days = fields.Number(required=True)
    value = fields.String(required=True)


@app.route('/shipping', methods=['GET'])
def index():
    get_shipping = Shipping.query.all()
    shipping_schema = ShippingSchema(many=True)
    shipping = shipping_schema.dump(get_shipping)
    return make_response(jsonify({"shipping": shipping}))


@app.route('/shipping/<id>', methods=['GET'])
def get_shipping_by_id(id):
    get_shipping = Shipping.query.get(id)
    shipping_schema = ShippingSchema()
    shipping = shipping_schema.dump(get_shipping)
    if not shipping:
        response = jsonify({'message': '(Not Found)'})
        return response, 404
    return make_response(jsonify({"shipping": shipping}))


@app.route('/shipping', methods=['POST'])
def create_shipping():
    data = request.get_json()
    shipping_schema = ShippingSchema()
    shipping = shipping_schema.load(data)
    result = shipping_schema.dump(shipping.create())
    return make_response(jsonify({"shipping": result}), 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
