from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
import requests

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@product-mysql/maccshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = "products"
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name        = db.Column(db.String(255))
    price       = db.Column(db.String(100))
    old_price   = db.Column(db.String(100))
    image_thumb = db.Column(db.String(255))
    category    = db.Column(db.String(255))
    quantity    = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, price, old_price, image_thumb, category):
        self.name        = name
        self.price       = price
        self.old_price   = old_price
        self.image_thumb = image_thumb
        self.category    = category
        self.quantity    = category


    def __repr__(self):
        return '' % self.id


db.create_all()


class ProductSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Product
        sqla_session = db.session

    id          = fields.Number(dump_only=True)
    name        = fields.String(required=True)
    price       = fields.String(required=True)
    old_price   = fields.String(required=True)
    image_thumb = fields.String(required=True)
    category    = fields.String(required=True)
    quantity    = fields.Number(required=True)


@app.route('/products', methods=['GET'])
def index():
    get_products = Product.query.all()
    product_schema = ProductSchema(many=True)
    products = product_schema.dump(get_products, )
    return make_response(jsonify({"product": products}))


@app.route('/products/<id>', methods=['GET'])
def get_product_by_id(id):
    #value = get_stock_by_id(id)
    get_product = Product.query.get(id)
    product_schema = ProductSchema()
    #get_product.quantity = value
    product = product_schema.dump(get_product)
    return make_response(jsonify({"product": product}))

@app.route('/products/category/<category>', methods=['GET'])
def get_product_by_category(category):
    product_schema = ProductSchema(many=True)
    get_product = Product.query.filter(Product.category == category).all()
    productReturn = product_schema.dump(get_product)
    return make_response(jsonify({"product": productReturn}))

@app.route('/products/<id>', methods=['PUT'])
def update_product_by_id(id):
    data = request.get_json()
    get_product = Product.query.get(id)
    if data.get('name'):
        get_product.name = data['name']
    if data.get('price'):
        get_product.price = data['price']
    if data.get('old_price'):
        get_product.old_price = data['old_price']
    if data.get('image_thumb'):
        get_product.image_thumb = data['image_thumb']
    if data.get('category'):
        get_product.image_thumb = data['category']
    if data.get('quantity'):
        get_product.image_thumb = data['quantity']
    db.session.add(get_product)
    db.session.commit()
    product_schema = ProductSchema(only=['id', 'name', 'price', 'old_price', 'image_thumb', 'category', 'quantity'])
    product = product_schema.dump(get_product)
    return make_response(jsonify({"product": product}))


@app.route('/products/<id>', methods=['DELETE'])
def delete_product_by_id(id):
    get_product = Product.query.get(id)
    db.session.delete(get_product)
    db.session.commit()
    return make_response("", 204)


@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product_schema = ProductSchema()
    product = product_schema.load(data)
    result = product_schema.dump(product.create())
    return make_response(jsonify({"product": result}), 200)

#def get_stock_by_id(id):
    #url = 'http://172.24.0.1:5010/stock/' + str(id)
    #headers = {'content-type': 'application/json'}
    #r = requests.get(url, headers=headers)
    #if not r:
    #    return 0

    #value = r.json()
    #return value['stock']['quantity']


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
