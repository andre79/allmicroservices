from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@cart-mysql/maccshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
db = SQLAlchemy(app)


class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProduct = db.Column(db.Integer)
    nameProduct = db.Column(db.String(255))
    quantity = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, idProduct, nameProduct, quantity):
        self.idProduct = idProduct
        self.nameProduct = nameProduct
        self.quantity = quantity

    def __repr__(self):
        return '' % self.id


db.create_all()


class CartSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Cart
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    idProduct = fields.Number(required=True)
    nameProduct = fields.String(required=True)
    quantity = fields.Number(dump_only=True)


@app.route('/cart', methods=['GET'])
def index():
    get_cart = Cart.query.all()
    cart_schema = CartSchema(many=True)
    cart = cart_schema.dump(get_cart)
    return make_response(jsonify({"cart": cart}))


@app.route('/cart/<id>', methods=['GET'])
def get_cart_by_id(id):
    get_cart = Cart.query.get(id)
    cart_schema = CartSchema()
    cart = cart_schema.dump(get_cart)
    return make_response(jsonify({"cart": cart}))


@app.route('/cart/<id>', methods=['PUT'])
def update_cart_by_id(id):
    data = request.get_json()
    get_cart = Cart.query.get(id)
    if data.get('idProduct'):
        get_cart.name = data['idProduct']
    if data.get('nameProduct'):
        get_cart.login = data['nameProduct']
    if data.get('quantity'):
        get_cart.password = data['quantity']
    db.session.add(get_cart)
    db.session.commit()
    cart_schema = CartSchema(only=['id', 'idProduct', 'nameProduct', 'quantity'])
    cart = cart_schema.dump(get_cart)
    return make_response(jsonify({"cart": cart}))


@app.route('/cart/<id>', methods=['DELETE'])
def delete_cart_by_id(id):
    get_cart = Cart.query.get(id)
    db.session.delete(get_cart)
    db.session.commit()
    return make_response("", 204)


@app.route('/cart', methods=['POST'])
def create_cart():
    data = request.get_json()
    cart_schema = CartSchema()
    cart = cart_schema.load(data)
    result = cart_schema.dump(cart.create())
    return make_response(jsonify({"cart": result}), 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
